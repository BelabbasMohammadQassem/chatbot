import random
import re
from datetime import datetime
import json
import string
from collections import Counter


class LocalChatbot:
    def __init__(self):
        self.name = "PortfolioBot"

        self.spelling_corrections = {
            # [Le dictionnaire de corrections reste identique...]
        }

        # Ajout du dictionnaire pour les détails des projets
        self.project_details = {
            "ofoot": "O'Foot est une application web développée en PHP/Symfony permettant la gestion complète de tournois de football. Elle inclut la création d'équipes, la gestion des matchs, le suivi des scores et un tableau des classements en temps réel.\n\n\n",

            "oflix": "Oflix est une plateforme de streaming développée en PHP/Symfony, permettant de gérer et visualiser un catalogue de films et séries. Elle comprend un système de notation, des critiques utilisateurs et des recommandations personnalisées.\n\n\n",

            "portfolio": "Un portfolio interactif présentant mes projets et compétences, avec un chatbot intégré permettant une navigation intuitive et une présentation dynamique de mon travail.\n\n\n"
        }

        self.knowledge_base = {
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
                    "Voici mes projets principaux :\n\n\n1. O'Foot PHP/Symfony\n\n\n2. Oflix PHP/Symfony\n\n\nLequel vous intéresse ?\n\n\n",
                    "J'ai réalisé plusieurs projets marquants :\n\n\n- Gestion de tournoi de Foot\n\n\n- Répertoire de films et série\n\n\n- Un portfolio interactif\n\n\nSouhaitez-vous plus de détails sur l'un d'eux ?\n\n\n",
                    "Mes réalisations incluent :\n\n\n• Projets web\n\n\n• Applications mobiles\n\n\n• Solutions desktop\n\n\nSur quel type de projet souhaitez-vous en savoir plus ?\n\n\n"
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
                    self.get_project_details  # Plus de lambda, on référence directement la méthode
                ]
            },
            "experience": {
                "patterns": [
                    r"expériences?.*",
                    r"parcours.*",
                    r"travail.*",
                    r"professionnelle?.*",
                    r"entreprise.*",
                    r"où\s*([aà]|avez)[-\s]vous\s*travaillé.*"
                ],
                "responses": [
                    "Mon parcours professionnel inclut :\n\n\n• Juin-Juillet 2024 : Développeur Web Fullstack O'Clock\n\n\nProjet de fin de formation Téléprésentiel\n\n\n• Décembre 2022 : Développeur Web E-Petitpas\n\n\n",
                    "Mon expérience couvre plusieurs domaines :\n\n\n1. Développement d'applications web\n\n\n2. Gestion d'équipe technique\n\n\n3. DevOps\n\n\nQue souhaitez-vous approfondir ?\n\n\n"
                ]
            },
            "formation": {
                "patterns": [
                    r"formation.*",
                    r"études.*",
                    r"diplômes?.*",
                    r"école.*",
                    r"université.*",
                    r"cursus.*"
                ],
                "responses": [
                    "Mon parcours académique :\n\n\n• Titre Pro niveau 5 - Ecole O'Clock\n\n\n• Formation Développeur Web - Assofac\n\n\n• Bac STMG - Lycée Alfred Nobel\n\n\n",
                    "J'ai suivi un cursus complet en informatique :\n\n\n• Formations spécialisées\n\n\n• Certifications professionnelles\n\n\nSouhaitez-vous des détails particuliers ?\n\n\n"
                ]
            }
        }

        self.conversation_history = []
        self.sentiment_history = []
        self.positive_words = set(['merci', 'super', 'génial', 'genial', 'excellent', 'excelent',
                                   'bien', 'cool', 'manifik', 'magnifique', 'parfait', 'parfé'])
        self.negative_words = set(['nul', 'mauvai', 'mauvais', 'terrible', 'terible', 'mal',
                                   'pas', 'pourit', 'pourri', 'naze'])

    def get_project_details(self, text):
        text = text.lower()
        if "o'foot" in text or "ofoot" in text or "tournoi" in text:
            return self.project_details["ofoot"]
        elif "oflix" in text or "film" in text or "série" in text:
            return self.project_details["oflix"]
        elif "portfolio" in text:
            return self.project_details["portfolio"]
        return "Pouvez-vous préciser quel projet vous intéresse ? O'Foot, Oflix ou le Portfolio ?\n\n\n"

    def correct_spelling(self, text):
        words = text.lower().split()
        corrected_words = []
        for word in words:
            if word in self.spelling_corrections:
                corrected_words.append(self.spelling_corrections[word])
            else:
                corrected_words.append(word)
        return ' '.join(corrected_words)

    def clean_text(self, text):
        text = text.lower()
        text = self.correct_spelling(text)
        text = text.translate(str.maketrans("", "", string.punctuation))
        text = " ".join(text.split())
        return text

    def calculate_similarity(self, text1, text2):
        words1 = set(self.clean_text(text1).split())
        words2 = set(self.clean_text(text2).split())
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        return len(intersection) / len(union) if union else 0

    def find_match(self, user_input):
        corrected_input = self.clean_text(user_input)
        best_match = None
        best_score = 0

        for intent, data in self.knowledge_base.items():
            for pattern in data["patterns"]:
                match = re.search(pattern, corrected_input, re.IGNORECASE)
                if match:
                    response = random.choice(data["responses"])
                    if callable(response):
                        return response(user_input)  # On passe l'input original à la fonction
                    return response

        for intent, data in self.knowledge_base.items():
            for pattern in data["patterns"]:
                clean_pattern = re.sub(r'[\.\*\[\]\(\)\?\+]', '', pattern)
                similarity = self.calculate_similarity(corrected_input, clean_pattern)
                if similarity > best_score and similarity > 0.2:
                    best_score = similarity
                    response = random.choice(data["responses"])
                    best_match = response(user_input) if callable(response) else response

        if best_match:
            return best_match

        return random.choice([
            "Je peux vous parler de mes projets, compétences ou expériences.\n\n\nQue souhaitez-vous savoir ?",
            "Je ne suis pas sûr de comprendre.\n\n\nVoulez-vous en savoir plus sur mon parcours, mes projets ou mes compétences ?",
            "Pour mieux vous aider, dites-moi si vous voulez connaître mes réalisations, mon expertise technique ou mon expérience."
        ])

    def get_response(self, user_input):
        if not user_input.strip():
            return "Je vous écoute !\n\n\nQue souhaitez-vous savoir sur mon parcours ?"

        response = self.find_match(user_input)
        self.save_to_history(user_input, response)
        return response

    def save_to_history(self, user_input, bot_response):
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
        words = text.lower().split()
        positive_count = sum(1 for word in words if word in self.positive_words)
        negative_count = sum(1 for word in words if word in self.negative_words)

        if positive_count > negative_count:
            return "positif"
        elif negative_count > positive_count:
            return "négatif"
        return "neutre"