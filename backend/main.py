import cv2
from detector import YoloDetector

detector = YoloDetector()

cap = cv2.VideoCapture(0)  # try 0 first

print("Camera opened:", cap.isOpened())

if not cap.isOpened():
    print("❌ Failed to open camera")
    exit(1)

while True:
    ret, frame = cap.read()

    if not ret:
        print("❌ Failed to read frame")
        break

    detections = detector.detect(frame)

    for d in detections:
        x1, y1, x2, y2 = d["bbox"]
        label = f"{d['label']} #{d['id']} ({d['confidence']})"

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
        cv2.putText(
    frame,
    label,
    (x1, max(y1 - 15, 20)),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.8,
    (0, 255,0) ,
2 )

    cv2.imshow("YOLO Vision Service", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
