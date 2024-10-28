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

        # Dictionnaire de corrections orthographiques courantes
        self.spelling_corrections = {
            # Salutations et état
            "bojour": "bonjour",
            "salu": "salut",
            "couco": "coucou",
            "sava": "ça va",
            "cv": "ça va",
            "sa va": "ça va",
            # Questions communes
            "ki": "qui",
            "koi": "quoi",
            "keske": "qu'est-ce que",
            "pk": "pourquoi",
            "pourkoi": "pourquoi",
            "kestion": "question",
            # Verbes courants
            "é": "est",
            "ai": "est",
            "ètes": "êtes",
            "etes": "êtes",
            "fet": "fait",
            "fé": "fait",
            # Articles et pronoms
            "ke": "que",
            "sa": "ça",
            "ca": "ça",
            "ta": "tu as",
            "tas": "tu as",
            # Autres mots fréquents
            "vréman": "vraiment",
            "vreman": "vraiment",
            "kom": "comme",
            "kelke": "quelque",
            "kelk": "quelque",
        }

        # Base de connaissances sous forme de dictionnaire
        self.knowledge_base = {
            # Catégorie des salutations
            "salutations": {
                "patterns": [
                    r"b[ao][nj]jour.*", r"salu[t]?.*", r"h[ea]ll?o.*", r"c[ao]uc[ao]u.*", r"h[ea]y.*"
                ],
                "responses": [
                    "Bonjour! Comment puis-je vous aider?",
                    "Salut! Que puis-je faire pour vous?",
                    "Hello! Comment allez-vous?"
                ]
            },
            "etat": {
                "patterns": [
                    r"[cs][av]\s*va.*",
                    r"cv.*",
                    r"comment\s*va.*",
                    r"(tu\s*va|vas)[s]?\s*bien.*",
                    r"[çc]a\s*se\s*passe.*",
                    r"comment\s*tu\s*te?\s*sens.*"
                ],
                "responses": [
                    "Je vais très bien, merci ! Et vous ?",
                    "Tout va bien de mon côté, j'espère que vous aussi !",
                    "Parfaitement bien, merci de demander ! Comment allez-vous ?",
                    "Je suis en pleine forme ! Et votre journée se passe bien ?",
                    "Super bien ! C'est gentil de demander. Et vous ?"
                ]
            },
            "identite": {
                "patterns": [
                    r"(ki|qui)\s*(es[- ]tu|tu\s*es).*",
                    r"([ct]|k)ommen[t]?\s*([tc]u)?\s*(t[''])?apell?es?.*",
                    r"[kq]uelle?\s*es[t]?\s*ton\s*nom.*"
                ],
                "responses": [
                    lambda self=self: f"Je suis {self.name}, un assistant conversationnel!",
                    lambda self=self: f"Je m'appelle {self.name}, je suis là pour discuter avec vous.",
                    "Je suis un chatbot créé pour vous aider."
                ]
            },
            "calcul": {
                "patterns": [
                    r"calcule (?P<expression>[\d\s\+\-\*\/\(\)]+)",
                    r"[kc]ombien\s*(f[ea][it]|fon[t]?) (?P<expression>[\d\s\+\-\*\/\(\)]+)"
                ],
                "responses": [
                    lambda expr: f"Le résultat est {eval(expr)}"
                ]
            },
            "meteo": {
                "patterns": [
                    r"[kq]el?\s*[tc]emps?\s*f[ea][it][-\s]?[it]l.*",
                    r"m[ée]t[ée]o.*",
                    r"[iv]l?\s*pl[eû][t].*"
                ],
                "responses": [
                    "Je ne peux pas vraiment voir dehors, mais je vous conseille de regarder par la fenêtre! 😊",
                    "Il fait beau quelque part dans le monde! 🌞",
                ]
            },
            "blague": {
                "patterns": [
                    r"ra[ck]ont[e].*bla[gh]ue.*",
                    r"f[eé]([ts])?.*rire.*",
                    r"[kc]on[ea][it]s.*bla[gh]ue.*"
                ],
                "responses": [
                    "Pourquoi les plongeurs plongent-ils toujours en arrière ? Parce que sinon ils tombent dans le bateau ! 😄",
                    "Que fait une fraise sur un cheval ? Tagada Tagada ! 🍓",
                    "Quel fruit est assez fort pour casser des noix ? Le casse-noix ! 🥜",
                    "Qu'est-ce qu'un chat qui tombe amoureux ? Un chamoureux !",
                    "Pourquoi les poissons détestent l'ordinateur ? À cause de la souris.",
                    "Quel est le comble pour un électricien ? De ne pas être au courant !",
                    "Que dit une imprimante dans une dispute ? J'en ai marre de tes papiers !",
                    "Pourquoi les mathématiciens détestent-ils les soirées ? Parce qu'ils n'aiment pas les inconnues."
                ]
            }
        }

        self.conversation_history = []
        self.sentiment_history = []
        self.positive_words = set(['merci', 'super', 'génial', 'genial', 'excellent', 'excelent',
                                   'bien', 'cool', 'manifik', 'magnifique', 'parfait', 'parfé'])
        self.negative_words = set(['nul', 'mauvai', 'mauvais', 'terrible', 'terible', 'mal',
                                   'pas', 'pourit', 'pourri', 'naze'])

    def correct_spelling(self, text):
        """
        Corrige les fautes d'orthographe courantes dans le texte
        """
        words = text.lower().split()
        corrected_words = []

        for word in words:
            if word in self.spelling_corrections:
                corrected_words.append(self.spelling_corrections[word])
            else:
                corrected_word = word
                if corrected_word.endswith('er') and len(corrected_word) > 2:
                    corrected_word = corrected_word.replace('er', 'é')

                common_doubles = [('m', 'mm'), ('n', 'nn'), ('l', 'll'), ('t', 'tt'), ('s', 'ss')]
                for single, double in common_doubles:
                    if single in corrected_word:
                        corrected_word = corrected_word.replace(single, double)

                corrected_words.append(corrected_word)

        return ' '.join(corrected_words)

    def clean_text(self, text):
        """
        Nettoie et normalise un texte
        """
        text = text.lower()
        text = self.correct_spelling(text)
        text = text.translate(str.maketrans("", "", string.punctuation))
        text = " ".join(text.split())
        return text

    def calculate_similarity(self, text1, text2):
        """
        Calcule la similarité entre deux textes (coefficient de Jaccard)
        """
        words1 = set(self.clean_text(text1).split())
        words2 = set(self.clean_text(text2).split())
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        return len(intersection) / len(union) if union else 0

    def find_match(self, user_input):
        """
        Trouve la meilleure réponse pour l'entrée utilisateur
        """
        corrected_input = self.clean_text(user_input)
        best_match = None
        best_score = 0

        for intent, data in self.knowledge_base.items():
            for pattern in data["patterns"]:
                match = re.match(pattern, corrected_input)
                if match:
                    response = random.choice(data["responses"])
                    if callable(response):
                        if intent == "calcul":
                            try:
                                expression = match.group("expression").strip()
                                return response(expression)
                            except:
                                return "Désolé, je n'ai pas pu effectuer ce calcul."
                        return response(self)
                    return response

        for intent, data in self.knowledge_base.items():
            for pattern in data["patterns"]:
                clean_pattern = re.sub(r'[\.\*\[\]\(\)\?\+]', '', pattern)
                similarity = self.calculate_similarity(corrected_input, clean_pattern)
                if similarity > best_score and similarity > 0.2:
                    best_score = similarity
                    response = random.choice(data["responses"])
                    best_match = response(self) if callable(response) else response

        if best_match:
            return best_match

        return random.choice([
            "Je ne suis pas sûr de comprendre. Pouvez-vous reformuler?",
            "Désolé, je n'ai pas compris. Pouvez-vous essayer autrement?",
            "Je ne sais pas comment répondre à cela. Pouvez-vous être plus précis?"
        ])

    def save_to_history(self, user_input, bot_response):
        """
        Sauvegarde une interaction dans l'historique avec horodatage et analyse du sentiment
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
        Analyse le sentiment d'un texte
        """
        words = text.lower().split()
        positive_count = sum(1 for word in words if word in self.positive_words)
        negative_count = sum(1 for word in words if word in self.negative_words)

        if positive_count > negative_count:
            return "positif"
        elif negative_count > positive_count:
            return "négatif"
        return "neutre"

    def get_response(self, user_input):
        """
        Point d'entrée principal pour obtenir une réponse du chatbot
        """
        if not user_input.strip():
            return "Je vous écoute..."

        response = self.find_match(user_input)
        self.save_to_history(user_input, response)
        return response

    def get_sentiment_stats(self):
        """
        Calcule les statistiques des sentiments des conversations
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
        """
        serializable_kb = {}
        for intent, data in self.knowledge_base.items():
            serializable_kb[intent] = {
                "patterns": data["patterns"],
                "responses": [r.__name__ if callable(r) else r for r in data["responses"]]
            }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(serializable_kb, f, ensure_ascii=False, indent=2)

    def load_knowledge_base(self, filename="knowledge_base.json"):
        """
        Charge la base de connaissances depuis un fichier JSON
        """
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for intent, content in data.items():
            self.knowledge_base[intent] = {
                "patterns": content["patterns"],
                "responses": content["responses"]
            }