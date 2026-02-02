from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
import time
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock Data State
stats = {
    "recyclable": 150,
    "toxic": 30,
    "human": 1
}

def generate_mock_frames():
    """Generates video feed from Real Webcam but with MOCK detections."""
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Could not open webcam, falling back to synthetic.")
        # Fallback to black screen if no camera
        width, height = 640, 480
        frame = np.zeros((height, width, 3), dtype=np.uint8)
    
    x, y = 320, 240
    dx, dy = 5, 5
    
    print("Starting video capture with COLOR DETECTION...")
    while True:
        if cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                time.sleep(0.05)
                continue
        else:
            frame[:] = (20, 20, 20)

        # Basic Color Detection (Computer Vision without AI)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Detect RED (Toxic)
        lower_red1 = np.array([0, 120, 70])
        upper_red1 = np.array([10, 255, 255])
        mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
        lower_red2 = np.array([170, 120, 70])
        upper_red2 = np.array([180, 255, 255])
        mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask_red = mask_red1 + mask_red2
        
        # Detect GREEN (Recyclable)
        lower_green = np.array([36, 25, 25])
        upper_green = np.array([86, 255, 255])
        mask_green = cv2.inRange(hsv, lower_green, upper_green)

        # Find contours for Red
        contours_r, _ = cv2.findContours(mask_red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours_r:
            area = cv2.contourArea(cnt)
            if area > 1000: # Filter small noise
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                cv2.putText(frame, "TOXIC (RED)", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # Find contours for Green
        contours_g, _ = cv2.findContours(mask_green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours_g:
            area = cv2.contourArea(cnt)
            if area > 1000:
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, "RECYCLABLE (GREEN)", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Add timestamp
        cv2.putText(frame, f"COLOR VISION MODE - {time.strftime('%H:%M:%S')}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

        # Encode
        _, buffer = cv2.imencode(".jpg", frame)
        frame_bytes = buffer.tobytes()

        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n")
        
        time.sleep(0.03)

@app.get("/video")
def video():
    return StreamingResponse(generate_mock_frames(), media_type="multipart/x-mixed-replace; boundary=frame")

@app.get("/stats")
def get_stats():
    # Simulate changing stats
    stats["recyclable"] += random.choice([0, 0, 0, 1])
    return {
        "total_objects": sum(stats.values()),
        **stats
    }

@app.get("/alert")
def get_alert():
    # Simulate an alert occasionally
    return {
        "id": int(time.time() // 10), # Changes every 10s
        "label": "cell phone",
        "type": "toxic"
    }
