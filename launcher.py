import customtkinter as ctk
import webbrowser
import json

# --- APP CONFIGURATION ---
DEFAULT_BUTTON_LAYOUT = [
    ("arlo", 0, 0), ("excellence", 0, 1), ("vibepy", 0, 2),
    ("gemgenieer", 1, 0), ("grok", 1, 1), ("printful", 1, 2),
    ("copilot", 2, 0), ("gemini", 2, 1), ("speedtest", 2, 2),
    (None, 3, 0), ("email", 3, 1), (None, 3, 2)
]

URLS = {
    "gemgenieer": "https://gemini.google.com/gem/59c4310b2893",
    "excellence": "https://gemini.google.com/gem/acf5c308f4c0",
    "gemini": "https://gemini.google.com/app",
    "printful": "https://www.printful.com/dashboard/default",
    "grok": "https://grok.com/",
    "arlo": "https://my.arlo.com/#/cameras_new",
    "vibepy": "https://gemini.google.com/gem/95f6d0a1d1bb",
    "copilot": "https://copilot.microsoft.com/chats/MRpAsgYGkmR7payGFmqoG",
    "speedtest": "https://www.speedtest.net/",
    "email": "https://app.clean.email/?a=08793111af54b14dd1f15527a2b338fb#/start"
}

BUTTON_LOGOS = {
    "gemgenieer": "🏎️", "excellence": "📊", "gemini": "✨",
    "printful": "👕", "grok": "🤖", "arlo": "📷",
    "vibepy": "👾", "copilot": "✈️", "speedtest": "⚡",
    "email": "✉️"
}

LABEL_TEXT = {
    "gemgenieer": "Engineer", "excellence": "G:Excel", "gemini": "Gemini",
    "printful": "Printful", "grok": "Grok", "arlo": "Cameras",
    "vibepy": "VibePy", "copilot": "Copilot", "speedtest": "Speedtest",
    "email": "Email"
}

# --- GLOBAL VARIABLES FOR DRAG & DROP ---
drag_data = {"widget": None, "start_info": {}, "ghost": None, "start_pos": (0, 0)}
is_edit_mode = False
widgets = {}

# --- FUNCTIONS ---
def open_link(url, status_label):
    if is_edit_mode: return
    try:
        webbrowser.open(url)
        status_label.configure(text="Opened link successfully!", text_color="green")
    except Exception as e:
        status_label.configure(text=f"Error: {e}", text_color="red")

def save_layout(layout):
    with open("layout.json", "w") as f:
        json.dump(layout, f, indent=4)
    print("Layout saved.")

def load_layout():
    try:
        with open("layout.json", "r") as f:
            return [tuple(item) for item in json.load(f)]
    except (FileNotFoundError, json.JSONDecodeError):
        return DEFAULT_BUTTON_LAYOUT

# --- DRAG & DROP LOGIC ---
def on_drag_start(event, widget):
    if not is_edit_mode: return
    drag_data["widget"] = widget
    drag_data["start_info"] = widget.grid_info()
    drag_data["start_pos"] = (event.x_root, event.y_root)
    
    # Create a semi-transparent "ghost" window
    drag_data["ghost"] = ctk.CTkToplevel(app)
    drag_data["ghost"].overrideredirect(True)
    drag_data["ghost"].attributes("-alpha", 0.7)
    drag_data["ghost"].attributes("-topmost", True)
    
    key = next(k for k, v in widgets.items() if v == widget)
    ghost_content = create_button_widget(drag_data["ghost"], key, status_label, is_ghost=True)
    ghost_content.pack(expand=True, fill="both")
    
    # Position ghost at the start position
    drag_data["ghost"].geometry(f"{widget.winfo_width()}x{widget.winfo_height()}+{widget.winfo_rootx()}+{widget.winfo_rooty()}")
    
    widget.grid_remove() # Hide the original widget

def on_drag_motion(event):
    if not drag_data["ghost"]: return
    # **FIX:** Correctly calculate new position based on initial mouse click
    dx = event.x_root - drag_data["start_pos"][0]
    dy = event.y_root - drag_data["start_pos"][1]
    start_x = drag_data["widget"].winfo_rootx()
    start_y = drag_data["widget"].winfo_rooty()
    drag_data["ghost"].geometry(f"+{start_x + dx}+{start_y + dy}")

    # Highlight target under cursor
    for w in widgets.values():
        w.configure(border_width=0)
    
    target_widget = find_target_widget(event)
    if target_widget:
        target_widget.configure(border_width=2, border_color="yellow")

def on_drop(event):
    if not drag_data["widget"]: return
    
    dragged_widget = drag_data["widget"]
    start_info = drag_data["start_info"]
    
    if drag_data["ghost"]:
        drag_data["ghost"].destroy()
        drag_data["ghost"] = None

    target_widget = find_target_widget(event)
    for w in widgets.values():
        w.configure(border_width=0)

    if target_widget:
        target_info = target_widget.grid_info()
        
        dragged_widget.grid(row=target_info['row'], column=target_info['column'], sticky="nsew", padx=10, pady=10)
        target_widget.grid(row=start_info['row'], column=start_info['column'], sticky="nsew", padx=10, pady=10)

        dragged_key = next(k for k, v in widgets.items() if v == dragged_widget)
        target_key = next(k for k, v in widgets.items() if v == target_widget)
        for i, (key, r, c) in enumerate(BUTTON_LAYOUT):
            if key == dragged_key:
                BUTTON_LAYOUT[i] = (dragged_key, target_info['row'], target_info['column'])
            elif key == target_key:
                BUTTON_LAYOUT[i] = (target_key, start_info['row'], start_info['column'])
        save_layout(BUTTON_LAYOUT)
    else:
        dragged_widget.grid(row=start_info['row'], column=start_info['column'], sticky="nsew", padx=10, pady=10)

    drag_data["widget"] = None

def find_target_widget(event):
    x, y = event.x_root, event.y_root
    for w in widgets.values():
        if w == drag_data["widget"]: continue
        wx, wy, ww, wh = w.winfo_rootx(), w.winfo_rooty(), w.winfo_width(), w.winfo_height()
        if wx < x < wx + ww and wy < y < wy + wh:
            return w
    return None

# --- GUI SETUP ---
ctk.set_appearance_mode("dark")
app = ctk.CTk()
app.title("App Launcher")
BUTTON_LAYOUT = load_layout()

app.geometry("600x650")
app.minsize(500, 500)

app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=1)

main_frame = ctk.CTkFrame(app, fg_color="black")
main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

for i in range(4): main_frame.grid_rowconfigure(i, weight=1)
for i in range(3): main_frame.grid_columnconfigure(i, weight=1)

# --- EDIT MODE TOGGLE ---
def toggle_edit_mode():
    global is_edit_mode
    is_edit_mode = not is_edit_mode
    mode_color = "green" if is_edit_mode else "#282828"
    mode_text = "✔️ Done" if is_edit_mode else "✏️ Edit"
    status_text = "Edit Mode: Drag to rearrange buttons." if is_edit_mode else "Ready"
    
    edit_button.configure(text=mode_text, fg_color=mode_color)
    status_label.configure(text=status_text)
    # Cursor is handled by the widget itself now

# --- CREATE WIDGETS ---
def create_button_widget(parent, logo_key, status_label, is_ghost=False):
    if logo_key is None: return None
    container = ctk.CTkFrame(parent, fg_color="transparent")
    
    button = ctk.CTkButton(container, text=BUTTON_LOGOS.get(logo_key, "❓"), font=("Segoe UI Emoji", 40), corner_radius=20, fg_color="#282828", hover_color="#3a3a3a", cursor="hand2", command=lambda: open_link(URLS[logo_key], status_label))
    button.pack(expand=True, fill="both", padx=10, pady=10)
    
    label = ctk.CTkLabel(container, text=LABEL_TEXT.get(logo_key, logo_key), font=("Segoe UI", 14, "bold"), text_color="white")
    label.pack(padx=5, pady=(0, 5))
    
    if not is_ghost:
        # Bind events to all children of the container as well
        for child in [container, button, label]:
            child.bind("<ButtonPress-1>", lambda event, w=container: on_drag_start(event, w))
            child.bind("<B1-Motion>", on_drag_motion)
            child.bind("<ButtonRelease-1>", on_drop)
    
    return container

# --- STATUS AND EDIT BAR ---
bottom_bar = ctk.CTkFrame(app, fg_color="transparent")
bottom_bar.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
bottom_bar.grid_columnconfigure(0, weight=1)

status_label = ctk.CTkLabel(bottom_bar, text="Ready", font=("Segoe UI", 12), text_color="gray")
status_label.grid(row=0, column=0, sticky="w")

edit_button = ctk.CTkButton(bottom_bar, text="✏️ Edit", width=100, command=toggle_edit_mode)
edit_button.grid(row=0, column=1, sticky="e")

# --- PLACE BUTTONS DYNAMICALLY ---
for key, row, col in BUTTON_LAYOUT:
    widget = create_button_widget(main_frame, key, status_label)
    if widget:
        widget.grid(row=row, column=col, sticky="nsew", padx=10, pady=10)
        widgets[key] = widget

app.mainloop()