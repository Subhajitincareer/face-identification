require('dotenv').config();
const { GoogleGenAI } = require('@google/genai');

const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });

async function testModels() {
  const models = ['gemini-3.8-flash', 'gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-1.0-pro', 'gemini-1.5-flash-8b'];
  
  for (const model of models) {
    try {
      console.log(`Testing ${model}...`);
      const response = await ai.models.generateContent({
        model: model,
        contents: 'Say hi'
      });
      console.log(`✅ ${model} works!`);
    } catch (e) {
      console.log(`❌ ${model} failed: ${e.message}`);
    }
  }
}

testModels();
