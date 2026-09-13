from typing import Dict, Any, List
from utils.errors import format_success, format_error
from utils.helpers import get_notepad_app
from pywinauto.findwindows import ElementNotFoundError

def _get_dialog(win):
    try:
        # Dialogs in Notepad typically use the #32770 class name
        dialog = win.child_window(class_name="#32770")
        if dialog.exists(timeout=1):
            return dialog
    except ElementNotFoundError:
        pass
    return None

def detect_dialogs() -> Dict[str, Any]:
    """Detect if any Notepad dialog is currently open."""
    try:
        app = get_notepad_app()
        if not app:
            return format_error("detect_dialogs", "Notepad instance not found.", "NotFoundError")
            
        win = app.top_window()
        dialog = _get_dialog(win)
        
        if not dialog:
            return format_success("detect_dialogs", "No dialogs detected.", data={"has_dialog": False})
            
        # Extract dialog info
        title = dialog.window_text()
        buttons = []
        for child in dialog.children():
            if child.element_info.control_type == "Button":
                buttons.append(child.window_text())
                
        return format_success("detect_dialogs", "Dialog detected.", data={
            "has_dialog": True,
            "title": title,
            "buttons": buttons
        })
    except Exception as e:
        return format_error("detect_dialogs", "Failed to detect dialogs.", type(e).__name__, str(e))

def click_dialog_button(button_name: str) -> Dict[str, Any]:
    """Click a button in the active Notepad dialog by its name or partial name."""
    try:
        app = get_notepad_app()
        if not app:
            return format_error("click_dialog_button", "Notepad instance not found.", "NotFoundError")
            
        win = app.top_window()
        dialog = _get_dialog(win)
        
        if not dialog:
            return format_error("click_dialog_button", "No dialog detected to click.", "NotFoundError")
            
        # Try finding the exact button or by regex
        btn = dialog.child_window(title_re=f".*{button_name}.*", control_type="Button")
        if btn.exists(timeout=1):
            btn.click()
            return format_success("click_dialog_button", f"Clicked button matching '{button_name}'.")
        else:
            return format_error("click_dialog_button", f"Button '{button_name}' not found in dialog.", "NotFoundError")
            
    except Exception as e:
        return format_error("click_dialog_button", "Failed to click dialog button.", type(e).__name__, str(e))
