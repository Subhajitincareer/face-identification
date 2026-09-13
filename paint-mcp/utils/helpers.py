import time
import psutil
from typing import Optional, List
from pywinauto.application import Application
from pywinauto.findwindows import find_windows, ElementNotFoundError
from .selectors import PAINT_EXE, PAINT_WINDOW_TITLE_RE
from .errors import PaintNotRunningError

def get_paint_pids() -> List[int]:
    pids = []
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'].lower() == PAINT_EXE:
                pids.append(proc.info['pid'])
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return pids

def get_paint_app(process_id: Optional[int] = None) -> Optional[Application]:
    try:
        if process_id:
            return Application(backend="uia").connect(process=process_id, timeout=2)
        else:
            from pywinauto import Desktop
            # Find all top level windows matching paint
            windows = Desktop(backend="uia").windows(title_re=PAINT_WINDOW_TITLE_RE)
            for win in windows:
                if win.is_visible():
                    return Application(backend="uia").connect(process=win.process_id(), timeout=2)
            
            # Fallback
            pids = get_paint_pids()
            if pids:
                return Application(backend="uia").connect(process=pids[-1], timeout=2)
    except Exception:
        pass
    return None

def wait_for_window(title_re: str = PAINT_WINDOW_TITLE_RE, timeout: float = 5.0) -> bool:
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            handles = find_windows(title_re=title_re)
            if handles:
                return True
        except ElementNotFoundError:
            pass
        time.sleep(0.5)
    return False

def get_main_window(app: Application):
    if not app:
        raise PaintNotRunningError("No Paint application instance.")
    try:
        return app.window(title_re=PAINT_WINDOW_TITLE_RE)
    except Exception as e:
        raise PaintNotRunningError(f"Failed to find Paint main window: {e}")
