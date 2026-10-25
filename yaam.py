import os
from fastapi import FastAPI, Request
import httpx
from groq import Groq

app = FastAPI()
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "yaam_olivier_2026")
PAGE_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
GROQ_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_KEY) if GROQ_KEY else None

@app.get("/webhook")
async def verify(request: Request):
    c = request.query_params.get("hub.challenge")
    if request.query_params.get("hub.verify_token") == VERIFY_TOKEN:
        return int(c)
    return "Error"

async def cerveau_yaam(text):
    resp = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "Tu es YAAM IA BF, créée par Olivier au Burkina. Parle avec Ne y yibeogo, Laafi, Barka. Tu vends Yaam Crème Lèvre Rose 3000F, Yaam Savon, à Ouagadougou. Réponds court, 2-3 phrases, amical, en mooré et français."},
            {"role": "user", "content": text}
        ],
        temperature=0.7,
        max_tokens=250
    )
    return resp.choices[0].message.content

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
