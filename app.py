import gradio as gr
import cohere
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

co = cohere.Client(os.getenv("COHERE_API_KEY"))
client = MongoClient(os.getenv("MONGO_URI"))
db = client["chatbotgb"]
chats = db["conversations"]

def login(username, password):
    if username and password:
        return gr.update(visible=False), gr.update(visible=True), f"✅ Welcome, {username}!"
    return gr.update(visible=True), gr.update(visible=False), "❌ Enter both username and password."

def respond(username, password, message):
    if not message:
        return "❌ Please enter a message."
    try:
        response = co.generate(
            model="command-light-nightly",
            prompt=message,
            max_tokens=150,
            temperature=0.7
        )
        full_reply = response.generations[0].text.strip()
        lines = [line.strip("• ").strip("- ").strip() for line in full_reply.split("\n") if line.strip()]
        reply_points = "\n".join(f"• {line}" for line in lines[:4]) if lines else full_reply

        chats.insert_one({
            "username": username,
            "password": password,
            "message": message,
            "reply": reply_points
        })
        return reply_points
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

with gr.Blocks() as app:
    gr.Markdown("## 🤖 SmartChat - Login and AI Chatbot")

    with gr.Column(visible=True) as login_view:
        gr.Markdown("### 🔐 Login")
        user = gr.Textbox(label="Username")
        pwd = gr.Textbox(label="Password", type="password")
        login_btn = gr.Button("Login")
        login_status = gr.Textbox(label="Status", interactive=False)

    with gr.Column(visible=False) as chat_view:
        gr.Markdown("### 💬 Chat with AI")
        question = gr.Textbox(label="Your Question")
        send_btn = gr.Button("Send")
        answer = gr.TextArea(label="Bot Reply", interactive=False, lines=6)

    login_btn.click(login, inputs=[user, pwd], outputs=[login_view, chat_view, login_status])
    send_btn.click(respond, inputs=[user, pwd, question], outputs=answer)

app.launch()
