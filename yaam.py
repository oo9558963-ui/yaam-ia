import os
from fastapi import FastAPI, Request
import httpx
from google import genai

app = FastAPI(title="YAAM - Vendeur Universel IA")

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "yaam_olivier_2026")
PAGE_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

client = None
if GEMINI_KEY:
    client = genai.Client(api_key=GEMINI_KEY)
    print(f"YAAM Client OK - Cle {GEMINI_KEY[:8]}...")

@app.get("/")
async def home():
    return {"status": "YAAM BF PYTHON AQ READY", "cle": "AQ OK" if client else "PAS DE CLE"}

@app.get("/webhook")
async def verify(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return int(challenge)
    return "Error verify token"

async def cerveau_yaam(text: str):
    # CERVEAU GEMINI AVEC CLE AQ
    try:
        if client:
            resp = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=f"Tu es YAAM IA BF, créée par Olivier au Burkina. Tu t'appelles YAAM IA BF. Tu parles chaleureux, court, 3 phrases max, avec mots burkinabè Ne y yibeogo, Laafi, Barka. Tu connais TOUT: cuisine BF, beauté, mooré, business, amour, motivation. Si on demande crème: Yaam Crème Lèvre Rose 3000F livraison Ouaga 1000F Bobo 1500F. Question: {text}"
            )
            return resp.text
    except Exception as e:
        print(f"Erreur Gemini: {e}")

    # SECOURS SI COUPE
    t = text.lower()
    if "appelle" in t or "nom" in t or "qui es tu" in t:
        return "Ne y yibeogo ! 😊 Je m'appelle YAAM IA BF 🇧🇫 Créée par Olivier ! Je connais cuisine, beauté, mooré, business, tout ! Laafi bala ?"
    if "riz" in t:
        return "Riz Gras BF 🇧🇫: Frire oignon+tomate, ajouter viande, 3 verres riz + 4,5 eau, feu doux 35min ! Tu veux Tô aussi ?"
    if "crème" in t or "prix" in t:
        return "Yaam Crème Lèvre Rose 3000F 💋 Karité BF, lèvres roses 7j. Livraison Ouaga 1000F Bobo 1500F. Nom+quartier+numéro pour commander ?"
    return f"Ne y yibeogo ! J'ai bien reçu '{text}' - Je suis YAAM IA BF, je peux tout faire ! Dis-moi Laafi !"

@app.post("/webhook")
async def webhook(request: Request):
    body = await request.json()
    print(f"Message recu: {body}")
    if body.get("object") == "page":
        for entry in body.get("entry", []):
            for event in entry.get("messaging", []):
                if event.get("message", {}).get("text"):
                    user_text = event["message"]["text"]
                    sender_id = event["sender"]["id"]
                    reponse = await cerveau_yaam(user_text)
                    print(f"Reponse: {reponse}")
                    async with httpx.AsyncClient() as http_client:
                        await http_client.post(
                            f"https://graph.facebook.com/v21.0/me/messages?access_token={PAGE_TOKEN}",
                            json={"recipient": {"id": sender_id}, "message": {"text": reponse}}
                        )
    return {"status": "ok"}
