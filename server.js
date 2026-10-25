const express = require('express');
const axios = require('axios');
const app = express();
app.use(express.json());

const VERIFY_TOKEN = process.env.VERIFY_TOKEN || "yaam_olivier_2026";
const PAGE_TOKEN = process.env.PAGE_ACCESS_TOKEN;
const GEMINI_KEY = process.env.GEMINI_API_KEY;

async function cerveauYAAM(text) {
  console.log("Question reçue:", text);
  console.log("Clé Gemini présente:", GEMINI_KEY ? "OUI " + GEMINI_KEY.substring(0,10) + "..." : "NON");
  
  try {
    if (!GEMINI_KEY) throw new Error("Pas de GEMINI_API_KEY sur Render");
    
    // NOUVEAU ENDPOINT QUI MARCHE AVEC LES CLES AQ...
    const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${GEMINI_KEY}`;
    
    const r = await axios.post(url, {
      contents: [{ parts: [{ text: `Tu es YAAM IA BF, créée par Olivier au Burkina Faso. Tu es une IA burkinabè chaleureuse. Parle Français, Mooré, Dioula. Réponds en 2-3 phrases courtes, avec Ne y yibeogo, Laafi, Anitché. Si on parle beauté/lèvres/prix, vends Yaam Crème Lèvre Rose 3000F livraison Ouaga 1000F. Question de l'utilisateur: ${text}` }] }]
    }, { timeout: 15000 });

    const rep = r.data.candidates[0].content.parts[0].text;
    console.log("Réponse Gemini:", rep);
    return rep;

  } catch (e) {
    console.log("ERREUR GEMINI DETAIL:", JSON.stringify(e.response?.data || e.message, null, 2));
    // Message temporaire pour voir l'erreur, après on remettra joli
    if (e.response?.data?.error?.message) {
      return "Erreur technique: " + e.response.data.error.message + " | Je suis YAAM, repose ta question Laafi !";
    }
    return "Ne y yibeogo ! Laafi bala ? 😊 Je suis YAAM IA BF, ton assistante burkinabè ! J'ai reçu: '" + text + "' Dis-moi ce que tu veux !";
  }
}

app.get('/', (req, res) => res.send('YAAM GEMINI V2 ON - ' + new Date()));
app.get('/webhook', (req, res) => {
  if (req.query['hub.verify_token'] === VERIFY_TOKEN) return res.send(req.query['hub.challenge']);
  res.sendStatus(403);
});
app.post('/webhook', async (req, res) => {
  if (req.body.object === 'page') {
    for (const entry of req.body.entry) {
      const ev = entry.messaging[0];
      if (ev.message?.text) {
        const rep = await cerveauYAAM(ev.message.text);
        await axios.post(`https://graph.facebook.com/v21.0/me/messages?access_token=${PAGE_TOKEN}`, {
          recipient: { id: ev.sender.id }, message: { text: rep }
        });
      }
    }
  }
  res.sendStatus(200);
});
app.listen(process.env.PORT || 10000, () => console.log('YAAM GEMINI V2 OK'));
