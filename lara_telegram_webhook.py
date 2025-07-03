import os
import requests
from flask import Flask, request

app = Flask(__name__)

# ✅ Set your Telegram bot token and OpenAI API key as environment variables in Render
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

# LARA: Main message handler
@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()

    if 'message' in data and 'text' in data['message']:
        chat_id = data['message']['chat']['id']
        user_msg = data['message']['text']

        # Call OpenAI to get response
        lara_reply = chatgpt_response(user_msg)

        # Send reply back via Telegram
        send_message(chat_id, lara_reply)

    return "OK"

# 🔁 Send message to Telegram user
def send_message(chat_id, text):
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    requests.post(TELEGRAM_API_URL, json=payload)

# 🤖 Generate response using OpenAI
def chatgpt_response(user_input):
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    json_data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are LARA, a Forex AI assistant for CashFX users. Be smart, friendly, and helpful."},
            {"role": "user", "content": user_input}
        ]
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=json_data)
    return response.json()['choices'][0]['message']['content'].strip()
