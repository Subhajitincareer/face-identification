import ctypes
user32 = ctypes.windll.user32
hdesk = user32.OpenInputDesktop(0, False, 0x01FF)
if hdesk: user32.SetThreadDesktop(hdesk)

from pywinauto import Desktop
import pyautogui
import time

d = Desktop(backend='uia')
paint_win = None
for w in d.windows():
    t = w.window_text().lower()
    if 'paint' in t and 'firefox' not in t and 'agent' not in t:
        paint_win = w
        break

if not paint_win:
    print("Paint window not found!")
    exit(1)

print("Found Paint:", paint_win.window_text())
paint_win.set_focus()
time.sleep(0.3)

# 1. Select Red color
for c in paint_win.descendants():
    if c.element_info.control_type == 'ListItem' and c.window_text().lower() == 'red':
        print("Clicking Red color:", c.rectangle())
        try:
            c.invoke()
        except Exception:
            c.click_input()
        break
time.sleep(0.2)

# 2. Select Oval tool
for c in paint_win.descendants():
    if c.element_info.control_type in ['Button', 'ListItem'] and c.window_text().lower() == 'oval':
        print("Clicking Oval shape:", c.rectangle())
        try:
            c.invoke()
        except Exception:
            c.click_input()
        break
time.sleep(0.2)

# 3. Find canvas
canvas_rect = None
for c in paint_win.descendants():
    aid = c.element_info.automation_id or ""
    txt = (c.window_text() or "").lower()
    if aid == 'image' or 'canvas' in txt:
        r = c.rectangle()
        if r.width() > 100 and r.height() > 100:
            canvas_rect = r
            print("Found canvas:", r)
            break

if not canvas_rect:
    print("Canvas not found!")
    exit(1)

# 4. Draw circle on canvas
# Let's draw a circle at relative (200, 200) to (400, 400)
start_x = canvas_rect.left + 200
start_y = canvas_rect.top + 200
end_x = canvas_rect.left + 400
end_y = canvas_rect.top + 400

print(f"Drawing oval from ({start_x}, {start_y}) to ({end_x}, {end_y})")
pyautogui.moveTo(start_x, start_y)
pyautogui.dragTo(end_x, end_y, duration=0.8, button='left')
print("Drawing completed successfully!")
