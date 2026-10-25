import os
from fastapi import FastAPI, Request
import httpx
from google import genai

app = FastAPI()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "yaam_olivier_2026")
PAGE_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

# CLIENT AVEC CLE AQ.
client = None
if GEMINI_KEY:
    try:
        client = genai.Client(api_key=GEMINI_KEY)
        print(f"YAAM CLIENT AQ OK: {GEMINI_KEY[:10]}...")
    except Exception as e:
        print(f"ERREUR CLIENT AQ: {e}")

@app.get("/")
async def home():
    return {"status": "YAAM BF V2.0 LIVE", "mode": "AQ + GEMINI 2.0"}

@app.get("/webhook")
async def verify(request: Request):
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    if token == VERIFY_TOKEN:
        return int(challenge)
    return "Error token"

async def cerveau_yaam(text: str):
    if not client:
        return "Ne y yibeogo ! Laafi ? Ma clé n'est pas encore active sur Render ! 🇧🇫"

    # ESSAI AVEC LES NOUVEAUX MODELES POUR CLE AQ.
    modeles_a_essayer = ["gemini-2.0-flash", "gemini-2.5-flash", "gemini-2.0-flash-001"]

    for modele in modeles_a_essayer:
        try:
            resp = client.models.generate_content(
                model=modele,
                contents=f"""Tu es YAAM IA BF, créée par Olivier au Burkina Faso. Tu t'appelles YAAM IA BF, jamais Gemini.
Tu es chaleureuse, courte (2-3 phrases max), tu utilises Ne y yibeogo, Laafi, Barka.
Tu connais TOUT: cuisine burkinabè, beauté, mooré, business, amour, motivation.
Si on parle crème: Yaam Crème Lèvre Rose 3000F, livraison Ouaga 1000F, Bobo 1500F. Prends nom+quartier+numéro pour commander.
Question de la cliente: {text}
Réponds en YAAM IA BF !"""
            )
            print(f"SUCCES AVEC MODELE: {modele}")
            return resp.text
        except Exception as e:
            print(f"Echec {modele}: {e}")
            continue
    
    # Si tous échouent
    return f"Ne y yibeogo ! Mon cerveau chauffe un peu Laafi, réessaie ! Je suis YAAM IA BF 🇧🇫"

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
                    print(f"Message: {txt}")
                    rep = await cerveau_yaam(txt)
                    print(f"Reponse: {rep}")
                    async with httpx.AsyncClient() as http:
                        await http.post(
                            f"https://graph.facebook.com/v21.0/me/messages?access_token={PAGE_TOKEN}",
                            json={"recipient": {"id": sid}, "message": {"text": rep}}
                        )
    return {"status": "ok"}
