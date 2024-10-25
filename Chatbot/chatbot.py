import random
import re
from datetime import datetime
import json
import string
from collections import Counter


class LocalChatbot:
    def __init__(self):
        """
        Initialisation du chatbot avec ses attributs et sa base de connaissances
        """
        self.name = "ChatBot"

        # Base de connaissances sous forme de dictionnaire
        # Chaque catégorie contient des patterns (expressions régulières) et leurs réponses associées
        self.knowledge_base = {
            # Catégorie des salutations
            "salutations": {
                "patterns": [
                    r"bonjour.*", r"salut.*", r"hello.*", r"coucou.*", r"hey.*"
                ],
                "responses": [
                    "Bonjour! Comment puis-je vous aider?",
                    "Salut! Que puis-je faire pour vous?",
                    "Hello! Comment allez-vous?"
                ]
            },
            # Catégorie identité du bot
            "identite": {
                "patterns": [
                    r"qui es[- ]tu.*", r"tu es qui.*",
                    r"comment tu t'appelles.*", r"quel est ton nom.*"
                ],
                "responses": [
                    f"Je suis {self.name}, un assistant conversationnel!",
                    f"Je m'appelle {self.name}, je suis là pour discuter avec vous.",
                    "Je suis un chatbot créé pour vous aider."
                ]
            },
            # Catégorie calculs mathématiques
            # Utilise des groupes nommés (?P<name>...) pour capturer l'expression à calculer
            "calcul": {
                "patterns": [
                    r"calcule (?P<expression>[\d\s\+\-\*\/\(\)]+)",
                    r"combien fait (?P<expression>[\d\s\+\-\*\/\(\)]+)"
                ],
                "responses": [
                    lambda expr: f"Le résultat est {eval(expr)}"  # Fonction lambda pour évaluer l'expression
                ]
            },
            # Catégorie météo (réponses simples car pas d'API météo)
            "meteo": {
                "patterns": [
                    r"quel temps fait[- ]il.*",
                    r"météo.*",
                    r"il pleut.*"
                ],
                "responses": [
                    "Je ne peux pas vraiment voir dehors, mais je vous conseille de regarder par la fenêtre! 😊",
                    "Il fait beau quelque part dans le monde! 🌞",
                ]
            },
            # Catégorie blagues
            "blague": {
                "patterns": [
                    r"raconte.*blague.*",
                    r"fais.*rire.*",
                    r"connais.*blague.*"
                ],
                "responses": [
                    "Pourquoi les plongeurs plongent-ils toujours en arrière ? Parce que sinon ils tombent dans le bateau ! 😄",
                    "Que fait une fraise sur un cheval ? Tagada Tagada ! 🍓",
                    "Quel fruit est assez fort pour casser des noix ? Le casse-noix ! 🥜",
                    "Qu'est-ce qu'un chat qui tombe amoureux ? Un chamoureux !",
                    "Pourquoi les poissons détestent l'ordinateur ? À cause de la souris.",
                    "Quel est le comble pour un électricien ? De ne pas être au courant !",
                    "Que dit une imprimante dans une dispute ? J’en ai marre de tes papiers !",
                    "Pourquoi les mathématiciens détestent-ils les soirées ? Parce qu’ils n’aiment pas les inconnues."
                ]
            }
        }

        # Liste pour stocker l'historique des conversations
        self.conversation_history = []
        # Liste pour stocker l'historique des sentiments
        self.sentiment_history = []

        # Ensembles de mots pour l'analyse des sentiments
        self.positive_words = set(['merci', 'super', 'génial', 'excellent', 'bien', 'cool'])
        self.negative_words = set(['nul', 'mauvais', 'terrible', 'mal', 'pas'])

    def save_to_history(self, user_input, bot_response):
        """
        Sauvegarde une interaction dans l'historique avec horodatage et analyse du sentiment
        Args:
            user_input (str): Message de l'utilisateur
            bot_response (str): Réponse du bot
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sentiment = self.analyze_sentiment(user_input)

        conversation_entry = {
            "timestamp": timestamp,
            "user": user_input,
            "bot": bot_response,
            "sentiment": sentiment
        }

        self.conversation_history.append(conversation_entry)
        self.sentiment_history.append(sentiment)

    def analyze_sentiment(self, text):
        """
        Analyse le sentiment d'un texte en comptant les mots positifs et négatifs
        Args:
            text (str): Texte à analyser
        Returns:
            str: 'positif', 'négatif' ou 'neutre'
        """
        words = text.lower().split()
        positive_count = sum(1 for word in words if word in self.positive_words)
        negative_count = sum(1 for word in words if word in self.negative_words)

        if positive_count > negative_count:
            return "positif"
        elif negative_count > positive_count:
            return "négatif"
        return "neutre"

    def clean_text(self, text):
        """
        Nettoie et normalise un texte
        Args:
            text (str): Texte à nettoyer
        Returns:
            str: Texte nettoyé
        """
        text = text.lower()  # Mise en minuscules
        text = text.translate(str.maketrans("", "", string.punctuation))  # Suppression ponctuation
        text = " ".join(text.split())  # Normalisation des espaces
        return text

    def calculate_similarity(self, text1, text2):
        """
        Calcule la similarité entre deux textes (coefficient de Jaccard)
        Args:
            text1, text2 (str): Textes à comparer
        Returns:
            float: Score de similarité entre 0 et 1
        """
        words1 = set(self.clean_text(text1).split())
        words2 = set(self.clean_text(text2).split())
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        return len(intersection) / len(union) if union else 0

    def find_match(self, user_input):
        """
        Trouve la meilleure réponse pour l'entrée utilisateur
        Args:
            user_input (str): Message de l'utilisateur
        Returns:
            str: Réponse du bot
        """
        user_input = user_input.lower()
        best_match = None
        best_score = 0

        # Première passe : recherche de correspondances exactes avec les patterns
        for intent, data in self.knowledge_base.items():
            for pattern in data["patterns"]:
                match = re.match(pattern, user_input)
                if match:
                    response = random.choice(data["responses"])
                    if callable(response):
                        # Cas spécial pour les calculs
                        if intent == "calcul":
                            try:
                                expression = match.group("expression").strip()
                                return response(expression)
                            except:
                                return "Désolé, je n'ai pas pu effectuer ce calcul."
                        return response()
                    return response

        # Deuxième passe : recherche de correspondances approximatives
        for intent, data in self.knowledge_base.items():
            for pattern in data["patterns"]:
                # Nettoyage du pattern pour la comparaison
                clean_pattern = re.sub(r'[\.\*\[\]\(\)\?\+]', '', pattern)
                similarity = self.calculate_similarity(user_input, clean_pattern)
                if similarity > best_score and similarity > 0.3:  # Seuil minimal de similarité
                    best_score = similarity
                    response = random.choice(data["responses"])
                    best_match = response() if callable(response) else response

        if best_match:
            return best_match

        # Réponse par défaut si aucune correspondance n'est trouvée
        return random.choice([
            "Je ne suis pas sûr de comprendre. Pouvez-vous reformuler?",
            "Désolé, je n'ai pas compris. Pouvez-vous essayer autrement?",
            "Je ne sais pas comment répondre à cela. Pouvez-vous être plus précis?"
        ])

    def get_response(self, user_input):
        """
        Point d'entrée principal pour obtenir une réponse du chatbot
        Args:
            user_input (str): Message de l'utilisateur
        Returns:
            str: Réponse du bot
        """
        if not user_input.strip():
            return "Je vous écoute..."

        response = self.find_match(user_input)
        self.save_to_history(user_input, response)
        return response

    def get_sentiment_stats(self):
        """
        Calcule les statistiques des sentiments des conversations
        Returns:
            dict: Pourcentages des différents sentiments
        """
        total = len(self.sentiment_history)
        if not total:
            return "Pas encore d'historique de sentiment."

        sentiment_counts = Counter(self.sentiment_history)
        stats = {
            "positif": (sentiment_counts["positif"] / total) * 100,
            "négatif": (sentiment_counts["négatif"] / total) * 100,
            "neutre": (sentiment_counts["neutre"] / total) * 100
        }
        return stats

    def save_knowledge_base(self, filename="knowledge_base.json"):
        """
        Sauvegarde la base de connaissances dans un fichier JSON
        Args:
            filename (str): Nom du fichier de sauvegarde
        """
        serializable_kb = {}
        for intent, data in self.knowledge_base.items():
            serializable_kb[intent] = {
                "patterns": [p.pattern for p in map(re.compile, data["patterns"])],
                "responses": [r.__name__ if callable(r) else r for r in data["responses"]]
            }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(serializable_kb, f, ensure_ascii=False, indent=2)

    def load_knowledge_base(self, filename="knowledge_base.json"):
        """
        Charge la base de connaissances depuis un fichier JSON
        Args:
            filename (str): Nom du fichier à charger
        """
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for intent, content in data.items():
            self.knowledge_base[intent] = {
                "patterns": content["patterns"],
                "responses": content["responses"]
            }