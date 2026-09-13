from .app import open_paint, close_paint, get_paint_state, inspect_paint
from .windows import list_paint_windows, focus_paint_window
from .canvas import get_canvas_info, new_canvas, resize_canvas, crop
from .drawing import select_tool, set_primary_color, set_secondary_color, set_brush_size, draw_line, draw_rectangle, draw_ellipse, draw_polygon, draw_freehand, draw_path, erase, fill_area
from .image import open_image, save_image, save_image_as, export_image
from .dialogs import detect_dialogs, click_dialog_button
from .keyboard import send_hotkey

__all__ = [
    "open_paint", "close_paint", "get_paint_state", "inspect_paint",
    "list_paint_windows", "focus_paint_window",
    "get_canvas_info", "new_canvas", "resize_canvas", "crop",
    "select_tool", "set_primary_color", "set_secondary_color", "set_brush_size", 
    "draw_line", "draw_rectangle", "draw_ellipse", "draw_polygon", "draw_freehand", "draw_path", 
    "erase", "fill_area",
    "open_image", "save_image", "save_image_as", "export_image",
    "detect_dialogs", "click_dialog_button",
    "send_hotkey"
]
