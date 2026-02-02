
from ultralytics import YOLO
from config import CONFIDENCE_THRESHOLD, ALLOWED_LABELS


class YoloDetector:
    def __init__(self):
        # Using Nano (n) model - fastest for real-time mobile/CPU performance
        self.model = YOLO("yolov8n.pt")

    def detect(self, frame):
        # 🔥 TRACKING instead of simple detection
        results = self.model.track(
            frame,
            persist=True,   # keeps IDs across frames
            verbose=False
        )

        detections = []

        for r in results:
            if r.boxes.id is None:
                continue

            for box, track_id in zip(r.boxes, r.boxes.id):
                cls_id = int(box.cls[0])
                label = self.model.names[cls_id]
                confidence = float(box.conf[0])

                if confidence < CONFIDENCE_THRESHOLD:
                    continue

                if ALLOWED_LABELS is not None and label not in ALLOWED_LABELS:
                    continue

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                detections.append({
                    "id": int(track_id),
                    "label": label,
                    "confidence": round(confidence, 2),
                    "bbox": [x1, y1, x2, y2]
                })

        return detections
