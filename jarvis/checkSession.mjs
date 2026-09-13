import fs from 'fs';
import { GoogleGenAI } from '@google/genai';

// Read .env.local
const env = fs.readFileSync('.env.local', 'utf-8');
const match = env.match(/GEMINI_API_KEY=([^\n\r]+)/);
const apiKey = match ? match[1] : null;

if (!apiKey) {
    console.error("No API key");
    process.exit(1);
}

const ai = new GoogleGenAI({ apiKey });
const session = await ai.live.connect({ model: "models/gemini-2.0-flash-exp" });

console.log("Session properties:", Object.keys(session));
let proto = Object.getPrototypeOf(session);
console.log("Proto properties:", Object.getOwnPropertyNames(proto));

session.close();
