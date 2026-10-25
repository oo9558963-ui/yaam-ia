from flask import Flask, request, jsonify, render_template_string
import json, os

app = Flask(__name__)

PRODUCTS_FILE = "products.json"

def load_products():
    if os.path.exists(PRODUCTS_FILE):
        try:
            with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return [
        {"id": 1, "nom": "Crème Lèvre Rose", "prix": "3000F", "description": "Rend les lèvres douces, roses et sans taches en 7 jours. 100% naturel"},
        {"id": 2, "nom": "Savon Éclaircissant", "prix": "2500F", "description": "Anti-taches visage et corps."}
    ]

def save_products(products):
    with open(PRODUCTS_FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=2)

products = load_products()

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>YAAM IA BF - Par Olivier</title>
<style>
body{background:#0a0a0a;color:white;font-family:Arial;padding:10px}
.header{background:linear-gradient(45deg,gold,orange);color:black;padding:15px;text-align:center;border-radius:10px;font-weight:bold}
#chat{height:400px;overflow-y:auto;background:#1a1a1a;border-radius:10px;padding:10px;margin:15px 0}
.msg-ia{background:#333;padding:10px;border-radius:10px;margin:5px 0;border-left:3px solid gold}
.msg-user{background:gold;color:black;padding:10px;border-radius:10px;margin:5px 0;text-align:right}
.bar{display:flex;gap:5px}
input{flex:1;padding:12px;border-radius:20px;border:none}
button{border:none;border-radius:50%;width:50px;height:50px;font-size:20px;cursor:pointer}
#micro{background:gold} #send{background:white} #parle{background:#00d4ff}
.prod{background:#222;padding:10px;border-radius:10px;margin:5px 0;border:1px solid gold}
</style>
</head>
<body>
<div class="header">🇧🇫 YAAM IA BF - Par Olivier<br><small>Votre commerce ne dort jamais - 65 39 95 53</small></div>

<div id="chat"><div class="msg-ia">👋 Salamu ! Je suis YAAM IA BF. Je peux parler vocal maintenant ! 🎤 Clique sur micro et parle moi ! Tu veux Crème Lèvre Rose 3000F ?</div></div>

<div class="bar">
<button id="micro">🎤</button>
<input id="msg" placeholder="Tape ou parle...">
<button id="send">➤</button>
<button id="parle">🔊</button>
</div>

<div style="margin-top:20px">
<h3>📦 Produits:</h3>
<div id="prods"></div>
</div>

<script>
const chat=document.getElementById('chat');
const msgInput=document.getElementById('msg');

function ajouterMsg(text,qui){
  const d=document.createElement('div');
  d.className=qui==='user'?'msg-user':'msg-ia';
  d.innerText=text;
  chat.appendChild(d);
  chat.scrollTop=chat.scrollHeight;
  if(qui==='ia'){parler(text);}
}

function parler(texte){
  const voix=new SpeechSynthesisUtterance(texte);
  voix.lang='fr-FR'; voix.rate=0.95;
  speechSynthesis.speak(voix);
}

async function envoyer(){
  const t=msgInput.value.trim();
  if(!t)return;
  ajouterMsg(t,'user');
  msgInput.value='';
  try{
    const r=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:t})});
    const data=await r.json();
    ajouterMsg(data.reponse,'ia');
  }catch(e){ajouterMsg("Erreur, réessaie",'ia');}
}

document.getElementById('send').onclick=envoyer;
msgInput.onkeypress=(e)=>{if(e.key==='Enter')envoyer();}

// 🎤 MICRO
document.getElementById('micro').onclick=function(){
  const Rec=window.SpeechRecognition||window.webkitSpeechRecognition;
  if(!Rec){alert("Micro non supporté, utilise Chrome");return;}
  const rec=new Rec(); rec.lang='fr-FR'; rec.start();
  this.innerText='🔴';
  rec.onresult=(e)=>{
    msgInput.value=e.results[0][0].transcript;
    this.innerText='🎤';
    envoyer();
  };
  rec.onerror=()=>{this.innerText='🎤';};
};

document.getElementById('parle').onclick=()=>{
  const last=document.querySelector('.msg-ia:last-child');
  if(last)parler(last.innerText);
};

// charger produits
fetch('/api/products').then(r=>r.json()).then(prods=>{
  const div=document.getElementById('prods');
  prods.forEach(p=>{
    div.innerHTML+=`<div class="prod"><b>${p.nom}</b> - ${p.prix}<br><small>${p.description}</small><br><button onclick="msgInput.value='Je veux ${p.nom}';envoyer()" style="background:gold;border:none;padding:5px 10px;border-radius:10px;margin-top:5px;width:auto;height:auto;font-size:14px">Commander 🎤</button></div>`;
  });
});
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@app.route('/chat')
def chat_page():
    return render_template_string(HTML_PAGE)

@app.route('/api/products')
def get_products():
    return jsonify(products)

@app.route('/api/chat', methods=['POST'])
def api_chat():
    data = request.get_json()
    message = data.get('message','').lower()
    
    # Logique YAAM
    if 'crème' in message or 'levre' in message or 'lèvre' in message or 'rose' in message:
        reponse = "Parfait ! 🌸 La Crème Lèvre Rose est à 3000F. Elle rend tes lèvres douces et roses en 7 jours. Livraison Ouaga 1000F, hors Ouaga 1500F. Tu veux que je te réserve ? Donne moi ton nom et quartier sur WhatsApp 65 39 95 53 😊"
    elif 'savon' in message:
        reponse = "Le Savon Éclaircissant est à 2500F, anti-taches visage et corps. Très efficace ! Tu veux les 2 produits ensemble ? 5000F seulement !"
    elif 'prix' in message or 'combien' in message:
        reponse = "Crème Lèvre Rose 3000F, Savon 2500F. Pack des 2 à 5000F. Livraison rapide ! Quelle est ta position ?"
    elif 'bonjour' in message or 'salut' in message or 'salam' in message:
        reponse = "Bonjour ! 👋 Bienvenue chez YAAM IA BF, créé par Olivier. Je suis ton assistante vocale ! Tu peux me parler avec le micro 🎤. Tu cherches quoi aujourd'hui ?"
    else:
        reponse = f"Merci pour ton message : '{data.get('message')}'. Je suis YAAM IA BF, je vends Crème Lèvre Rose 3000F et Savon 2500F. Dis moi ce que tu veux, ou parle moi en vocal 🎤 ! Et contacte Olivier direct sur WhatsApp 65 39 95 53 pour commander."

    return jsonify({"reponse": reponse})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
