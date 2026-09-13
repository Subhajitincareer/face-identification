import time
import psutil
from pywinauto.application import Application
from pywinauto.findwindows import find_windows, ElementNotFoundError
from typing import Optional, List, Dict, Any
from .selectors import NOTEPAD_EXE, MAIN_WINDOW_CLASS, EDITOR_CLASS_WIN10, EDITOR_CLASS_WIN11

def get_notepad_pids() -> List[int]:
    """Return a list of all running notepad.exe PIDs."""
    pids = []
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'].lower() == NOTEPAD_EXE:
                pids.append(proc.info['pid'])
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return pids

def get_notepad_app(process_id: Optional[int] = None) -> Optional[Application]:
    """Connect to a Notepad application instance."""
    try:
        if process_id:
            return Application(backend="uia").connect(process=process_id, timeout=2)
        else:
            pids = get_notepad_pids()
            if pids:
                return Application(backend="uia").connect(process=pids[0], timeout=2)
            else:
                return None
    except Exception:
        return None

def find_editor_control(window):
    """Attempt to find the main editor control in a Notepad window."""
    try:
        # Try Windows 11 RichEdit first
        editor = window.child_window(class_name=EDITOR_CLASS_WIN11, control_type="Document")
        if editor.exists(timeout=1):
            return editor
    except ElementNotFoundError:
        pass

    try:
        # Try Windows 10 Edit
        editor = window.child_window(class_name=EDITOR_CLASS_WIN10, control_type="Document")
        if editor.exists(timeout=1):
            return editor
    except ElementNotFoundError:
        pass
        
    try:
        # Fallback 1: Just control_type
        editor = window.child_window(control_type="Document")
        if editor.exists(timeout=1):
            return editor
    except ElementNotFoundError:
        pass
    
    return None

def wait_for_window(title_re: str = ".*", class_name: str = MAIN_WINDOW_CLASS, timeout: float = 5.0) -> bool:
    """Wait for a window matching criteria to appear."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            handles = find_windows(title_re=title_re, class_name=class_name)
            if handles:
                return True
        except ElementNotFoundError:
            pass
        time.sleep(0.5)
    return False
