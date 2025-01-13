import random
import re
from datetime import datetime
import string
from collections import Counter


class LocalChatbot:
    def __init__(self):
        self.name = "PortfolioBot"
        self.first_message = True
        self.conversation_active = False

        # Dictionnaire des corrections orthographiques
        self.spelling_corrections = {
            "salu": "salut",
            "bonjour": "Bonjour",
            "projek": "projet",
            "realisation": "réalisation",
            "portefeuil": "portfolio",
            "montré": "montrez",
            "avé": "avez",
            "fé": "fait",
            "aplikation": "application",
            "o'foot": "O'Foot",
            "ofliks": "Oflix",
            "tournoit": "tournoi",
            "film": "film",
            "seri": "série",
            "interaktif": "interactif",
            "expériance": "expérience",
            "parcour": "parcours",
            "travail": "travail",
            "professionnel": "professionnelle",
            "entreprise": "entreprise",
            "travaillé": "travaillé",
            "formassion": "formation",
            "etude": "études",
            "diplôme": "diplômes",
            "école": "école",
            "université": "université",
            "curse": "cursus",
            "développeur": "développeur",
            "deveop": "devops",
            "manifik": "magnifique",
            "genial": "génial",
            "excelent": "excellent",
            "terible": "terrible",
            "pourit": "pourri",
            "Quel est mon age": "quel est mon âge"
        }

        # Détails des projets
        self.project_details = {
            "ofoot": "O'Foot est une application web développée en PHP/Symfony permettant la gestion complète de tournois de football. Elle inclut la création d'équipes, la gestion des matchs, le suivi des scores et un tableau des classements en temps réel.\n\n\n",
            "oflix": "Oflix est une plateforme de streaming développée en PHP/Symfony, permettant de gérer et visualiser un catalogue de films et séries. Elle comprend un système de notation, des critiques utilisateurs et des recommandations personnalisées.\n\n\n",
            "portfolio": "Un portfolio interactif présentant mes projets et compétences, avec un chatbot intégré permettant une navigation intuitive et une présentation dynamique de mon travail.\n\n\n"
        }

        # Base de connaissances
        self.knowledge_base = {
            "greetings": {
                "patterns": [
                    r"^salut$",
                    r"^bonjour$"
                ],
                "responses": [
                    "Salut ! Je suis ravi de vous rencontrer. Je suis Mohammad-Qassem, développeur web fullstack et Data Scientist. Souhaitez-vous discuter de mon parcours, de mes compétences, de mes expériences ou de mes projets ?"
                ]
            },

            "expertise": {
                "patterns": [
                    r"compétences?.*",
                    r"connaissances?.*",
                    r"capacités?.*",
                    r"que sais[-\s]tu faire.*",
                    r"quelles? sont? tes? compétences?.*",
                    r"quelles? technologies?.*",
                    r"stack.*technique.*",
                    r"savoir[-\s]faire.*"
                ],
                "responses": [
                    "Voici mes compétences techniques :Compétences :\n👨‍💻 Langages : HTML5, CSS3, PHP 8, JavaScript, Python, MySQL\n\n🛠 Frameworks : Symfony, Laravel, Django, Flask, Bootstrap, Tailwind CSS, Pandas, Seaborn, Numpy\n\n🔧 Outils : Git, VS Code, Jetbrains, MySQL\n\n🌐 Méthodologies : Agile/Scrum, Architecture MVC, API REST\n\n🛠 DevOps : Docker, Hidora, Heroku"
                ]
            },

            "projets": {
                "patterns": [
                    r"projet.*",
                    r"réalisation.*",
                    r"portfolio.*",
                    r"montr[ez]?\s*[- ]?moi.*",
                    r"qu['']av[ez]?\s*[- ]?vous\s*fait.*",
                    r"application.*"
                ],
                "responses": [
                    "J'ai 2 projets principaux :\n\n1. O'Foot - Gestion de tournois\n2. Oflix - Streaming de films\n\nSur lequel souhaitez-vous en savoir plus ?"

                ]
            },
            "projet_details": {
                "patterns": [
                    r".*o'?foot.*",
                    r".*oflix.*",
                    r".*tournoi.*foot.*",
                    r".*film.*série.*",
                    r".*portfolio.*interactif.*"
                ],
                "responses": [
                    lambda x: self.get_project_details(x)
                ]
            },

            "experience": {
                "patterns": [
                    r"expériences?.*",
                    r"travail.*",
                    r"professionnelle?.*",
                    r"entreprise.*",
                    r"où\s*([aà]|avez)[-\s]vous\s*travaillé.*"
                ],
                "responses": [
                    "Mon parcours professionnel inclut :\n\n1. Développeur Web Fullstack (Juin-Juillet 2024) chez O'Clock - O'Foot\n\n2. Stage (Décembre 2022) chez EpetitPas - Page Formateur"
                ]
            },

            "formation": {
                "patterns": [
                    r"formation.*",
                    r"études.*",
                    r"diplômes?.*",
                    r"école.*",
                    r"université.*",
                    r"cursus.*",
                    r"parcours.*",
                    r"parcours.*formation.*",
                    r"parcours.*académique.*",
                    r"parcours.*scolaire.*",
                    r"formation.*suivie.*",
                    r"où.*étudié.*",
                    r"quelle.*formation.*"
                ],
                "responses": [
                    "Je dispose de 3 formations :\n\n1. Titre Pro Développeur Web (O'Clock, 2024)\n2. Formation Dev Web Remise à Niveau (Assofac, 2022)\n3. BAC STMG (Lycée A. Nobel, 2021)"
                ]
            },
            # [Other existing patterns remain the same]

            # Séparation des expertises en deux catégories distinctes
            "dev_web": {
                "patterns": [
                    r"développeur\s*web",
                    r"développement\s*web",
                    r"web\s*developer"
                ],
                "responses": [
                    "En tant que développeur web, je maîtrise les technologies suivantes :\n\n\n- PHP/Symfony\n\n\n- JavaScript\n\n\n- HTML/CSS\n\n\n- MySQL\n\n\n- Bootstrap\n\n\n- Je peux concevoir et développer des applications web complètes, du backend au frontend."
                ]
            },

            "devops": {
                "patterns": [
                    r"data",
                    r"dataScience",
                    r"data science",
                    r"machine learning",
                    r"algorithmes",
                    r"visualisation de données",
                    r"traitement des données"
                ],
                "responses": [
                    "En Data Science, je travaille principalement avec :\n\n- Pandas pour la manipulation et l'analyse de données\n\n- Numpy pour les calculs mathématiques et le traitement de tableaux\n\n- Seaborn pour la visualisation de données statistiques\n\nCes outils sont essentiels pour l'exploration, l'analyse et la visualisation des données dans mes projets."
                ]
            }
        }

        # Historique et analyse des sentiments
        self.conversation_history = []
        self.sentiment_history = []
        self.positive_words = set(['merci', 'super', 'génial', 'genial', 'excellent', 'excelent',
                                   'bien', 'cool', 'manifik', 'magnifique', 'parfait', 'parfé'])
        self.negative_words = set(['nul', 'mauvai', 'mauvais', 'terrible', 'terible', 'mal',
                                   'pas', 'pourit', 'pourri', 'naze'])

    def get_welcome_message(self):
        """Retourne le message de bienvenue initial formaté en JSON"""
        welcome_message = {
            "message": ("Bonjour ! Je suis Mohammad-Qassem, développeur web fullstack.\n\n\n"
                        "Je peux vous parler de :\n\n\n"
                        "1. Mes projets (O'Foot, Oflix)\n\n\n"
                        "2. Mon parcours\n\n\n"
                        "3. Mes compétences\n\n\n"
                        "N'hésitez pas à me dire 'Bonjour' ou 'Salut' pour commencer !")
        }
        return welcome_message

    def get_response(self, user_input):
        """Traite l'entrée utilisateur et retourne une réponse appropriée"""
        # Suppression de la vérification du premier message
        if not user_input.strip():
            return "Que souhaitez-vous savoir sur mon parcours ?"

        # Questions spécifiques
        user_input = user_input.lower()
        if user_input.startswith("quel est votre âge"):
            return "J'ai 22 ans."
        elif user_input.startswith("comment tu t'appelles"):
            return "Je m'appelle Mohammad-Qassem."

        # Traitement normal des messages
        response = self.find_match(user_input)
        self.save_to_history(user_input, response)
        return response

    def get_project_details(self, text):
        """Retourne les détails d'un projet spécifique"""
        text = text.lower()
        if "o'foot" in text or "ofoot" in text or "tournoi" in text:
            return self.project_details["ofoot"]
        elif "oflix" in text or "film" in text or "série" in text:
            return self.project_details["oflix"]
        elif "portfolio" in text:
            return self.project_details["portfolio"]
        return "Pouvez-vous préciser quel projet vous intéresse ? O'Foot, Oflix ou le Portfolio ?\n\n\n"

    def correct_spelling(self, text):
        """Corrige l'orthographe du texte"""
        words = text.lower().split()
        return ' '.join(self.spelling_corrections.get(word, word) for word in words)

    def clean_text(self, text):
        """Nettoie et normalise le texte"""
        text = text.lower()
        text = self.correct_spelling(text)
        text = text.translate(str.maketrans("", "", string.punctuation))
        return " ".join(text.split())

    def calculate_similarity(self, text1, text2):
        """Calcule la similarité entre deux textes"""
        words1 = set(self.clean_text(text1).split())
        words2 = set(self.clean_text(text2).split())
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        return len(intersection) / len(union) if union else 0

    def find_match(self, user_input):
        """Trouve la meilleure réponse correspondant à l'entrée utilisateur"""
        corrected_input = self.clean_text(user_input)

        # Recherche de correspondance exacte
        for intent, data in self.knowledge_base.items():
            for pattern in data["patterns"]:
                if re.search(pattern, corrected_input, re.IGNORECASE):
                    response = random.choice(data["responses"])
                    return response(user_input) if callable(response) else response

        # Recherche par similarité
        best_match = None
        best_score = 0.2  # Seuil minimum de similarité

        for intent, data in self.knowledge_base.items():
            for pattern in data["patterns"]:
                clean_pattern = re.sub(r'[\.\*\[\]\(\)\?\+]', '', pattern)
                similarity = self.calculate_similarity(corrected_input, clean_pattern)
                if similarity > best_score:
                    best_score = similarity
                    response = random.choice(data["responses"])
                    best_match = response(user_input) if callable(response) else response

        if best_match:
            return best_match

        # Réponse par défaut
        return random.choice([
            "Je peux vous parler de mes projets, compétences ou expériences.\n\n\nQue souhaitez-vous savoir ?",
            "Je ne suis pas sûr de comprendre.\n\n\nVoulez-vous en savoir plus sur mon parcours, mes projets ou mes compétences ?",
            "Pour mieux vous aider, dites-moi si vous voulez connaître mes réalisations, mon expertise technique ou mon expérience."
        ])

    def save_to_history(self, user_input, bot_response):
        """Sauvegarde l'historique de la conversation et le sentiment"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sentiment = self.analyze_sentiment(user_input)

        self.conversation_history.append({
            "timestamp": timestamp,
            "user": user_input,
            "bot": bot_response,
            "sentiment": sentiment
        })
        self.sentiment_history.append(sentiment)

    def analyze_sentiment(self, text):
        """Analyse le sentiment du message utilisateur"""
        words = text.lower().split()
        positive_count = sum(1 for word in words if word in self.positive_words)
        negative_count = sum(1 for word in words if word in self.negative_words)

        if positive_count > negative_count:
            return "positif"
        elif negative_count > positive_count:
            return "négatif"
        return "neutre"