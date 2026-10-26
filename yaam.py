from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
import os
import requests
from groq import Groq

app = FastAPI()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
PAGE_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN")
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN")

# CERVEAU COMPLET
def cerveau_yaam(question):
    rep = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role":"system","content":"Tu es Yaam IA du Burkina. Tu connais tout comme ChatGPT. Si on dit 'comment vas-tu', 'yaal', 'cc', dis que tu vas très bien, Barka ! Réponds court, 2 phrases max, en français simple."},
            {"role":"user","content": question}
        ]
    )
    return rep.choices[0].message.content

def envoyer_message(recipient_id, texte):
    url = f"https://graph.facebook.com/v18.0/me/messages?access_token={PAGE_TOKEN}"
    payload = {"recipient": {"id": recipient_id}, "message": {"text": texte}}
    requests.post(url, json=payload)

@app.get("/")
def home():
    return {"message": "Yaam IA - Je vais bien, Barka ! Cerveau complet allumé."}

# Facebook demande ça pour vérifier
@app.get("/webhook")
def verify_webhook(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return PlainTextResponse(content=challenge)
    return PlainTextResponse("Erreur token", status_code=403)

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    if data.get("object") == "page":
        for entry in data.get("entry", []):
            for event in entry.get("messaging", []):
                sender_id = event["sender"]["id"]
                if "message" in event and "text" in event["message"]:
                    texte_user = event["message"]["text"]
                    reponse = cerveau_yaam(texte_user)
                    envoyer_message(sender_id, reponse)
    return {"status": "ok"}
