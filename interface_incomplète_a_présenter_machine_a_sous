import tkinter as tk # En le remplacant par tk On importe le module tkinter en appelant ses fonctions
import random
#1. Initialisation de la fenetre : titre, taille couleur de fond.
window = tk.Tk() # ouvre une fenêtre
window.title("Casino - Machine à sous") # donne un titre à cette fenêtre
window.geometry("900x700") # donne les dimensions de la fenetre : largeur * hauteur.
window.configure(bg = "#1b4d3e") # background couleur vert bouteille.


# 2. Titre principal
titre = tk.Label( #un titre utilisé par les fonction de tkinter.
    window, #dans la fenetre
    text="MACHINE A SOUS", # texte du titre
    font=("Georgia", 36, "italic", "bold"), #police, taille style
    fg="#d4af37",      # Couleur du texte (Doré mat)
    bg="#1b4d3e"       # Couleur de fond (même vert que la fenêtre)
)
titre.pack(pady=30, padx=0) # alignement

# 3. Phrase d'ambiance en bas
phrase_ambiance = tk.Label(
    window, 
    text="Faites vos jeux, rien ne va plus !", 
    font=("Palatino Linotype", 16, "italic"), 
    fg="#d4af37",      # Doré
    bg="#1b4d3e"       # Même vert feutré
)
# side="bottom" colle le texte en bas, pady=20 laisse une petite marge
phrase_ambiance.pack(side="bottom", pady=20, padx=0)

#4. rouleaux : FAIRE LES COMMENTAIRES !!!!!!!!!!


liste_images = ["cherry.png", "7.png", "diamond.png", "star.png", "key.png", "coin.png", "grape.png", "gem.png"]

cadre_general = tk.Frame(window, bg="#1b4d3e")
cadre_general.pack(pady=30)

rouleau_1 = tk.Frame(cadre_general, bd=4, bg="white", width=110, height=140)
rouleau_1.pack(side="left", padx=10)
rouleau_1.pack_propagate(False)

img_file_1 = random.choice(liste_images)
img_brute_1 = tk.PhotoImage(file=img_file_1)
img_1 = img_brute_1.subsample(2)
label_1 = tk.Label(rouleau_1, image=img_1, bg="white")
label_1.pack(expand=True)

rouleau_2 = tk.Frame(cadre_general, bd=4, bg="white", width=110, height=140)
rouleau_2.pack(side="left", padx=10)
rouleau_2.pack_propagate(False)

img_file_2 = random.choice(liste_images)
img_brute_2 = tk.PhotoImage(file=img_file_2)
img_2 = img_brute_2.subsample(2)
label_2 = tk.Label(rouleau_2, image=img_2, bg="white")
label_2.pack(expand=True)

rouleau_3 = tk.Frame(cadre_general, bd=4, bg="white", width=110, height=140)
rouleau_3.pack(side="left", padx=10)
rouleau_3.pack_propagate(False)

img_file_3 = random.choice(liste_images)
img_brute_3 = tk.PhotoImage(file=img_file_3)
img_3 = img_brute_3.subsample(2)
label_3 = tk.Label(rouleau_3, image=img_3, bg="white")
label_3.pack(expand=True)





