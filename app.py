from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

API_KEY = "".join((os.getenv("OPENROUTER_API_KEY") or "").split())
MODEL = "openai/gpt-4o-mini"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    if not API_KEY:
        return jsonify({"error": "API anahtarı ayarlanmamış."}), 500

    data = request.json
    messages = data.get("messages", [])

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": MODEL,
            "messages": messages
        },
        timeout=120
    )

    return jsonify(response.json()), response.status_code

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
