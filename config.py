"""Configuration management for the launcher application."""
from typing import List, Tuple, Dict, Any, Optional
from pathlib import Path
import json

class Config:
    """Manages application configuration and settings."""
    
    def __init__(self):
        """Initialize configuration with default values."""
        self.URLS = {
            "ChatGPT": "https://chat.openai.com",
            "Gmail": "https://mail.google.com",
            "YouTube": "https://www.youtube.com",
            "GitHub": "https://github.com",
            "Reddit": "https://reddit.com"
        }
        
        self.BUTTON_LOGOS = {
            "ChatGPT": "🤖",
            "Gmail": "📧",
            "YouTube": "▶️",
            "GitHub": "🐱",
            "Reddit": "🌐"
        }
        
        self.LABEL_TEXT = {
            "ChatGPT": "ChatGPT",
            "Gmail": "Gmail",
            "YouTube": "YouTube",
            "GitHub": "GitHub",
            "Reddit": "Reddit"
        }
        
        self.THEMES = {
            "dark": {
                "bg_color": "black",
                "button_color": "#282828",
                "hover_color": "#3a3a3a",
                "highlight_color": "#4a4a4a"
            },
            "light": {
                "bg_color": "white",
                "button_color": "#e0e0e0",
                "hover_color": "#d0d0d0",
                "highlight_color": "#c0c0c0"
            }
        }
        
        self.SETTINGS = {
            "confirm_on_exit": True,
            "enable_analytics": True,
            "show_tooltips": True
        }
        
        self._layout_file = Path("layout.json")
        self._default_layout = [
            ("ChatGPT", 0, 0), ("Gmail", 0, 1), ("YouTube", 0, 2),
            ("GitHub", 1, 0), ("Reddit", 1, 1), (None, 1, 2),
            (None, 2, 0), (None, 2, 1), (None, 2, 2)
        ]

    def load_layout(self) -> List[Tuple[Optional[str], int, int]]:
        """Load button layout from file or return default layout."""
        try:
            if self._layout_file.exists():
                with open(self._layout_file, 'r') as f:
                    return json.load(f)
            return self._default_layout
        except Exception as e:
            print(f"Error loading layout: {e}")
            return self._default_layout

    def save_layout(self, layout: List[Tuple[Optional[str], int, int]]) -> None:
        """Save button layout to file."""
        try:
            with open(self._layout_file, 'w') as f:
                json.dump(layout, f)
        except Exception as e:
            print(f"Error saving layout: {e}")

    def update_settings(self, settings: Dict[str, Any]) -> None:
        """Update application settings."""
        self.SETTINGS.update(settings)

    def get_url(self, key: str) -> str:
        """Get URL for a given key."""
        return self.URLS.get(key, "")
