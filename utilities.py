"""Utility functions and classes for the launcher application."""
import logging
from datetime import datetime
from typing import Optional
import webbrowser
import json
from pathlib import Path

# Set up logging
logger = logging.getLogger('launcher')
logger.setLevel(logging.INFO)

# Create handlers
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler('launcher.log')

# Create formatters and add it to handlers
log_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(log_format)
file_handler.setFormatter(log_format)

# Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

class Analytics:
    """Tracks application usage analytics."""
    
    def __init__(self):
        """Initialize analytics with default values."""
        self.analytics_file = Path('analytics.json')
        self.data = self._load_data()

    def _load_data(self) -> dict:
        """Load analytics data from file."""
        try:
            if self.analytics_file.exists():
                with open(self.analytics_file, 'r') as f:
                    return json.load(f)
            return {"launches": 0, "button_clicks": {}}
        except Exception as e:
            logger.error(f"Failed to load analytics: {e}")
            return {"launches": 0, "button_clicks": {}}

    def save_data(self) -> None:
        """Save analytics data to file."""
        try:
            with open(self.analytics_file, 'w') as f:
                json.dump(self.data, f)
        except Exception as e:
            logger.error(f"Failed to save analytics: {e}")

    def track_launch(self) -> None:
        """Track application launch."""
        self.data["launches"] += 1
        self.save_data()

    def track_button_click(self, button_key: str) -> None:
        """Track button click."""
        if button_key not in self.data["button_clicks"]:
            self.data["button_clicks"][button_key] = 0
        self.data["button_clicks"][button_key] += 1
        self.save_data()

def open_link(url: str, status_label: Optional[any] = None) -> None:
    """Open URL in default browser and update status."""
    try:
        webbrowser.open(url)
        if status_label:
            status_label.configure(text=f"Opening {url}...")
        logger.info(f"Opened URL: {url}")
    except Exception as e:
        error_msg = f"Failed to open {url}: {str(e)}"
        if status_label:
            status_label.configure(text=error_msg)
        logger.error(error_msg)

def get_session_id() -> str:
    """Generate a unique session ID."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")
