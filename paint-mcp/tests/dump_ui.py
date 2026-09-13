import sys, os, json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tools.app import open_paint, inspect_paint

open_paint(reuse_existing=True)
res = inspect_paint()
with open('paint_ui.json', 'w') as f:
    json.dump(res, f, indent=2)
