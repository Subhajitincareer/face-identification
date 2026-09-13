import { NextResponse } from 'next/server';
import { getMcpClient, getMcpTools } from '@/lib/mcpClient';

// Explicitly use the Node.js runtime to support child_process for the MCP Stdio transport
export const runtime = 'nodejs';

export async function GET() {
  try {
    const tools = await getMcpTools();
    return NextResponse.json({ tools });
  } catch (error: any) {
    console.error("GET /api/mcp error:", error);
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { toolName, args } = body;

    if (!toolName) {
      return NextResponse.json({ error: "toolName is required" }, { status: 400 });
    }

    const client = await getMcpClient();
    console.log(`Executing MCP Tool: ${toolName}`, args);
    
    const result = await client.callTool({
      name: toolName,
      arguments: args || {}
    });

    return NextResponse.json({ result });
  } catch (error: any) {
    console.error(`POST /api/mcp error calling tool:`, error);
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
