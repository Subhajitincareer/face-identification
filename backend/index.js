require('dotenv').config();
const express = require('express');
const cors = require('cors');
const { GoogleGenAI } = require('@google/genai');

const app = express();
app.use(cors());
// Increase payload limit for base64 images
app.use(express.json({ limit: '50mb' }));

// Initialize the SDK
const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });

app.post('/analyze', async (req, res) => {
  try {
    const { base64Image } = req.body;
    
    if (!base64Image) {
      return res.status(400).json({ error: 'No image provided' });
    }

    let response;
    let retries = 3;
    
    // Retry loop for handling 503 High Demand errors from Google
    while (retries > 0) {
      try {
        response = await ai.models.generateContent({
          model: 'gemini-3.8-flash',
          contents: [
            {
              inlineData: {
                mimeType: 'image/jpeg',
                data: base64Image,
              },
            },
            {
              text: `
You are an object safety scanner.
Analyze ONLY the main object visible in the image.
Return the result in this exact JSON format:

{
  "object": "name of the main object",
  "category": "category",
  "description": "one short sentence describing what it is",
  "harmful": true,
  "danger_level": "low | medium | high | unknown",
  "hazards": [
    "possible hazard 1",
    "possible hazard 2"
  ],
  "reason": "short explanation of why it may or may not be harmful",
  "visible_signs": [
    "only describe hazards or features clearly visible in the image"
  ],
  "confidence": 0.0
}

Rules:
1. Identify only the MAIN object.
2. Do not describe unrelated background objects.
3. Do not invent properties that cannot be determined from the image.
4. If safety cannot be determined from the image, use:
   "harmful": null, "danger_level": "unknown"
5. Distinguish between "visible evidence of danger" and "possible danger".
6. Do not assume an object is dangerous merely because it could be used dangerously.
7. Do not identify a person's identity.
8. Keep the response concise.
9. Return ONLY valid JSON. No markdown. No extra text.
10. ALL STRING VALUES in the JSON (like object, category, description, reason, hazards etc.) MUST BE WRITTEN IN BENGALI LANGUAGE (বাংলা).
              `,
            },
          ],
        });
        break; // Success, exit retry loop
      } catch (e) {
        if (e.status === 503 && retries > 1) {
          console.warn(`Google API high demand. Retrying... (${retries - 1} attempts left)`);
          retries--;
          await new Promise(resolve => setTimeout(resolve, 2000)); // Wait 2 seconds before retry
        } else {
          throw e; // Throw if not 503 or out of retries
        }
      }
    }

    let rawText = response.text.replace(/```json/g, '').replace(/```/g, '').trim();
    const result = JSON.parse(rawText);
    res.json(result);

  } catch (error) {
    console.error('Error analyzing image:', error);
    res.status(500).json({ error: 'Failed to analyze image' });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, '0.0.0.0', () => {
  console.log(`Pokedex Backend running on http://0.0.0.0:${PORT}`);
});
