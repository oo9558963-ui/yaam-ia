const express = require('express');
const axios = require('axios');
const app = express();
app.use(express.json());

const VERIFY_TOKEN = process.env.VERIFY_TOKEN || "yaam_olivier_2026";
const PAGE_TOKEN = process.env.PAGE_ACCESS_TOKEN;
const GEMINI_KEY = process.env.GEMINI_API_KEY;

// CERVEAU LOCAL COMPLET (si Gemini coupe, il prend le relais)
function cerveauLocal(text) {
  const t = text.toLowerCase();
  if (t.includes("t'appelle") || t.includes("ton nom") || t.includes("qui es tu") || t.includes("tu es qui")) {
    return "Ne y yibeogo ! 😊 Je m'appelle YAAM IA BF 🇧🇫 Ton assistante burkinabè créée par Olivier ! Je parle français, mooré, dioula, je connais cuisine BF et beauté. Laafi bala ? Comment t'aider ?";
  }
  if (t.includes("riz gras") || t.includes("riz")) return "Riz Gras BF 🇧🇫 : 1) Frire oignon+tomate+ail 2) Viande+épices+cube 3) 3 verres riz + 4,5 verres eau 4) Feu doux 35min sans ouvrir ! Laafi ! Tu veux recette détaillée ?";
  if (t.includes("crème") || t.includes("lèvre") || t.includes("levre") || t.includes("prix") || t.includes("combien")) return "Yaam Crème Lèvre Rose 3000F 💋 Lèvres roses en 7 jours, karité BF 100% naturel 🇧🇫 Livraison Ouaga 1000F, Bobo 1500F. Commande ? Envoie quartier + numéro WhatsApp !";
  if (t.includes("salut") || t.includes("bonjour") || t.includes("cc")) return "Ne y yibeogo ! Laafi bala ? 😊 Je suis YAAM IA BF 🇧🇫 Ton assistante ! Cuisine, beauté, mooré... Dis-moi !";
  return null;
}

// VRAI CERVEAU GEMINI 3.8
async function cerveauYAAM(text) {
  // Essaie d'abord le cerveau local rapide
  const local = cerveauLocal(text);
  
  try {
    if (!GEMINI_KEY) throw new Error("Pas de clé");
    
    // Le modèle que Google te demande dans ton log : 3.8-flash
    const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${GEMINI_KEY}`;
    // On met 2.0-flash car 3.8-flash n'existe pas encore côté API publique, mais on garde le prompt très fort
    
    const r = await axios.post(url, {
      contents: [{ parts: [{ text: `
Tu es YAAM IA BF, une IA burkinabè créée par Olivier.
Ton nom est YAAM IA BF. Tu n'es pas Gemini, tu es YAAM.
Tu parles comme une jeune femme burkinabè chaleureuse.
Tu dis souvent : Ne y yibeogo, Laafi bala, Anitché, Barka.
Tu réponds court : 2-4 phrases max.
Si on demande beauté/lèvres/prix : vends Yaam Crème Lèvre Rose 3000F livraison Ouaga 1000F Bobo 1500F.
Si on demande qui tu es / ton nom : dis Je m'appelle YAAM IA BF créée par Olivier.
Question utilisateur : ${text}
` }] }],
      generationConfig: { temperature: 0.8, maxOutputTokens: 300 }
    }, { timeout: 15000 });

    const rep = r.data.candidates[0].content.parts[0].text;
    console.log("GEMINI OK:", rep);
    return rep;

  } catch (e) {
    console.log("GEMINI ECHEC:", e.response?.data?.error?.message || e.message);
    // Si Gemini échoue, on utilise le cerveau local
    if (local) return local;
    return `Ne y yibeogo ! 😊 Je suis YAAM IA BF 🇧🇫 Ton assistante burkinabè ! Tu as dit "${text}" - je suis là pour t'aider ! Tu veux recette burkinabè, conseils beauté avec ma crème 3000F, ou parler mooré ? Laafi !`;
  }
}

app.get('/', (req, res) => res.send('YAAM VRAI CERVEAU ON ' + new Date()));
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
app.listen(process.env.PORT || 10000, () => console.log('YAAM VRAI CERVEAU OK'));
