from typing import Dict, Any
import time
import os
from utils.errors import format_success, format_error
from utils.helpers import get_paint_app, get_main_window
from pywinauto.keyboard import send_keys

def open_image(path: str) -> Dict[str, Any]:
    try:
        abs_path = os.path.abspath(path)
        if not os.path.exists(abs_path):
            return format_error("open_image", f"File not found: {abs_path}", "FileNotFoundError")
            
        app = get_paint_app()
        if not app:
            # We could launch paint here, but let's assume it's running
            from .app import open_paint
            open_paint()
            app = get_paint_app()
            
        win = get_main_window(app)
        win.set_focus()
        
        send_keys("^o")
        time.sleep(1.5)
        
        send_keys(abs_path.replace(" ", "{SPACE}"))
        send_keys("{ENTER}")
        time.sleep(1)
        
        return format_success("open_image", "Opened image.", {"path": abs_path, "window_title": win.window_text()})
    except Exception as e:
        return format_error("open_image", "Failed to open image.", type(e).__name__, str(e))

def save_image() -> Dict[str, Any]:
    try:
        app = get_paint_app()
        win = get_main_window(app)
        win.set_focus()
        
        send_keys("^s")
        time.sleep(1)
        return format_success("save_image", "Triggered save.")
    except Exception as e:
        return format_error("save_image", "Failed to save image.", type(e).__name__, str(e))

def save_image_as(path: str) -> Dict[str, Any]:
    try:
        abs_path = os.path.abspath(path)
        if os.path.exists(abs_path):
            return format_error("save_image_as", f"File already exists: {abs_path}. Will not silently overwrite.", "FileExistsError")
            
        app = get_paint_app()
        win = get_main_window(app)
        win.set_focus()
        
        # F12 is Save As in Paint, or Ctrl+Shift+S
        send_keys("{F12}")
        time.sleep(1.5)
        
        send_keys(abs_path.replace(" ", "{SPACE}"))
        send_keys("{ENTER}")
        time.sleep(1)
        
        if os.path.exists(abs_path):
            return format_success("save_image_as", "Saved image.", {"path": abs_path})
        else:
            return format_error("save_image_as", "Save dialog accepted but file not found on disk.", "FileOperationError")
    except Exception as e:
        return format_error("save_image_as", "Failed to save image.", type(e).__name__, str(e))

def export_image(path: str, format: str) -> Dict[str, Any]:
    # In paint, saving as with a specific extension generally handles the format export.
    return save_image_as(path)
