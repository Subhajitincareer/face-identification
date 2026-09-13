from typing import Dict, Any, List
from utils.errors import format_success, format_error
from utils.helpers import get_notepad_app
from pywinauto.findwindows import find_windows, ElementNotFoundError
from pywinauto.application import Application

def list_notepad_windows() -> Dict[str, Any]:
    """Return all visible Notepad windows."""
    try:
        handles = find_windows(title_re=".*Notepad", class_name="Notepad")
        windows_info = []
        
        for hwnd in handles:
            try:
                # Try to get basic window info without full connect for speed
                app = Application(backend="uia").connect(handle=hwnd)
                win = app.window(handle=hwnd)
                
                info = {
                    "title": win.window_text(),
                    "process_id": app.process,
                    "handle": hwnd,
                    "visible": win.is_visible(),
                    "focused": win.has_keyboard_focus()
                }
                windows_info.append(info)
            except Exception:
                pass
                
        return format_success("list_notepad_windows", f"Found {len(windows_info)} windows.", {"windows": windows_info})
    except Exception as e:
        return format_error("list_notepad_windows", "Failed to list windows.", type(e).__name__, str(e))

def focus_notepad(identifier: str) -> Dict[str, Any]:
    """Focus a specific Notepad window by title or process ID."""
    try:
        # Check if identifier is process ID
        try:
            pid = int(identifier)
            app = get_notepad_app(process_id=pid)
        except ValueError:
            # It's a title
            handles = find_windows(title_re=f".*{identifier}.*", class_name="Notepad")
            if not handles:
                return format_error("focus_notepad", f"No window found matching '{identifier}'", "NotFoundError")
            app = Application(backend="uia").connect(handle=handles[0])
            
        if not app:
            return format_error("focus_notepad", "Could not connect to Notepad instance.", "ConnectionError")
            
        win = app.top_window()
        win.set_focus()
        
        return format_success("focus_notepad", "Focused Notepad window.", {"title": win.window_text()})
    except Exception as e:
        return format_error("focus_notepad", "Failed to focus window.", type(e).__name__, str(e))

def get_window_text() -> Dict[str, Any]:
    """Return the current Notepad window title."""
    try:
        app = get_notepad_app()
        if not app:
            return format_error("get_window_text", "No Notepad instance found.", "NotFoundError")
            
        win = app.top_window()
        return format_success("get_window_text", data={"title": win.window_text()})
    except Exception as e:
        return format_error("get_window_text", "Failed to get window title.", type(e).__name__, str(e))
