from email_service import EmailService
from ollama_service import OllamaService

class AlertManager:
    def __init__(self):
        self.alerted_ids = set()
        self.last_alert = None
        self.ollama = OllamaService()

    def handle_detection(self, detection, category):
        # Trigger for everything except "other" to show off AI capabilities
        if category == "other":
            return

        obj_id = detection["id"]

        if obj_id in self.alerted_ids:
            return

        self.alerted_ids.add(obj_id)

        # 1. Store initial alert state
        self.last_alert = {
            "id": obj_id,
            "label": detection["label"],
            "type": category,
            "advice": "🤖 AI Analyzing molecular composition..."
        }

        # 2. Callback when AI is ready
        def on_ai_response(advice):
            if self.last_alert and self.last_alert["id"] == obj_id:
                self.last_alert["advice"] = advice
                print(f"✅ AI Advice Updated: {advice}")

        # 3. Trigger Async AI
        print(f"⏳ Asking AI about '{detection['label']}'...")
        self.ollama.ask_async(detection["label"], on_ai_response)

        # 4. Email Triggers
        if category == "toxic":
            EmailService.send_toxic_alert(
                object_id=obj_id,
                label=detection["label"],
                confidence=detection["confidence"],
            )
        elif category == "human":
            EmailService.send_human_alert(
                object_id=obj_id,
                label=detection["label"],
                confidence=detection["confidence"],
                location="GPS: 52.5200°N, 13.4050°E"  # TODO: Get from GPS module
            )

    def get_last_alert(self):
        return self.last_alert

