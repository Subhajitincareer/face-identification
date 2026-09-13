import asyncio
import sys
import logging
from mcp.server.mcpserver import MCPServer

# Import all tools
from tools.app import open_notepad, close_notepad, inspect_notepad
from tools.windows import list_notepad_windows, focus_notepad, get_window_text
from tools.editor import (
    type_text, append_text, select_all, clear_document, send_hotkey,
    save_document, get_document_info, get_editor_text,
    open_document, save_document_as, find_text, replace_text,
    copy_selection, paste_text, cut_selection, undo, redo, get_selected_text
)
from tools.dialogs import detect_dialogs, click_dialog_button

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("notepad-mcp")

server = MCPServer(
    name="notepad-mcp",
    version="0.1.0"
)

# Register tools
server.tool()(open_notepad)
server.tool()(close_notepad)
server.tool()(inspect_notepad)
server.tool()(list_notepad_windows)
server.tool()(focus_notepad)
server.tool()(get_window_text)
server.tool()(type_text)
server.tool()(append_text)
server.tool()(select_all)
server.tool()(clear_document)
server.tool()(send_hotkey)
server.tool()(save_document)
server.tool()(get_document_info)
server.tool()(get_editor_text)
server.tool()(open_document)
server.tool()(save_document_as)
server.tool()(find_text)
server.tool()(replace_text)
server.tool()(copy_selection)
server.tool()(paste_text)
server.tool()(cut_selection)
server.tool()(undo)
server.tool()(redo)
server.tool()(get_selected_text)
server.tool()(detect_dialogs)
server.tool()(click_dialog_button)

async def main():
    logger.info("Starting Notepad MCP server using stdio transport")
    # Run the server on stdio
    await server.run_stdio_async()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server stopped.")
