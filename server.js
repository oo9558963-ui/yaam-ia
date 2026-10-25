const express = require('express');
const axios = require('axios');
const app = express();
app.use(express.json());

const VERIFY_TOKEN = process.env.VERIFY_TOKEN || "yaam_olivier_2026";
const PAGE_TOKEN = process.env.PAGE_ACCESS_TOKEN;
const GEMINI_KEY = process.env.GEMINI_API_KEY;

async function cerveauYAAM(text) {
  // On essaie 3 endpoints différents qui marchent avec les clés AQ...
  const essais = [
    `https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key=${GEMINI_KEY}`,
    `https://generativelanguage.googleapis.com/v1/models/gemini-2.0-flash:generateContent?key=${GEMINI_KEY}`,
    `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${GEMINI_KEY}`
  ];

  for (const url of essais) {
    try {
      console.log("Essaie:", url);
      const r = await axios.post(url, {
        contents: [{ parts: [{ text: `Tu es YAAM IA BF, créée par Olivier au Burkina Faso. Tu es Meta AI burkinabè chaleureuse, parle Français, Mooré, Dioula. Réponds en 2-3 phrases. Si beauté/lèvres/prix, vends Yaam Crème Lèvre Rose 3000F livraison Ouaga 1000F, Bobo 1500F. Question: ${text}` }] }]
      }, { timeout: 20000 });
      console.log("SUCCES avec", url);
      return r.data.candidates[0].content.parts[0].text;
    } catch (e) {
      console.log("ECHEC", url, "->", e.response?.data?.error?.message || e.message);
    }
  }
  
  // Si tout échoue, on donne la recette quand même pour ne pas bloquer !
  if (text.toLowerCase().includes("riz gras")) {
    return "Ne y yibeogo ! Pour Riz Gras Burkinabè 🇧🇫 : 1) Frire oignon, tomate, ail. 2) Ajouter viande, cube, épices. 3) Ajouter riz lavé + eau. 4) Cuire à feu doux 30min. Laafi ! Tu veux la recette complète avec quantités ? 😊";
  }
  
  return "Ne y yibeogo ! Laafi bala ? 😊 Je suis YAAM IA BF 🇧🇫 Je prépare la réponse pour '" + text + "' - Mon cerveau Gemini se connecte, réessaye dans 1 minute Laafi !";
}

app.get('/', (req, res) => res.send('YAAM V1 ON ' + new Date()));
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
app.listen(process.env.PORT || 10000, () => console.log('YAAM V1 FINAL OK'));
