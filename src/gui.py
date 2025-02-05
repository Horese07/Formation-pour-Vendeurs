import tkinter as tk
from tkinter import messagebox
from src.models import Level
from src.game_logic import GameLogic
from src.data_handler import charger_produits, charger_questions

class GameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Jeu de Calcul Mental")
        
        self.level_var = tk.StringVar(value="facile")
        self.question_label = tk.Label(root, text="Bienvenue dans le jeu de calcul mental !")
        self.question_label.pack()

        # Sélection du niveau
        self.level_frame = tk.Frame(root)
        self.level_frame.pack()
        tk.Label(self.level_frame, text="Choisissez un niveau:").pack(side=tk.LEFT)
        tk.Radiobutton(self.level_frame, text="Facile", variable=self.level_var, value="facile").pack(side=tk.LEFT)
        tk.Radiobutton(self.level_frame, text="Intermédiaire", variable=self.level_var, value="intermediaire").pack(side=tk.LEFT)
        tk.Radiobutton(self.level_frame, text="Difficile", variable=self.level_var, value="difficile").pack(side=tk.LEFT)

        # Zone de réponse
        self.response_label = tk.StringVar(value="Ici la réponse sera affichée")
        self.response_display = tk.Label(root, textvariable=self.response_label)
        self.response_display.pack()

        self.answer_entry = tk.Entry(root)
        self.answer_entry.pack()

        # Bouton pour démarrer le jeu
        self.start_button = tk.Button(root, text="Démarrer le jeu", command=self.start_game)
        self.start_button.pack()

        # Bouton pour soumettre la réponse
        self.submit_button = tk.Button(root, text="Soumettre", command=self.check_answer)
        self.submit_button.pack()

        self.timer_label = tk.Label(root, text="Temps restant : 10")
        self.timer_label.pack()

        self.game_logic = None
        self.current_question = None
        self.time_remaining = 10
        self.timer_running = False

    def start_game(self):
        """Initialise le jeu et charge les questions."""
        niveau = self.level_var.get()
        produits = charger_produits("data/products.csv")
        questions = charger_questions("data/questions.json")
        
        if not questions["questions"]:
            messagebox.showerror("Erreur", "Aucune question disponible.")
            return
        
        level = Level(niveau)
        self.game_logic = GameLogic(level, produits, questions)
        self.ask_question()

    def ask_question(self):
        """Affiche la prochaine question."""
        self.current_question = self.game_logic.generate_question()
        self.question_label.config(text=self.current_question["question"])
        self.response_label.set("Ici la réponse sera affichée")
        self.answer_entry.delete(0, tk.END)
        self.time_remaining = 10 if self.level_var.get() == "facile" else 5
        self.update_timer()

    def update_timer(self):
        """Met à jour le chronomètre."""
        if self.time_remaining > 0:
            self.timer_label.config(text=f"Temps restant : {self.time_remaining}")
            self.time_remaining -= 1
            self.root.after(1000, self.update_timer)
        else:
            self.timer_label.config(text="Temps écoulé !")
            self.response_label.set(f"Temps écoulé ! La bonne réponse était : {self.current_question['answer']}")
            self.root.after(2000, self.ask_question)

    def check_answer(self):
        """Vérifie la réponse et met à jour l'affichage."""
        user_input = self.answer_entry.get().strip().lower()
        correct_answer = str(self.current_question["answer"]).strip().lower()

        # Vérifier si la réponse contient "oui"
        if "oui" in user_input:
            correct = True
        else:
            # Vérifier si la réponse contient au moins un mot correct
            user_words = set(user_input.split())
            answer_words = set(correct_answer.split())
            correct = any(word in answer_words for word in user_words)

            # Vérifier si la réponse est un nombre équivalent
            if not correct:
                try:
                    user_number = float(user_input)
                    correct_number = float(correct_answer)
                    correct = user_number == correct_number
                except ValueError:
                    pass

        if correct:
            self.response_label.set("Bonne réponse !")
            self.game_logic.game.update_score(10)
        else:
            self.response_label.set(f"Mauvaise réponse. La bonne réponse était : {self.current_question['answer']}")

        self.root.after(2000, self.ask_question)  # Attendre 2 secondes avant de poser la question suivante
        self.answer_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = GameApp(root)
    root.mainloop()
