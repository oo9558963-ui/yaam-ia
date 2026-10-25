import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai

app = FastAPI(title="YAAM - Vendeur Universel IA")

# Initialisation du client GenAI (la clé API doit être définie dans les variables d'environnement de Render)
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# Modèle de données pour recevoir les messages du client
class ChatRequest(BaseModel):
    store_name: str
    store_type: str  # Ex: "boulangerie", "prêt-à-porter", "quincaillerie"
    catalog_summary: str # Description rapide des produits disponibles
    message: str

@app.post("/chat")
async def chat_with_seller(request: ChatRequest):
    try:
        # Construction dynamique du "System Prompt" selon le commerçant
        system_instructions = (
            f"Tu es un vendeur expert, chaleureux, persuasif et honnête. "
            f"Tu travailles pour la boutique '{request.store_name}', qui est un commerce de type '{request.store_type}'. "
            f"Voici un résumé du catalogue et des informations de la boutique : {request.catalog_summary}. "
            f"Ton rôle est d'accueillir le client, de comprendre son besoin, de lui conseiller les bons produits de la boutique "
            f"et de l'aider à finaliser son achat. Reste toujours professionnel, courtois et orienté conversion."
        )

        # Appel au modèle Gemini (utilisation de gemini-2.5-flash pour la rapidité et la pertinence)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=request.message,
            config={
                'system_instruction': system_instructions,
                'temperature': 0.7, # Un peu de créativité pour la vente, mais mesuré
            }
        )

        return {"response": response.text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def home():
    return {"status": "YAAM IA Server is running!"}
