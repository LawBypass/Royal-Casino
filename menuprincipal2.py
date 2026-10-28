import tkinter as tk

# ----- La taille de la fenêtre (format 16/9, pour un écran de taille moyenne) -----
LARGEUR = 1152
HAUTEUR = 648

# ----- Les couleurs et la police (les mêmes dans tous les fichiers) -----
FOND = "#14171f"      # noir anthracite
OR = "#d4af37"        # doré
CLAIR = "#f5d77a"     # doré clair
ROUGE = "#c8102e"     # rouge vif
POLICE = "DM Sans"    # il faut installer la police DM Sans sur l'ordinateur

# ----- L'argent du joueur -----
monnaie = 10000       # la monnaie totale au départ
reserve = 0           # la mise globale (l'argent engagé dans la partie)


# ----- Les fonctions -----
def mettre_a_jour():
    """Met à jour les textes de la monnaie et de la mise globale."""
    canvas.itemconfig(texte_monnaie, text="Monnaie : " + str(monnaie))
    canvas.itemconfig(texte_reserve, text="Mise globale : " + str(reserve))


def message(texte, couleur=CLAIR):
    """Affiche un petit message d'information sous les boutons."""
    canvas.itemconfig(texte_message, text=texte, fill=couleur)


def valider_mise():
    """Le joueur valide sa mise globale : on la retranche de la monnaie totale."""
    global monnaie, reserve

    if reserve > 0:
        message("Tu as déjà une mise globale en cours !", ROUGE)
        return

    try:
        mise = int(champ_mise.get())
    except ValueError:
        message("Entre un nombre entier, par exemple 500.", ROUGE)
        return

    if mise <= 0:
        message("La mise doit être supérieure à 0.", ROUGE)
    elif mise > monnaie:
        message("Tu n'as pas assez de monnaie !", ROUGE)
    else:
        monnaie = monnaie - mise      # on retranche la mise de la monnaie totale
        reserve = mise                # cet argent est maintenant engagé
        champ_mise.delete(0, tk.END)
        mettre_a_jour()
        message("Mise validée ! Choisissez votre jeu")


def rendre_reserve():
    """À appeler quand on ferme un jeu : ce qui reste de la mise retourne dans la monnaie."""
    global monnaie, reserve
    monnaie = monnaie + reserve
    reserve = 0
    mettre_a_jour()


def mise_faite():
    """Vérifie que le joueur a bien validé une mise globale avant de jouer."""
    if reserve <= 0:
        message("Validez d'abord votre mise globale !", ROUGE)
        return False
    return True


def roulette():
    if mise_faite():
        print("Roulette : bientôt !")


def machine():
    if mise_faite():
        print("Machine à sous : bientôt !")


def blackjack():
    if mise_faite():
        print("Blackjack : bientôt !")


def quitter():
    fenetre.destroy()


def creer_bouton(x, texte, commande):
    """Crée un bouton doré (texte noir bien lisible) à la position x."""
    bouton = tk.Button(fenetre, text=texte, font=(POLICE, 16, "bold"),
                       bg=OR, fg="black", width=14, command=commande)
    canvas.create_window(x, 522, window=bouton)


# ----- La fenêtre et la zone de dessin -----
fenetre = tk.Tk()
fenetre.title("Royal Casino")
fenetre.geometry("1152x648")
canvas = tk.Canvas(fenetre, width=LARGEUR, height=HAUTEUR, bg=FOND, highlightthickness=0)
canvas.pack()

# ----- Le cadre autour de la fenêtre (doré puis rouge) -----
canvas.create_rectangle(10, 10, LARGEUR - 10, HAUTEUR - 10, outline=OR, width=4)
canvas.create_rectangle(20, 20, LARGEUR - 20, HAUTEUR - 20, outline=ROUGE, width=2)

# ----- Les lumières en haut et en bas (une boucle) -----
for i in range(41):
    x = 76 + i * 25
    if i % 2 == 0:
        couleur_lumiere = ROUGE
    else:
        couleur_lumiere = CLAIR
    canvas.create_oval(x - 6, 39, x + 6, 51, fill=couleur_lumiere, outline="black")
    canvas.create_oval(x - 6, 597, x + 6, 609, fill=couleur_lumiere, outline="black")

# ----- La case Monnaie (en haut à droite) -----
canvas.create_rectangle(900, 62, 1110, 96, fill="black", outline=OR, width=2)
texte_monnaie = canvas.create_text(1005, 79, text="", font=(POLICE, 13, "bold"), fill="white")
texte_reserve = canvas.create_text(1005, 115, text="", font=(POLICE, 11, "italic"), fill=CLAIR)

# ----- La couronne et le titre -----
canvas.create_text(576, 115, text="♛", font=(POLICE, 54), fill=OR)
canvas.create_text(576, 190, text="ROYAL CASINO", font=(POLICE, 52, "bold"), fill=OR)

# ----- La ligne de décoration et le sous-titre -----
canvas.create_line(376, 240, 556, 240, fill=ROUGE, width=2)
canvas.create_text(576, 240, text="♦", font=(POLICE, 16), fill=ROUGE)
canvas.create_line(596, 240, 776, 240, fill=ROUGE, width=2)
canvas.create_text(576, 275, text="Bienvenue !",
                   font=(POLICE, 15, "italic"), fill=CLAIR)
canvas.create_text(576, 295, text="Que la chance soit avec vous !",
                   font=(POLICE, 15, "italic"), fill=CLAIR)

# ----- Les symboles de cartes -----
canvas.create_text(496, 345, text="♠", font=(POLICE, 36), fill="white")
canvas.create_text(549, 345, text="♥", font=(POLICE, 36), fill=ROUGE)
canvas.create_text(603, 345, text="♦", font=(POLICE, 36), fill=ROUGE)
canvas.create_text(656, 345, text="♣", font=(POLICE, 36), fill="white")

# ----- La mise globale : un texte, une case à remplir et un bouton -----
canvas.create_text(430, 442, text="Mise globale :", font=(POLICE, 14, "bold"), fill=OR)

champ_mise = tk.Entry(fenetre, font=(POLICE, 14), width=8, justify="center")
canvas.create_window(570, 442, window=champ_mise)

bouton_valider = tk.Button(fenetre, text="VALIDER", font=(POLICE, 12, "bold"),
                           bg=OR, fg="black", command=valider_mise)
canvas.create_window(690, 442, window=bouton_valider)

# ----- Les boutons (côte à côte) -----
creer_bouton(216, "ROULETTE", roulette)
creer_bouton(456, "MACHINE À SOUS", machine)
creer_bouton(696, "BLACKJACK", blackjack)
creer_bouton(936, "QUITTER", quitter)

# ----- Le message d'information (au-dessus de la mise globale) -----
texte_message = canvas.create_text(576, 402, text="Entrez votre mise globale pour commencer",
                                   font=(POLICE, 13), fill=CLAIR)

# ----- On affiche la monnaie de départ, puis on lance la fenêtre -----
mettre_a_jour()
fenetre.mainloop()
