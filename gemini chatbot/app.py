from flask import Flask, render_template, request, jsonify
from google import genai
import json
from datetime import datetime
import os

app = Flask(__name__)


client = genai.Client(api_key="YOUR_API_KEY")

MODEL_NAME = "gemini-2.5-flash"

MEMORY_FILE = "memory.json"

# ---------------- MEMORY ---------------- #

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {"conversation": []}
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)

def add_message(role, message):
    memory = load_memory()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    memory["conversation"].append({
        "role": role,
        "message": message,
        "timestamp": timestamp
    })

    save_memory(memory)

# ---------------- ROUTES ---------------- #

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    try:
        add_message("user", user_message)

        memory = load_memory()

        system_prompt = """
You are a Career Guidance Assistant for students after 10th standard.
You ONLY guide about:
- Intermediate streams
- Diploma
- ITI
- Polytechnic
- Entrance exams
- Career scope
- Application process

If question is outside this domain reply exactly:
"I am only designed to guide students after 10th standard. Please ask career-related questions."
"""

        context = system_prompt + "\n\n"

        for msg in memory["conversation"]:
            context += f"{msg['role']}: {msg['message']}\n"

        
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=context
        )

        bot_reply = response.text

        add_message("assistant", bot_reply)

        return jsonify({
    "reply": bot_reply,
    "history": load_memory()["conversation"]
})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, use_reloader = False)
