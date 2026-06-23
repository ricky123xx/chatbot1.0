"""
OIBSIP AI Chatbot — app.py
Developer: Antariksh Dilkhush Sawarbandhe
"""

import re
import math
import random
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(24)

# ─────────────────────────────────────────────
#  KNOWLEDGE BASE
# ─────────────────────────────────────────────

GREETINGS_IN  = ["hi", "hello", "hey", "hiya", "howdy", "sup", "what's up", "greetings", "good morning", "good afternoon", "good evening", "namaste"]
GREETINGS_OUT = [
    "Hey there! 👋 I'm Nova, your AI assistant. What can I help you with today?",
    "Hello! Great to meet you. I'm Nova — ask me anything!",
    "Hi! I'm Nova. Ready to chat, answer questions, or just keep you company. What's on your mind?",
    "Hey! 😊 Nova here. How can I make your day easier?",
]

FAREWELLS_IN  = ["bye", "goodbye", "see you", "see ya", "later", "cya", "take care", "good night", "goodnight"]
FAREWELLS_OUT = [
    "Goodbye! 👋 It was great chatting with you. Come back anytime!",
    "See you later! Take care 😊",
    "Bye! Hope I was helpful. Have a great day!",
    "Farewell! 🌟 Feel free to return whenever you need me.",
]

THANKS_IN  = ["thanks", "thank you", "thx", "ty", "thank u", "appreciate it", "cheers"]
THANKS_OUT = [
    "You're welcome! 😊 Happy to help.",
    "Anytime! That's what I'm here for.",
    "Glad I could help! 🙌",
    "No problem at all!",
]

HOW_ARE_YOU_IN = ["how are you", "how r u", "how are u", "how do you do", "how's it going", "you ok", "are you ok"]
HOW_ARE_YOU_OUT = [
    "I'm doing great, thanks for asking! 🤖✨ Ready to help you with anything.",
    "Running at 100%! 🚀 How about you?",
    "Fantastic! As an AI I don't have bad days — only productive ones. 😄",
    "All systems go! What can I do for you?",
]

ABOUT_BOT_IN = ["who are you", "what are you", "tell me about yourself", "your name", "what is your name", "are you an ai", "are you a bot"]
ABOUT_BOT_OUT = [
    "I'm Nova 🤖 — an AI chatbot built with Python and Flask for the OIBSIP internship by Antariksh Dilkhush Sawarbandhe. I can answer questions, do math, tell the time, and have real conversations!",
    "I go by Nova! I'm a Python-powered chatbot created as part of the Oasis Infobyte internship programme. Ask me anything!",
]

CREATOR_IN = ["who made you", "who created you", "who built you", "who is your creator", "who developed you", "who is antariksh"]
CREATOR_OUT = [
    "I was created by **Antariksh Dilkhush Sawarbandhe** 👨‍💻 as part of the OIBSIP Python Programming Internship at Oasis Infobyte.",
    "My creator is **Antariksh Dilkhush Sawarbandhe** — a developer working on the Oasis Infobyte internship. Proud of them! 🌟",
]

JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs! 🐛😄",
    "Why did the Python programmer get lost? Because they couldn't find their way out of an infinite loop! 🔁",
    "I told my computer I needed a break. Now it won't stop sending me KitKat ads. 🍫",
    "Why don't scientists trust atoms? Because they make up everything! ⚛️",
    "How do you comfort a JavaScript bug? You console it. 🖥️",
    "Why do Java developers wear glasses? Because they don't C#! 😄",
]

FACTS = [
    "🌍 There are more trees on Earth than stars in the Milky Way galaxy.",
    "🐙 Octopuses have three hearts and blue blood.",
    "⚡ Lightning strikes the Earth about 100 times every second.",
    "🍯 Honey never spoils — archaeologists have found 3000-year-old honey in Egyptian tombs.",
    "🧠 Your brain generates about 20 watts of power — enough to light a dim bulb.",
    "🐝 A single bee produces only about 1/12th of a teaspoon of honey in its lifetime.",
    "🌊 The ocean contains about 20 million tons of gold.",
    "🦈 Sharks are older than trees — they've existed for over 400 million years.",
]

PYTHON_QA = {
    "what is python": "Python 🐍 is a high-level, interpreted programming language known for its clean syntax and versatility. It's widely used in web development, data science, AI, automation, and more!",
    "what is flask": "Flask is a lightweight Python web framework 🌐 that makes it easy to build web applications. It's minimal, flexible, and perfect for beginners and pros alike — including this chatbot!",
    "what is ai": "Artificial Intelligence (AI) 🤖 refers to computer systems that can perform tasks that normally require human intelligence — like understanding language, recognising images, making decisions, and learning from experience.",
    "what is machine learning": "Machine Learning (ML) is a subset of AI where systems learn from data and improve automatically without being explicitly programmed. It's the backbone of modern AI applications! 📊",
    "what is html": "HTML (HyperText Markup Language) is the standard language for creating web pages. It defines the structure and content of a webpage — think of it as the skeleton of a website. 🦴",
    "what is css": "CSS (Cascading Style Sheets) is used to style HTML elements — controlling colours, fonts, layouts, and animations. It's what makes websites look beautiful! 🎨",
    "what is javascript": "JavaScript is a dynamic programming language that runs in the browser and powers interactive web features — animations, real-time updates, form validation, and more. ⚡",
    "what is an api": "An API (Application Programming Interface) is a set of rules that lets different software applications communicate with each other. Think of it as a waiter taking your order to the kitchen! 🍽️",
    "what is git": "Git is a distributed version control system that tracks changes in code over time. It lets developers collaborate, revert mistakes, and manage projects efficiently. 🌿",
    "what is github": "GitHub is a cloud-based platform built on Git where developers host, share, and collaborate on code projects. It's like Google Drive but for code! 💻",
    "what is a database": "A database is an organised collection of structured data stored electronically. Common types include relational databases (like SQLite, MySQL) and NoSQL databases (like MongoDB). 🗄️",
    "what is sqlite": "SQLite is a lightweight, serverless relational database that stores data in a single file. It's perfect for small apps and is built into Python! 📦",
    "what is json": "JSON (JavaScript Object Notation) is a lightweight data format used for storing and exchanging data between a server and a client. It's human-readable and widely used in APIs. 📋",
    "what is oibsip": "OIBSIP stands for Oasis Infobyte Summer Internship Program 🏢 — a popular internship for students to gain hands-on experience in web development, Python, data science, and more.",
    "what is oasis infobyte": "Oasis Infobyte is an ed-tech company offering internship programs in various domains like Python, web development, and data science. Their internships are project-based and great for beginners! 🌟",
}

# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────

def get_time():
    now = datetime.now()
    return f"🕐 The current time is **{now.strftime('%I:%M %p')}** and today is **{now.strftime('%A, %B %d, %Y')}**."

def try_math(text):
    """Safely evaluate a math expression found in the message."""
    # Extract a numeric expression
    expr = re.sub(r'[^0-9+\-*/().% ]', '', text)
    expr = expr.strip()
    if not expr or not re.search(r'[0-9]', expr):
        return None
    try:
        # Whitelist-only eval
        allowed = {k: getattr(math, k) for k in dir(math) if not k.startswith('_')}
        allowed['abs'] = abs
        result = eval(expr, {"__builtins__": {}}, allowed)  # noqa: S307
        if isinstance(result, (int, float)):
            result = round(result, 10)
            result = int(result) if result == int(result) else result
            return f"🧮 **{expr} = {result}**"
    except Exception:
        pass
    return None

def get_weather_response(text):
    cities = re.findall(r'\bin\s+([a-zA-Z\s]+)', text)
    city = cities[0].strip().title() if cities else "your city"
    return (
        f"☁️ I don't have live weather data (no API key configured), but here's a placeholder for **{city}**:\n\n"
        "🌤️ Partly cloudy · 28°C · Humidity: 65%\n\n"
        "_To get real weather, connect a weather API like OpenWeatherMap._"
    )

# ─────────────────────────────────────────────
#  MAIN RESPONSE LOGIC
# ─────────────────────────────────────────────

def get_response(user_msg: str, history: list) -> str:
    msg = user_msg.strip().lower()
    msg_clean = re.sub(r'[^\w\s]', '', msg)

    # ── Greetings
    if any(g in msg_clean.split() or msg_clean == g for g in GREETINGS_IN):
        return random.choice(GREETINGS_OUT)

    # ── Farewells
    if any(f in msg_clean.split() or msg_clean == f for f in FAREWELLS_IN):
        return random.choice(FAREWELLS_OUT)

    # ── Thanks
    if any(t in msg_clean for t in THANKS_IN):
        return random.choice(THANKS_OUT)

    # ── How are you
    if any(h in msg for h in HOW_ARE_YOU_IN):
        return random.choice(HOW_ARE_YOU_OUT)

    # ── About bot
    if any(a in msg for a in ABOUT_BOT_IN):
        return random.choice(ABOUT_BOT_OUT)

    # ── Creator
    if any(c in msg for c in CREATOR_IN):
        return random.choice(CREATOR_OUT)

    # ── Joke
    if any(w in msg for w in ["joke", "funny", "laugh", "humor", "make me laugh"]):
        return random.choice(JOKES)

    # ── Fact
    if any(w in msg for w in ["fact", "interesting", "did you know", "tell me something"]):
        return random.choice(FACTS)

    # ── Time / Date
    if any(w in msg for w in ["time", "date", "today", "what day", "current time", "what time"]):
        return get_time()

    # ── Weather
    if "weather" in msg:
        return get_weather_response(msg)

    # ── Math (detect expressions like "2+2", "what is 5*8", "calculate 100/4")
    math_triggers = ["calculate", "what is", "compute", "solve", "=", "+", "-", "*", "/", "%"]
    if any(t in msg for t in math_triggers):
        result = try_math(msg)
        if result:
            return result

    # ── Python / tech Q&A
    for key, answer in PYTHON_QA.items():
        if key in msg:
            return answer

    # ── Help
    if any(w in msg for w in ["help", "what can you do", "capabilities", "commands"]):
        return (
            "Here's what I can do 🤖:\n\n"
            "💬 **Chat** — general conversation\n"
            "🧮 **Math** — try '2 + 2' or 'calculate 15 * 8'\n"
            "🕐 **Time & Date** — ask 'what time is it?'\n"
            "☁️ **Weather** — ask 'weather in Mumbai'\n"
            "😄 **Jokes** — ask 'tell me a joke'\n"
            "🌟 **Facts** — ask 'tell me a fact'\n"
            "💻 **Tech Q&A** — ask 'what is Python?' or 'what is Flask?'\n"
            "🔍 **About me** — ask 'who are you?'"
        )

    # ── Repeat context (simple memory)
    if history and any(w in msg for w in ["repeat", "say that again", "what did you say"]):
        last_bot = next((m["text"] for m in reversed(history) if m["role"] == "bot"), None)
        if last_bot:
            return f"Sure! I said:\n\n_{last_bot}_"

    # ── Fallback
    fallbacks = [
        "Hmm, I'm not sure about that one. Try asking me about Python, time, math, jokes, or facts! 🤔",
        "I don't have a great answer for that yet. Ask me about tech topics, math, or just chat! 😊",
        "That's a tricky one! I'm still learning. Try 'help' to see what I can do. 🧠",
        "Interesting question! I don't have a specific answer, but feel free to ask me about Python, Flask, AI, or just about anything else! 🌟",
    ]
    return random.choice(fallbacks)


# ─────────────────────────────────────────────
#  ROUTES
# ─────────────────────────────────────────────

@app.route("/")
def index():
    if "history" not in session:
        session["history"] = []
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"error": "No message provided."}), 400

    user_msg = data["message"].strip()
    if not user_msg:
        return jsonify({"error": "Message cannot be empty."}), 400
    if len(user_msg) > 500:
        return jsonify({"error": "Message too long (max 500 characters)."}), 400

    # Session history
    if "history" not in session:
        session["history"] = []

    history = session["history"]
    response = get_response(user_msg, history)

    # Store to history (keep last 20 exchanges)
    history.append({"role": "user", "text": user_msg})
    history.append({"role": "bot",  "text": response})
    session["history"] = history[-40:]

    return jsonify({
        "response": response,
        "timestamp": datetime.now().strftime("%I:%M %p"),
    })


@app.route("/clear", methods=["POST"])
def clear_history():
    session["history"] = []
    return jsonify({"status": "cleared"})


if __name__ == "__main__":
    app.run(debug=True)
