from pywinauto import Desktop
for w in Desktop(backend='uia').windows():
    if w.is_visible() and w.window_text():
        print(f"'{w.window_text()}' ({w.element_info.class_name})")
