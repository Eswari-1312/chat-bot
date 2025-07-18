﻿SmartChat - AI Chatbot with Login, Cohere API, and MongoDB
📌 Project Overview
SmartChat is a simple yet effective AI chatbot web application developed using Gradio, Cohere NLP API, and MongoDB. It allows users to log in, interact with an AI model, and stores all conversations in a MongoDB database for future reference.

🚀 Features
🔐 User Login
Basic login system using Gradio's interactive UI to authenticate users.

🤖 AI Chatbot Responses
Uses Cohere’s command-light-nightly model to generate intelligent and relevant replies to user queries.

💾 Data Storage

Stores usernames, passwords (currently stored as plain text – not recommended), user messages, and bot responses in MongoDB.

Helps track and manage conversation history.

🖥️ User Interface
Built using Gradio Blocks to provide a clean, responsive, and intuitive chat interface.

🛠️ Technologies Used
Technology	Purpose
Gradio	For creating a web-based user interface
Cohere API	For generating natural language responses
MongoDB	For storing user conversations
Python	Backend logic and API handling

⚠️ Recommendations
Security

⚠️ Do NOT store raw passwords.

Use secure password hashing (e.g., bcrypt or argon2) before saving them to MongoDB.

Feature Enhancements

🕒 Add timestamps to each MongoDB record to track message history.

🧹 Automatically clear the input field after each message submission for improved UX.

📦 Installation & Setup
Install Dependencies

bash
Copy
Edit
pip install gradio cohere pymongo python-dotenv
Setup .env File

Create a .env file in the root directory and include:

env
Copy
Edit
COHERE_API_KEY=your_cohere_api_key
MONGO_URI=your_mongo_connection_string
Run the Application

bash
Copy
Edit
python app.py
Then open the Gradio interface in your browser to start chatting.

