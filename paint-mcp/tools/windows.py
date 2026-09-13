from typing import Dict, Any
from utils.errors import format_success, format_error
from utils.helpers import get_paint_app
from pywinauto.findwindows import find_windows
from pywinauto.application import Application
from utils.selectors import PAINT_WINDOW_TITLE_RE

def list_paint_windows() -> Dict[str, Any]:
    try:
        handles = find_windows(title_re=PAINT_WINDOW_TITLE_RE)
        windows_info = []
        
        for hwnd in handles:
            try:
                app = Application(backend="uia").connect(handle=hwnd)
                win = app.window(handle=hwnd)
                
                info = {
                    "title": win.window_text(),
                    "process_id": app.process,
                    "handle": hwnd,
                    "visible": win.is_visible(),
                    "enabled": win.is_enabled(),
                    "focused": win.has_keyboard_focus()
                }
                windows_info.append(info)
            except Exception:
                pass
                
        return format_success("list_paint_windows", f"Found {len(windows_info)} windows.", {"windows": windows_info})
    except Exception as e:
        return format_error("list_paint_windows", "Failed to list windows.", type(e).__name__, str(e))

def focus_paint_window(identifier: str) -> Dict[str, Any]:
    try:
        try:
            pid = int(identifier)
            app = get_paint_app(process_id=pid)
        except ValueError:
            handles = find_windows(title_re=f".*{identifier}.*")
            if not handles:
                return format_error("focus_paint_window", f"No window found matching '{identifier}'", "PaintWindowNotFoundError")
            app = Application(backend="uia").connect(handle=handles[0])
            
        if not app:
            return format_error("focus_paint_window", "Could not connect to Paint instance.", "ConnectionError")
            
        win = app.top_window()
        win.set_focus()
        
        return format_success("focus_paint_window", "Focused Paint window.", {"title": win.window_text()})
    except Exception as e:
        return format_error("focus_paint_window", "Failed to focus window.", type(e).__name__, str(e))
