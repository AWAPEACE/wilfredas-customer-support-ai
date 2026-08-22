from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import requests

KNOWLEDGE_BASE_FILE = "knowledge_base.txt"

with open(KNOWLEDGE_BASE_FILE, "r", encoding="utf-8") as file:
    knowledge_base = file.read()

conversation_history = []

def get_ai_response(user_message):
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return "Sorry, the AI service is not connected. Please configure the GROQ_API_KEY."

    conversation_history.append({
        "role": "user",
        "content": user_message
    })

    system_prompt = f"""
You are the customer support AI assistant for Wilfreda's Collection.

Use ONLY the information in the knowledge base below.

KNOWLEDGE BASE:
{knowledge_base}

Rules:
- Be friendly, respectful and professional.
- Do not invent prices, products, availability, delivery fees or policies.
- If information is unavailable, tell the customer that a human staff member needs to confirm it.
- Remember previous messages in the conversation.
"""

    messages = [
        {"role": "system", "content": system_prompt}
    ] + conversation_history[-10:]

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-oss-20b",
                "messages": messages,
                "temperature": 0.3
            },
            timeout=60
        )

        response.raise_for_status()

        answer = response.json()["choices"][0]["message"]["content"]

        conversation_history.append({
            "role": "assistant",
            "content": answer
        })

        return answer

    except Exception as error:
        return f"Sorry, something went wrong: {error}"


HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Wilfreda's Collection - Customer Support</title>

    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #f7f7f7;
        }

        .header {
            background: #8b0000;
            color: white;
            padding: 20px;
            text-align: center;
        }

        .header h1 {
            margin: 0;
            font-size: 24px;
        }

        .header p {
            margin: 6px 0 0;
        }

        .chat {
            max-width: 700px;
            margin: auto;
            height: 75vh;
            display: flex;
            flex-direction: column;
            background: white;
        }

        #messages {
            flex: 1;
            overflow-y: auto;
            padding: 20px;
        }

        .message {
            padding: 12px 15px;
            margin: 10px 0;
            border-radius: 15px;
            max-width: 80%;
            white-space: pre-wrap;
        }

        .user {
            background: #eee;
            margin-left: auto;
        }

        .bot {
            background: #f4dede;
            margin-right: auto;
        }

        .input-area {
            display: flex;
            padding: 12px;
            border-top: 1px solid #ddd;
        }

        #input {
            flex: 1;
            padding: 12px;
            border: 1px solid #ccc;
            border-radius: 20px;
            outline: none;
        }

        button {
            margin-left: 8px;
            padding: 12px 20px;
            border: none;
            border-radius: 20px;
            background: #8b0000;
            color: white;
            font-weight: bold;
        }

        button:disabled {
            background: #999;
        }
    </style>
</head>

<body>

<div class="header">
    <h1>Wilfreda's Collection</h1>
    <p>Customer Support AI</p>
</div>

<div class="chat">

    <div id="messages">
        <div class="message bot">
            Hello! 👋 Welcome to Wilfreda's Collection.
            How can I help you today?
        </div>
    </div>

    <div class="input-area">
        <input
            id="input"
            placeholder="Type your message..."
            onkeydown="if(event.key === 'Enter') sendMessage()"
        >

        <button
