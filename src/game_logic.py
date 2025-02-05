from src.models import Customer, Level, Game
from src.data_handler import charger_produits, charger_questions
import logging
import random
import time

# Configuration du logging
logging.basicConfig(filename="transactions.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class GameLogic:
    def __init__(self, level: Level, produits, questions):
        self.level = level
        self.produits = produits
        self.questions = questions

        self.customer = Customer("Client")
        self.game = Game(level)
    
    def generate_question(self):
        """Sélectionne une question aléatoire."""
        if "questions" not in self.questions or not self.questions["questions"]:
            raise ValueError("Aucune question disponible.")
        return random.choice(self.questions["questions"])

    def process_transaction(self, product_name: str, quantity: int):
        """Ajoute un produit au panier du client et enregistre la transaction."""
        product = next((p for p in self.produits if p[1] == product_name), None)
        if not product:
            raise ValueError("Produit non disponible.")
        price = float(product[2])
        total_cost = price * quantity
        self.customer.add_purchase(product_name, total_cost)
        logging.info(f"Achat enregistré : {quantity}x {product_name} pour {total_cost:.2f} DH")
    
    

    def ask_question(self, user_input=None):
        """Pose une question et vérifie la réponse en permettant des correspondances partielles."""
        question = self.generate_question()
        
        if user_input is None:
            print(question["question"])
            start_time = time.time()
            time_limit = self.level.get_time_limit()
            user_input = input("Votre réponse : ")
            elapsed_time = time.time() - start_time
            if elapsed_time > time_limit:
                print("Temps écoulé !")
                correct = False
            else:
                user_words = set(user_input.strip().lower().split())
                answer_words = set(str(question["answer"]).strip().lower().split())
                correct = any(word in answer_words for word in user_words)
        else:
            user_words = set(user_input.strip().lower().split())
            answer_words = set(str(question["answer"]).strip().lower().split())
            correct = any(word in answer_words for word in user_words)

        if correct:
            print("Bonne réponse !")
            self.game.update_score(10)
        else:
            print(f"Mauvaise réponse. La bonne réponse était : {question['answer']}")

        logging.info(f"Question posée : {question['question']} | Réponse : {user_input} | Score : {self.game.get_score()}")
        return correct

    def save_conversation(self, message: str):
        """Enregistre les interactions du joueur."""
        with open("conversations.txt", "a", encoding="utf-8") as file:
            file.write(message + "\n")
    
    def start_game(self):
        """Démarre une session de jeu."""
        print(f"Bienvenue dans le jeu de calcul mental - Niveau : {self.level.difficulty}")

        for _ in range(self.level.get_config()["questions"]):  # Nombre de questions par session
            self.ask_question()

        print(f"Fin du jeu ! Score final : {self.game.get_score()}")
        logging.info(f"Jeu terminé. Score final : {self.game.get_score()}")