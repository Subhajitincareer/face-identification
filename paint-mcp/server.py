import asyncio
from mcp.server.mcpserver import MCPServer
from mcp.server.stdio import stdio_server
import tools as paint_tools

# Create server instance
server = MCPServer("Paint Desktop Control", "1.0.0")

# App Tools
server.tool(name="open_paint", description="Launch Microsoft Paint. Supports new_window=True.")(paint_tools.open_paint)
server.tool(name="close_paint", description="Close the current Paint window safely.")(paint_tools.close_paint)
server.tool(name="get_paint_state", description="Return running state, window title, and canvas bounds.")(paint_tools.get_paint_state)
server.tool(name="inspect_paint", description="Inspect the current Paint window and return a structured UI tree.")(paint_tools.inspect_paint)

# Window Tools
server.tool(name="list_paint_windows", description="Return all visible Paint windows.")(paint_tools.list_paint_windows)
server.tool(name="focus_paint_window", description="Focus a specific Paint window by ID or Title.")(paint_tools.focus_paint_window)

# Canvas Tools
server.tool(name="get_canvas_info", description="Return the detected Paint canvas bounding rectangle in screen coordinates.")(paint_tools.get_canvas_info)
server.tool(name="new_canvas", description="Create a new Paint canvas with width and height.")(paint_tools.new_canvas)
server.tool(name="resize_canvas", description="Resize the current canvas to width and height.")(paint_tools.resize_canvas)
server.tool(name="crop", description="Crop to current selection.")(paint_tools.crop)

# Drawing Tools
server.tool(name="select_tool", description="Select a drawing tool (e.g. pencil, brush, rectangle).")(paint_tools.select_tool)
server.tool(name="set_primary_color", description="Set primary color (e.g. #FF0000).")(paint_tools.set_primary_color)
server.tool(name="set_secondary_color", description="Set secondary color.")(paint_tools.set_secondary_color)
server.tool(name="set_brush_size", description="Set brush size (px).")(paint_tools.set_brush_size)
server.tool(name="draw_line", description="Draw line from x1,y1 to x2,y2 (canvas-relative coordinates).")(paint_tools.draw_line)
server.tool(name="draw_rectangle", description="Draw rectangle from x1,y1 to x2,y2 (canvas-relative).")(paint_tools.draw_rectangle)
server.tool(name="draw_ellipse", description="Draw ellipse from x1,y1 to x2,y2 (canvas-relative).")(paint_tools.draw_ellipse)
server.tool(name="draw_polygon", description="Draw polygon using list of [x, y] points (canvas-relative).")(paint_tools.draw_polygon)
server.tool(name="draw_freehand", description="Draw freehand path using list of [x, y] points (canvas-relative).")(paint_tools.draw_freehand)
server.tool(name="draw_path", description="Draw continuous path using list of [x, y] points (canvas-relative), optionally closing it.")(paint_tools.draw_path)
server.tool(name="erase", description="Erase area from x1,y1 to x2,y2 (canvas-relative).")(paint_tools.erase)
server.tool(name="fill_area", description="Fill area at x,y (canvas-relative).")(paint_tools.fill_area)

# Image Tools
server.tool(name="open_image", description="Open an existing image in Paint.")(paint_tools.open_image)
server.tool(name="save_image", description="Save current image.")(paint_tools.save_image)
server.tool(name="save_image_as", description="Save current image to the specified path.")(paint_tools.save_image_as)
server.tool(name="export_image", description="Export current canvas to requested format.")(paint_tools.export_image)

# Planning Engine Tools
from tools import planning
server.tool(name="plan_drawing", description="Convert a natural-language visual request into a validated geometric scene plan. Use this before executing complex illustrations.")(planning.plan_drawing)
server.tool(name="validate_drawing_plan", description="Validate the current drawing plan geometry and bounds.")(planning.validate_drawing_plan)
server.tool(name="preview_drawing_plan", description="Generate an SVG preview of the current plan to inspect geometry.")(planning.preview_drawing_plan)
server.tool(name="execute_drawing_plan", description="Execute a validated drawing plan in Microsoft Paint in z-order phases. This modifies the canvas.")(planning.execute_drawing_plan)
server.tool(name="cancel_drawing_plan", description="Send cancellation signal to stop an ongoing execution.")(planning.cancel_drawing_plan)

# Dialog & Keyboard
server.tool(name="detect_dialogs", description="Detect Paint dialogs such as Save As.")(paint_tools.detect_dialogs)
server.tool(name="click_dialog_button", description="Click a specific dialog button by name.")(paint_tools.click_dialog_button)
server.tool(name="send_hotkey", description="Send hotkeys to Paint (e.g. ^s, ^+s).")(paint_tools.send_hotkey)

async def main():
    await server.run_stdio_async()

if __name__ == "__main__":
    asyncio.run(main())
