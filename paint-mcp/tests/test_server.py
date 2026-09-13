import asyncio
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from server import server

async def test_tools_registered():
    """Test that all required tools are registered with the server."""
    tools = await server.list_tools()
    tool_names = [tool.name for tool in tools]
    
    assert "open_paint" in tool_names
    assert "inspect_paint" in tool_names
    assert "get_canvas_info" in tool_names
    assert "draw_rectangle" in tool_names
    assert "save_image_as" in tool_names
    assert "send_hotkey" in tool_names
    
    print("Test passed: All required tools are registered.")

if __name__ == "__main__":
    asyncio.run(test_tools_registered())
