import tkinter as tk
from math import *
from random import choice
from time import sleep

# ==========================================
# 1. INITIALISATION DU SOLDE & DONNÉES DU JEU
# ==========================================

gains = 2000  # Solde initial

# Dictionnaire d'abondance de ton script
abondance = {
    "7": 3,
    "coin": 6,
    "gem": 6,
    "star": 4,
    "key": 6,
    "cherry": 9,
    "grape": 10,
    "diamond": 4
}

# Ta liste pondérée exacte de symboles
symboles = (
    ["7"] * 3 +
    ["coin"] * 5 +
    ["gem"] * 6 +
    ["star"] * 4 +
    ["key"] * 6 +
    ["cherry"] * 9 +
    ["grape"] * 10 +
    ["diamond"] * 4
)

# Correspondance entre le nom du symbole et ton fichier image .png
fichiers_images = {
    "7": "7.png",
    "coin": "coin.png",
    "gem": "gem.png",
    "star": "star.png",
    "key": "key.png",
    "cherry": "cherry.png",
    "grape": "grape.png",
    "diamond": "diamond.png"
}

# Liste pour conserver la référence des PhotoImage en mémoire
images_courantes = []


# ==========================================
# 2. LOGIQUE DU JEU INTÉGRÉE (FONCTION JOUER)
# ==========================================

def lancer_jeu():
    global gains, images_courantes

    # --- PARTIE A : VERIFICATION DE LA MISE ---
    try:
        mise = int(entree_mise.get())
        if mise > gains:
            label_message.config(text=f"Vous n'avez pas assez de monnaie ! (max {gains})", fg="#ff4d4d")
            return
        elif mise <= 0:
            label_message.config(text="La mise doit être supérieure à 0 !", fg="#ff4d4d")
            return
        else:
            gains -= mise
            label_solde.config(text=f"Solde actuel : {gains} unités")
            label_message.config(text="Bouton activé ! Le jeu commence...", fg="#d4af37")
            bouton_jouer.config(state="disabled")
    except ValueError:
        label_message.config(text="Oups ! Veuillez entrer un nombre valide (pas de lettres).", fg="#ff4d4d")
        return

    # --- PARTIE C : TIRAGE DES ROULEAUX ---
    r1 = choice(symboles)
    r2 = choice(symboles)
    r3 = choice(symboles)
    tirage = [r1, r2, r3]

    images_courantes = []

    # Simulation progressive de l'affichage (effet sleep)
    def afficher_étape(index):
        if index < 3:
            symb = tirage[index]
            img_brute = tk.PhotoImage(file=fichiers_images[symb])
            img = img_brute.subsample(2)
            images_courantes.append(img)
            
            if index == 0:
                label_1.config(image=img)
            elif index == 1:
                label_2.config(image=img)
            elif index == 2:
                label_3.config(image=img)
                
            window.after(600, afficher_étape, index + 1)
        else:
            # Traitement des résultats après le dernier rouleau
            calculer_gains(r1, r2, r3, mise)

    afficher_étape(0)


# --- PARTIE D : VÉRIFICATIONS ET GAINS ---
def calculer_gains(rouleau_1, rouleau_2, rouleau_3, mise):
    global gains

    if rouleau_1 == rouleau_2 == rouleau_3:
        if rouleau_1 == "7":
            txt = "Bravo : c'est le JACKPOT : vous gagnez 3 fois votre mise en plus de la récupérer !!!!!"
            nb_abondance = abondance["7"]
            gains = gains + mise + (1 / nb_abondance) * mise * 3
        else:
            txt = "Bravo vous avez gagné le gros lot : 3 éléments identiques"
            nb_abondance = abondance[rouleau_1]
            gains = gains + mise + (1 / nb_abondance) * mise * 3
            
        gains = round(gains)
        msg_final = f"{txt}\nVoici vos nouveaux gains : {gains} unités de monnaie."
        color = "#00ff00"

    elif rouleau_1 == rouleau_2 or rouleau_2 == rouleau_3 or rouleau_1 == rouleau_3:
        if rouleau_1 == rouleau_2 or rouleau_1 == rouleau_3:
            symbole_double = rouleau_1
        else:
            symbole_double = rouleau_2

        nb_abondance = abondance[symbole_double]

        if symbole_double in ["7", "diamond", "coin"]:
            gains = gains + mise + (1 / nb_abondance) * mise * 2
            gains = round(gains)
            msg_final = f"Bravo vous avez gagné : 2 éléments identiques !\nBonus spécial : tu récupères ta mise en plus du gain !, Voici tes nouveaux gains : {gains}"
        else:
            gains = gains + (1 / nb_abondance) * mise * 2
            gains = round(gains)
            msg_final = f"Bravo vous avez gagné : 2 éléments identiques !\nVoici vos gains : {gains} unités de monnaie."
            
        color = "#00ff00"

    else:
        msg_final = f"VOUS AVEZ PERDU ! RETENTEZ VOTRE CHANCE !\nVos gains actuels sont : {gains}"
        color = "#d4af37"

    # Mise à jour des affichages
    label_solde.config(text=f"Solde actuel : {gains} unités")
    label_message.config(text=msg_final, fg=color)

    if gains <= 0:
        label_message.config(text="Vous n'avez plus aucun gain, vous avez perdu !", fg="#ff0000")
        bouton_jouer.config(state="disabled")
    else:
        bouton_jouer.config(state="normal")


# ==========================================
# 3. TA FENÊTRE ET TES ÉLÉMENTS GRAPHIQUES
# ==========================================

# 1. Initialisation de la fenetre : titre, taille, couleur de fond.
window = tk.Tk()
window.title("Casino - Machine à sous")
window.geometry("900x700")
window.configure(bg="#1b4d3e")

# 2. Titre principal
titre = tk.Label(
    window,
    text="MACHINE A SOUS",
    font=("Georgia", 36, "italic", "bold"),
    fg="#d4af37",
    bg="#1b4d3e"
)
titre.pack(pady=30, padx=0)

# Affichage du solde du joueur
label_solde = tk.Label(
    window,
    text=f"Solde actuel : {gains} unités",
    font=("Georgia", 16, "bold"),
    fg="white",
    bg="#1b4d3e"
)
label_solde.pack(pady=5)

# 3. Phrase d'ambiance en bas
phrase_ambiance = tk.Label(
    window, 
    text="Faites vos jeux, rien ne va plus !", 
    font=("Palatino Linotype", 16, "italic"), 
    fg="#d4af37", 
    bg="#1b4d3e"
)
phrase_ambiance.pack(side="bottom", pady=20, padx=0)

# 4. Rouleaux
cadre_general = tk.Frame(window, bg="#1b4d3e")
cadre_general.pack(pady=20)

# --- Rouleau 1 ---
rouleau_1 = tk.Frame(cadre_general, bd=4, bg="white", width=110, height=140)
rouleau_1.pack(side="left", padx=10)
rouleau_1.pack_propagate(False)

img_file_1 = choice(list(fichiers_images.values()))
img_brute_1 = tk.PhotoImage(file=img_file_1)
img_1 = img_brute_1.subsample(2)
label_1 = tk.Label(rouleau_1, image=img_1, bg="white")
label_1.pack(expand=True)

# --- Rouleau 2 ---
rouleau_2 = tk.Frame(cadre_general, bd=4, bg="white", width=110, height=140)
rouleau_2.pack(side="left", padx=10)
rouleau_2.pack_propagate(False)

img_file_2 = choice(list(fichiers_images.values()))
img_brute_2 = tk.PhotoImage(file=img_file_2)
img_2 = img_brute_2.subsample(2)
label_2 = tk.Label(rouleau_2, image=img_2, bg="white")
label_2.pack(expand=True)

# --- Rouleau 3 ---
rouleau_3 = tk.Frame(cadre_general, bd=4, bg="white", width=110, height=140)
rouleau_3.pack(side="left", padx=10)
rouleau_3.pack_propagate(False)

img_file_3 = choice(list(fichiers_images.values()))
img_brute_3 = tk.PhotoImage(file=img_file_3)
img_3 = img_brute_3.subsample(2)
label_3 = tk.Label(rouleau_3, image=img_3, bg="white")
label_3.pack(expand=True)

images_courantes = [img_1, img_2, img_3]

# 5. Zone de saisie de la mise & bouton de lancement
cadre_action = tk.Frame(window, bg="#1b4d3e")
cadre_action.pack(pady=10)

lbl_mise_txt = tk.Label(cadre_action, text="Mise :", font=("Georgia", 14, "bold"), fg="white", bg="#1b4d3e")
lbl_mise_txt.pack(side="left", padx=5)

entree_mise = tk.Entry(cadre_action, font=("Georgia", 14), width=8, justify="center")
entree_mise.insert(0, "100")
entree_mise.pack(side="left", padx=10)

bouton_jouer = tk.Button(cadre_action, text="JOUER", font=("Georgia", 12, "bold"), bg="#d4af37", fg="black", command=lancer_jeu, padx=10)
bouton_jouer.pack(side="left", padx=10)

# Zone d'information et messages de résultats
label_message = tk.Label(window, text="Choisissez votre mise puis cliquez sur JOUER", font=("Georgia", 12, "italic"), fg="#d4af37", bg="#1b4d3e")
label_message.pack(pady=10)

# À la fin de ta fonction calculer_gains, si le joueur n'a plus de crédits :
if gains <= 0:
    label_message.config(text="Vous n'avez plus aucun gain, partie terminée !", fg="#ff0000")
    bouton_jouer.config(state="disabled")
        
        # On peut afficher un bouton pour quitter ou recommencer à zéro
bouton_quitter = tk.Button(cadre_action, text="QUITTER", font=("Georgia", 12, "bold"), bg="#ff4d4d", fg="black", command=window.destroy)
bouton_quitter.pack(side="left", padx=10)

window.update()
window.mainloop()