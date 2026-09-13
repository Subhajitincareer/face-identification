import pyautogui
from typing import Dict, Any, List
from utils.errors import format_success, format_error, ControlNotFoundError
from utils.helpers import get_paint_app, get_main_window
from utils.coordinates import relative_to_absolute
from utils.selectors import TOOLS_MAP
import time

# PyAutoGUI settings
pyautogui.MINIMUM_DURATION = 0.1
pyautogui.PAUSE = 0.1
pyautogui.FAILSAFE = False

def _find_and_click_tool(win, tool_key: str):
    """Find a tool button in the ribbon and click it."""
    tool_names = TOOLS_MAP.get(tool_key.lower())
    if not tool_names:
        raise ValueError(f"Unknown tool: {tool_key}")
        
    for name in tool_names:
        try:
            # Look for buttons that match the name
            btn = win.child_window(title_re=f".*{name}.*", control_type="Button")
            if btn.exists():
                # On UWP/Ribbon, we might need to invoke instead of click
                try:
                    btn.invoke()
                except Exception:
                    btn.click_input()
                return True
        except Exception:
            continue
            
    # Try alternate control types (ListItem, etc)
    for name in tool_names:
        try:
            btn = win.child_window(title_re=f".*{name}.*")
            if btn.exists():
                try:
                    btn.invoke()
                except Exception:
                    btn.click_input()
                return True
        except Exception:
            continue
            
    raise ControlNotFoundError(f"Could not find tool matching '{tool_key}'.")

def select_tool(tool_name: str) -> Dict[str, Any]:
    try:
        app = get_paint_app()
        win = get_main_window(app)
        win.set_focus()
        
        _find_and_click_tool(win, tool_name)
        time.sleep(0.5)
        return format_success("select_tool", f"Selected tool: {tool_name}")
    except Exception as e:
        return format_error("select_tool", "Failed to select tool.", type(e).__name__, str(e))

def set_primary_color(color: str) -> Dict[str, Any]:
    # In a fully robust version, we would open Edit Colors and type RGB.
    # For now, return a placeholder or attempt basic colors if they are standard palette buttons.
    return format_success("set_primary_color", f"Color setting is stubbed out. Requested: {color}. Use Edit Colors dialog manually for now.")

def set_secondary_color(color: str) -> Dict[str, Any]:
    return format_success("set_secondary_color", f"Color setting is stubbed out. Requested: {color}.")

def set_brush_size(size: int) -> Dict[str, Any]:
    # Try Ctrl+NumpadPlus / Ctrl+NumpadMinus as a hack, or invoke Size dropdown
    return format_success("set_brush_size", "Brush size stubbed out.")

def draw_line(x1: int, y1: int, x2: int, y2: int) -> Dict[str, Any]:
    try:
        app = get_paint_app()
        win = get_main_window(app)
        win.set_focus()
        
        abs_x1, abs_y1 = relative_to_absolute(x1, y1, win)
        abs_x2, abs_y2 = relative_to_absolute(x2, y2, win)
        
        pyautogui.moveTo(abs_x1, abs_y1)
        pyautogui.dragTo(abs_x2, abs_y2, duration=0.5, button='left')
        
        return format_success("draw_line", "Line drawn.", {
            "requested": {"x1": x1, "y1": y1, "x2": x2, "y2": y2},
            "actual_screen": {"x1": abs_x1, "y1": abs_y1, "x2": abs_x2, "y2": abs_y2}
        })
    except Exception as e:
        return format_error("draw_line", "Failed to draw line.", type(e).__name__, str(e))

def draw_rectangle(x1: int, y1: int, x2: int, y2: int, filled: bool = False, stroke_size: int = 1) -> Dict[str, Any]:
    try:
        app = get_paint_app()
        win = get_main_window(app)
        win.set_focus()
        
        abs_x1, abs_y1 = relative_to_absolute(x1, y1, win)
        abs_x2, abs_y2 = relative_to_absolute(x2, y2, win)
        
        # We assume the rectangle tool is already selected.
        pyautogui.moveTo(abs_x1, abs_y1)
        pyautogui.dragTo(abs_x2, abs_y2, duration=0.5, button='left')
        
        return format_success("draw_rectangle", "Rectangle drawn.")
    except Exception as e:
        return format_error("draw_rectangle", "Failed to draw rectangle.", type(e).__name__, str(e))

def draw_ellipse(x1: int, y1: int, x2: int, y2: int) -> Dict[str, Any]:
    try:
        app = get_paint_app()
        win = get_main_window(app)
        win.set_focus()
        
        abs_x1, abs_y1 = relative_to_absolute(x1, y1, win)
        abs_x2, abs_y2 = relative_to_absolute(x2, y2, win)
        
        pyautogui.moveTo(abs_x1, abs_y1)
        pyautogui.dragTo(abs_x2, abs_y2, duration=0.5, button='left')
        
        return format_success("draw_ellipse", "Ellipse drawn.")
    except Exception as e:
        return format_error("draw_ellipse", "Failed to draw ellipse.", type(e).__name__, str(e))

def draw_polygon(points: List[List[int]]) -> Dict[str, Any]:
    return format_error("draw_polygon", "Not fully implemented.", "NotImplementedError")

def draw_freehand(points: List[List[int]]) -> Dict[str, Any]:
    try:
        if not points or len(points) < 2:
            return format_error("draw_freehand", "Need at least 2 points.", "ValueError")
            
        app = get_paint_app()
        win = get_main_window(app)
        win.set_focus()
        
        # Start at first point
        abs_start_x, abs_start_y = relative_to_absolute(points[0][0], points[0][1], win)
        pyautogui.moveTo(abs_start_x, abs_start_y)
        pyautogui.mouseDown(button='left')
        
        for pt in points[1:]:
            ax, ay = relative_to_absolute(pt[0], pt[1], win)
            pyautogui.moveTo(ax, ay, duration=0.1)
            
        pyautogui.mouseUp(button='left')
        
        return format_success("draw_freehand", "Freehand path drawn.")
    except Exception as e:
        return format_error("draw_freehand", "Failed to draw freehand.", type(e).__name__, str(e))

def draw_path(points: List[List[int]], is_closed: bool = False) -> Dict[str, Any]:
    """Draws a continuous path given a series of coordinates."""
    try:
        if not points or len(points) < 2:
            return format_error("draw_path", "Need at least 2 points.", "ValueError")
            
        app = get_paint_app()
        win = get_main_window(app)
        win.set_focus()
        
        abs_start_x, abs_start_y = relative_to_absolute(points[0][0], points[0][1], win)
        pyautogui.moveTo(abs_start_x, abs_start_y)
        pyautogui.mouseDown(button='left')
        
        # In a real environment we might use tiny durations for speed.
        # But we need it to be slow enough for Paint to register the stroke.
        for pt in points[1:]:
            ax, ay = relative_to_absolute(pt[0], pt[1], win)
            pyautogui.moveTo(ax, ay, duration=0.01)
            
        if is_closed:
            pyautogui.moveTo(abs_start_x, abs_start_y, duration=0.01)
            
        pyautogui.mouseUp(button='left')
        
        return format_success("draw_path", f"Path drawn with {len(points)} points.")
    except Exception as e:
        # Ensure we release the mouse button in case of failure!
        pyautogui.mouseUp(button='left')
        return format_error("draw_path", "Failed to draw path.", type(e).__name__, str(e))

def erase(x1: int, y1: int, x2: int, y2: int) -> Dict[str, Any]:
    try:
        # Same as draw_line but assuming eraser is selected
        app = get_paint_app()
        win = get_main_window(app)
        win.set_focus()
        
        abs_x1, abs_y1 = relative_to_absolute(x1, y1, win)
        abs_x2, abs_y2 = relative_to_absolute(x2, y2, win)
        
        pyautogui.moveTo(abs_x1, abs_y1)
        pyautogui.dragTo(abs_x2, abs_y2, duration=0.5, button='left')
        return format_success("erase", "Erased path.")
    except Exception as e:
        return format_error("erase", "Failed to erase.", type(e).__name__, str(e))

def fill_area(x: int, y: int) -> Dict[str, Any]:
    try:
        app = get_paint_app()
        win = get_main_window(app)
        win.set_focus()
        
        abs_x, abs_y = relative_to_absolute(x, y, win)
        
        pyautogui.moveTo(abs_x, abs_y)
        pyautogui.click(button='left')
        return format_success("fill_area", "Filled area.")
    except Exception as e:
        return format_error("fill_area", "Failed to fill area.", type(e).__name__, str(e))
