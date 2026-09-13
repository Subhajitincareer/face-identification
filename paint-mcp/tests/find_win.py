from pywinauto import Desktop
windows = Desktop(backend='uia').windows()
for w in windows:
    if w.is_visible() and 'paint' in w.window_text().lower():
        print(f"FOUND: '{w.window_text()}' PID: {w.process_id()}")
