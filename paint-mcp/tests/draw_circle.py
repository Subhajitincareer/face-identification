import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tools.app import open_paint, close_paint
from tools.drawing import draw_ellipse
from tools.image import save_image_as

def test():
    print("Opening Paint...")
    res = open_paint(reuse_existing=False, new_window=True)
    print(res)
    
    time.sleep(2)
    
    print("Drawing circle...")
    # draw a smaller circle to fit default small canvas
    res = draw_ellipse(20, 20, 100, 100)
    print(res)
    
    time.sleep(1)
    
    output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'circle.png'))
    print(f"Taking screenshot to {output_path}...")
    from utils.helpers import get_paint_app, get_main_window
    app = get_paint_app()
    if app:
        win = get_main_window(app)
        win.capture_as_image().save(output_path)
        print("Screenshot saved.")
    
    time.sleep(1)
    close_paint(force=True)

if __name__ == "__main__":
    test()
