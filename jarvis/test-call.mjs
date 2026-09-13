import fetch from 'node-fetch';

async function testCall() {
  console.log("Executing 'navigate' MCP tool...");
  try {
    const resNav = await fetch('http://localhost:3000/api/mcp', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        toolName: 'navigate',
        args: { url: "https://example.com" }
      })
    });
    console.log("Navigate result:", JSON.stringify(await resNav.json(), null, 2));

    const resTitle = await fetch('http://localhost:3000/api/mcp', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        toolName: 'get_title',
        args: {}
      })
    });
    console.log("Title result:", JSON.stringify(await resTitle.json(), null, 2));
  } catch (err) {
    console.error("Error:", err);
  }
}

testCall();
