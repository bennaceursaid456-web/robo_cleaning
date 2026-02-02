"""
Daily Location Reporter for AquaMind

This script should be run once per day (e.g., via Windows Task Scheduler)
to send a location report email for anti-theft monitoring.
"""

from email_service import EmailService
from stats_manager import StatsManager
import sys

# Mock GPS coordinates (replace with actual GPS module in production)
LATITUDE = 52.5200
LONGITUDE = 13.4050

# Mock battery level (replace with actual battery sensor)
BATTERY_LEVEL = 85

def send_daily_report(stats_manager=None):
    """Send daily location and status report"""
    
    # Get total objects collected (if stats manager is available)
    if stats_manager:
        total_collected = stats_manager.get_stats()["total_objects"]
    else:
        # Fallback: read from a persistent file or database
        total_collected = 0
    
    EmailService.send_daily_location(
        latitude=LATITUDE,
        longitude=LONGITUDE,
        battery_level=BATTERY_LEVEL,
        objects_collected=total_collected
    )
    
    print("✅ Daily location report sent successfully")

if __name__ == "__main__":
    send_daily_report()
