from typing import Dict, Any
from utils.errors import format_success, format_error
from utils.helpers import get_paint_app, get_main_window
from utils.selectors import DIALOG_CLASS

def detect_dialogs() -> Dict[str, Any]:
    try:
        app = get_paint_app()
        if not app:
            return format_error("detect_dialogs", "No Paint instance found.", "PaintNotRunningError")
            
        win = get_main_window(app)
        
        dialogs = []
        for dlg in win.children(class_name=DIALOG_CLASS):
            if dlg.is_visible():
                buttons = []
                for child in dlg.children(control_type="Button"):
                    buttons.append({
                        "name": child.window_text(),
                        "automation_id": child.element_info.automation_id
                    })
                dialogs.append({
                    "title": dlg.window_text(),
                    "buttons": buttons
                })
                
        return format_success("detect_dialogs", "Detected dialogs.", {"dialogs": dialogs})
    except Exception as e:
        return format_error("detect_dialogs", "Failed to detect dialogs.", type(e).__name__, str(e))

def click_dialog_button(button_name: str) -> Dict[str, Any]:
    try:
        app = get_paint_app()
        win = get_main_window(app)
        
        for dlg in win.children(class_name=DIALOG_CLASS):
            if dlg.is_visible():
                btn = dlg.child_window(title_re=f".*{button_name}.*", control_type="Button")
                if btn.exists():
                    btn.click()
                    return format_success("click_dialog_button", f"Clicked button '{button_name}'.")
                    
        return format_error("click_dialog_button", f"Button '{button_name}' not found.", "ControlNotFoundError")
    except Exception as e:
        return format_error("click_dialog_button", "Failed to click button.", type(e).__name__, str(e))
