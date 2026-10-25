import os
from fastapi import FastAPI, Request
import httpx
from google import genai

app = FastAPI()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "yaam_olivier_2026")
PAGE_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_KEY) if GEMINI_KEY else None

@app.get("/webhook")
async def verify(request: Request):
    c = request.query_params.get("hub.challenge")
    if request.query_params.get("hub.verify_token") == VERIFY_TOKEN:
        return int(c)
    return "Error"

async def cerveau_yaam(text):
    if not client:
        return "Pas de client AQ"
    try:
        # LISTE LES MODELES DISPO POUR TA CLE AQ
        models = client.models.list()
        liste = [m.name for m in models]
        print(f"MODELES DISPO: {liste}")

        # ESSAI LE PREMIER MODELE DISPO
        resp = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"Tu es YAAM IA BF Burkina, réponds court avec Ne y yibeogo, Laafi. Question: {text}"
        )
        return resp.text
    except Exception as e:
        # ICI ON AFFICHE LA VRAIE ERREUR DANS MESSENGER
        err = str(e)[:500]
        print(f"ERREUR COMPLETE: {err}")
        return f"ERREUR DEBUG: {err}"

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
