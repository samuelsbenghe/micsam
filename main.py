# System imports
import os
import sys
import threading
import json
from pathlib import Path
from typing import Any, cast

# Keyboard
import keyboard

# Windows-specific imports for mutex and tray icon
import win32event
import win32api
import winerror
import pystray

# HTTP requests
import requests

# PIL
from PIL import Image, ImageDraw, ImageFont

# GUI
import tkinter as tk

# prevent duplicate instance
mutex = win32event.CreateMutex(  # pyright: ignore[reportUnknownMemberType]
    cast(Any, None), False, "MicSamMutex"
)

if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
    sys.exit(0)
# ---------------- UPDATER CHECK ----------------

VERSION = "0.0.1"
REPORT = "samuelsbenghe/micsam"


def get_latest_release():
    url = f"https://api.github.com/repos/{REPORT}/releases/latest"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


# ---------------- STATE MANAGEMENT ----------------
state = {"active": False}
appdata = Path(os.getenv("APPDATA", "."))
mic_sam_dir = appdata / "MicSam"
mic_sam_dir.mkdir(exist_ok=True)
config_file = mic_sam_dir / "config.json"

if config_file.exists():
    with open(config_file, "r") as f:
        state.update(json.load(f))
else:
    with open(config_file, "w") as f:
        json.dump(state, f)


# ---------------- GUI SETUP ----------------
root = tk.Tk()
root.title("MicSam Controller v" + VERSION)


# ---------------- ICON ----------------
def create_icon(color: str) -> Image.Image:
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    text = "100"
    font = ImageFont.truetype("arial.ttf", 36)

    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = (64 - text_width) // 2
    y = (64 - text_height) // 2

    circle_color = (0, 200, 0, 255) if color == "green" else (200, 0, 0, 255)

    draw.ellipse(
        (5, 5, 20, 20),
        fill=circle_color,
    )
    draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)

    return img


# ---------------- HOTKEY ACTIONS ----------------
def hotkey_toggle():
    state["active"] = not state["active"]

    icon.icon = create_icon("green" if state["active"] else "red")
    icon.title = "Active" if state["active"] else "Inactive"


def keyboard_listener():
    keyboard.add_hotkey("f8", hotkey_toggle)
    keyboard.wait()


# ---------------- TRAY ACTIONS ----------------


def toggle_state(icon, item):
    state["active"] = not state["active"]

    icon.icon = create_icon("green" if state["active"] else "red")
    icon.title = "Active" if state["active"] else "Inactive"


def show_window(icon=None, item=None):
    root.after(0, root.deiconify)


def hide_window():
    root.withdraw()


def quit_app(icon=None, item=None):
    icon.stop()
    root.destroy()


# ---------------- TRAY SETUP ----------------

icon = pystray.Icon(
    "MicSam",
    create_icon("red"),
    "Inactive",
    menu=pystray.Menu(
        pystray.MenuItem("Open", show_window),
        pystray.MenuItem("Toggle", toggle_state),
        pystray.MenuItem("Quit", quit_app),
    ),
)


def run_tray():
    icon.run()


# ---------------- GUI BEHAVIOR ----------------


def on_minimize(event):
    hide_window()


def on_close():
    hide_window()  # instead of exiting


root.protocol("WM_DELETE_WINDOW", on_close)
root.bind("<Unmap>", on_minimize)

# Example GUI content
label = tk.Label(root, text="My App Running")
label.pack(padx=20, pady=20)

# ---------------- START ----------------

threading.Thread(target=keyboard_listener, daemon=True).start()
threading.Thread(target=run_tray, daemon=True).start()
root.mainloop()
