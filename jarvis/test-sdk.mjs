import { GoogleGenAI } from '@google/genai';
const ai = new GoogleGenAI({apiKey: 'dummy'});
try {
  ai.live.connect({model:'models/gemini-2.0-flash-exp'}).then(async session => {
    try {
      session.sendRealtimeInput([{
        mimeType: "audio/pcm;rate=16000",
        data: "dummyBase64"
      }]);
      console.log("sendRealtimeInput (Array) called successfully");
    } catch(e) {
      console.error("sendRealtimeInput (Array) error:", e.message);
    }

    try {
      session.sendRealtimeInput({
        media: { mimeType: "audio/pcm;rate=16000", data: "dummyBase64" }
      });
      console.log("sendRealtimeInput (Object) called successfully");
    } catch(e) {
      console.error("sendRealtimeInput (Object) error:", e.message);
    }
  });
} catch(e) { console.error("connect error:", e.message); }
