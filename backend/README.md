# vision_service

A small vision service for object detection and alerts.

Included:
- Python source files for detection, alerting, and email notifications.
- YOLOv8 model weights: `yolov8m.pt`, `yolov8n.pt` (included per request).

Quick start:

1. Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Run the service:

```bash
python main.py
```

Notes:
- The repository includes model weight files which are large.
- Add any sensitive credentials to a local `.env` file (and don't commit them).
