from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

import cv2
import time

from detector import YoloDetector
from stats_manager import StatsManager
from alert_manager import AlertManager


# 🔹 FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all ports (5173, 5174, etc.)
    # allow_origins=[
    #     "http://localhost:5173",
    #     "http://127.0.0.1:5173",
    # ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔹 Core components
detector = YoloDetector()
stats = StatsManager()
alert_manager = AlertManager()

# 🔹 Camera (open once, globally)
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)


def generate_frames():
    """
    Robust MJPEG stream generator with frame skipping for performance.
    """
    frame_count = 0
    detections = []
    
    while True:
        try:
            success, frame = cap.read()

            if not success or frame is None:
                time.sleep(0.01)
                continue

            # 🔹 Frame skipping: Only run AI every 3 frames
            if frame_count % 3 == 0:
                detections = detector.detect(frame)

                # 🔹 Determine what is currently active (visible)
                current_active = set()
                for d in detections:
                    cat = stats.classify(d["label"])
                    current_active.add(cat)
                
                stats.set_active(current_active)
                stats.update(detections)

            frame_count += 1

            # 🔹 Handle alerts + draw boxes (draw previous detections on skipped frames)
            for d in detections:
                category = stats.classify(d["label"])

                # 🚨 Trigger email alert if needed (only on new detection frames)
                if frame_count % 3 == 1:
                    alert_manager.handle_detection(d, category)

                # 🎨 Draw bounding box
                x1, y1, x2, y2 = d["bbox"]
                label = f"{d['label']} #{d['id']} ({category})"

                # Color coding (OpenCV uses BGR)
                if category == "recyclable":
                    color = (0, 255, 0)    # Green
                elif category == "toxic":
                    color = (0, 0, 255)    # Red
                elif category == "human":
                    color = (0, 255, 255)  # Yellow (Mix of Green+Red)
                else:
                    color = (200, 200, 200) # Grey/White for others

                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 3)
                cv2.putText(
                    frame,
                    label,
                    (x1, max(y1 - 10, 20)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    color,
                    2
                )

            # 🔹 Encode frame as JPEG
            ret, buffer = cv2.imencode(".jpg", frame)
            if not ret:
                continue

            frame_bytes = buffer.tobytes()

            # 🔹 MJPEG chunk
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" +
                frame_bytes +
                b"\r\n"
            )

        except Exception as e:
            # ❗ NEVER crash the stream
            print("⚠️ Video stream error:", e)
            time.sleep(0.05)
            continue


# 🎥 Live video endpoint
@app.get("/video")
def video():
    return StreamingResponse(
        generate_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )


# 📊 Live statistics endpoint
@app.get("/stats")
def get_stats():
    return stats.get_stats()


# 🚨 Last alert endpoint
@app.get("/alert")
def get_alert():
    return alert_manager.get_last_alert()
