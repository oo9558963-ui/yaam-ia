from flask import Flask, request, jsonify

app = Flask(__name__)

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
.status{margin-top:20px;background:#00ff88;color:#000;padding:8px 20px;border-radius:20px;font-weight:bold;display:inline-block}
</style>
</head>
<body>
<h1>YAAM <span>IA</span></h1>
<p class="slogan">L'Intelligence Artificielle par l'Afrique, pour l'Afrique</p>
<div class="card">
<p>🌍 Bienvenue sur la plateforme officielle de YAAM IA</p>
<p>Développé par Olivier à Ouagadougou</p>
<a class="btn" href="#">🚀 Entrer dans YAAM IA</a>
<a class="btn" style="background:white;" href="#">💬 Parler à YAAM</a>
</div>
<div class="status">● EN LIGNE - yaam-ia.onrender.com</div>
<p style="margin-top:30px;opacity:.6;">Version 1.0 - Octobre 2026</p>
<p><a href="/privacy" style="color:#ffcc00;">Privacy</a> | <a href="/terms" style="color:#ffcc00;">Terms</a></p>
</body>
</html>
"""

@app.route('/privacy')
def privacy():
    return "<h1>Politique de confidentialite - YAAM IA</h1><p>YAAM respecte votre vie privee. Donnees utilisees uniquement pour repondre automatiquement.</p><p>Contact: contact@yaam-ia.com</p>"

@app.route('/terms')
def terms():
    return "<h1>Conditions d'utilisation - YAAM IA</h1><p>Service pour votre business de maniere responsable.</p><p>Contact: contact@yaam-ia.com</p>"

@app.route('/data-deletion')
def data_deletion():
    return "<h1>Suppression des donnees - YAAM IA</h1><p>Pour supprimer vos donnees, envoyez email a contact@yaam-ia.com avec votre numero.</p>"

@app.route('/webhook', methods=['GET'])
def verify_webhook():
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    if mode == 'subscribe' and token == 'yaam_verify_token_123':
        return challenge, 200
    else:
        return 'Verification failed', 403

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print(data)
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run()
