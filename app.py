from flask import Flask, request, jsonify
app = Flask(__name__)
@app.route('/')
def home():
    return """<!DOCTYPE html><html><head><meta charset="UTF-8"><title>YAAM IA</title><style>body{margin:0;font-family:Arial;background:linear-gradient(135deg,#0f0c29,#302b63,#24243e);color:white;min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:20px}h1{font-size:3em}h1 span{color:#ffcc00}.btn{display:block;background:#ffcc00;color:#000;padding:15px;border-radius:50px;text-decoration:none;font-weight:bold;margin:15px 0}</style></head><body><h1>YAAM <span>IA</span></h1><p>L'Intelligence par l'Afrique, pour l'Afrique</p><a href="/chat" class="btn">Entrer dans YAAM IA</a><a href="/chat" class="btn">Parler a YAAM</a><p>Dev par Olivier - Ouaga</p></body></html>"""
@app.route('/chat')
def chat():
    return """<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Chat YAAM</title><style>body{margin:0;font-family:Arial;background:#0f0c29;color:white;display:flex;flex-direction:column;height:100vh}.header{background:#302b63;padding:15px;text-align:center}#messages{flex:1;overflow-y:auto;padding:20px}.msg{margin:10px 0;padding:12px;border-radius:18px;max-width:80%}.user{background:#ffcc00;color:#000;margin-left:auto}.ia{background:rgba(255,255,255,.15)} .input-area{display:flex;padding:15px;background:#1a1a3e}input{flex:1;padding:15px;border-radius:30px;border:none}button{margin-left:10px;background:#ffcc00;border:none;border-radius:50%;width:50px;height:50px}</style></head><body><div class="header"><a href="/" style="color:#ffcc00">← YAAM IA</a> Chat</div><div id="messages"><div class="msg ia">Salut Olivier! Je suis YAAM IA, cree a Ouaga. Comment aider?</div></div><div class="input-area"><input id="input" placeholder="Ecris..." onkeypress="if(event.key==='Enter')send()"><button onclick="send()">></button></div><script>async function send(){let i=document.getElementById('input');let t=i.value.trim();if(!t)return;let b=document.getElementById('messages');b.innerHTML+=`<div class='msg user'>${t}</div>`;i.value='';let r=await fetch('/ask',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:t})});let d=await r.json();b.innerHTML+=`<div class='msg ia'>${d.reply}</div>`;b.scrollTop=b.scrollHeight}</script></body></html>"""
@app.route('/ask', methods=['POST'])
def ask():
    d=request.get_json(); m=d.get('message','').lower()
    if 'salut' in m or 'bonjour' in m: r="Salut! Content de te voir! Je suis YAAM IA, 100% burkinabe!"
    elif 'qui es tu' in m or 'qui est tu' in m: r="Je suis YAAM IA, l'IA africaine par l'Afrique, pour l'Afrique! Developpe par Olivier a Ouaga!"
    elif 'olivier' in m: r="Olivier c'est mon createur! Un genie a Ouagadougou!"
    else: r=f"Tu as dit: {d.get('message')}. Je suis YAAM IA, je t'ecoute!"
    return jsonify({'reply':r})
