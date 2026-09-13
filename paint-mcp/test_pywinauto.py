import ctypes
from ctypes import wintypes
from pywinauto.application import Application

user32 = ctypes.windll.user32
hdesk = user32.OpenInputDesktop(0, False, 0x01FF)
if hdesk:
    user32.SetThreadDesktop(hdesk)

paint_hwnds = []
def enum_cb(hwnd, extra):
    if user32.IsWindowVisible(hwnd):
        length = user32.GetWindowTextLengthW(hwnd)
        if length > 0:
            buff = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buff, length + 1)
            if "paint" in buff.value.lower():
                paint_hwnds.append((hwnd, buff.value))
    return True

WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
user32.EnumWindows(WNDENUMPROC(enum_cb), 0)

print("Found paint_hwnds:", paint_hwnds)
for hwnd, title in paint_hwnds:
    try:
        app = Application(backend="uia").connect(handle=hwnd)
        win = app.window(handle=hwnd)
        print("Connected to:", title, "rect:", win.rectangle())
    except Exception as e:
        print("Failed to connect to", title, e)
