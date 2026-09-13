"""
UI Automation selectors and constants for Microsoft Paint.
"""

PAINT_EXE = "mspaint.exe"

# Window selectors
PAINT_WINDOW_TITLE_RE = r".*Paint$"
# Win 10 uses MSPaintApp, Win 11 uses a different frame, but title match works.

# Dialog Selectors
DIALOG_CLASS = "#32770"
UWP_DIALOG_TYPE = "Window" # Win 11 might use UWP dialogs

# Common UI elements
CANVAS_CONTROL_TYPE = "Pane" 
CANVAS_CLASS_NAME_WIN10 = "MSPaintView" # Usually what the canvas view is called
CANVAS_AUTOMATION_ID = "10000" # Fallback heuristic

# Tools semantic names (these might differ by localization or exact OS build, 
# so we rely on regex and multiple strategies)
TOOLS_MAP = {
    "pencil": ["Pencil"],
    "brush": ["Brushes", "Brush"],
    "eraser": ["Eraser"],
    "fill": ["Fill", "Fill with color"],
    "text": ["Text"],
    "line": ["Line"],
    "rectangle": ["Rectangle"],
    "ellipse": ["Oval", "Ellipse"],
    "polygon": ["Polygon"],
    "color_picker": ["Color picker"],
    "select": ["Select"]
}
