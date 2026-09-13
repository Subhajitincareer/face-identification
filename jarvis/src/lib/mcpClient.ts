import { Client } from "@modelcontextprotocol/client";
import { StdioClientTransport } from "@modelcontextprotocol/client/stdio";
import fs from "fs";
import path from "path";

// Define a global to hold the cached instances across hot-reloads
const globalForMcp = globalThis as unknown as {
  __jarvisMcpClient?: Client;
  __jarvisMcpToolsCache?: any[];
};

export async function getMcpClient(): Promise<Client> {
  if (globalForMcp.__jarvisMcpClient) {
    return globalForMcp.__jarvisMcpClient;
  }

  // Read MCP config
  const configPath = path.resolve(process.cwd(), "..", ".agents", "mcp_config.json");
  let chromeMcpConfig;
  try {
    const configContent = fs.readFileSync(configPath, "utf-8");
    const mcpConfig = JSON.parse(configContent);
    chromeMcpConfig = mcpConfig?.mcpServers?.["chrome-mcp"];
  } catch (err) {
    console.error("Failed to load mcp_config.json:", err);
  }

  if (!chromeMcpConfig) {
    throw new Error("chrome-mcp configuration not found in .agents/mcp_config.json");
  }

  const transport = new StdioClientTransport({
    command: chromeMcpConfig.command,
    args: chromeMcpConfig.args,
  });

  const client = new Client({
    name: "jarvis-mcp-client",
    version: "1.0.0",
  }, {
    capabilities: {}
  });

  await client.connect(transport);
  globalForMcp.__jarvisMcpClient = client;
  console.log("MCP Client connected successfully.");

  return client;
}

// Map JSON schema types to Gemini SDK Types
function mapType(jsonType: string): string {
  switch (jsonType?.toLowerCase()) {
    case 'string': return 'STRING';
    case 'number': return 'NUMBER';
    case 'integer': return 'INTEGER';
    case 'boolean': return 'BOOLEAN';
    case 'array': return 'ARRAY';
    case 'object': return 'OBJECT';
    default: return 'TYPE_UNSPECIFIED';
  }
}

// Recursively normalizes a JSON schema into the Gemini Schema format
function normalizeSchema(schema: any): any {
  if (!schema || typeof schema !== 'object') return schema;
  
  const normalized: any = {};
  
  if (schema.type) {
    normalized.type = mapType(schema.type);
  }
  
  if (schema.description) normalized.description = schema.description;
  if (schema.enum) normalized.enum = schema.enum;
  if (schema.required) normalized.required = schema.required;
  
  if (schema.properties) {
    normalized.properties = {};
    for (const [key, val] of Object.entries(schema.properties)) {
      normalized.properties[key] = normalizeSchema(val);
    }
  }
  
  if (schema.items) {
    normalized.items = normalizeSchema(schema.items);
  }
  
  return normalized;
}

export async function getMcpTools(): Promise<any[]> {
  if (globalForMcp.__jarvisMcpToolsCache) {
    return globalForMcp.__jarvisMcpToolsCache;
  }

  const client = await getMcpClient();
  const toolsResponse = await client.listTools();
  
  const geminiTools = toolsResponse.tools.map((tool: any) => ({
    name: tool.name,
    description: tool.description || `Execute ${tool.name}`,
    parameters: tool.inputSchema ? normalizeSchema(tool.inputSchema) : undefined
  }));
  
  globalForMcp.__jarvisMcpToolsCache = geminiTools;
  return geminiTools;
}
