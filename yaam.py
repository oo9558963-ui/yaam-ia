import os
from fastapi import FastAPI, Request
import httpx
from google import genai

app = FastAPI()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "yaam_olivier_2026")
PAGE_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

client = None
if GEMINI_KEY:
    try:
        client = genai.Client(api_key=GEMINI_KEY)
        print(f"CLIENT OK AQ: {GEMINI_KEY[:10]}")
    except Exception as e:
        print(f"ERREUR CLIENT: {e}")

@app.get("/")
async def home():
    return {"status": "YAAM BF AQ READY"}

@app.get("/webhook")
async def verify(request: Request):
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    if token == VERIFY_TOKEN:
        return int(challenge)
    return "Error"

async def cerveau_yaam(text):
    if not client:
        print("PAS DE CLIENT")
        return "Ne y yibeogo ! Je suis YAAM IA BF mais ma clé n'est pas configurée sur Render !"
    try:
        # MODELE QUI MARCHE AVEC CLE AQ
        resp = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=f"Tu es YAAM IA BF créée par Olivier Burkina. Réponds court, chaleureux, 3 phrases max, avec mots Ne y yibeogo, Laafi, Barka. Tu connais cuisine, beauté, mooré. Si crème: Yaam Crème Lèvre Rose 3000F livraison Ouaga 1000F Bobo 1500F. Question: {text}"
        )
        print(f"GEMINI OK: {resp.text[:50]}")
        return resp.text
    except Exception as e:
        print(f"ERREUR GEMINI DETAILLEE: {e}")
        # Retourne l'erreur pour qu'on la voie dans Messenger
        return f"Ne y yibeogo ! Soucis technique: {str(e)[:100]} - mais je suis là Laafi !"

@app.post("/webhook")
async def webhook(request: Request):
    body = await request.json()
    if body.get("object") == "page":
        for entry in body.get("entry", []):
            for ev in entry.get("messaging", []):
                if ev.get("message", {}).get("text"):
                    txt = ev["message"]["text"]
                    sid = ev["sender"]["id"]
                    rep = await cerveau_yaam(txt)
                    async with httpx.AsyncClient() as http:
                        await http.post(f"https://graph.facebook.com/v21.0/me/messages?access_token={PAGE_TOKEN}",
                                        json={"recipient": {"id": sid}, "message": {"text": rep}})
    return {"ok": True}
