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
        systemInstruction: { parts: [{ text: "You are JARVIS..." }] },
        responseModalities: ["AUDIO"],
      },
      callbacks: {
          onmessage: (response) => {
            console.log("onmessage", Object.keys(response));
            if (response.serverContent) {
               console.log("serverContent keys:", Object.keys(response.serverContent));
            }
          },
          onclose: () => {
            console.log("onclose");
          },
          onerror: (err) => {
            console.error("onerror", err);
          }
      }
    });
    console.log("Connected successfully! Sending audio...");
    
    // Simulate empty pcm chunk
    const dummyPcm = new Int16Array(512);
    const buffer = new Uint8Array(dummyPcm.buffer);
    let binary = '';
    for (let i = 0; i < buffer.byteLength; i++) {
        binary += String.fromCharCode(buffer[i]);
    }
    const base64Data = btoa(binary);

    session.sendRealtimeInput({
        media: {
            mimeType: "audio/pcm;rate=16000",
            data: base64Data
        }
    });
    console.log("Audio sent!");

    setTimeout(() => {
        session.close();
    }, 3000);
  } catch (e) {
    console.error("Connection failed:", e);
  }
}

run();
