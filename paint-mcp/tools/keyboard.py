from typing import Dict, Any
from utils.errors import format_success, format_error
from utils.helpers import get_paint_app, get_main_window
from pywinauto.keyboard import send_keys

ALLOWED_KEYS = [
    "^n", "^o", "^s", "^+s", "^z", "^y", "^a", "^c", "^v", 
    "{DELETE}", "{ESC}", "%{F4}", "{F12}", "^+x", "^w"
]

def send_hotkey(keys: str) -> Dict[str, Any]:
    try:
        if keys not in ALLOWED_KEYS:
            return format_error("send_hotkey", f"Key sequence '{keys}' not allowed for safety.", "ValueError")
            
        app = get_paint_app()
        if not app:
            return format_error("send_hotkey", "No Paint instance found.", "PaintNotRunningError")
            
        win = get_main_window(app)
        win.set_focus()
        send_keys(keys)
        
        return format_success("send_hotkey", f"Sent hotkey {keys}.")
    except Exception as e:
        return format_error("send_hotkey", "Failed to send hotkey.", type(e).__name__, str(e))
