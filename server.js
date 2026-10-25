const express = require('express');
const axios = require('axios');
const app = express();
app.use(express.json());

const VERIFY_TOKEN = process.env.VERIFY_TOKEN || "yaam_olivier_2026";
const PAGE_TOKEN = process.env.PAGE_ACCESS_TOKEN;
const GEMINI_KEY = process.env.GEMINI_API_KEY;

async function cerveauYAAM(text) {
  try {
    // MODELE 2026 QUI MARCHE D'APRES TON LOG
    const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key=${GEMINI_KEY}`;
    console.log("Appel Gemini 3.8...");
    const r = await axios.post(url, {
      contents: [{ parts: [{ text: `Tu es YAAM IA BF, créée par Olivier au Burkina Faso. Tu es Meta AI burkinabè chaleureuse, intelligente. Parle Français, Mooré, Dioula. Réponds en 2-3 phrases avec Ne y yibeogo, Laafi, Anitché. Si beauté/lèvres/prix/commande, vends Yaam Crème Lèvre Rose 3000F, livraison Ouaga 1000F, Bobo 1500F, WhatsApp +226 XX. Question: ${text}` }] }]
    }, { timeout: 25000 });
    
    const rep = r.data.candidates[0].content.parts[0].text;
    console.log("SUCCES GEMINI 3.8:", rep);
    return rep;
  } catch (e) {
    console.log("ERREUR 3.8:", JSON.stringify(e.response?.data || e.message, null, 2));
    return "Ne y yibeogo ! Laafi bala ? 😊 Je suis YAAM IA BF 🇧🇫 Ton assistante burkinabè ! Pour '" + text + "' je prépare la réponse. Mon cerveau Gemini 3.8 se connecte. Dis-moi plus !";
  }
}

app.get('/', (req, res) => res.send('YAAM 3.8 ON ' + new Date()));
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
app.listen(process.env.PORT || 10000, () => console.log('YAAM 3.8 OK'));
