# Notepad MCP Server

A Model Context Protocol (MCP) server that allows AI agents to control Windows Notepad through Windows UI Automation.

## Features

- Launch and manage Notepad instances.
- Open, edit, and save documents.
- Support for type_text, append_text, select_all, copy, cut, paste, undo, redo.
- Find and replace dialog handling.
- Detect unsaved changes and manage confirmation dialogs.
- Detailed UI inspection to help the AI understand the state of the editor.
- Compatible with Windows 10 and 11 Notepad.

## Prerequisites

- Windows 10 or 11
- Python 3.10+
- (Optional) `uv` for running the MCP server easily via the CLI

## Setup & Installation

1. Create a virtual environment and activate it:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install the dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

## Running the Server

Using `uv` with the MCP CLI (recommended if testing with Inspector):
```powershell
uv run mcp dev server.py
```

Or just directly via Python (useful when configuring Claude Desktop or another client):
```powershell
python server.py
```

## Example Client Configuration (Claude Desktop)

Add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "notepad": {
      "command": "python",
      "args": [
        "E:\\path\\to\\notepad-mcp\\server.py"
      ]
    }
  }
}
```

## Example Agent Workflow

An AI agent will typically use these tools in a step-by-step loop. For example, to write and save notes:

1. `open_notepad(reuse_existing=True)` - Returns the title and process ID of the window.
2. `inspect_notepad()` - Checks the UI to see if the editor control is available.
3. `type_text(text="Meeting notes...")` - Writes text into the Notepad window.
4. `save_document_as(path="C:\\Users\\...\\notes.txt")` - Invokes the Save As dialog.
5. `inspect_notepad()` / `detect_dialogs()` - Confirms the dialog is open or complete.
6. `close_notepad(save_if_needed=False)` - Closes Notepad safely.

## Limitations & Troubleshooting

- **Windows UI Automation**: The server uses `pywinauto` with the `uia` backend. While this is robust on modern Windows, some Notepad versions (especially the tabbed Windows 11 version) may have deeply nested UI trees. If elements are not found, use `inspect_notepad` to have the AI view the UI tree.
- **Permissions**: Ensure your agent or terminal runs with the necessary permissions to automate UI applications on Windows.
- **Screen Scaling**: UI Automation relies heavily on accessibility APIs rather than visual coordinates, so screen scaling usually does not break it.
- **Speed**: UI Automation can sometimes be slow. The server uses intelligent waits to handle loading dialogs and elements.
