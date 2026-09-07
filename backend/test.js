require('dotenv').config();
const { GoogleGenAI } = require('@google/genai');

async function test() {
  try {
    const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });
    const response = await ai.models.generateContent({
      model: 'gemini-3.8-flash',
      contents: 'Hello',
    });
    console.log("Success! Response:", response.text);
  } catch (e) {
    console.error("Error:", e.message);
  }
}
test();
