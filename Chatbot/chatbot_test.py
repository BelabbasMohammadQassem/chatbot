class SimpleChatbot:
    def __init__(self):
        self.responses = {
            "salut": "Bonjour! Comment puis-je vous aider?",
            "bonjour": "Salut! Comment allez-vous?",
            "ça va": "Je vais bien, merci! Et vous?",
            "au revoir": "Au revoir! Passez une bonne journée!",
            "qui es-tu": "Je suis un chatbot simple créé pour des tests.",
            "help": "Je peux répondre à des salutations simples et quelques questions basiques.",
            "": "Je ne comprends pas. Pouvez-vous reformuler?"
        }

    def get_response(self, message):
        message = message.lower().strip()

        # Cherche la meilleure correspondance
        for key in self.responses:
            if key in message:
                return self.responses[key]

        return "Je ne suis pas sûr de comprendre. Pouvez-vous reformuler ou essayer autre chose?"


def main():
    chatbot = SimpleChatbot()
    print("Chatbot: Bonjour! Je suis un chatbot simple. Tapez 'quit' pour quitter.")

    while True:
        user_input = input("Vous: ")

        if user_input.lower() == 'quit':
            print("Chatbot: Au revoir!")
            break

        response = chatbot.get_response(user_input)
        print(f"Chatbot: {response}")


if __name__ == "__main__":
    main()