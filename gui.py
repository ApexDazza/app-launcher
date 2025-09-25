"""GUI components for the launcher application."""
from typing import Dict, Any, Optional, Callable
import customtkinter as ctk
from utilities import open_link, logger

class LauncherButton(ctk.CTkFrame):
    """Custom button widget for the launcher application."""
    
    def __init__(self, parent: any, logo: str, label: str, url: str,
                 status_label: ctk.CTkLabel, theme: Dict[str, str],
                 analytics: Optional[Any] = None):
        """Initialize the button widget."""
        super().__init__(parent, fg_color="transparent")
        
        self.url = url
        self.analytics = analytics
        self.key = label
        
        # Create button
        self.button = ctk.CTkButton(
            self,
            text=logo,
            font=("Segoe UI Emoji", 40),
            corner_radius=20,
            fg_color=theme["button_color"],
            hover_color=theme["hover_color"],
            cursor="hand2",
            command=lambda: self._handle_click(status_label)
        )
        self.button.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Create label
        self.label = ctk.CTkLabel(
            self,
            text=label,
            font=("Segoe UI", 14, "bold"),
            text_color="white"
        )
        self.label.pack(padx=5, pady=(0, 5))

    def _handle_click(self, status_label: ctk.CTkLabel) -> None:
        """Handle button click event."""
        open_link(self.url, status_label)
        if self.analytics:
            self.analytics.track_button_click(self.key)

    def set_drag_bindings(self, start_fn: Callable, motion_fn: Callable,
                         end_fn: Callable) -> None:
        """Set drag and drop event bindings."""
        for widget in [self, self.button, self.label]:
            widget.bind("<ButtonPress-1>",
                       lambda event, w=self: start_fn(event, w))
            widget.bind("<B1-Motion>", motion_fn)
            widget.bind("<ButtonRelease-1>", end_fn)


class DragDropManager:
    """Manages drag and drop operations for buttons."""
    
    def __init__(self):
        """Initialize drag and drop manager."""
        self.drag_data = {
            "widget": None,
            "ghost": None,
            "start_pos": (0, 0),
            "start_info": None
        }

    def start_drag(self, event: any, widget: LauncherButton) -> None:
        """Start dragging a widget."""
        if not hasattr(event, "widget"):  # Skip invalid events
            return
            
        self.drag_data["widget"] = widget
        self.drag_data["start_pos"] = (event.x_root, event.y_root)
        self.drag_data["start_info"] = widget.grid_info()
        
        # Create ghost button
        ghost = self._create_ghost_button(event, widget)
        self.drag_data["ghost"] = ghost
        ghost.lift()  # Keep ghost on top
        logger.debug(f"Started dragging widget at ({event.x_root}, {event.y_root})")

    def _create_ghost_button(self, event: any, widget: LauncherButton) -> ctk.CTkToplevel:
        """Create a ghost button for drag visualization."""
        ghost = ctk.CTkToplevel()
        ghost.overrideredirect(True)
        ghost.attributes('-alpha', 0.5)
        ghost.geometry(f"{widget.winfo_width()}x{widget.winfo_height()}")
        
        # Create ghost content
        frame = ctk.CTkFrame(ghost, fg_color=widget.cget("fg_color"))
        frame.pack(fill="both", expand=True)
        
        # Position ghost at cursor
        ghost.geometry(f"+{event.x_root-30}+{event.y_root-30}")
        return ghost
