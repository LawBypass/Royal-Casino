# argent.py : l'argent du joueur, commun à tous les jeux du casino.
# Chaque jeu est un programme séparé, donc l'argent est gardé dans un petit fichier texte (argent.txt).

import os  # os sert à trouver le dossier où se trouve ce fichier

DEPART = 3000  # l'argent avec lequel le joueur commence une session de casino
FICHIER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "argent.txt")  # fichier qui garde l'argent


def lire():
    """Renvoie l'argent du joueur (DEPART si le fichier n'existe pas encore)."""  # description de la fonction
    try:  # on essaie de lire le fichier
        with open(FICHIER) as fichier:  # ouvre le fichier en lecture
            return int(fichier.read().strip())  # transforme le texte du fichier en nombre
    except (OSError, ValueError):  # fichier absent ou texte invalide
        return DEPART  # on repart de l'argent de départ


def ecrire(valeur):
    """Enregistre l'argent du joueur pour que les autres jeux le retrouvent."""  # description de la fonction
    with open(FICHIER, "w") as fichier:  # ouvre le fichier en écriture (efface l'ancien contenu)
        fichier.write(str(int(round(valeur))))  # écrit l'argent sous forme d'un nombre entier
