import { GoogleGenAI } from '@google/genai';

async function test() {
  const ai = new GoogleGenAI({ apiKey: 'dummy' });
  try {
    const session = await ai.live.connect({ model: "models/gemini-2.0-flash-exp" });
    console.log("Keys:", Object.keys(session));
    let proto = Object.getPrototypeOf(session);
    console.log("Proto 1:", Object.getOwnPropertyNames(proto));
  } catch(e) {
    console.error(e);
  }
}
test();
