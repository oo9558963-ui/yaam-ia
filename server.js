const express = require('express');
const axios = require('axios');
const app = express();
app.use(express.json());
const VERIFY_TOKEN = process.env.VERIFY_TOKEN || "yaam_olivier_2026";
const PAGE_TOKEN = process.env.PAGE_ACCESS_TOKEN;
function cerveauYAAM(text){
 const t=text.toLowerCase();
 if(t.includes("riz")) return "Ne y yibeogo ! Riz Gras BF 🇧🇫 : Frire oignon+tomate+ail, ajouter viande+épices, ajouter 3 verres riz + 4 verres eau, cuire 35min feu doux ! Laafi ! Tu veux recette détaillée ?";
 if(t.includes("crème")||t.includes("levre")||t.includes("lèvre")||t.includes("prix")) return "Ne y yibeogo ! Yaam Crème Lèvre Rose 3000F 💋 Lèvres roses 7 jours, karité BF 🇧🇫 Livraison Ouaga 1000F, Bobo 1500F. Commande ? Envoie quartier+numéro !";
 return "Ne y yibeogo ! Laafi bala ? 😊 Je suis YAAM IA BF 🇧🇫 Ton assistante burkinabè ! J'ai reçu: "+text+" - Comment t'aider ?";
}
app.get('/',(req,res)=>res.send('YAAM BF ON'));
app.get('/webhook',(req,res)=>{if(req.query['hub.verify_token']===VERIFY_TOKEN)return res.send(req.query['hub.challenge']);res.sendStatus(403);});
app.post('/webhook',async(req,res)=>{
 if(req.body.object==='page'){
  for(const entry of req.body.entry){
   const ev=entry.messaging[0];
   if(ev.message?.text){
    const rep=cerveauYAAM(ev.message.text);
    await axios.post(`https://graph.facebook.com/v21.0/me/messages?access_token=${PAGE_TOKEN}`,{recipient:{id:ev.sender.id},message:{text:rep}});
   }
  }
 }
 res.sendStatus(200);
});
app.listen(process.env.PORT||10000,()=>console.log('YAAM OK'));
