"""
UI Automation selectors and constants for Notepad.
"""

NOTEPAD_EXE = "notepad.exe"

# Main Window
MAIN_WINDOW_CLASS = "Notepad"
MAIN_WINDOW_TITLE_RE = r".*Notepad"

# Editor Controls
EDITOR_CLASS_WIN10 = "Edit"
EDITOR_CLASS_WIN11 = "RichEditD2DPT"
EDITOR_CONTROL_TYPE = "Document"
EDITOR_AUTOMATION_ID = "15" # Often used in classic Notepad, but we should fallback to class name

# Dialogs
DIALOG_CLASS = "#32770"
DIALOG_CONTROL_TYPE = "Window"

# Dialog Buttons
BUTTON_CONTROL_TYPE = "Button"
SAVE_BUTTON_TEXTS = ["Save", "Yes"]
DONT_SAVE_BUTTON_TEXTS = ["Don't Save", "No"]
CANCEL_BUTTON_TEXTS = ["Cancel"]
REPLACE_BUTTON_TEXTS = ["Replace"]
REPLACE_ALL_BUTTON_TEXTS = ["Replace All"]
FIND_NEXT_BUTTON_TEXTS = ["Find Next"]
