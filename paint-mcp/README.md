# Paint MCP Server

An MCP Server that exposes Microsoft Paint capabilities as composable tools for AI agents on Windows 10/11.

## Objective
Provide a robust, step-by-step way for AI models (like Gemini or Claude) to control Microsoft Paint using the official Python MCP SDK v2. This server uses `pywinauto` for semantic UI discovery and `pyautogui` for coordinate-based drawing bounded to the actual canvas dimensions.

## Requirements
- Windows 10/11
- Python 3.10+
- `mcp[cli]`

## Installation
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Running the Server (Development / Inspector)
To test the server using the MCP Inspector UI:
```powershell
uv run mcp dev server.py
```
*Note: Make sure `uv` is installed, or run `npx @modelcontextprotocol/inspector` directly passing the python execution command.*

### Test Procedure in Inspector
1. **`open_paint()`**: Opens a new Microsoft Paint window.
2. **`inspect_paint()`**: Returns a detailed UI tree of the current Paint window (including buttons, menus, dialogs).
3. **`get_canvas_info()`**: Returns the detected bounds of the drawing surface.
4. **`new_canvas(800, 600)`**: Uses keyboard shortcuts to invoke the resize dialog and set a new canvas size.
5. **`draw_rectangle(100, 100, 400, 300)`**: Draws a rectangle using canvas-relative coordinates.
6. **`save_image_as("C:\\path\\to\\image.png")`**: Saves the drawing.

## AI Agent Integration (Claude / Gemini)

To configure an AI client (like Claude Desktop or Gemini) to use this server, add the following to its configuration file (e.g. `claude_desktop_config.json` or `.agents/mcp_config.json`):

```json
{
  "mcpServers": {
    "paint-mcp": {
      "command": "C:\\absolute\\path\\to\\paint-mcp\\.venv\\Scripts\\python.exe",
      "args": [
        "C:\\absolute\\path\\to\\paint-mcp\\server.py"
      ]
    }
  }
}
```

## AI Agent Workflow Example
The server relies on the AI to compose atomic actions step-by-step:
1. AI calls `open_paint()` to start the app.
2. AI calls `inspect_paint()` to verify the UI layout dynamically (important because Windows 10 and 11 Paint UIs differ).
3. AI calls `select_tool("rectangle")`.
4. AI calls `draw_rectangle(50, 50, 200, 200, filled=False)`.
5. AI calls `save_image_as(...)` to store the output.

## Architecture
- **`tools/`**: Domain specific tool groups (canvas, drawing, dialogs, image, windows).
- **`utils/`**: Core logic for process discovery, UI tree traversal, and canvas coordinate translations.
- **`server.py`**: MCP SDK v2 initialization and tool registration.
