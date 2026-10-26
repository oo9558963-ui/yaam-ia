import os
import requests
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from groq import Groq

app = FastAPI()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "yaam2024")
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

PROMPT = """Tu es Yaam IA, créé par Olivier à Bobo-Dioulasso, expert en aviculture.
Tu aides les éleveurs : coq, poule, poussin, couvaison, maladies, alimentation.
Tu parles en français simple, chaleureux, avec un peu de dioula. Réponses courtes et utiles.
"""

@app.get("/")
def home():
    return {"status": "Yaam IA OK - Barka !"}

@app.get("/webhook")
def verify(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return PlainTextResponse(challenge)
    return PlainTextResponse("Token error", status_code=403)

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    print("message reçu:", data)

    if data.get("object") == "page":
        for entry in data.get("entry", []):
            for event in entry.get("messaging", []):
                if "message" in event and "text" in event["message"]:
                    sender_id = event["sender"]["id"]
                    user_text = event["message"]["text"]

                    try:
                        # NOUVEAU MODELE GROQ 2026 - CORRECTION ICI
                        completion = client.chat.completions.create(
                            model="openai/gpt-oss-20b",
                            messages=[
                                {"role": "system", "content": PROMPT},
                                {"role": "user", "content": user_text}
                            ],
                            temperature=0.7,
                            max_tokens=500
                        )
                        reply = completion.choices[0].message.content

                    except Exception as e:
                        print(f"Erreur Groq: {e}")
                        reply = f"Barka, erreur technique: {e}. Redis après."

                    # Envoi réponse Facebook
                    url = f"https://graph.facebook.com/v18.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
                    payload = {
                        "recipient": {"id": sender_id},
                        "message": {"text": reply}
                    }
                    r = requests.post(url, json=payload)
                    print("Envoi FB:", r.text)

    return {"status": "ok"}
