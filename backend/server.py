from flask import Flask, request, jsonify
from flask_cors import CORS
import os, traceback
from openai import OpenAI

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.get("/")
def home():
    return jsonify({
        "ok": True,
        "service": "lucy-backend",
        "msg": "Lucy 🐱 backend is running 💗"
    })

@app.post("/arena")
def arena():
    try:
        data = request.get_json(force=True) or {}
        messages = data.get("messages", [])

        if not isinstance(messages, list) or not messages:
            messages = [{"role": "user", "content": "هلا لوسي"}]

        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.6,
            max_tokens=400
        )
        reply = resp.choices[0].message.content
        return jsonify({"reply": reply})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8787")))
