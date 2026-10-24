from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "YAAM IA est en ligne !"

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
    VERIFY_TOKEN = 'MON_TOKEN_SECRET_YAAM'
    if mode == 'subscribe' and token == VERIFY_TOKEN:
        return challenge, 200
    return "Forbidden", 403

@app.route('/webhook', methods=['POST'])
def receive_message():
    data = request.get_json()
    print("Nouveau message recu !")
    print(data)
    return jsonify({"status":"ok"}), 200

if __name__ == '__main__':
    app.run(port=5000)
