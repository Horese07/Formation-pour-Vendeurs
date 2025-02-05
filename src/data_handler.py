import csv
import json
import os
import logging

# Configuration du logging
logging.basicConfig(filename="data_handler.log", level=logging.INFO, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

def charger_produits(fichier_produits):
    """Charge la liste des produits à partir d'un fichier CSV."""
    produits = []
    if not os.path.exists(fichier_produits):
        logging.warning("Fichier des produits non trouvé !")
        return []
    try:
        with open(fichier_produits, newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader, None)  # Ignorer l'en-tête
            for row in reader:
                if len(row) == 3:
                    produits.append(tuple(row))  # (type_produit, nom, prix)
    except Exception as e:
        logging.error(f"Erreur lors du chargement des produits: {e}")
    return produits

def sauvegarder_produits(fichier_produits, produits):
    """Sauvegarde la liste des produits dans un fichier CSV."""
    try:
        with open(fichier_produits, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Type", "Nom", "Prix"])
            writer.writerows(produits)
    except Exception as e:
        logging.error(f"Erreur lors de la sauvegarde des produits: {e}")

def charger_questions(fichier_questions):
    """Charge les questions à partir d'un fichier JSON."""
    if not os.path.exists(fichier_questions):
        logging.warning("Fichier des questions non trouvé !")
        return {"questions": []}
    try:
        with open(fichier_questions, encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        logging.error(f"Erreur de décodage JSON: {e}")
        return {"questions": []}

def sauvegarder_questions(fichier_questions, questions):
    """Sauvegarde les questions dans un fichier JSON."""
    try:
        with open(fichier_questions, 'w', encoding='utf-8') as file:
            json.dump(questions, file, indent=4, ensure_ascii=False)
    except Exception as e:
        logging.error(f"Erreur lors de la sauvegarde des questions: {e}")

def sauvegarder_score(fichier_scores, client_id, total, paiement, rendu, temps):
    """Ajoute une ligne au fichier des scores CSV."""
    file_exists = os.path.isfile(fichier_scores)

    try:
        with open(fichier_scores, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            if not file_exists:
                writer.writerow(["Client ID", "Total", "Paiement", "Rendu", "Temps (s)"])

            writer.writerow([client_id, total, paiement, rendu, f"{temps:.2f}"])
    except Exception as e:
        logging.error(f"Erreur lors de la sauvegarde du score: {e}")