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

    data = request.json or {}
    messages = data.get("messages", [])

    try:
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

        try:
            result = response.json()
        except ValueError:
            return jsonify({"error": "API geçerli JSON yanıtı döndürmedi."}), 502

        return jsonify(result), response.status_code

    except requests.exceptions.Timeout:
        return jsonify({"error": "API zaman aşımına uğradı."}), 504

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Bağlantı hatası: " + str(e)}), 502

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
