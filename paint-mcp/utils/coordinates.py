from typing import Tuple, Dict, Any
from .errors import InvalidCoordinateError, CanvasNotFoundError
from .helpers import get_paint_app, get_main_window
from pywinauto.findwindows import ElementNotFoundError

def get_canvas_rect(win) -> Dict[str, int]:
    """
    Attempt to find the canvas bounding box dynamically.
    Returns {"x": left, "y": top, "width": width, "height": height}
    """
    # Windows 10 Paint has a control with class MSPaintView or Pane inside a ScrollViewer.
    # Windows 11 Paint might have a different hierarchy.
    try:
        # Search for something that looks like the canvas
        # Usually it's a Pane that is very large or has a specific automation id
        canvas = None
        
        # Try generic pane and group searches
        for child in win.descendants():
            if child.element_info.control_type not in ("Pane", "Group"):
                continue
            rect = child.rectangle()
            # The canvas is typically large and not at the very top (because of ribbon)
            if rect.width() > 100 and rect.height() > 100:
                text = (child.window_text() or "").lower()
                if "canvas" in text or "image" in text:
                    canvas = child
                    break
                # Fallback: largest pane is usually the canvas container
                if not canvas or (rect.width() * rect.height() > canvas.rectangle().width() * canvas.rectangle().height()):
                    # Avoid picking the main window itself if it's somehow a Pane
                    if rect.top > win.rectangle().top + 50:
                        canvas = child

        if canvas:
            rect = canvas.rectangle()
            return {
                "x": rect.left,
                "y": rect.top,
                "width": rect.width(),
                "height": rect.height()
            }
            
        raise CanvasNotFoundError("Could not reliably detect the drawing canvas.")
    except Exception as e:
        if isinstance(e, CanvasNotFoundError):
            raise
        raise CanvasNotFoundError(f"Error finding canvas: {e}")

def relative_to_absolute(x: int, y: int, win=None) -> Tuple[int, int]:
    """Convert canvas-relative (x, y) to absolute screen coordinates."""
    if not win:
        app = get_paint_app()
        win = get_main_window(app)
        
    rect = get_canvas_rect(win)
    
    # Check bounds
    if x < 0 or x > rect["width"] or y < 0 or y > rect["height"]:
        raise InvalidCoordinateError(
            f"Coordinate ({x}, {y}) is outside canvas bounds ({rect['width']}x{rect['height']})."
        )
        
    abs_x = rect["x"] + x
    abs_y = rect["y"] + y
    return abs_x, abs_y
