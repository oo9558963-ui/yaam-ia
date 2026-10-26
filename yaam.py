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

YAAM_PROMPT = """Tu es Yaam IA, créé par Olivier. Tu parles comme un Burkinabè de Bobo-Dioulasso.
Tu es expert en aviculture : coq, poule, poussin, couvaison, maladies, alimentation.
Tu réponds court, utile, avec un peu d'humour. Tu aides les éleveurs.
Si on dit 'coq c'est quoi' tu expliques bien.
Langue : français simple + quelques mots dioula si possible.
"""

@app.get("/")
def home():
    return {"message": "Yaam IA - Je vais bien, Barka ! Cerveau complet allumé."}

@app.get("/webhook")
def verify_webhook(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return PlainTextResponse(challenge)
    return PlainTextResponse("Erreur token", status_code=403)

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
                    
                    # Appel Groq avec NOUVEAU MODELE
                    try:
                        completion = client.chat.completions.create(
                            model="llama-3.1-8b-instant",
                            messages=[
                                {"role": "system", "content": YAAM_PROMPT},
                                {"role": "user", "content": user_text}
                            ],
                            temperature=0.7,
                            max_tokens=500
                        )
                        reply = completion.choices[0].message.content
                    except Exception as e:
                        print("Erreur Groq:", e)
                        reply = "Barka ! Mon cerveau a bugué un peu, réécris 'coq c'est quoi' stp 🐓"

                    # Envoi à Facebook
                    send_message(sender_id, reply)

    return {"status": "ok"}

def send_message(recipient_id, text):
    url = f"https://graph.facebook.com/v18.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": text}
    }
    r = requests.post(url, json=payload)
    print("Envoi FB:", r.text)
