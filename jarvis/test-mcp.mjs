import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

async function run() {
  const transport = new StdioClientTransport({
    command: "C:\\Python313\\python.exe",
    args: ["e:\\cloning_project\\face-identification\\chrome-mcp\\src\\chrome_mcp\\server.py"]
  });

  const client = new Client({
    name: "jarvis-mcp-client",
    version: "1.0.0"
  }, {
    capabilities: {}
  });

  await client.connect(transport);
  console.log("Connected to MCP server!");
  
  const tools = await client.listTools();
  console.log("Available tools:", tools.tools.map(t => t.name));

  await client.close();
}

run().catch(console.error);
