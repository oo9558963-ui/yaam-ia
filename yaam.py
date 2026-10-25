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
    return {"YAAM IA BF": "OK"}

@app.get("/webhook")
async def verify(request: Request):
    if request.query_params.get("hub.verify_token") == VERIFY_TOKEN:
        return int(request.query_params.get("hub.challenge"))
    return "Error"

async def cerveau_yaam(text):
    try:
        resp = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "system", "content": "Tu es YAAM IA BF créée par Olivier au Burkina. Tu parles français et mooré avec Ne y yibeogo, Laafi, Barka. Tu vends Crème Lèvre Rose 3000F, Savon Yaam. Livraison Ouaga. Réponds court 2-3 phrases, vendeuse sympa."},
                {"role": "user", "content": text}
            ],
            temperature=0.8,
            max_tokens=300
        )
        return resp.choices[0].message.content
    except Exception as e:
        print(f"GROQ ERROR: {e}")
        return None

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
                    if not rep:
                        rep = "Ne y yibeogo ! Laafi ? Yaam est là pour ta crème lèvre rose 3000F, tu veux commander ?"
                    async with httpx.AsyncClient() as http:
                        await http.post(f"https://graph.facebook.com/v21.0/me/messages?access_token={PAGE_TOKEN}",
                                        json={"recipient": {"id": sid}, "message": {"text": rep}})
    return {"ok": True}
