import asyncio
from typing import Any

from mcp.server.mcpserver import MCPServer
from chrome_mcp.browser import ChromeBrowser

# Initialize server
mcp = MCPServer("chrome-mcp", "0.1.0")
browser = ChromeBrowser()

@mcp.tool()
def navigate(url: str) -> str:
    """Navigate the browser to a URL"""
    return browser.navigate(url)

@mcp.tool()
def get_title() -> str:
    """Get the title of the current page"""
    return browser.get_title()

@mcp.tool()
def get_page_source() -> str:
    """Get the HTML source of the current page"""
    return browser.get_page_source()

@mcp.tool()
def click(selector: str, by_type: str = "css selector") -> str:
    """Click on an element on the page
    
    Args:
        selector: The selector to find the element
        by_type: The type of selector (e.g. 'css selector', 'id', 'xpath')
    """
    return browser.click(selector, by_type)

@mcp.tool()
def type_text(selector: str, text: str, by_type: str = "css selector") -> str:
    """Type text into an input field
    
    Args:
        selector: The selector to find the element
        text: The text to type
        by_type: The type of selector (e.g. 'css selector', 'id', 'xpath')
    """
    return browser.type_text(selector, text, by_type)

@mcp.tool()
def execute_script(script: str) -> str:
    """Execute JavaScript on the current page"""
    return browser.execute_script(script)

@mcp.tool()
def take_screenshot() -> str:
    """Take a screenshot of the current page. Returns a base64 encoded image."""
    return browser.take_screenshot()

def main():
    mcp.run()

if __name__ == "__main__":
    main()
