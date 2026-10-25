const express = require('express');
const axios = require('axios');
const app = express();
app.use(express.json());

const VERIFY_TOKEN = "yaam_olivier_2026";
const PAGE_TOKEN = process.env.PAGE_ACCESS_TOKEN;

app.get('/', (req,res)=> res.send('YAAM IA BF - Ne y yibeogo ! En ligne BF') );

app.get('/webhook', (req,res)=>{
  if(req.query['hub.verify_token'] === VERIFY_TOKEN){
    return res.send(req.query['hub.challenge']);
  }
  res.sendStatus(403);
});

app.post('/webhook', async (req,res)=>{
  const body = req.body;
  if(body.object === 'page'){
    for(const entry of body.entry){
      const event = entry.messaging[0];
      if(event.message && event.message.text){
        const sender = event.sender.id;
        const text = event.message.text.toLowerCase();
        let reply = `Ne y yibeogo ! Yaam IA BF la ! 😊\n\nYaam Crème Lèvre Rose 3000F 💄\nCommande: yaam-ia.onrender.com\nOrange Money disponible !`;

        if(text.includes('soma') || text.includes('prix') || text.includes('combien')){
          reply = `Ma Crème Lèvre Rose ya 3000F la! 💋\nLivraison Ouaga 1000F\nTape ton quartier + Orange Money pour commander!`;
        }

        await axios.post(`https://graph.facebook.com/v21.0/me/messages?access_token=${PAGE_TOKEN}`, {
          recipient: {id: sender},
          message: {text: reply}
        });
      }
    }
    return res.sendStatus(200);
  }
  res.sendStatus(404);
});

const PORT = process.env.PORT || 10000;
app.listen(PORT, ()=> console.log('YAAM IA BF en ligne !'));
