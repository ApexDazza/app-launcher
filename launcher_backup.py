"""
App Launcher - A customizable application launcher
Main application file that brings everything together
Created by ApexDazza
"""

import customtkinter as ctk
import keyboard
from typing import Dict, Optional
from typing import Optional
from config import Config
from utilities import logger, Analytics
from gui import LauncherButton, DragDropManager
import keyboard
import customtkinter as ctk

class AppLauncher:
    def __init__(self):
        self.config = Config()
        self.analytics = Analytics()
        self.drag_manager = DragDropManager()
        self.is_edit_mode = False
        self.widgets: Dict[str, LauncherButton] = {}
        
        # Load layout
        self.button_layout = self.config.load_layout()
        
        self.setup_gui()
        self.setup_keyboard_shortcuts()

    def setup_gui(self) -> None:
        """Initialize the main GUI window"""
        # Set theme
        ctk.set_appearance_mode("dark")
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("App Launcher")
        self.root.geometry("600x650")
        self.root.minsize(500, 500)
        
        # Configure grid
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Create main frame
        self.main_frame = ctk.CTkFrame(
            self.root,
            fg_color=self.config.THEMES["dark"]["bg_color"]
        )
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Configure main frame grid
        for i in range(4):
            self.main_frame.grid_rowconfigure(i, weight=1)
        for i in range(3):
            self.main_frame.grid_columnconfigure(i, weight=1)
        
        # Create status bar
        self.create_status_bar()
        
        # Create buttons
        self.create_buttons()
        
        # Set up window close handler
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_status_bar(self) -> None:
        """Create the status and edit bar"""
        self.bottom_bar = ctk.CTkFrame(
            self.root,
            fg_color="transparent"
        )
        self.bottom_bar.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        self.bottom_bar.grid_columnconfigure(0, weight=1)
        
        self.status_label = ctk.CTkLabel(
            self.bottom_bar,
            text="Ready",
            font=("Segoe UI", 12),
            text_color="gray"
        )
        self.status_label.grid(row=0, column=0, sticky="w")
        
        self.edit_button = ctk.CTkButton(
            self.bottom_bar,
            text="✏️ Edit",
            width=100,
            command=self.toggle_edit_mode
        )
        self.edit_button.grid(row=0, column=1, sticky="e")

    def create_buttons(self) -> None:
        """Create all launcher buttons"""
        self.widgets.clear()
        for key, row, col in self.button_layout:
            if key is None:
                continue
                
            button = LauncherButton(
                self.main_frame,
                key,
                self.config,
                self.status_label,
                self.drag_manager.start_drag,
                self.on_drag_motion,
                self.on_drop
            )
            button.grid(row=row, column=col, sticky="nsew", padx=10, pady=10)
            self.widgets[key] = button

    def toggle_edit_mode(self) -> None:
        """Toggle between edit and normal mode"""
        self.is_edit_mode = not self.is_edit_mode
        mode_color = "green" if self.is_edit_mode else self.config.THEMES["dark"]["button_color"]
        mode_text = "✔️ Done" if self.is_edit_mode else "✏️ Edit"
        status_text = "Edit Mode: Drag to rearrange buttons." if self.is_edit_mode else "Ready"
        
        self.edit_button.configure(text=mode_text, fg_color=mode_color)
        self.status_label.configure(text=status_text)

    def on_drag_motion(self, event) -> None:
        """Handle drag motion"""
        if not self.drag_manager.drag_data["ghost"]:
            return
            
        # Update ghost position
        dx = event.x_root - self.drag_manager.drag_data["start_pos"][0]
        dy = event.y_root - self.drag_manager.drag_data["start_pos"][1]
        ghost = self.drag_manager.drag_data["ghost"]
        ghost.geometry(f"+{event.x_root-30}+{event.y_root-30}")
        
        # Highlight potential drop target
        self.highlight_drop_target(event)

    def highlight_drop_target(self, event) -> None:
        """Highlight the potential drop target"""
        for widget in self.widgets.values():
            widget.configure(border_width=0)
        
        target = self.find_target_widget(event)
        if target:
            target.configure(
                border_width=2,
                border_color=self.config.THEMES["dark"]["highlight_color"]
            )

    def find_target_widget(self, event) -> Optional[LauncherButton]:
        """Find the widget under the cursor"""
        x, y = event.x_root, event.y_root
        for widget in self.widgets.values():
            if widget == self.drag_manager.drag_data["widget"]:
                continue
            wx = widget.winfo_rootx()
            wy = widget.winfo_rooty()
            ww = widget.winfo_width()
            wh = widget.winfo_height()
            if wx < x < wx + ww and wy < y < wy + wh:
                return widget
        return None

    def on_drop(self, event) -> None:
        """Handle drop event"""
        if not self.drag_manager.drag_data["widget"]:
            return
        
        dragged = self.drag_manager.drag_data["widget"]
        start_info = self.drag_manager.drag_data["start_info"]
        
        if self.drag_manager.drag_data["ghost"]:
            self.drag_manager.drag_data["ghost"].destroy()
            self.drag_manager.drag_data["ghost"] = None
        
        target = self.find_target_widget(event)
        for widget in self.widgets.values():
            widget.configure(border_width=0)
        
        if target:
            # Swap positions
            target_info = target.grid_info()
            dragged.grid(row=target_info['row'], column=target_info['column'],
                        sticky="nsew", padx=10, pady=10)
            target.grid(row=start_info['row'], column=start_info['column'],
                       sticky="nsew", padx=10, pady=10)
            
            # Update layout
            dragged_key = next(k for k, v in self.widgets.items() if v == dragged)
            target_key = next(k for k, v in self.widgets.items() if v == target)
            
            self.update_layout(dragged_key, target_key,
                             target_info['row'], target_info['column'],
                             start_info['row'], start_info['column'])
        else:
            # Return to original position
            dragged.grid(row=start_info['row'], column=start_info['column'],
                        sticky="nsew", padx=10, pady=10)
        
        self.drag_manager.drag_data["widget"] = None

    def update_layout(self, dragged_key: str, target_key: str,
                     target_row: int, target_col: int,
                     start_row: int, start_col: int) -> None:
        """Update and save the button layout"""
        for i, (key, r, c) in enumerate(self.button_layout):
            if key == dragged_key:
                self.button_layout[i] = (dragged_key, target_row, target_col)
            elif key == target_key:
                self.button_layout[i] = (target_key, start_row, start_col)
        
        self.config.save_layout(self.button_layout)

    def setup_keyboard_shortcuts(self) -> None:
        """Set up keyboard shortcuts"""
        keyboard.add_hotkey('ctrl+e', self.toggle_edit_mode)
        keyboard.add_hotkey('ctrl+s', 
                          lambda: self.config.save_layout(self.button_layout))
        keyboard.add_hotkey('ctrl+r', self.refresh_layout)

    def refresh_layout(self) -> None:
        """Refresh the button layout"""
        self.button_layout = self.config.load_layout()
        self.create_buttons()

    def on_close(self) -> None:
        """Handle window close event"""
        if self.config.SETTINGS["confirm_on_exit"]:
            if not ctk.messagebox.askokcancel("Quit", "Do you want to quit?"):
                return
        self.root.destroy()

    def run(self) -> None:
        """Start the application"""
        try:
            self.root.mainloop()
        except Exception as e:
            logger.error(f"Application error: {str(e)}")
            raise

if __name__ == "__main__":
    try:
        app = AppLauncher()
        app.run()
    except Exception as e:
        logger.critical(f"Failed to start application: {str(e)}")
        raise

app.mainloop()