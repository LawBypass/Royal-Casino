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

# ----- La réserve (la mise globale choisie dans le menu) -----
# Pour l'instant on met 10000 pour tester. Plus tard, elle viendra du menu.
reserve = 10000


# ----- Les fonctions -----
def dessiner_rouleau(x, symbole, couleur):
    """Dessine un rouleau (une case blanche avec un symbole) à la position x."""
    canvas.create_rectangle(x - 54, 215, x + 54, 405, fill="white", outline=OR, width=4)
    canvas.create_text(x, 310, text=symbole, font=(POLICE, 76, "bold"), fill=couleur)


def tirer():
    """Le code décide de la mise (10 % de la réserve, minimum 1) et la prélève."""
    global reserve

    if reserve <= 0:
        print("Réserve vide : impossible de tirer le levier.")
        return

    mise = max(1, reserve // 10)     # montant misé à ce tirage, choisi par le code
    reserve = reserve - mise         # on le retranche de la réserve
    canvas.itemconfig(texte_reserve, text="Solde monnaie : " + str(reserve))
    print("Le levier est tiré ! Mise :", mise)


def retour():
    fenetre.destroy()


# ----- La fenêtre et la zone de dessin -----
fenetre = tk.Tk()
fenetre.title("Royal Casino - Machine à sous")
fenetre.geometry("1152x648")

canvas = tk.Canvas(fenetre, width=LARGEUR, height=HAUTEUR, bg=FOND, highlightthickness=0)
canvas.pack()

# ----- Le cadre autour de la fenêtre (doré puis rouge) -----
canvas.create_rectangle(10, 10, LARGEUR - 10, HAUTEUR - 10, outline=OR, width=4)
canvas.create_rectangle(20, 20, LARGEUR - 20, HAUTEUR - 20, outline=ROUGE, width=2)

# ----- La barre du haut : bouton retour à gauche, solde monnaie à droite -----
bouton_retour = tk.Button(fenetre, text="< Menu", font=(POLICE, 11), command=retour)
canvas.create_window(80, 45, window=bouton_retour)

canvas.create_rectangle(905, 30, 1105, 62, fill="black", outline=OR, width=2)
texte_reserve = canvas.create_text(1005, 46, text="Solde monnaie : " + str(reserve),
                                   font=(POLICE, 12, "bold"), fill="white")

# ----- Le titre et le jackpot -----
canvas.create_text(576, 75, text="MACHINE À SOUS", font=(POLICE, 34, "bold"), fill=OR)
canvas.create_text(576, 125, text="JACKPOT : 5000", font=(POLICE, 14, "bold"), fill=CLAIR)

# ===== PARTIE GAUCHE : la machine =====
# Le corps de la machine (rectangle doré, puis rectangle noir dedans)
canvas.create_rectangle(90, 170, 570, 450, fill=OR, outline=ROUGE, width=4)
canvas.create_rectangle(108, 188, 552, 432, fill="black", outline="black", width=2)

# Les lumières : une boucle qui alterne rouge et doré clair
for i in range(19):
    x = 105 + i * 25
    if i % 2 == 0:
        couleur_lumiere = ROUGE
    else:
        couleur_lumiere = CLAIR
    canvas.create_oval(x - 6, 173, x + 6, 185, fill=couleur_lumiere, outline="black")
    canvas.create_oval(x - 6, 435, x + 6, 447, fill=couleur_lumiere, outline="black")

# Les 3 rouleaux (on appelle 3 fois la fonction)
dessiner_rouleau(200, "7", ROUGE)
dessiner_rouleau(330, "★", "black")
dessiner_rouleau(460, "♦", ROUGE)

# Les triangles (la ligne de gain)
canvas.create_polygon(112, 298, 112, 322, 130, 310, fill=ROUGE)
canvas.create_polygon(548, 298, 548, 322, 530, 310, fill=ROUGE)

# Le levier (à droite de la machine)
canvas.create_line(600, 360, 600, 255, fill="gray70", width=10)
canvas.create_oval(583, 225, 617, 259, fill=ROUGE, outline="white", width=3)

# ----- Une ligne de séparation entre la machine et les commandes -----
canvas.create_line(680, 170, 680, 450, fill=OR, width=1)

# ===== PARTIE DROITE : les commandes =====
# Le message de résultat
canvas.create_text(900, 235, text="Tentez votre chance !", font=(POLICE, 24, "bold"), fill=OR)

# Le gros bouton pour tirer le levier (texte noir sur fond doré = bien lisible)
bouton_tirer = tk.Button(fenetre, text="TIRER LE LEVIER", font=(POLICE, 18, "bold"),
                         bg=OR, fg="black", width=18, command=tirer)
canvas.create_window(900, 340, window=bouton_tirer)

# ----- Les pictos de casino sous le bouton -----
canvas.create_text(810, 415, text="♠", font=(POLICE, 36), fill="white")
canvas.create_text(870, 415, text="♥", font=(POLICE, 36), fill=ROUGE)
canvas.create_text(930, 415, text="♦", font=(POLICE, 36), fill=ROUGE)
canvas.create_text(990, 415, text="♣", font=(POLICE, 36), fill="white")

# Une petite ligne de décoration (comme sur le menu) avec une étoile et des 7
canvas.create_line(760, 470, 840, 470, fill=ROUGE, width=2)
canvas.create_text(900, 470, text="  ★  ", font=(POLICE, 18, "bold"), fill=OR)
canvas.create_line(960, 470, 1040, 470, fill=ROUGE, width=2)

# ----- On lance la fenêtre -----
fenetre.mainloop()