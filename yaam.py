import os
from fastapi import FastAPI, Request
import httpx
from google import genai

app = FastAPI()
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "yaam_olivier_2026")
PAGE_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_KEY) if GEMINI_KEY else None

@app.get("/")
async def home():
    return {"status": "YAAM BF 3.8 LIVE"}

@app.get("/webhook")
async def verify(request: Request):
    c = request.query_params.get("hub.challenge")
    if request.query_params.get("hub.verify_token") == VERIFY_TOKEN:
        return int(c)
    return "Error"

async def cerveau_yaam(text):
    try:
        resp = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Tu es YAAM IA BF créée par Olivier Burkina. Réponds court 2-3 phrases max avec Ne y yibeogo, Laafi, Barka. Tu connais cuisine, beauté, mooré. Produit: Yaam Crème Lèvre Rose 3000F livraison Ouaga 1000F Bobo 1500F. Question: {text}"
        )
        return resp.text
    except Exception as e:
        # Si 2.5 plante, essaie 3.8
        try:
            resp = client.models.generate_content(
                model="gemini-2.5-flash-preview-04-17",
                contents=f"Tu es YAAM IA BF Burkina, réponds court avec Ne y yibeogo Laafi. Question: {text}"
            )
            return resp.text
        except Exception as e2:
            return f"Ne y yibeogo ! Dernière erreur: {str(e2)[:300]}"

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
