import tkinter as tk
import math   # pour placer les numéros en cercle (cos et sin)

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


# ----- Les fonctions (pour l'instant, juste des messages) -----
def pari_numero(n):
    print("Tu paries sur le numéro", n)


def pari_rouge():
    print("Tu paries sur ROUGE")


def pari_noir():
    print("Tu paries sur NOIR")


def pari_pair():
    print("Tu paries sur PAIR")


def pari_impair():
    print("Tu paries sur IMPAIR")


def lancer():
    """Le code décide de la mise (10 % de la réserve, minimum 1) et la prélève."""
    global reserve

    if reserve <= 0:
        print("Réserve vide : impossible de lancer la roue.")
        return

    mise = max(1, reserve // 10)     # montant misé à ce lancer, choisi par le code
    reserve = reserve - mise         # on le retranche de la réserve
    canvas.itemconfig(texte_reserve, text="Solde monnaie : " + str(reserve))
    print("La roue va tourner ! Mise :", mise)


def retour():
    fenetre.destroy()


def creer_bouton_pari(x, texte, commande):
    """Crée un bouton de pari doré (texte noir bien lisible) à la position x."""
    bouton = tk.Button(fenetre, text=texte, font=(POLICE, 12, "bold"),
                       bg=OR, fg="black", width=7, command=commande)
    canvas.create_window(x, 335, window=bouton)


# ----- La fenêtre et la zone de dessin -----
fenetre = tk.Tk()
fenetre.title("Royal Casino - Roulette")
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

# ----- Le titre -----
canvas.create_text(576, 75, text="ROULETTE", font=(POLICE, 34, "bold"), fill=OR)

# ===== PARTIE GAUCHE : la roue =====
# On dessine 12 parts de 30 degrés, une rouge, une noire, une rouge...
for i in range(12):
    if i % 2 == 0:
        couleur = ROUGE
    else:
        couleur = "black"
    canvas.create_arc(130, 150, 470, 490, start=i * 30, extent=30,
                      fill=couleur, outline=OR)

    # On place le numéro au milieu de la part
    angle = math.radians(i * 30 + 15)       # milieu de la part, en radians
    x = 300 + 120 * math.cos(angle)         # 300 = centre de la roue, 120 = distance du centre
    y = 320 - 120 * math.sin(angle)         # 320 = centre de la roue
    canvas.create_text(x, y, text=str(i + 1), font=(POLICE, 16, "bold"), fill="white")

# Le centre de la roue
canvas.create_oval(250, 270, 350, 370, fill="black", outline=OR, width=3)
canvas.create_text(300, 320, text="♠", font=(POLICE, 38), fill=OR)

# Le petit triangle en haut (il montre le numéro gagnant)
canvas.create_polygon(286, 138, 314, 138, 300, 166, fill=CLAIR, outline="black")

# ----- Une ligne de séparation entre la roue et les paris -----
canvas.create_line(590, 150, 590, 590, fill=OR, width=1)

# ===== PARTIE DROITE : les paris =====
# ----- Les mises sur un numéro de 1 à 12 (2 lignes de 6 boutons) -----
canvas.create_text(850, 165, text="Pariez sur un numéro",
                   font=(POLICE, 13), fill=CLAIR)

for n in range(1, 13):
    colonne = (n - 1) % 6          # 0, 1, 2, 3, 4, 5
    if n <= 6:
        y = 215                    # première ligne
    else:
        y = 265                    # deuxième ligne
    x = 685 + colonne * 66
    # "lambda n=n" permet de donner le bon numéro à la fonction pari_numero
    bouton_numero = tk.Button(fenetre, text=str(n), font=(POLICE, 13, "bold"),
                              bg=OR, fg="black", width=3,
                              command=lambda n=n: pari_numero(n))
    canvas.create_window(x, y, window=bouton_numero)

# ----- Les autres paris -----
creer_bouton_pari(705, "ROUGE", pari_rouge)
creer_bouton_pari(805, "NOIR", pari_noir)
creer_bouton_pari(905, "PAIR", pari_pair)
creer_bouton_pari(1005, "IMPAIR", pari_impair)

# ----- Le gros bouton pour lancer la roue -----
bouton_lancer = tk.Button(fenetre, text="LANCER LA ROUE", font=(POLICE, 18, "bold"),
                          bg=OR, fg="black", width=18, command=lancer)
canvas.create_window(850, 440, window=bouton_lancer)

# ----- On lance la fenêtre -----
fenetre.mainloop()