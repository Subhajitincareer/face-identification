import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tools.app import open_paint
from tools.canvas import new_canvas
from tools.drawing import select_tool, draw_rectangle

def test():
    print("Opening Paint...")
    res = open_paint(reuse_existing=True)
    print(res)
    
    time.sleep(2)
    
    print("Drawing rectangle...")
    # draw a rectangle from (10, 10) to (90, 90) on the canvas
    res = draw_rectangle(10, 10, 90, 90, filled=False, stroke_size=1)
    print(res)

if __name__ == "__main__":
    test()
