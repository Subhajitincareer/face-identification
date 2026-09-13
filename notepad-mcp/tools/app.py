import subprocess
from typing import Dict, Any
from utils.errors import format_success, format_error
from utils.helpers import get_notepad_app, wait_for_window
from utils.selectors import MAIN_WINDOW_CLASS
from pywinauto.findwindows import find_window

def open_notepad(reuse_existing: bool = True, new_window: bool = False) -> Dict[str, Any]:
    """Launch Windows Notepad or reuse an existing one."""
    try:
        if reuse_existing and not new_window:
            app = get_notepad_app()
            if app:
                # Find the main window
                try:
                    win = app.top_window()
                    return format_success(
                        action="open_notepad",
                        message="Reused existing Notepad instance.",
                        data={
                            "window_title": win.window_text(),
                            "process_id": app.process
                        }
                    )
                except Exception:
                    pass
        
        # Start new Notepad
        process = subprocess.Popen(["notepad.exe"])
        
        # Wait for window to appear
        success = wait_for_window(class_name=MAIN_WINDOW_CLASS)
        if not success:
            return format_error("open_notepad", "Started Notepad but window did not appear.", "TimeoutError")
            
        app = get_notepad_app(process.pid)
        if app:
            win = app.top_window()
            return format_success(
                action="open_notepad",
                message="Launched new Notepad instance.",
                data={
                    "window_title": win.window_text(),
                    "process_id": process.pid
                }
            )
        return format_error("open_notepad", "Could not connect to new Notepad instance.", "ConnectionError")
    except Exception as e:
        return format_error("open_notepad", "Failed to launch Notepad.", type(e).__name__, str(e))

def close_notepad(save_if_needed: bool = False, force: bool = False) -> Dict[str, Any]:
    """Close the current Notepad window."""
    try:
        app = get_notepad_app()
        if not app:
            return format_error("close_notepad", "No Notepad instance found.", "NotFoundError")
            
        win = app.top_window()
        win.set_focus()
        win.close()
        
        # Check for save dialog
        try:
            # Wait briefly for dialog
            dialog = win.child_window(class_name="#32770", timeout=2)
            if dialog.exists():
                if force:
                    # Click Don't Save
                    btn = dialog.child_window(title_re=".*Don't Save.*|.*No.*", control_type="Button")
                    if btn.exists():
                        btn.click()
                        return format_success("close_notepad", "Closed Notepad (unsaved changes discarded).")
                elif save_if_needed:
                    # Click Save
                    btn = dialog.child_window(title_re=".*Save.*|.*Yes.*", control_type="Button")
                    if btn.exists():
                        btn.click()
                        return format_success("close_notepad", "Closed Notepad after saving.")
                else:
                    # Neither force nor save_if_needed, so we require confirmation
                    # Click Cancel to abort closing
                    btn = dialog.child_window(title_re=".*Cancel.*", control_type="Button")
                    if btn.exists():
                        btn.click()
                    return format_error(
                        "close_notepad", 
                        "Unsaved changes detected. Aborted close.", 
                        "ConfirmationRequired",
                        "Please pass save_if_needed=True or force=True to proceed."
                    )
        except Exception:
            pass # No dialog appeared
            
        return format_success("close_notepad", "Notepad closed successfully.")
    except Exception as e:
        return format_error("close_notepad", "Failed to close Notepad.", type(e).__name__, str(e))

def inspect_notepad() -> Dict[str, Any]:
    """Return a structured representation of the current Notepad UI."""
    try:
        app = get_notepad_app()
        if not app:
            return format_error("inspect_notepad", "No Notepad instance found.", "NotFoundError")
            
        win = app.top_window()
        elements = []
        
        # We limit the inspection depth and types to avoid too much data
        for child in win.children():
            try:
                elements.append({
                    "name": child.window_text(),
                    "control_type": child.element_info.control_type,
                    "automation_id": child.element_info.automation_id,
                    "class_name": child.element_info.class_name,
                    "enabled": child.is_enabled(),
                    "visible": child.is_visible()
                })
            except Exception:
                pass
                
        # Also grab any dialogs
        try:
            dialog = win.child_window(class_name="#32770", timeout=0.1)
            if dialog.exists():
                for d_child in dialog.children():
                    try:
                        elements.append({
                            "name": d_child.window_text(),
                            "control_type": d_child.element_info.control_type,
                            "automation_id": d_child.element_info.automation_id,
                            "class_name": d_child.element_info.class_name,
                            "enabled": d_child.is_enabled(),
                            "visible": d_child.is_visible(),
                            "parent": "Dialog"
                        })
                    except Exception:
                        pass
        except Exception:
            pass

        return format_success("inspect_notepad", data={
            "window": {
                "title": win.window_text(),
                "process_id": app.process
            },
            "elements": elements
        })
    except Exception as e:
        return format_error("inspect_notepad", "Failed to inspect Notepad.", type(e).__name__, str(e))
