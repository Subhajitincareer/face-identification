import fetch from 'node-fetch';

async function test() {
  console.log("Fetching MCP tools from Next.js API...");
  try {
    const res = await fetch('http://localhost:3000/api/mcp');
    const data = await res.json();
    console.log(JSON.stringify(data, null, 2));
  } catch (err) {
    console.error("Error:", err);
  }
}

test();
