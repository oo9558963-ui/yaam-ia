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
        {"id": 1, "nom": "Crème Lèvre Rose", "prix": "3000F", "description": "Rend les lèvres douces, roses et sans taches en 7 jours. 100% naturel, Ouaga."},
        {"id": 2, "nom": "Savon Éclaircissant", "prix": "2500F", "description": "Anti-taches visage et corps."}
    ]

def save_products(products):
    with open(PRODUCTS_FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=2)

products = load_products()

@app.route("/")
def home():
    return render_template_string("""
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>body{background:#0a1931;color:white;font-family:Arial;text-align:center;padding:30px}
    .btn{background:#ffcc00;color:black;padding:15px 30px;border-radius:30px;text-decoration:none;font-weight:bold;display:block;margin:20px auto;width:260px}
    </style></head><body>
    <h1>YAAM IA 🇧🇫</h1>
    <p>L'Intelligence par l'Afrique, pour l'Afrique</p>
    <a class="btn" href="/chat">Entrer dans YAAM IA</a>
    <a class="btn" href="/dashboard">Dashboard Vendeur</a>
    <p>Produits: {{count}}</p>
    </body></html>
    """, count=len(products))

@app.route("/chat")
def chat_page():
    return render_template_string("""
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>body{background:#111;color:white;font-family:Arial;padding:10px}
    #box{height:65vh;overflow-y:auto;border:1px solid #333;padding:10px;border-radius:10px}
    .msg{padding:10px;margin:5px;border-radius:10px;max-width:85%}
    .user{background:#ffcc00;color:black;margin-left:auto}
    .bot{background:#222}
    input{width:68%;padding:12px;border-radius:20px;border:none}
    button{padding:12px 18px;border-radius:20px;background:#ffcc00;border:none;font-weight:bold}
    </style></head><body>
    <h3>YAAM IA - Vendeuse auto</h3>
    <div id="box"><div class="msg bot">Salut ! Je suis YAAM IA, de Ouaga. Tu veux crème lèvre rose ?</div></div>
    <div style="display:flex;gap:8px;margin-top:10px">
    <input id="inp" placeholder="Ecris ici..."><button onclick="send()">Envoyer</button></div>
    <script>
    async function send(){
      let txt=document.getElementById('inp').value; if(!txt) return;
      let box=document.getElementById('box');
      box.innerHTML+=`<div class="msg user">${txt}</div>`;
      document.getElementById('inp').value='';
      let res=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:txt})});
      let data=await res.json();
      box.innerHTML+=`<div class="msg bot">${data.reply}</div>`;
      box.scrollTop=box.scrollHeight;
    }
    </script></body></html>
    """)

@app.route("/dashboard")
def dashboard():
    prod_html = "".join([f"<li><b>{p['nom']}</b> - {p['prix']} - {p['description']}</li>" for p in products])
    return render_template_string(f"""
    <html><head><meta name="viewport" content="width=device-width, initial-scale=1">
    <style>body{{font-family:Arial;padding:20px;background:#f5f5f5}}
    input,textarea{{width:90%;padding:10px;margin:5px 0;border-radius:8px;border:1px solid #ccc}}
    button{{background:#0a1931;color:white;padding:12px 20px;border:none;border-radius:8px}}</style></head><body>
    <h2>Dashboard Olivier</h2>
    <h3>Produits actuels:</h3><ul>{prod_html}</ul>
    <h3>Ajouter produit:</h3>
    <form onsubmit="add(event)"><input id="nom" placeholder="Nom ex: Crème Lèvre Rose" required><br>
    <input id="prix" placeholder="Prix ex: 3000F" required><br>
    <textarea id="desc" placeholder="Description"></textarea><br>
    <button type="submit">Ajouter</button></form>
    <p><a href="/">Accueil</a> | <a href="/chat">Voir le chat</a></p>
    <script>
    async function add(e){{e.preventDefault();
      let p={{nom:document.getElementById('nom').value,prix:document.getElementById('prix').value,description:document.getElementById('desc').value}};
      await fetch('/api/products',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify(p)}});
      alert('Produit ajoute !'); location.reload();
    }}
    </script></body></html>
    """)

@app.route("/api/chat", methods=["POST"])
def api_chat():
    msg = request.json.get("message","").lower()
    for p in products:
        if p['nom'].lower() in msg or "levre" in msg or "rose" in msg or "creme" in msg or "savon" in msg:
            return jsonify({"reply": f"Oui j'ai <b>{p['nom']}</b> 😍<br>Prix: <b>{p['prix']}</b><br>{p['description']}<br><br>Tu veux commander ? Envoie ton quartier et numero WhatsApp, je livre a Ouaga aujourd'hui !"})
    if "prix" in msg or "combien" in msg:
        liste = "<br>".join([f"- {p['nom']}: {p['prix']}" for p in products])
        return jsonify({"reply": f"Voici mes prix :<br>{liste}<br><br>Quel produit tu veux ?"})
    if "bonjour" in msg or "salut" in msg:
        return jsonify({"reply": "Salut ! C'est YAAM IA. Je vends des crèmes pour belles lèvres. Tu cherches quoi ?"})
    return jsonify({"reply": f"Je vends : {', '.join([p['nom'] for p in products])}. Dis quel produit t'interesse et je te donne prix + livraison."})

@app.route("/api/products", methods=["POST"])
def api_add_product():
    global products
    data = request.json
    new_id = max([p['id'] for p in products], default=0) + 1
    products.append({"id": new_id, "nom": data['nom'], "prix": data['prix'], "description": data.get('description',''), "stock": "Dispo"})
    save_products(products)
    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
