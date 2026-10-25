const express = require('express');
const axios = require('axios');
const app = express();
app.use(express.json());

const VERIFY_TOKEN = process.env.VERIFY_TOKEN || "yaam_olivier_2026";
const PAGE_TOKEN = process.env.PAGE_ACCESS_TOKEN;
const GEMINI_KEY = process.env.GEMINI_API_KEY;

// Route de vérification pour le Webhook Facebook
app.get('/webhook', (req, res) => {
    const mode = req.query['hub.mode'];
    const token = req.query['hub.verify_token'];
    const challenge = req.query['hub.challenge'];

    if (mode && token === VERIFY_TOKEN) {
        res.status(200).send(challenge);
    } else {
        res.sendStatus(403);
    }
});

// Route principale pour recevoir les messages de Facebook
app.post('/webhook', async (req, res) => {
    const body = req.body;

    if (body.object === 'page') {
        for (const entry of body.entry) {
            const webhookEvent = entry.messaging[0];
            const senderPsid = webhookEvent.sender.id;

            if (webhookEvent.message && webhookEvent.message.text) {
                const incomingText = webhookEvent.message.text;
                
                // Appel du cerveau de l'IA
                const replyText = await cerveauYAAM(incomingText);
                
                // Réponse envoyée sur Messenger
                await sendMessage(senderPsid, replyText);
            }
        }
        res.status(200).send('EVENT_RECEIVED');
    } else {
        res.sendStatus(404);
    }
});

// VRAI CERVEAU GEMINI
async function cerveauYAAM(text) {
    try {
        if (!GEMINI_KEY) {
            return "Ne y yibeogo ! Erreur : La clé GEMINI_API_KEY n'est pas configurée sur Render.";
        }

        // Utilisation du modèle rapide et performant de Gemini
        const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${GEMINI_KEY}`;
        
        const promptSysteme = `Tu es YAAM IA BF 🇧🇫, une assistante virtuelle burkinabè chaleureuse, polie et experte, créée par Olivier. 
        Tu aides les utilisateurs sur Facebook (cuisine burkinabè comme le riz gras, conseils beauté comme la crème lèvre rose à 3000F, langues locales comme le mooré ou le dioula, etc.). 
        Sois toujours accueillante, utilise parfois des expressions locales ("Laafi bala ?", "Ne y yibeogo") et réponds de façon claire et utile.`;

        const response = await axios.post(url, {
            contents: [
                {
                    parts: [
                        { text: `${promptSysteme}\n\nClient : ${text}` }
                    ]
                }
            ]
        });

        const candidates = response.data.candidates;
        if (candidates && candidates[0] && candidates[0].content) {
            return candidates[0].content.parts[0].text;
        } else {
            return "Désolé, je n'ai pas pu générer de réponse claire. Laafi ?";
        }
    } catch (error) {
        console.error("Erreur Gemini:", error.response?.data || error.message);
        // Solution de secours locale si l'API rencontre un souci
        if (text.toLowerCase().includes("riz")) {
            return "Riz Gras BF 🇧🇫 : Frire oignon+tomate+ail, ajouter viande+épices, puis le riz et l'eau à feu doux 35 min ! Laafi !";
        }
        return "Ne y yibeogo ! Un petit souci technique m'empêche de réfléchir, réessaie dans un instant ! 🇧🇫";
    }
}

// Fonction pour envoyer un message via l'API Facebook Messenger
async function sendMessage(senderPsid, responseText) {
    try {
        await axios.post(`https://graph.facebook.com/v18.0/me/messages?access_token=${PAGE_TOKEN}`, {
            recipient: { id: senderPsid },
            message: { text: responseText }
        });
    } catch (error) {
        console.error("Erreur d'envoi Facebook:", error.response?.data || error.message);
    }
}

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Serveur YAAM IA démarré sur le port ${PORT}`);
});
