"use client";

import { useState, useRef, useCallback, useEffect } from 'react';
import { GoogleGenAI, Modality } from '@google/genai';
import { eventBus } from '../lib/eventBus';

// Using Gemini 3.1 Flash Live Preview
const MODEL = "models/gemini-3.1-flash-live-preview";

export function useGeminiLive() {
  const [isConnected, setIsConnected] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");
  // Store the active session from @google/genai
  const sessionRef = useRef<any>(null);
  
  // Audio playback context
  const audioContextRef = useRef<AudioContext | null>(null);
  const nextPlayTimeRef = useRef<number>(0);

  const connect = useCallback(async () => {
    // Setup audio context for playback
    if (!audioContextRef.current) {
      const AudioContext = window.AudioContext || (window as any).webkitAudioContext;
      audioContextRef.current = new AudioContext({ sampleRate: 24000 }); // Gemini outputs 24kHz audio typically
      nextPlayTimeRef.current = audioContextRef.current.currentTime;
    }

    try {
      const apiKey = process.env.NEXT_PUBLIC_GEMINI_API_KEY;
      if (!apiKey) {
        throw new Error("NEXT_PUBLIC_GEMINI_API_KEY is not defined in the environment.");
      }

      const ai = new GoogleGenAI({ 
        apiKey,
        apiVersion: 'v1alpha' // Force v1alpha for Gemini Live API
      });
      console.log("Attempting to connect to Gemini Live...");

      // Fetch MCP tools
      let mcpTools = [];
      try {
        const response = await fetch('/api/mcp');
        const data = await response.json();
        if (data.tools) {
          mcpTools = data.tools;
          console.log("Fetched MCP tools:", mcpTools.length);
        }
      } catch (err) {
        console.error("Failed to fetch MCP tools:", err);
      }

      const session = await ai.live.connect({
        model: MODEL,
        config: {
          tools: mcpTools.length > 0 ? [{ functionDeclarations: mcpTools }] : undefined,
          systemInstruction: {
            parts: [{
              text: `You are JARVIS, a highly intelligent personal AI assistant. 
Personality:
- Calm
- Extremely professional
- Polite
- Confident
- Concise
- Helpful
- Slightly witty
- Never overly emotional

Speaking style:
- Speak naturally and clearly.
- Use a calm, sophisticated tone.
- Give concise answers first.
- Do not sound robotic.
- When the user interrupts, stop and listen.
- Address the user respectfully.`
            }]
          },
          responseModalities: [Modality.AUDIO],
          speechConfig: {
            voiceConfig: {
              prebuiltVoiceConfig: {
                voiceName: "Algieba"
              }
            }
          }
        },
        callbacks: {
          onmessage: async (response) => {
            if (response.serverContent?.modelTurn) {
              eventBus.emit({ type: 'MODEL_TURN_STARTED', source: 'Gemini', status: 'INFO' });
            }
            if (response.serverContent?.modelTurn?.parts) {
              const parts = response.serverContent.modelTurn.parts;
              for (const part of parts) {
                if (part.inlineData && part.inlineData.data) {
                  eventBus.emit({ type: 'MODEL_AUDIO_STARTED', source: 'Gemini', status: 'INFO' });
                  playAudioChunk(part.inlineData.data);
                }
              }
            }

            if (response.toolCall && response.toolCall.functionCalls) {
              const functionResponses = [];
              for (const call of response.toolCall.functionCalls) {
                if (call.name && call.id) {
                  eventBus.emit({ 
                    type: 'TOOL_CALL_STARTED', 
                    source: 'Gemini', 
                    status: 'INFO',
                    toolCallId: call.id,
                    metadata: { toolName: call.name, args: call.args }
                  });
                  
                  eventBus.emit({ 
                    type: 'MCP_REQUEST_SENT', 
                    source: 'MCP', 
                    status: 'PENDING',
                    toolCallId: call.id,
                    metadata: { toolName: call.name }
                  });
                  
                  const startMs = Date.now();
                  
                  try {
                    const mcpRes = await fetch('/api/mcp', {
                      method: 'POST',
                      headers: { 'Content-Type': 'application/json' },
                      body: JSON.stringify({ toolName: call.name, args: call.args || {} })
                    });
                    const mcpData = await mcpRes.json();
                    const durationMs = Date.now() - startMs;
                    
                    if (mcpData.error) {
                      eventBus.emit({ 
                        type: 'MCP_RESPONSE_RECEIVED', 
                        source: 'MCP', 
                        status: 'ERROR',
                        toolCallId: call.id,
                        durationMs,
                        metadata: { error: mcpData.error }
                      });
                    } else {
                      eventBus.emit({ 
                        type: 'MCP_RESPONSE_RECEIVED', 
                        source: 'MCP', 
                        status: 'SUCCESS',
                        toolCallId: call.id,
                        durationMs
                      });
                    }
                    
                    functionResponses.push({
                      id: call.id,
                      name: call.name,
                      response: { result: mcpData.result || mcpData.error }
                    });
                  } catch (err: any) {
                    const durationMs = Date.now() - startMs;
                    eventBus.emit({ 
                      type: 'MCP_RESPONSE_RECEIVED', 
                      source: 'MCP', 
                      status: 'ERROR',
                      toolCallId: call.id,
                      durationMs,
                      metadata: { error: err.message }
                    });
                    
                    functionResponses.push({
                      id: call.id,
                      name: call.name,
                      response: { result: "Error executing tool: " + err.message }
                    });
                  }
                }
              }
              
              if (functionResponses.length > 0 && sessionRef.current) {
                sessionRef.current.sendToolResponse({ functionResponses });
              }
            }
          },
          onclose: (e: any) => {
            setIsConnected(false);
            const closeInfo = e ? `Code: ${e.code}, Reason: ${e.reason}` : 'No info';
            setErrorMsg("Connection closed: " + closeInfo);
            eventBus.emit({ type: 'ERROR_OCCURRED', source: 'Gemini', status: 'ERROR', metadata: { error: closeInfo } });
          },
          onerror: (err) => {
            setErrorMsg("WS Error: " + err.message);
            eventBus.emit({ type: 'ERROR_OCCURRED', source: 'Gemini', status: 'ERROR', metadata: { error: err.message } });
          }
        }
      });

      sessionRef.current = session;
      setIsConnected(true);
      setErrorMsg("");
      console.log("Connected to Gemini Live using @google/genai SDK");

    } catch (err: any) {
      console.error("Failed to connect to Gemini Live:", err);
      setErrorMsg("Connection failed: " + err.message);
      setIsConnected(false);
    }
  }, []);

  const playAudioChunk = (base64Audio: string) => {
    if (!audioContextRef.current) return;
    
    // Convert base64 to array buffer
    const binaryString = window.atob(base64Audio);
    const len = binaryString.length;
    const bytes = new Uint8Array(len);
    for (let i = 0; i < len; i++) {
      bytes[i] = binaryString.charCodeAt(i);
    }
    
    // Gemini returns 16-bit PCM at 24kHz. We need to convert it to Float32 for Web Audio API
    const pcmData = new Int16Array(bytes.buffer);
    const audioBuffer = audioContextRef.current.createBuffer(1, pcmData.length, 24000);
    const channelData = audioBuffer.getChannelData(0);
    
    for (let i = 0; i < pcmData.length; i++) {
      channelData[i] = pcmData[i] / 32768.0; // Convert Int16 to Float32
    }
    
    const source = audioContextRef.current.createBufferSource();
    source.buffer = audioBuffer;
    source.connect(audioContextRef.current.destination);
    
    // Schedule playback seamlessly
    const currentTime = audioContextRef.current.currentTime;
    if (nextPlayTimeRef.current < currentTime) {
      nextPlayTimeRef.current = currentTime; // Reset if we fell behind
    }
    source.start(nextPlayTimeRef.current);
    nextPlayTimeRef.current += audioBuffer.duration;
  };

  const sendAudio = useCallback((pcm16Data: Int16Array) => {
    if (sessionRef.current) {
      // Convert Int16Array to Base64
      const buffer = new Uint8Array(pcm16Data.buffer);
      let binary = '';
      for (let i = 0; i < buffer.byteLength; i++) {
        binary += String.fromCharCode(buffer[i]);
      }
      const base64Data = window.btoa(binary);

      // Using the SDK's sendRealtimeInput method with 'audio' instead of deprecated 'media'
      sessionRef.current.sendRealtimeInput({
        audio: {
          mimeType: "audio/pcm;rate=16000",
          data: base64Data
        }
      });
    }
  }, []);

  const disconnect = useCallback(() => {
    if (sessionRef.current) {
      // Use the SDK's method to close the connection if available.
      // Usually it's close() or we just set it to null.
      if (typeof sessionRef.current.close === 'function') {
        sessionRef.current.close();
      }
      sessionRef.current = null;
    }
    if (audioContextRef.current) {
      audioContextRef.current.close();
      audioContextRef.current = null;
    }
    setIsConnected(false);
  }, []);

  useEffect(() => {
    return () => {
      disconnect();
    };
  }, [disconnect]);

  return {
    isConnected,
    errorMsg,
    connect,
    disconnect,
    sendAudio
  };
}
