import fs from 'fs';
import WebSocket from 'ws';

const env = fs.readFileSync('.env.local', 'utf-8');
const match = env.match(/GEMINI_API_KEY=([^\n\r]+)/);
const apiKey = match ? match[1] : null;

const ws = new WebSocket(`wss://generativelanguage.googleapis.com/ws/google.ai.generativelanguage.v1alpha.GenerativeService.BidiGenerateContent?key=${apiKey}`);

ws.on('open', () => {
    console.log("WebSocket opened!");
    ws.send(JSON.stringify({
        setup: {
            model: "models/gemini-3.1-flash-live-preview",
            generationConfig: {
                responseModalities: ["AUDIO"],
                speechConfig: {
                    voiceConfig: {
                        prebuiltVoiceConfig: {
                            voiceName: "Algieba"
                        }
                    }
                }
            }
        }
    }));
});

ws.on('message', (data) => {
    console.log("Received:", data.toString());
});

ws.on('close', (code, reason) => {
    console.log("WebSocket closed!", code, reason.toString());
});

ws.on('error', (err) => {
    console.error("WS Error:", err);
});
