const express = require('express');
const axios = require('axios');
const app = express();
app.use(express.json());

const VERIFY_TOKEN = process.env.VERIFY_TOKEN || "yaam_olivier_2026";
const PAGE_TOKEN = process.env.PAGE_ACCESS_TOKEN;
const GEMINI_KEY = process.env.GEMINI_API_KEY;

async function cerveauYAAM(text) {
  try {
    const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${GEMINI_KEY}`;
    const r = await axios.post(url, {
      contents: [{ parts: [{ text: `Tu es YAAM IA BF, créée par Olivier au Burkina Faso. Tu es Meta AI burkinabè chaleureuse. Parle Français, Mooré, Dioula. Réponds court 2-3 phrases, dis Ne y yibeogo, Laafi, Anitché. Si beauté/lèvre/prix, vends Yaam Crème Lèvre Rose 3000F livraison Ouaga 1000F. Question: ${text}` }] }]
    }, { timeout: 15000 });
    return r.data.candidates[0].content.parts[0].text;
  } catch (e) {
    console.log("ERREUR:", e.response?.data || e.message);
    return "Ne y yibeogo ! Laafi bala ? 😊 Je suis YAAM IA BF 🇧🇫 Ton assistante ! J'ai reçu: '" + text + "' Comment puis-je t'aider ?";
  }
}

app.get('/', (req, res) => res.send('YAAM GEMINI 2.0 ON'));
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
app.listen(process.env.PORT || 10000, () => console.log('YAAM 2.0 OK'));
