const express = require("express");
const cors = require("cors");
const dotenv = require("dotenv");
const mongoose = require("mongoose");
const axios = require("axios");

dotenv.config();
const app = express();

app.use(cors());
app.use(express.json());

mongoose.connect(process.env.MONGO_URI, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});

const chatSchema = new mongoose.Schema({
  username: String,
  password: String,
  userMessage: String,
  botReply: String,
  timestamp: { type: Date, default: Date.now },
});

const Chat = mongoose.model("Chat", chatSchema);

app.post("/chat", async (req, res) => {
  const { username, password, message } = req.body;

  if (!username || !password || !message) {
    return res.status(400).json({ error: "Missing required fields" });
  }

  try {
    const response = await axios.post(
      "https://api.cohere.ai/v1/generate",
      {
        model: "command-light-nightly",
        prompt: message,
        max_tokens: 100,
        temperature: 0.7
      },
      {
        headers: {
          Authorization: `Bearer ${process.env.COHERE_API_KEY}`,
          "Content-Type": "application/json"
        }
      }
    );

    const botReply = response.data.generations[0].text.trim();

    const chat = new Chat({
      username,
      password,
      userMessage: message,
      botReply
    });

    await chat.save();

    res.json({ reply: botReply });
  } catch (error) {
    console.error("Cohere API Error:", error.message);
    res.status(500).json({ error: "Something went wrong" });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`✅ Server running on http://localhost:${PORT}`));
