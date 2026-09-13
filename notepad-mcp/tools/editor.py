import os
import time
from typing import Dict, Any, Optional
from utils.errors import format_success, format_error
from utils.helpers import get_notepad_app, find_editor_control
from pywinauto.keyboard import send_keys

def _get_editor():
    app = get_notepad_app()
    if not app:
        raise Exception("No Notepad instance found.")
    win = app.top_window()
    editor = find_editor_control(win)
    if not editor:
        raise Exception("Could not find editor control.")
    return win, editor

def type_text(text: str) -> Dict[str, Any]:
    try:
        win, editor = _get_editor()
        win.set_focus()
        editor.set_focus()
        # send_keys uses {SPACE} for spaces if we don't pass with_spaces=True, etc.
        # But for arbitrary text, setting value or using type_keys is better
        editor.type_keys(text, with_spaces=True, with_newlines=True)
        return format_success("type_text", "Typed text successfully.")
    except Exception as e:
        return format_error("type_text", "Failed to type text.", type(e).__name__, str(e))

def append_text(text: str) -> Dict[str, Any]:
    try:
        win, editor = _get_editor()
        win.set_focus()
        editor.set_focus()
        # Ctrl+End to go to end
        send_keys("^{END}")
        editor.type_keys(text, with_spaces=True, with_newlines=True)
        return format_success("append_text", "Appended text successfully.")
    except Exception as e:
        return format_error("append_text", "Failed to append text.", type(e).__name__, str(e))

def get_editor_text() -> Dict[str, Any]:
    try:
        win, editor = _get_editor()
        
        # Try UIA property first
        try:
            text = editor.window_text()
            if text:
                return format_success("get_editor_text", data={"text": text})
        except Exception:
            pass
            
        # Fallback to clipboard
        win.set_focus()
        editor.set_focus()
        send_keys("^a")
        time.sleep(0.1)
        send_keys("^c")
        time.sleep(0.1)
        # We need a clipboard accessor, using win32clipboard or pywinauto.clipboard
        from pywinauto import clipboard
        text = clipboard.GetData()
        # Deselect
        send_keys("{RIGHT}")
        
        return format_success("get_editor_text", data={"text": text})
    except Exception as e:
        return format_error("get_editor_text", "Failed to get editor text.", type(e).__name__, str(e))

def select_all() -> Dict[str, Any]:
    try:
        win, editor = _get_editor()
        win.set_focus()
        editor.set_focus()
        send_keys("^a")
        return format_success("select_all", "Selected all text.")
    except Exception as e:
        return format_error("select_all", "Failed to select all.", type(e).__name__, str(e))

def clear_document() -> Dict[str, Any]:
    try:
        win, editor = _get_editor()
        win.set_focus()
        editor.set_focus()
        send_keys("^a{BACKSPACE}")
        return format_success("clear_document", "Cleared document.")
    except Exception as e:
        return format_error("clear_document", "Failed to clear document.", type(e).__name__, str(e))

def send_hotkey(keys: str) -> Dict[str, Any]:
    try:
        win, _ = _get_editor()
        win.set_focus()
        send_keys(keys)
        return format_success("send_hotkey", f"Sent hotkey {keys}.")
    except Exception as e:
        return format_error("send_hotkey", "Failed to send hotkey.", type(e).__name__, str(e))

def save_document() -> Dict[str, Any]:
    try:
        win, _ = _get_editor()
        win.set_focus()
        send_keys("^s")
        return format_success("save_document", "Triggered save. (Check dialogs if it was a new file)")
    except Exception as e:
        return format_error("save_document", "Failed to save.", type(e).__name__, str(e))

def save_document_as(path: str) -> Dict[str, Any]:
    try:
        win, _ = _get_editor()
        win.set_focus()
        send_keys("^+s") # Ctrl+Shift+S (or F12, depending on windows version, but Ctrl+Shift+S works in Win11 Notepad)
        
        # Wait longer for the Save As dialog to appear and gain focus
        time.sleep(1.5)
        
        # In the save dialog, type the path and hit enter
        # We assume the user has the dialog active now
        send_keys(path.replace(" ", "{SPACE}"))
        send_keys("{ENTER}")
        
        return format_success("save_document_as", f"Triggered save as to '{path}'. Check dialogs if overwrite is required.")
    except Exception as e:
        return format_error("save_document_as", "Failed to save as.", type(e).__name__, str(e))

def open_document(path: str) -> Dict[str, Any]:
    try:
        if not os.path.exists(path):
            return format_error("open_document", f"File '{path}' does not exist.", "FileNotFoundError")
            
        win, _ = _get_editor()
        win.set_focus()
        send_keys("^o")
        
        # Wait longer for the Open dialog to appear and gain focus
        time.sleep(1.5)
        
        send_keys(path.replace(" ", "{SPACE}"))
        send_keys("{ENTER}")
        return format_success("open_document", f"Triggered open for '{path}'.")
    except Exception as e:
        return format_error("open_document", "Failed to open document.", type(e).__name__, str(e))

def find_text(query: str) -> Dict[str, Any]:
    try:
        win, _ = _get_editor()
        win.set_focus()
        send_keys("^f")
        time.sleep(0.5)
        send_keys(query.replace(" ", "{SPACE}"))
        return format_success("find_text", f"Opened find dialog for '{query}'.")
    except Exception as e:
        return format_error("find_text", "Failed to find text.", type(e).__name__, str(e))

def replace_text(find: str, replace: str, replace_all: bool = False) -> Dict[str, Any]:
    try:
        win, _ = _get_editor()
        win.set_focus()
        send_keys("^h")
        time.sleep(0.5)
        send_keys(find.replace(" ", "{SPACE}"))
        send_keys("{TAB}")
        send_keys(replace.replace(" ", "{SPACE}"))
        
        # We just setup the dialog. Clicking replace all requires more specific UI manipulation
        # which can be done via `click_dialog_button` by the agent.
        return format_success("replace_text", "Opened replace dialog and populated fields. Use click_dialog_button to execute.")
    except Exception as e:
        return format_error("replace_text", "Failed to setup replace.", type(e).__name__, str(e))

def copy_selection() -> Dict[str, Any]:
    try:
        win, _ = _get_editor()
        win.set_focus()
        send_keys("^c")
        return format_success("copy_selection", "Triggered copy.")
    except Exception as e:
        return format_error("copy_selection", "Failed to copy.", type(e).__name__, str(e))

def cut_selection() -> Dict[str, Any]:
    try:
        win, _ = _get_editor()
        win.set_focus()
        send_keys("^x")
        return format_success("cut_selection", "Triggered cut.")
    except Exception as e:
        return format_error("cut_selection", "Failed to cut.", type(e).__name__, str(e))

def paste_text(text: Optional[str] = None) -> Dict[str, Any]:
    try:
        win, editor = _get_editor()
        win.set_focus()
        
        if text:
            # If text is provided, we type it directly instead of pasting from clipboard
            editor.type_keys(text, with_spaces=True, with_newlines=True)
            return format_success("paste_text", "Typed provided text directly.")
        else:
            send_keys("^v")
            return format_success("paste_text", "Triggered paste from clipboard.")
    except Exception as e:
        return format_error("paste_text", "Failed to paste.", type(e).__name__, str(e))

def undo() -> Dict[str, Any]:
    try:
        win, _ = _get_editor()
        win.set_focus()
        send_keys("^z")
        return format_success("undo", "Triggered undo.")
    except Exception as e:
        return format_error("undo", "Failed to undo.", type(e).__name__, str(e))

def redo() -> Dict[str, Any]:
    try:
        win, _ = _get_editor()
        win.set_focus()
        send_keys("^y")
        return format_success("redo", "Triggered redo.")
    except Exception as e:
        return format_error("redo", "Failed to redo.", type(e).__name__, str(e))

def get_selected_text() -> Dict[str, Any]:
    try:
        win, _ = _get_editor()
        win.set_focus()
        send_keys("^c")
        time.sleep(0.1)
        from pywinauto import clipboard
        text = clipboard.GetData()
        return format_success("get_selected_text", data={"text": text})
    except Exception as e:
        return format_error("get_selected_text", "Failed to get selected text.", type(e).__name__, str(e))

def get_document_info() -> Dict[str, Any]:
    try:
        app = get_notepad_app()
        if not app:
            raise Exception("Notepad not found.")
        win = app.top_window()
        title = win.window_text()
        unsaved = "*" in title
        return format_success("get_document_info", data={
            "title": title,
            "unsaved": unsaved,
            "process_id": app.process
        })
    except Exception as e:
        return format_error("get_document_info", "Failed to get info.", type(e).__name__, str(e))
