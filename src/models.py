class Customer:
    """
    Représente un client avec ses achats.
    """
    def __init__(self, name: str):
        self.name = name
        self.purchases = []

    def add_purchase(self, item: str, price: float):
        """Ajoute un achat à la liste des achats du client."""
        self.purchases.append((item, price))

    def get_total_spent(self) -> float:
        """Retourne le total dépensé par le client."""
        return sum(price for _, price in self.purchases)


class Level:
    """
    Configuration des niveaux de difficulté.
    """
    LEVELS = {
        "facile": {"min": 1, "max": 10, "questions": 5},
        "intermediaire": {"min": 10, "max": 50, "questions": 7},
        "difficile": {"min": 50, "max": 100, "questions": 10}
    }

    def __init__(self, difficulty: str):
        if difficulty not in self.LEVELS:
            raise ValueError("Niveau inconnu. Choisissez entre 'facile', 'intermediaire' et 'difficile'.")
        self.difficulty = difficulty
        self.config = self.LEVELS[difficulty]

    def get_config(self):
        """Retourne les paramètres du niveau."""
        return self.config

    def get_time_limit(self) -> int:
        """Retourne la limite de temps en secondes pour répondre aux questions."""
        if self.difficulty == "facile":
            return 10
        else:
            return 5


class Game:
    """
    État global de la partie en cours.
    """
    def __init__(self, level: Level):
        self.level = level
        self.score = 0
        self.history = []

    def update_score(self, points: int):
        """Met à jour le score de la partie."""
        self.score += points

    def add_to_history(self, question: str, answer: str, correct: bool):
        """Ajoute une entrée à l'historique des réponses du joueur."""
        self.history.append({"question": question, "answer": answer, "correct": correct})

    def get_score(self) -> int:
        """Retourne le score actuel."""
        return self.score

    def get_history(self):
        """Retourne l'historique des réponses."""
        return self.history