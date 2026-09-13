import { GoogleGenAI, Modality } from '@google/genai';
import fs from 'fs';

const env = fs.readFileSync('.env.local', 'utf-8');
const match = env.match(/GEMINI_API_KEY=([^\n\r]+)/);
const apiKey = match ? match[1] : null;

const ai = new GoogleGenAI({ 
  apiKey,
  apiVersion: 'v1alpha' 
});

const MODEL = "models/gemini-3.1-flash-live-preview";

async function run() {
  console.log("Connecting...");
  try {
    const session = await ai.live.connect({
      model: MODEL,
      config: {
        systemInstruction: {
          parts: [{ text: "You are JARVIS..." }]
        },
        responseModalities: ["AUDIO"],
        speechConfig: {
          voiceConfig: {
            prebuiltVoiceConfig: { voiceName: "Algieba" }
          }
        }
      },
      callbacks: {
          onmessage: (response) => {
            console.log("onmessage", Object.keys(response));
          },
          onclose: () => {
            console.log("onclose");
          },
          onerror: (err) => {
            console.error("onerror", err);
          }
      }
    });
    console.log("Connected successfully!");
    
    // Keep it alive to see if setupComplete arrives
    setTimeout(() => {
        session.close();
    }, 3000);
  } catch (e) {
    console.error("Connection failed:", e);
  }
}

run();
