import ctypes
from ctypes import wintypes
import psutil

user32 = ctypes.windll.user32

pids = {p.info['pid'] for p in psutil.process_iter(['pid', 'name']) if 'paint' in p.info['name'].lower()}
print("mspaint PIDs:", pids)

def enum_windows_callback(hwnd, extra):
    lpdw = wintypes.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(lpdw))
    if lpdw.value in pids:
        length = user32.GetWindowTextLengthW(hwnd)
        buff = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buff, length + 1)
        is_visible = user32.IsWindowVisible(hwnd)
        rect = wintypes.RECT()
        user32.GetWindowRect(hwnd, ctypes.byref(rect))
        print(f"HWND: {hwnd}, PID: {lpdw.value}, Visible: {is_visible}, Title: '{buff.value}', Rect: ({rect.left},{rect.top},{rect.right},{rect.bottom})")
    return True

WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
user32.EnumWindows(WNDENUMPROC(enum_windows_callback), 0)
