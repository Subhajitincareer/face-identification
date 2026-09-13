import ctypes
user32 = ctypes.windll.user32
hdesk = user32.OpenInputDesktop(0, False, 0x01FF)
if hdesk:
    user32.SetThreadDesktop(hdesk)

from pywinauto import Desktop
d = Desktop(backend='uia')
paint_win = None
for w in d.windows():
    if 'paint' in w.window_text().lower() and 'firefox' not in w.window_text().lower():
        paint_win = w
        break

print("Found Paint Window:", paint_win.window_text(), paint_win.handle)

for c in paint_win.descendants():
    try:
        t = c.window_text()
        cid = c.element_info.automation_id or ""
        ctype = c.element_info.control_type or ""
        text_id = (t + " " + cid).lower()
        if any(k in text_id for k in ['oval', 'ellipse', 'circle', 'canvas', 'shape', 'tool', 'brush', 'color', 'pencil']):
            print(f"{ctype} | text='{t}' | id='{cid}' | rect={c.rectangle()}")
    except Exception:
        pass
