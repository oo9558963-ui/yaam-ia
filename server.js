const express = require('express');
const bodyParser = require('body-parser');
const axios = require('axios');
const app = express();
app.use(bodyParser.json());
const PAGE_ACCESS_TOKEN = process.env.PAGE_ACCESS_TOKEN;
const VERIFY_TOKEN = process.env.VERIFY_TOKEN || "yaam_olivier_2026";
app.get('/webhook', (req, res) => {
  if (req.query['hub.verify_token'] === VERIFY_TOKEN) {
    res.send(req.query['hub.challenge']);
  } else {
    res.send('Erreur token');
  }
});
app.post('/webhook', async (req, res) => {
  try {
    let body = req.body;
    if (body.object === 'page') {
      for (const entry of body.entry) {
        for (const messaging of entry.messaging) {
          if (messaging.message && messaging.message.text) {
            let senderId = messaging.sender.id;
            let userText = messaging.message.text;
            let reponse = "Salut ! Yaam IA BF est là comme Meta AI ! Tu as dit : " + userText;
            await axios.post(`https://graph.facebook.com/v18.0/me/messages?access_token=${PAGE_ACCESS_TOKEN}`, {
              recipient: { id: senderId },
              message: { text: reponse }
            });
          }
        }
      }
      res.status(200).send('EVENT_RECEIVED');
    } else {
      res.sendStatus(404);
    }
  } catch (err) {
    res.status(200).send('EVENT_RECEIVED');
  }
});
const PORT = process.env.PORT || 10000;
app.listen(PORT, () => console.log('Yaam BF Live'));
