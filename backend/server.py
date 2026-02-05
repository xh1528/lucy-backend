from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# قراءة مفتاح OpenAI من Render Environment Variables
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

        # حماية لو وصلت بيانات غلط
        if not isinstance(messages, list) or len(messages) == 0:
            messages = [
                {"role": "user", "content": "هلا لوسي"}
            ]

        # طلب OpenAI مع timeout (مهم جدًا)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.6,
            max_tokens=300,
            timeout=15
        )

        reply = response.choices[0].message.content

        return jsonify({
            "reply": reply
        })

    except Exception as e:
        # 🔴 حتى لو فشل OpenAI نرجّع رد (عشان ما يعلّق الفرونت)
        return jsonify({
            "reply": "🐱 لوسي: صحيت متأخرة شوي… جربي ترسلين مرة ثانية 💗"
        })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8787))
    app.run(host="0.0.0.0", port=port)
