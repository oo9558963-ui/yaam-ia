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
    # LISTE DES NOMS QUI MARCHENT AVEC LES CLES AQ. EN 2026
    modeles = [
        "gemini-2.5-flash",
        "gemini-flash-latest",
        "gemini-2.0-flash-lite",
        "gemini-2.5-flash-lite",
        "gemini-pro-latest"
    ]
    for m in modeles:
        try:
            print(f"ESSAI MODELE: {m}")
            resp = client.models.generate_content(
                model=m,
                contents=f"Tu es YAAM IA BF créée par Olivier Burkina. Réponds court 2-3 phrases avec Ne y yibeogo, Laafi, Barka. Question: {text}"
            )
            print(f"OK AVEC {m}")
            return resp.text
        except Exception as e:
            print(f"ECHEC {m}: {e}")
            last_err = str(e)
            continue
    return f"Ne y yibeogo ! Tous les modèles échouent. Dernier: {last_err[:300]}"

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
