from flask import Flask, request, jsonify

app = Flask(__name__)

# --- PAGE D'ACCUEIL ---
@app.route('/')
def home():
    return """
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>YAAM IA - L'Intelligence Africaine</title>
<style>
body{margin:0;font-family:Arial,sans-serif;background:linear-gradient(135deg,#0f0c29,#302b63,#24243e);color:white;min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:20px}
h1{font-size:3em;margin:0;letter-spacing:3px}h1 span{color:#ffcc00}
.slogan{font-size:1.3em;opacity:.9;margin-top:10px}
.card{background:rgba(255,255,255,.1);backdrop-filter:blur(10px);border:1px solid rgba(255,255,255,.2);border-radius:20px;padding:30px;margin-top:30px;max-width:500px;width:90%}
.btn{display:block;background:#ffcc00;color:#000;padding:15px;border-radius:50px;text-decoration:none;font-weight:bold;margin:15px 0;font-size:1.1em}
.btn2{display:block;background:transparent;border:2px solid #ffcc00;color:#ffcc00;padding:12px;border-radius:50px;text-decoration:none;font-weight:bold;margin:15px 0}
.status{margin-top:20px;background:#00ff88;color:#000;padding:8px 20px;border-radius:20px;font-weight:bold;display:inline-block}
</style>
</head>
<body>
<h1>YAAM <span>IA</span></h1>
<p class="slogan">L'Intelligence Artificielle par l'Afrique, pour l'Afrique</p>
<div class="card">
<a href="/chat" class="btn">🚀 Entrer dans YAAM IA</a>
<a href="/chat" class="btn2">💬 Parler à YAAM</a>
<p>Développé par Olivier à Ouagadougou 🇧🇫</p>
</div>
<div class="status">🟢 EN LIGNE - yaam-ia.onrender.com</div>
<p style="margin-top:15px;opacity:.6">Version 2.0 - Octobre 2026</p>
</body>
</html>
"""

# --- PAGE DE CHAT ---
@app.route('/chat')
def chat():
    return """
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Chat YAAM IA</title>
<style>
body{margin:0;font-family:Arial;background:#0f0c29;color:white;display:flex;flex-direction:column;height:100vh}
.header{background:#302b63;padding:15px;text-align:center;font-weight:bold;font-size:1.3em}
.header a{color:#ffcc00;text-decoration:none}
#messages{flex:1;overflow-y:auto;padding:20px}
.msg{margin:10px 0;padding:12px 18px;border-radius:18px;max-width:80%}
.user{background:#ffcc00;color:#000;margin-left:auto}
.ia{background:rgba(255,255,255,.15);border:1px solid rgba(255,255,255,.2)}
.input-area{display:flex;padding:15px;background:#1a1a3e}
input{flex:1;padding:15px;border-radius:30px;border:none;outline:none;font-size:1em}
button{margin-left:10px;background:#ffcc00;border:none;border-radius:50%;width:50px;height:50px;font-size:1.5em;cursor:pointer}
</style>
</head>
<body>
<div class="header"><a href="/">← YAAM IA</a> - Chat Intelligent 🇧🇫</div>
<div id="messages">
<div class="msg ia">Salut Olivier ! 👋 Je suis YAAM IA, l'IA africaine créée à Ouagadougou. Comment je peux t'aider aujourd'hui ?</div>
</div>
<div class="input-area">
<input id="input" placeholder="Écris ton message..." onkeypress="if(event.key==='Enter')send()">
<button onclick="send()">➤</button>
</div>
<script>
async function send(){
let inp=document.getElementById('input');
let txt=inp.value.trim();
if(!txt) return;
let box=document.getElementById('messages');
box.innerHTML+=`<div class='msg user'>${txt}</div>`;
inp.value='';
let res=await fetch('/ask',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:txt})});
let data=await res.json();
box.innerHTML+=`<div class='msg ia'>${data.reply}</div>`;
box.scrollTop=box.scrollHeight;
}
</script>
</body>
</html>
"""

# --- CERVEAU DE YAAM IA ---
@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    msg = data.get('message','').lower()
    if 'salut' in msg or 'bonjour' in msg or 'hello' in msg:
        reply = "Salut ! 😊 Content de te voir ! Je suis YAAM IA, 100% burkinabè ! Que veux-tu savoir ?"
    elif 'qui es tu' in msg or 'qui est tu' in msg or 'tu es qui' in msg:
        reply = "Je suis YAAM IA, l'Intelligence Artificielle par l'Afrique, pour l'Afrique ! Développé par Olivier à Ouagadougou 🇧🇫. Je ne suis pas ChatGPT, je suis YAAM !"
    elif 'ouagadougou' in msg or 'burkina' in msg:
        reply = "Ouagadougou ! ❤️ La capitale du Burkina Faso, le pays des Hommes Intègres ! C'est là que je suis né, grâce à Olivier !"
    elif 'olivier' in msg:
        reply = "Olivier c'est mon créateur ! Un génie à Ouagadougou qui m'a donné vie ! Respect à lui ! 🙏🇧🇫"
    else:
        reply = f"Tu as dit : '{data.get('message')}'. Intéressant ! Je suis YAAM IA, je peux parler de tout : culture africaine, tech, conseils... Dis-m'en plus ! 🚀"
    return jsonify({'reply': reply})

if __name__ == '__main__':
    app.run()
