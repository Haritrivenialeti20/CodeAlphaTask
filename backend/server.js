const express = require("express");
const cors = require("cors");
require("dotenv").config();

const app = express();

const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());

// Test route
app.get("/", (req, res) => {
    res.json({
        message: "CodeAlpha Language Translation API is running"
    });
});

// Translation route
app.post("/translate", async (req, res) => {
    try {
        const { text, sourceLanguage, targetLanguage } = req.body;

        // Validate input
        if (!text || !text.trim()) {
            return res.status(400).json({
                error: true,
                message: "Text is required"
            });
        }

        if (!sourceLanguage || !targetLanguage) {
            return res.status(400).json({
                error: true,
                message: "Source and target languages are required"
            });
        }

        // If both languages are the same
        if (sourceLanguage === targetLanguage) {
            return res.json({
                success: true,
                translatedText: text
            });
        }

        // MyMemory Translation API
 // Translation API
const url =
    `https://translate.googleapis.com/translate_a/single` +
    `?client=gtx` +
    `&sl=${encodeURIComponent(sourceLanguage)}` +
    `&tl=${encodeURIComponent(targetLanguage)}` +
    `&dt=t` +
    `&q=${encodeURIComponent(text)}`;

const response = await fetch(url);

if (!response.ok) {
    throw new Error("Translation API request failed");
}

const data = await response.json();

if (!data || !data[0]) {
    throw new Error("Translation was not returned");
}

const translated = data[0]
    .map(item => item[0])
    .filter(Boolean)
    .join("");

res.json({
    success: true,
    translatedText: translated
});
    } catch (error) {

        console.error("Translation error:", error);

        res.status(500).json({
            error: true,
            message: "Translation failed. Please try again."
        });
    }
});


// Start server
app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
});