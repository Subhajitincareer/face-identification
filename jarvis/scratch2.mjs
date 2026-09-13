import { GoogleGenAI } from '@google/genai';
import { loadEnvConfig } from '@next/env';

loadEnvConfig(process.cwd());
const apiKey = process.env.NEXT_PUBLIC_GEMINI_API_KEY || process.env.GEMINI_API_KEY;

async function test() {
  const ai = new GoogleGenAI({ apiKey });
  const session = await ai.live.connect({ model: "models/gemini-2.0-flash-exp" });
  console.log("Receive properties:", Object.keys(session).filter(k => typeof session[k] === 'function' || k.includes('receive') || k.includes('on')));
  console.log("Proto:", Object.getOwnPropertyNames(Object.getPrototypeOf(session)));
  session.close();
}
test().catch(console.error);
