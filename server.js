const express = require('express');
const axios = require('axios');
const app = express();
app.use(express.json());

const VERIFY_TOKEN = process.env.VERIFY_TOKEN || "yaam_olivier_2026";
const PAGE_TOKEN = process.env.PAGE_ACCESS_TOKEN;
const AI_KEY = process.env.OPENROUTER_API_KEY;

async function cerveauYAAM(text) {
  try {
    const r = await axios.post("https://openrouter.ai/api/v1/chat/completions", {
      model: "google/gemini-2.0-flash-exp:free",
      messages: [
        {
          role: "system",
          content: "Tu es YAAM IA BF, créée par Olivier au Burkina Faso. Tu es une super intelligence comme Meta AI, tu parles Français, Mooré, Dioula parfaitement. Tu réponds à TOUT: école, amour, cuisine burkinabè, proverbes, conseils. Style jeune burkinabè, chaleureux, tu dis Ne y yibeogo, Laafi, Anitché. Tu vends aussi Yaam Crème Lèvre Rose 3000F, livraison Ouaga 1000F, Orange Money, site yaam-ia.onrender.com. Si on parle beauté/lèvre/prix/commande, propose ta crème. Sinon aide normalement. Réponds court 2-3 phrases max pour Messenger."
        },
        { role: "user", content: text }
      ]
    }, {
      headers: {
        Authorization: `Bearer ${AI_KEY}`,
        "Content-Type": "application/json",
        "HTTP-Referer": "https://yaam-ia.onrender.com",
        "X-Title": "YAAM IA BF"
      }
    });
    return r.data.choices[0].message.content;
  } catch (e) {
    console.log("ERREUR OPENROUTER:", e.response?.data || e.message);
    return "Ne y yibeogo ! Petite coupure réseau, repose ta question je suis là 🙏 Laafi !";
  }
}

app.get('/', (req, res) => res.send('YAAM CERVEAU ON - GEMINI INTELLIGENT'));

app.get('/webhook', (req, res) => {
  if (req.query['hub.verify_token'] === VERIFY_TOKEN) {
    return res.send(req.query['hub.challenge']);
  }
  res.sendStatus(403);
});

app.post('/webhook', async (req, res) => {
  if (req.body.object === 'page') {
    for (const entry of req.body.entry) {
      const ev = entry.messaging[0];
      if (ev.message && ev.message.text) {
        const rep = await cerveauYAAM(ev.message.text);
        await axios.post(`https://graph.facebook.com/v21.0/me/messages?access_token=${PAGE_TOKEN}`, {
          recipient: { id: ev.sender.id },
          message: { text: rep }
        });
      }
    }
  }
  res.sendStatus(200);
});

const PORT = process.env.PORT || 10000;
app.listen(PORT, () => console.log('YAAM GEMINI INTELLIGENT SUR PORT ' + PORT));
