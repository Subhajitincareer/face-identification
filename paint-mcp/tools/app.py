import subprocess
from typing import Dict, Any
from utils.errors import format_success, format_error, PaintNotRunningError
from utils.helpers import get_paint_app, wait_for_window, get_main_window

def open_paint(reuse_existing: bool = True, new_window: bool = False) -> Dict[str, Any]:
    try:
        if reuse_existing and not new_window:
            app = get_paint_app()
            if app:
                try:
                    win = get_main_window(app)
                    return format_success(
                        action="open_paint",
                        message="Reused existing Paint instance.",
                        data={
                            "window_title": win.window_text(),
                            "process_id": app.process
                        }
                    )
                except Exception:
                    pass
        
        # Start new Paint
        process = subprocess.Popen(["mspaint.exe"])
        
        # Wait for window
        success = wait_for_window()
        if not success:
            return format_error("open_paint", "Started Paint but window did not appear.", "TimeoutError")
            
        app = get_paint_app()
        if app:
            win = get_main_window(app)
            return format_success(
                action="open_paint",
                message="Launched new Paint instance.",
                data={
                    "window_title": win.window_text(),
                    "process_id": app.process
                }
            )
        return format_error("open_paint", "Could not connect to new Paint instance.", "ConnectionError")
    except Exception as e:
        return format_error("open_paint", "Failed to launch Paint.", type(e).__name__, str(e))

def close_paint(save_if_needed: bool = False, force: bool = False) -> Dict[str, Any]:
    try:
        app = get_paint_app()
        if not app:
            return format_error("close_paint", "No Paint instance found.", "PaintNotRunningError")
            
        win = get_main_window(app)
        win.set_focus()
        win.close()
        
        # Check for save dialog
        try:
            dialog = win.child_window(class_name="#32770", timeout=2)
            if dialog.exists():
                if force:
                    btn = dialog.child_window(title_re=".*Don't Save.*|.*No.*", control_type="Button")
                    if btn.exists():
                        btn.click()
                        return format_success("close_paint", "Closed Paint (unsaved changes discarded).")
                elif save_if_needed:
                    btn = dialog.child_window(title_re=".*Save.*|.*Yes.*", control_type="Button")
                    if btn.exists():
                        btn.click()
                        return format_success("close_paint", "Closed Paint after saving.")
                else:
                    btn = dialog.child_window(title_re=".*Cancel.*", control_type="Button")
                    if btn.exists():
                        btn.click()
                    return format_error(
                        "close_paint", 
                        "Unsaved changes detected. Aborted close.", 
                        "ConfirmationRequired"
                    )
        except Exception:
            pass
            
        return format_success("close_paint", "Paint closed successfully.")
    except Exception as e:
        return format_error("close_paint", "Failed to close Paint.", type(e).__name__, str(e))

def get_paint_state() -> Dict[str, Any]:
    try:
        app = get_paint_app()
        if not app:
            return format_success("get_paint_state", data={"running": False})
            
        win = get_main_window(app)
        title = win.window_text()
        
        from utils.coordinates import get_canvas_rect
        try:
            canvas = get_canvas_rect(win)
        except Exception:
            canvas = None
            
        return format_success("get_paint_state", data={
            "running": True,
            "window_title": title,
            "process_id": app.process,
            "canvas_bounds": canvas
        })
    except Exception as e:
        return format_error("get_paint_state", "Failed to get state.", type(e).__name__, str(e))

def inspect_paint() -> Dict[str, Any]:
    try:
        app = get_paint_app()
        if not app:
            return format_error("inspect_paint", "No Paint instance found.", "PaintNotRunningError")
            
        win = get_main_window(app)
        elements = []
        
        def traverse(element, depth=0):
            if depth > 5: # Limit depth to avoid massive output
                return
            for child in element.children():
                try:
                    rect = child.rectangle()
                    elements.append({
                        "name": child.window_text(),
                        "control_type": child.element_info.control_type,
                        "automation_id": child.element_info.automation_id,
                        "class_name": child.element_info.class_name,
                        "visible": child.is_visible(),
                        "enabled": child.is_enabled(),
                        "rectangle": {"x": rect.left, "y": rect.top, "width": rect.width(), "height": rect.height()}
                    })
                    traverse(child, depth + 1)
                except Exception:
                    pass
                    
        traverse(win)
        
        return format_success("inspect_paint", data={
            "window": {
                "title": win.window_text(),
                "process_id": app.process
            },
            "elements": elements
        })
    except Exception as e:
        return format_error("inspect_paint", "Failed to inspect Paint.", type(e).__name__, str(e))
