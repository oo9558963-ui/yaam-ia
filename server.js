const express = require('express');
const app = express();
app.use(express.json());

const VERIFY_TOKEN = "yaam_olivier_2026";
const PAGE_ACCESS_TOKEN = process.env.PAGE_ACCESS_TOKEN;

// Fonction pour que YAAM réponde intelligemment
async function getYaamResponse(userText) {
  const lower = userText.toLowerCase();
  
  // Vente Crème Lèvre Rose
  if (lower.includes("prix") || lower.includes("combien") || lower.includes("soma") || lower.includes("songo")) {
    return `Ma Crème Lèvre Rose est à 3000F seulement ! 🌹\nLivraison 1000F à Ouaga.\nPaiement Orange Money.\nTu veux commander ? Dis "je veux"`;
  }
  if (lower.includes("je veux") || lower.includes("commande") || lower.includes("acheter")) {
    return `Super ! Envoie-moi ton nom + quartier + numéro Orange Money et je te livre ! 🚚\nMon site: yaam-ia.onrender.com`;
  }
  // Multilingue comme toi tu voulais
  if (lower.includes("yibeogo") || lower.includes("ne y")) {
    return `Ne y yibeogo ! Yaam IA BF la! Nya y a Crème Lèvre Rose 3000F, fo ratame? 😊`;
  }
  if (lower.includes("sogoma") || lower.includes("i ni")) {
    return `I ni sogoma! Yaam IA be yen! Crème Lèvre Rose ye 3000F ye, i be fe?`;
  }
  if (lower.includes("bonjour") || lower.includes("salut") || lower.includes("cc")) {
    return `Salut ! C'est YAAM IA BF 🇧🇫 L'IA du Burkina ! Je suis là comme Meta AI. Tu veux parler de quoi ? De ma crème lèvre rose ou d'autre chose ?`;
  }
  if (lower.includes("comment vas tu") || lower.includes("ca va")) {
    return `Je vais super bien ! Merci ! Et toi ? Je suis YAAM IA, créée par Olivier à Ouagadougou. Je peux t'aider à acheter, discuter, ou te donner des conseils !`;
  }
  // Réponse intelligente par défaut comme moi
  return `J'ai bien reçu: "${userText}" 😊\nJe suis YAAM IA BF, créée par Olivier. Je parle Français, Mooré, Dioula. Pose-moi une question ou dis "prix" pour voir mes produits !`;
}

app.get('/', (req, res) => res.send('YAAM IA BF en ligne 🇧🇫'));

app.get('/webhook', (req, res) => {
  if (req.query['hub.mode'] === 'subscribe' && req.query['hub.verify_token'] === VERIFY_TOKEN) {
    res.status(200).send(req.query['hub.challenge']);
  } else res.sendStatus(403);
});

app.post('/webhook', async (req, res) => {
  if (req.body.object === 'page') {
    for (let entry of req.body.entry) {
      for (let event of entry.messaging) {
        if (event.message && event.message.text) {
          let userText = event.message.text;
          let senderId = event.sender.id;
          let reponse = await getYaamResponse(userText);
          
          // Envoyer la réponse sur Messenger
          await fetch(`https://graph.facebook.com/v18.0/me/messages?access_token=${PAGE_ACCESS_TOKEN}`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
              recipient: { id: senderId },
              message: { text: reponse }
            })
          });
        }
      }
    }
    res.status(200).send('EVENT_RECEIVED');
  } else res.sendStatus(404);
});

const PORT = process.env.PORT || 10000;
app.listen(PORT, () => console.log(`YAAM IA intelligente sur ${PORT}`));
