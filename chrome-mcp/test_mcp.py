import asyncio
import os
import sys

async def main():
    # Use mcp client to connect to the local server
    from mcp.client.stdio import stdio_client, StdioServerParameters
    from mcp.client.session import ClientSession

    server_params = StdioServerParameters(
        command="python",
        args=["-m", "chrome_mcp.server"]
    )

    print("Connecting to MCP server...")
    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            print("Connected and initialized.")
            
            # List tools
            tools = await session.list_tools()
            print(f"Available tools: {[t.name for t in tools.tools]}")
            
            # Navigate to google
            print("Navigating to google.com...")
            result = await session.call_tool("navigate", {"url": "https://www.google.com"})
            print(f"Result: {result.content[0].text}")
            
            # Wait for page to load
            await asyncio.sleep(2)
            
            # Get title
            print("Getting title...")
            title_result = await session.call_tool("get_title", {})
            print(f"Title: {title_result.content[0].text}")
            
            # Click something maybe? No need, title is enough for a basic test.
            
            print("Test complete.")

if __name__ == "__main__":
    asyncio.run(main())
