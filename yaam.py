from fastapi import FastAPI, Request
from groq import Groq
import os

app = FastAPI()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.get("/")
def home():
    return {"message": "Yaam IA - Je vais bien, Barka ! Cerveau complet allumé."}

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    print(data)
    # Ici on testera le cerveau
    try:
        q = data.get("message", "comment vas-tu ?")
        rep = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role":"system","content":"Tu es Yaam IA du Burkina. Tu connais tout. Si on dit comment vas-tu, dis que tu vas bien."},
                {"role":"user","content": q}
            ]
        )
        print(rep.choices[0].message.content)
    except Exception as e:
        print(e)
    return {"status": "ok"}
