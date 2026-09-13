import sys
import os

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import server

import asyncio

async def test_server_tools_registered():
    tools = await server.list_tools()
    assert len(tools) > 0, "No tools registered"
    
    tool_names = [t.name for t in tools]
    assert "open_notepad" in tool_names
    assert "close_notepad" in tool_names
    assert "type_text" in tool_names
    assert "save_document" in tool_names
    
    print(f"Server successfully verified with {len(tools)} tools registered.")
    for tool in tools:
        print(f" - {tool.name}")

if __name__ == "__main__":
    asyncio.run(test_server_tools_registered())
