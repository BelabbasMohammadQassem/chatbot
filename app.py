# Importation des modules nécessaires
from flask import Flask, render_template, request, jsonify  # Flask pour le serveur web, les templates, et les requêtes/réponses
from Chatbot.chatbot import LocalChatbot  # Import de notre classe de chatbot local

# Création de l'application Flask
app = Flask(__name__)

# Création d'une instance unique du chatbot qui sera partagée par toutes les sessions
# C'est une variable globale pour maintenir l'état du chatbot entre les requêtes
chatbot = LocalChatbot()

# Route principale qui affiche la page d'accueil
@app.route('/')  # Décorateur qui définit l'URL racine
def home():
    # Renvoie le template HTML qui contient l'interface utilisateur
    return render_template('index.html')

# Route pour gérer les messages envoyés par l'utilisateur
@app.route('/send_message', methods=['POST'])  # Ne répond qu'aux requêtes POST
def send_message():
    # Récupère le message de l'utilisateur depuis les données JSON de la requête
    # Si 'message' n'existe pas, retourne une chaîne vide
    user_message = request.json.get('message', '')

    try:
        # Demande une réponse au chatbot en fonction du message utilisateur
        bot_response = chatbot.get_response(user_message)

        # Renvoie la réponse au format JSON avec :
        # - le statut de la requête
        # - la réponse du bot
        # - le nom du bot
        return jsonify({
            'status': 'success',
            'response': bot_response,
            'botName': chatbot.name
        })

    except Exception as e:
        # En cas d'erreur, on log l'erreur et on renvoie un message d'erreur
        # Le code 500 indique une erreur serveur
        print(f"Erreur lors du traitement du message: {e}")
        return jsonify({
            'status': 'error',
            'message': "Désolé, une erreur s'est produite."
        }), 500

# Route pour récupérer l'historique des conversations
@app.route('/get_history', methods=['GET'])  # Ne répond qu'aux requêtes GET
def get_history():
    try:
        # Renvoie tout l'historique des conversations stocké dans le chatbot
        return jsonify({
            'status': 'success',
            'history': chatbot.conversation_history
        })
    except Exception as e:
        # En cas d'erreur, renvoie le message d'erreur
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# Point d'entrée du programme
if __name__ == '__main__':
    # Lance le serveur Flask en mode debug
    # Le mode debug permet le rechargement automatique du serveur quand le code change
    # et affiche les erreurs détaillées
    app.run(debug=True)