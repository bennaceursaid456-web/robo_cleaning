import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from email_config import (
    SMTP_SERVER,
    SMTP_PORT,
    SENDER_EMAIL,
    SENDER_PASSWORD,
    RECEIVER_EMAIL,
)


class EmailService:
    @staticmethod
    def send_toxic_alert(object_id, label, confidence):
        subject = "🚨 Toxic Object Detected – AquaMind Alert"

        body = f"""
Hello,

The AquaMind water-cleaning system detected a TOXIC object.

Details:
- Object ID: #{object_id}
- Type: {label}
- Confidence: {confidence}

Risk Level: HIGH

Immediate attention is recommended.

— AquaMind AI System
"""

        EmailService._send_email(subject, body)

    @staticmethod
    def send_human_alert(object_id, label, confidence, location="Unknown"):
        subject = "⚠️ HUMAN DETECTED – Immediate Action Required"

        body = f"""
URGENT ALERT

The AquaMind robot has detected a HUMAN in the water.

Details:
- Object ID: #{object_id}
- Type: {label}
- Confidence: {confidence}
- Location: {location}

⚠️ ACTION REQUIRED: Please come to the robot's location immediately.

This could indicate:
- Someone in distress
- Unauthorized access to the cleaning area
- Potential safety hazard

— AquaMind Emergency System
"""

        EmailService._send_email(subject, body)

    @staticmethod
    def send_daily_location(latitude, longitude, battery_level, objects_collected):
        subject = "📍 AquaMind Daily Report – Location & Status"

        body = f"""
Daily Status Report

Your AquaMind robot is operational and reporting its location.

Current Status:
- GPS Location: {latitude}°N, {longitude}°E
- Battery Level: {battery_level}%
- Objects Collected Today: {objects_collected}

🔒 Anti-Theft Notice:
This automated report confirms the robot's location. If you did not authorize
any movement, please investigate immediately.

View location on map:
https://www.google.com/maps?q={latitude},{longitude}

— AquaMind Security System
"""

        EmailService._send_email(subject, body)

    @staticmethod
    def _send_email(subject, body):
        """Internal method to handle actual email sending"""
        try:
            msg = MIMEMultipart()
            msg["From"] = SENDER_EMAIL
            msg["To"] = RECEIVER_EMAIL
            msg["Subject"] = subject

            msg.attach(MIMEText(body, "plain"))

            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(SENDER_EMAIL, SENDER_PASSWORD)
                server.send_message(msg)
            
            print(f"✅ Email sent: {subject}")
        except Exception as e:
            print(f"❌ Email failed: {e}")


