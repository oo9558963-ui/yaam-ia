import os
from fastapi import FastAPI, Request
import httpx
from groq import Groq

app = FastAPI()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "yaam_olivier_2026")
PAGE_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
GROQ_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_KEY) if GROQ_KEY else None

@app.get("/")
async def home():
    return {"status": "YAAM IA BF OK"}

@app.get("/webhook")
async def verify(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return int(challenge)
    return "Error"

async def cerveau_yaam(text):
    try:
        resp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Tu es YAAM IA BF, créée par Olivier au Burkina Faso. Tu parles français et mooré (Ne y yibeogo, Laafi, Barka). Tu vends Yaam Crème Lèvre Rose 3000F, savon, à Ouagadougou. Réponds court, 2-3 phrases, amical, utile."},
                {"role": "user", "content": text}
            ],
            temperature=0.7,
            max_tokens=250
        )
        return resp.choices[0].message.content
    except Exception as e:
        # Si encore erreur, on le voit dans les logs Render
        print(f"GROQ ERROR: {e}")
        return f"Ne y yibeogo ! Laafi ? Yaam est là, dis-moi pour ta crème lèvre rose !"

@app.post("/webhook")
async def webhook(request: Request):
    body = await request.json()
    print(f"WEBHOOK RECU: {body}")
    if body.get("object") == "page":
        for entry in body.get("entry", []):
            for ev in entry.get("messaging", []):
                if ev.get("message", {}).get("text"):
                    txt = ev["message"]["text"]
                    sid = ev["sender"]["id"]
                    rep = await cerveau_yaam(txt)
                    print(f"REPONSE YAAM: {rep}")
                    async with httpx.AsyncClient() as http:
                        await http.post(
                            f"https://graph.facebook.com/v21.0/me/messages?access_token={PAGE_TOKEN}",
                            json={"recipient": {"id": sid}, "message": {"text": rep}}
                        )
    return {"ok": True}
