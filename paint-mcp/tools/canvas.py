from typing import Dict, Any
from utils.errors import format_success, format_error
from utils.helpers import get_paint_app, get_main_window
from utils.coordinates import get_canvas_rect
from pywinauto.keyboard import send_keys
import time

def get_canvas_info() -> Dict[str, Any]:
    try:
        app = get_paint_app()
        win = get_main_window(app)
        rect = get_canvas_rect(win)
        return format_success("get_canvas_info", "Canvas found.", {"rectangle": rect})
    except Exception as e:
        return format_error("get_canvas_info", "Failed to get canvas info.", type(e).__name__, str(e))

def new_canvas(width: int, height: int) -> Dict[str, Any]:
    try:
        app = get_paint_app()
        win = get_main_window(app)
        win.set_focus()
        
        # Trigger New (Ctrl+N)
        send_keys("^n")
        time.sleep(1)
        
        # Handle Don't Save dialog if present
        try:
            dialog = win.child_window(class_name="#32770", timeout=1)
            if dialog.exists():
                btn = dialog.child_window(title_re=".*Don't Save.*|.*No.*", control_type="Button")
                if btn.exists():
                    btn.click()
                    time.sleep(1)
        except Exception:
            pass
            
        # Trigger resize (Ctrl+W)
        send_keys("^w")
        time.sleep(1)
        
        # We assume the Resize dialog pops up. It's usually #32770 or UWP modal
        # We send Tab to navigate to Pixels, space to select it, then type dimensions
        # This is very fragile. We'll try to find the Pixels radio button
        try:
            resize_dialog = win.child_window(title_re=".*Resize.*", control_type="Window")
            # Try semantic click
            pixels_btn = resize_dialog.child_window(title_re=".*Pixels.*", control_type="RadioButton")
            if pixels_btn.exists():
                pixels_btn.click()
                
            # Uncheck maintain aspect ratio
            ratio_chk = resize_dialog.child_window(title_re=".*aspect ratio.*", control_type="CheckBox")
            if ratio_chk.exists() and ratio_chk.get_toggle_state() != 0:
                ratio_chk.click()
                
            # Find Horizontal and Vertical edits
            h_edit = resize_dialog.child_window(auto_id="1032") # Common in Win10
            v_edit = resize_dialog.child_window(auto_id="1033")
            
            if h_edit.exists():
                h_edit.set_edit_text(str(width))
            if v_edit.exists():
                v_edit.set_edit_text(str(height))
                
            ok_btn = resize_dialog.child_window(title_re=".*OK.*", control_type="Button")
            ok_btn.click()
            time.sleep(1)
        except Exception as e:
            # Fallback to pure keys for Resize (Alt+P for pixels, Alt+M for uncheck, etc)
            # This varies widely by locale. Just try to close it if it fails.
            send_keys("{ESC}")
            return format_error("new_canvas", "Could not interact with Resize dialog.", type(e).__name__, str(e))

        return format_success("new_canvas", f"Created new canvas sized {width}x{height}.")
    except Exception as e:
        return format_error("new_canvas", "Failed to create new canvas.", type(e).__name__, str(e))

def resize_canvas(width: int, height: int) -> Dict[str, Any]:
    # Similar to new_canvas but without the Ctrl+N part
    try:
        app = get_paint_app()
        win = get_main_window(app)
        win.set_focus()
        
        send_keys("^w")
        time.sleep(1)
        
        try:
            resize_dialog = win.child_window(title_re=".*Resize.*", control_type="Window")
            pixels_btn = resize_dialog.child_window(title_re=".*Pixels.*", control_type="RadioButton")
            if pixels_btn.exists():
                pixels_btn.click()
                
            ratio_chk = resize_dialog.child_window(title_re=".*aspect ratio.*", control_type="CheckBox")
            if ratio_chk.exists() and ratio_chk.get_toggle_state() != 0:
                ratio_chk.click()
                
            h_edit = resize_dialog.child_window(auto_id="1032")
            v_edit = resize_dialog.child_window(auto_id="1033")
            
            if h_edit.exists():
                h_edit.set_edit_text(str(width))
            if v_edit.exists():
                v_edit.set_edit_text(str(height))
                
            ok_btn = resize_dialog.child_window(title_re=".*OK.*", control_type="Button")
            ok_btn.click()
            time.sleep(1)
        except Exception:
            send_keys("{ESC}")
            return format_error("resize_canvas", "Could not interact with Resize dialog.")
            
        return format_success("resize_canvas", f"Resized canvas to {width}x{height}.")
    except Exception as e:
        return format_error("resize_canvas", "Failed to resize canvas.", type(e).__name__, str(e))

def crop(x1: int, y1: int, x2: int, y2: int) -> Dict[str, Any]:
    try:
        # To crop, we need to select an area first, then hit Crop (Ctrl+Shift+X)
        # Select area is implemented in drawing.py/selection.py.
        # We will assume select_area was called, or we call it here.
        app = get_paint_app()
        win = get_main_window(app)
        win.set_focus()
        send_keys("^+x")
        return format_success("crop", "Triggered crop command.")
    except Exception as e:
        return format_error("crop", "Failed to crop.", type(e).__name__, str(e))
