import tkinter as tk  # tkinter est la bibliothèque qui sert à créer la fenêtre et les boutons
import math  # math donne cos, sin et radians pour placer les numéros sur le cercle
import random  # random permet au code de choisir le numéro gagnant
import argent  # argent.py garde l'argent du joueur, commun à tous les jeux du casino

# ----- Taille de la fenêtre (format 16/9) -----
LARGEUR = 1152  # largeur de la fenêtre en pixels
HAUTEUR = 648  # hauteur de la fenêtre en pixels

# ----- Couleurs et police (les mêmes dans tous les fichiers du casino) -----
FOND = "#14171f"  # noir anthracite, utilisé comme fond
OR = "#d4af37"  # doré
CLAIR = "#f5d77a"  # doré clair
ROUGE = "#c8102e"  # rouge vif
VERT = "#2ecc71"  # vert vif, utilisé pour les messages de gain
TAPIS = "#0b6b3a"  # vert foncé du tapis de la table de casino
VERT_ZERO = "#0a8f4a"  # vert du zéro
POLICE = "DM Sans"  # la police DM Sans doit être installée (sinon tkinter en utilise une par défaut)

# ----- Les jetons : valeur -> (couleur du jeton, couleur du texte, couleur de l'anneau) -----
JETONS = {
    1: ("#f2f2f2", "#1b3a6b", "#1b5e9b"),  # jeton 1 : blanc avec un anneau bleu
    5: ("#2e9e4f", "white", "white"),  # jeton 5 : vert
    25: ("#d6303a", "white", "white"),  # jeton 25 : rouge
    100: ("#1a1a1a", "white", "white"),  # jeton 100 : noir
    500: ("#7b3fb0", "white", "white"),  # jeton 500 : violet
    1000: ("#e0b020", "#3a2a00", "white"),  # jeton 1k : doré
}
VALEURS_JETONS = [1, 5, 25, 100, 500, 1000]  # les jetons affichés en bas, de gauche à droite

# ----- Géométrie de la roue -----
CX = 230  # position x du centre de la roue
CY = 330  # position y du centre de la roue
RAYON = 150  # rayon de la roue en pixels
NB_PARTS = 37  # nombre de parts sur la roue (0 à 36)
ANGLE_PART = 360 / NB_PARTS  # angle d'une part en degrés

# ----- Ordre réel des numéros autour d'une roue de roulette européenne -----
ORDRE = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1,
         20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]  # la part i contient le numéro ORDRE[i]

# ----- Géométrie de la table (la table de mise verte) -----
TX = 440  # x du côté gauche de la table (la colonne du zéro)
ZW = 50  # largeur de la colonne du zéro
CW = 50  # largeur d'une case de numéro
CH = 54  # hauteur d'une case de numéro
DH = 40  # hauteur de la ligne des douzaines et de la ligne du bas
Y_DOUZ = 160  # y du haut de la ligne des douzaines (1-12, 13-24, 25-36)
Y_GRILLE = Y_DOUZ + DH  # y du haut des 3 lignes de numéros
Y_BAS = Y_GRILLE + 3 * CH  # y du haut de la ligne du bas (1-18, Even...)
COL_X0 = TX + ZW  # x où commencent les 12 colonnes de numéros
CENTRE_TABLE = COL_X0 + 6 * CW  # x du milieu de la table

# ----- Règles du jeu -----
ROUGES = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]  # les numéros rouges
MISE_MAX = 2000  # la mise totale maximale sur la table
ARGENT_DEPART = argent.lire()  # l'argent du joueur, lu dans le fichier commun à tous les jeux
JETONS_VISIBLES = 10  # nombre maximal de jetons dessinés dans une pile
DUREE_ANIMATION = 4000  # durée totale du tour de roue en millisecondes
DELAI_IMAGE = 30  # temps entre deux images de l'animation en millisecondes
TOURS_MINI = 4  # nombre minimal de tours complets que fait la roue

# ----- État du jeu (variables globales, pas de classes) -----
reserve = ARGENT_DEPART  # l'argent du joueur (il vient du menu et il est commun à tous les jeux)
mises = {}  # les mises sur la table : (type, valeur) -> {"x", "y", "jetons": [valeurs des jetons]}
historique = []  # l'ordre dans lequel les jetons ont été posés (utilisé par le bouton UNDO)
jeton_choisi = 1  # la valeur du jeton actuellement sélectionné en bas
angle_roue = 0.0  # rotation actuelle de la roue en degrés
en_rotation = False  # True pendant que la roue tourne (bloque les mises)
ids_parts = []  # liste des identifiants canvas des 37 parts
ids_numeros = []  # liste des identifiants canvas des 37 numéros


# ----- Fonctions utiles -----
def couleur_du_numero(n):
    """Renvoie la couleur du numéro n."""  # description de la fonction
    if n == 0:  # le zéro
        return VERT_ZERO  # est vert
    if n in ROUGES:  # si le numéro est dans la liste des rouges
        return ROUGE  # il est rouge
    return "black"  # sinon il est noir


def texte_jeton(valeur):
    """Raccourcit les grands montants pour qu'ils tiennent sur un jeton (1000 -> 1k, 1500 -> 1.5k)."""  # description de la fonction
    if valeur >= 1000:  # 1000 et plus
        if valeur % 1000 == 0:  # un nombre rond de milliers
            return str(valeur // 1000) + "k"  # par exemple 1k ou 2k
        return str(valeur // 100 / 10) + "k"  # par exemple 1.5k
    return str(valeur)  # les petits montants sont écrits en entier


def total_mise():
    """Renvoie le montant total de tous les jetons sur la table."""  # description de la fonction
    total = 0  # on part de zéro
    for cle in mises:  # pour chaque mise sur la table
        total = total + sum(mises[cle]["jetons"])  # on ajoute tous les jetons de cette mise
    return total  # le montant total


def maj_affichage():
    """Met à jour le solde et le texte de la mise totale."""  # description de la fonction
    argent.ecrire(reserve)  # on enregistre l'argent pour que les autres jeux le retrouvent
    canvas.itemconfig(texte_reserve, text="Solde monnaie : " + str(reserve))  # met à jour le solde
    canvas.itemconfig(texte_total, text="Total bet: " + str(total_mise()) + " / " + str(MISE_MAX))  # met à jour le total


def dessiner_jeton(x, y, rayon, valeur, texte, tag, actif):
    """Dessine un jeton et renvoie la liste de ses identifiants canvas."""  # description de la fonction
    fond, couleur_texte, anneau = JETONS[valeur]  # couleurs de ce jeton
    etat = "normal" if actif else "disabled"  # les éléments "disabled" ignorent la souris (les clics passent à travers)
    exterieur = canvas.create_oval(x - rayon, y - rayon, x + rayon, y + rayon,
                                   fill=fond, outline=anneau, width=2, tags=tag, state=etat)  # disque extérieur
    interieur = canvas.create_oval(x - rayon + 5, y - rayon + 5, x + rayon - 5, y + rayon - 5,
                                   fill=fond, outline=anneau, width=1, dash=(3, 2),
                                   tags=tag, state=etat)  # anneau intérieur en pointillés
    nombre = canvas.create_text(x, y, text=texte, font=(POLICE, int(rayon / 2), "bold"),
                                fill=couleur_texte, tags=tag, state=etat)  # le nombre sur le dessus du jeton
    return [exterieur, interieur, nombre]  # on renvoie les identifiants (utilisés pour lier les clics)


def dessiner_mises():
    """Redessine toutes les piles de jetons sur la table."""  # description de la fonction
    canvas.delete("jeton")  # supprime tous les jetons dessinés sur la table
    for cle in mises:  # pour chaque mise sur la table
        pari = mises[cle]  # les données de cette mise
        pile = pari["jetons"][-JETONS_VISIBLES:]  # les derniers jetons de la pile (les seuls dessinés)
        total = sum(pari["jetons"])  # montant total de cette mise
        for k in range(len(pile)):  # du jeton du bas au jeton du haut
            y = pari["y"] + 6 - k * 4  # chaque jeton est dessiné 4 pixels plus haut que le précédent
            if k == len(pile) - 1:  # le jeton du haut de la pile
                texte = texte_jeton(total)  # affiche le montant total de la mise
            else:  # les jetons du dessous
                texte = ""  # n'ont pas de texte (ils sont cachés par le jeton au-dessus)
            dessiner_jeton(pari["x"], y, 17, pile[k], texte, "jeton", False)  # dessine le jeton


def dessiner_selecteur():
    """Dessine les 6 jetons en bas (le jeton sélectionné est surélevé et entouré d'un halo doré)."""  # description de la fonction
    canvas.delete("selecteur")  # supprime les anciens jetons du sélecteur
    for k in range(len(VALEURS_JETONS)):  # pour chaque jeton
        valeur = VALEURS_JETONS[k]  # la valeur de ce jeton
        x = CENTRE_TABLE + (k - 2.5) * 72  # les jetons sont répartis autour du milieu de la table
        y = 575  # hauteur normale des jetons
        if valeur == jeton_choisi:  # si c'est le jeton sélectionné
            y = y - 8  # on le surélève un peu
            canvas.create_oval(x - 31, y - 31, x + 31, y + 31, outline=OR, width=3,
                               tags="selecteur", state="disabled")  # halo doré autour de lui
        ids = dessiner_jeton(x, y, 26, valeur, texte_jeton(valeur), "selecteur", True)  # dessine le jeton
        for element in ids:  # pour chaque partie du jeton
            canvas.tag_bind(element, "<Button-1>", lambda event, v=valeur: choisir_jeton(v))  # clic = le sélectionner
            canvas.tag_bind(element, "<Enter>", lambda event: canvas.config(cursor="hand2"))  # curseur en forme de main
            canvas.tag_bind(element, "<Leave>", lambda event: canvas.config(cursor=""))  # curseur normal


def choisir_jeton(valeur):
    """Sélectionne le jeton que le joueur veut utiliser."""  # description de la fonction
    global jeton_choisi  # on modifie la variable globale
    jeton_choisi = valeur  # on retient le jeton sélectionné
    dessiner_selecteur()  # redessine le sélecteur avec le nouveau jeton mis en valeur


def placer_roue():
    """Dessine chaque part et chaque numéro selon l'angle_roue actuel."""  # description de la fonction
    for i in range(NB_PARTS):  # boucle sur les 37 parts
        debut = i * ANGLE_PART + angle_roue  # angle de début de cette part, décalé par la rotation
        canvas.itemconfig(ids_parts[i], start=debut)  # fait tourner la part en changeant son angle de début
        milieu = math.radians(debut + ANGLE_PART / 2)  # milieu de la part, en radians
        x = CX + 122 * math.cos(milieu)  # x du numéro (122 = distance au centre)
        y = CY - 122 * math.sin(milieu)  # y du numéro (moins car y descend sur l'écran)
        canvas.coords(ids_numeros[i], x, y)  # déplace le numéro vers sa nouvelle position


def poser_jeton(type_pari, valeur, x, y):
    """Pose le jeton sélectionné sur une case de la table (les jetons s'empilent les uns sur les autres)."""  # description de la fonction
    global reserve  # on modifie la réserve
    if en_rotation:  # si la roue tourne
        return  # on ignore le clic, pas de mise pendant le tour
    if jeton_choisi > reserve:  # si le joueur n'a pas les moyens de ce jeton
        canvas.itemconfig(texte_resultat, text="Not enough money !", fill=ROUGE)  # on prévient le joueur
        return  # on s'arrête ici
    if total_mise() + jeton_choisi > MISE_MAX:  # si la table dépasserait la mise maximale
        canvas.itemconfig(texte_resultat, text="Max bet is " + str(MISE_MAX) + " !", fill=ROUGE)  # on prévient le joueur
        return  # on s'arrête ici
    cle = (type_pari, valeur)  # la clé qui identifie cette case
    if cle not in mises:  # s'il n'y a pas encore de jeton sur cette case
        mises[cle] = {"x": x, "y": y, "jetons": []}  # on crée une pile vide pour elle
    mises[cle]["jetons"].append(jeton_choisi)  # on ajoute le jeton sur le dessus de la pile
    historique.append(cle)  # on le retient pour le bouton UNDO
    reserve = reserve - jeton_choisi  # on retire la valeur du jeton de la réserve
    canvas.itemconfig(texte_resultat, text="Place your bets !", fill=CLAIR)  # remet le message de départ
    maj_affichage()  # met à jour le solde et la mise totale
    dessiner_mises()  # redessine les piles


def annuler():
    """UNDO : retire le dernier jeton posé et rend son argent."""  # description de la fonction
    global reserve  # on modifie la réserve
    if en_rotation or len(historique) == 0:  # pendant un tour ou s'il n'y a rien à retirer
        return  # on ne fait rien
    cle = historique.pop()  # la case du dernier jeton posé
    valeur = mises[cle]["jetons"].pop()  # on enlève le jeton de sa pile
    if len(mises[cle]["jetons"]) == 0:  # si la pile est maintenant vide
        del mises[cle]  # on retire la mise de la table
    reserve = reserve + valeur  # on rend l'argent
    maj_affichage()  # met à jour le solde et la mise totale
    dessiner_mises()  # redessine les piles


def effacer():
    """CLEAR : retire tous les jetons de la table et rend tout l'argent."""  # description de la fonction
    while len(historique) > 0 and not en_rotation:  # tant qu'il reste des jetons à retirer
        annuler()  # on retire le dernier jeton


def multiplicateur(numero, cle):
    """Renvoie combien de fois un jeton est payé pour la mise 'cle' quand 'numero' gagne."""  # description de la fonction
    type_pari, valeur = cle  # sépare la clé en type et valeur
    if type_pari == "numero":  # mise sur un seul numéro
        if valeur == numero:  # le numéro est sorti
            return 36  # paie 36 fois la mise
        return 0  # sinon la mise est perdue
    if numero == 0:  # le zéro fait perdre toutes les autres mises
        return 0  # la maison gagne
    if type_pari == "douzaine":  # mise sur une douzaine
        if (numero - 1) // 12 + 1 == valeur:  # le numéro est dans la douzaine choisie (1, 2 ou 3)
            return 3  # paie 3 fois la mise
        return 0  # sinon la mise est perdue
    if type_pari == "rouge" and numero in ROUGES:  # mise sur rouge et un numéro rouge
        return 2  # paie 2 fois la mise
    if type_pari == "noir" and numero not in ROUGES:  # mise sur noir et un numéro noir
        return 2  # paie 2 fois la mise
    if type_pari == "pair" and numero % 2 == 0:  # mise sur pair et un numéro pair
        return 2  # paie 2 fois la mise
    if type_pari == "impair" and numero % 2 == 1:  # mise sur impair et un numéro impair
        return 2  # paie 2 fois la mise
    if type_pari == "manque" and numero <= 18:  # mise sur 1-18 et le numéro est entre 1 et 18
        return 2  # paie 2 fois la mise
    if type_pari == "passe" and numero >= 19:  # mise sur 19-36 et le numéro est entre 19 et 36
        return 2  # paie 2 fois la mise
    return 0  # sinon le joueur perd la mise


def finir(gagnant):
    """Appelée quand la roue s'arrête : paie chaque mise, vide la table et affiche le résultat."""  # description de la fonction
    global reserve, en_rotation  # on modifie ces variables globales
    mise = total_mise()  # montant total qui a été misé
    gain = 0  # argent total rendu au joueur
    for cle in mises:  # pour chaque mise sur la table
        gain = gain + sum(mises[cle]["jetons"]) * multiplicateur(gagnant, cle)  # on ajoute ce que paie cette mise
    reserve = reserve + gain  # on ajoute les gains à la réserve
    mises.clear()  # la table est vidée
    historique.clear()  # l'historique est vidé aussi
    en_rotation = False  # la roue est arrêtée, les mises sont de nouveau permises
    bouton_lancer.config(state="normal")  # réactive le gros bouton pour lancer
    bouton_annuler.config(state="normal")  # réactive le bouton UNDO
    bouton_effacer.config(state="normal")  # réactive le bouton CLEAR
    maj_affichage()  # met à jour le solde et la mise totale
    dessiner_mises()  # redessine la table (maintenant vide)
    net = gain - mise  # bénéfice (positif) ou perte (négative)
    if net > 0:  # le joueur a fait un bénéfice
        message = "Number " + str(gagnant) + " - You win " + str(net) + " !"  # message de victoire
        canvas.itemconfig(texte_resultat, text=message, fill=VERT)  # on l'affiche en vert
    elif net == 0:  # le joueur récupère exactement son argent
        message = "Number " + str(gagnant) + " - You break even"  # message neutre
        canvas.itemconfig(texte_resultat, text=message, fill=CLAIR)  # on l'affiche en doré clair
    else:  # le joueur a perdu de l'argent
        message = "Number " + str(gagnant) + " - You lose " + str(-net)  # message de défaite
        canvas.itemconfig(texte_resultat, text=message, fill="white")  # on l'affiche en blanc
    if reserve <= 0:  # si le joueur n'a plus d'argent
        canvas.itemconfig(texte_resultat, text="No money left !", fill=ROUGE)  # message de fin de partie


def tourner(etape, total, angle_depart, rotation_totale, gagnant):
    """Une image de l'animation du tour de roue (elle s'appelle elle-même avec after)."""  # description de la fonction
    global angle_roue  # on modifie la rotation de la roue
    t = etape / total  # avancement de l'animation entre 0 et 1
    facile = 1 - (1 - t) ** 3  # ralentissement : rapide au début, puis de plus en plus lent
    angle_roue = angle_depart - rotation_totale * facile  # nouvel angle (moins = tour dans le sens des aiguilles d'une montre)
    placer_roue()  # redessine la roue à cet angle
    if etape < total:  # si l'animation n'est pas finie
        fenetre.after(DELAI_IMAGE, tourner, etape + 1, total, angle_depart,
                      rotation_totale, gagnant)  # programme l'image suivante
    else:  # dernière image atteinte
        finir(gagnant)  # la roue s'est arrêtée : on paie les mises


def lancer():
    """Lance la roue (les jetons sont déjà payés quand on les pose)."""  # description de la fonction
    global en_rotation  # on modifie cette variable globale
    if en_rotation:  # si la roue tourne déjà
        return  # on ne fait rien
    if len(mises) == 0:  # s'il n'y a aucun jeton sur la table
        canvas.itemconfig(texte_resultat, text="Place a chip on the table first !", fill=CLAIR)  # on prévient le joueur
        return  # on s'arrête ici

    canvas.itemconfig(texte_resultat, text="No more bets...", fill=OR)  # message pendant le tour
    en_rotation = True  # bloque les mises pendant le tour
    bouton_lancer.config(state="disabled")  # désactive le bouton pour lancer pendant le tour
    bouton_annuler.config(state="disabled")  # désactive le bouton UNDO pendant le tour
    bouton_effacer.config(state="disabled")  # désactive le bouton CLEAR pendant le tour

    gagnant = random.randint(0, 36)  # le code choisit le numéro gagnant
    index = ORDRE.index(gagnant)  # position de sa part sur la roue
    cible = (90 - (index * ANGLE_PART + ANGLE_PART / 2)) % 360  # angle qui place cette part sous le pointeur (90 = en haut)
    reste = (angle_roue - cible) % 360  # distance à parcourir dans le sens horaire pour atteindre l'angle cible
    rotation_totale = reste + 360 * (TOURS_MINI + random.randint(0, 2))  # on ajoute plusieurs tours complets
    total = DUREE_ANIMATION // DELAI_IMAGE  # nombre d'images dans l'animation
    tourner(0, total, angle_roue, rotation_totale, gagnant)  # démarre l'animation


def retour():
    effacer()  # on rend au joueur les jetons posés sur la table avant de partir
    fenetre.destroy()  # ferme la fenêtre


def creer_case(x1, y1, x2, y2, couleur, texte, taille, type_pari, valeur, losange=None):
    """Crée une case cliquable de la table (rectangle + texte ou losange)."""  # description de la fonction
    cx = (x1 + x2) / 2  # x du centre de la case
    cy = (y1 + y2) / 2  # y du centre de la case
    elements = []  # liste des éléments canvas qui font partie de cette case
    rect = canvas.create_rectangle(x1, y1, x2, y2, fill=couleur, outline="white", width=1)  # la case elle-même
    elements.append(rect)  # le rectangle est cliquable
    if losange is not None:  # si la case montre un losange rouge ou noir
        points = [cx, cy - 15, cx + 26, cy, cx, cy + 15, cx - 26, cy]  # les 4 coins du losange
        elements.append(canvas.create_polygon(points, fill=losange, outline="white"))  # dessine le losange
    else:  # sinon la case montre un texte
        elements.append(canvas.create_text(cx, cy, text=texte, font=(POLICE, taille, "bold"),
                                           fill="white"))  # dessine le texte
    for element in elements:  # pour chaque élément de la case
        canvas.tag_bind(element, "<Button-1>",
                        lambda event: poser_jeton(type_pari, valeur, cx, cy))  # clic = poser un jeton ici
        canvas.tag_bind(element, "<Enter>", lambda event: canvas.config(cursor="hand2"))  # curseur en main au survol
        canvas.tag_bind(element, "<Leave>", lambda event: canvas.config(cursor=""))  # curseur normal en dehors


# ----- La fenêtre et la zone de dessin -----
fenetre = tk.Tk()  # crée la fenêtre principale
fenetre.title("Royal Casino - Roulette")  # titre de la fenêtre
fenetre.geometry("1152x648")  # taille de la fenêtre
fenetre.protocol("WM_DELETE_WINDOW", retour)  # la croix de la fenêtre fait comme le bouton < Menu (les jetons sont rendus)

canvas = tk.Canvas(fenetre, width=LARGEUR, height=HAUTEUR, bg=FOND, highlightthickness=0)  # zone de dessin
canvas.pack()  # affiche le canvas dans la fenêtre

# ----- Le cadre autour de la fenêtre (doré puis rouge) -----
canvas.create_rectangle(10, 10, LARGEUR - 10, HAUTEUR - 10, outline=OR, width=4)  # cadre doré
canvas.create_rectangle(20, 20, LARGEUR - 20, HAUTEUR - 20, outline=ROUGE, width=2)  # cadre rouge

# ----- Barre du haut : bouton retour à gauche, solde à droite -----
bouton_retour = tk.Button(fenetre, text="< Menu", font=(POLICE, 11), command=retour)  # bouton retour
canvas.create_window(80, 45, window=bouton_retour)  # place le bouton retour

canvas.create_rectangle(905, 30, 1105, 62, fill="black", outline=OR, width=2)  # boîte noire pour le solde
texte_reserve = canvas.create_text(1005, 46, text="Solde monnaie : " + str(reserve),  # texte du solde
                                   font=(POLICE, 12, "bold"), fill="white")  # police grasse blanche

# ----- Le titre -----
canvas.create_text(576, 75, text="ROULETTE", font=(POLICE, 34, "bold"), fill=OR)  # grand titre doré

# ===== PARTIE GAUCHE : la roue =====
canvas.create_oval(CX - RAYON - 8, CY - RAYON - 8, CX + RAYON + 8, CY + RAYON + 8,
                   outline=OR, width=4)  # anneau doré autour de la roue

for i in range(NB_PARTS):  # crée les 37 parts une seule fois (elles sont déplacées ensuite)
    couleur = couleur_du_numero(ORDRE[i])  # couleur du numéro écrit sur cette part
    part = canvas.create_arc(CX - RAYON, CY - RAYON, CX + RAYON, CY + RAYON,  # boîte du cercle
                             start=i * ANGLE_PART, extent=ANGLE_PART,  # position et taille de la part
                             fill=couleur, outline=OR, width=1)  # couleur de la part et bordure dorée
    ids_parts.append(part)  # garde son identifiant pour la faire tourner plus tard

for i in range(NB_PARTS):  # crée les 37 numéros une seule fois
    numero = canvas.create_text(0, 0, text=str(ORDRE[i]),  # texte créé en (0, 0), déplacé juste après
                                font=(POLICE, 9, "bold"), fill="white")  # petite police grasse blanche
    ids_numeros.append(numero)  # garde son identifiant pour le déplacer plus tard

placer_roue()  # met chaque part et chaque numéro à sa position de départ

# Le centre de la roue
canvas.create_oval(CX - 50, CY - 50, CX + 50, CY + 50, fill="black", outline=OR, width=3)  # disque noir
canvas.create_text(CX, CY, text="♠", font=(POLICE, 38), fill=OR)  # symbole pique doré

# Le petit triangle en haut (il montre le numéro gagnant)
canvas.create_polygon(CX - 14, CY - RAYON - 14, CX + 14, CY - RAYON - 14, CX, CY - RAYON + 14,
                      fill=CLAIR, outline="black")  # pointeur fixe

# Texte sous la roue qui montre les messages et le résultat du tour
texte_resultat = canvas.create_text(CX, 525, text="Pick a chip and click on the table !",  # texte du message
                                    font=(POLICE, 15, "bold"), fill=CLAIR)  # police grasse dorée claire

# ===== PARTIE DROITE : la table de mise verte =====
canvas.create_rectangle(TX - 14, Y_DOUZ - 14, COL_X0 + 12 * CW + 14, Y_BAS + DH + 14,
                        fill=TAPIS, outline=OR, width=3)  # le tapis vert avec une bordure dorée

# ----- Le zéro (à gauche, aussi haut que les 3 lignes de numéros) -----
creer_case(TX, Y_GRILLE, TX + ZW, Y_BAS, VERT_ZERO, "0", 16, "numero", 0)  # la case du 0

# ----- Les 36 numéros (3 lignes x 12 colonnes) -----
for n in range(1, 37):  # une case par numéro
    colonne = (n - 1) // 3  # numéro de colonne de 0 à 11 (3 numéros par colonne)
    ligne = 2 - (n - 1) % 3  # numéro de ligne : 0 = haut (3, 6, 9...), 2 = bas (1, 4, 7...)
    x1 = COL_X0 + colonne * CW  # côté gauche de la case
    y1 = Y_GRILLE + ligne * CH  # côté haut de la case
    creer_case(x1, y1, x1 + CW, y1 + CH, couleur_du_numero(n), str(n), 14, "numero", n)  # case du numéro n

# ----- Les 3 douzaines (au-dessus des numéros) -----
noms_douzaines = ["1-12", "13-24", "25-36"]  # noms des 3 douzaines
for k in range(3):  # pour chaque douzaine
    x1 = COL_X0 + k * 4 * CW  # une douzaine fait 4 colonnes de large
    creer_case(x1, Y_DOUZ, x1 + 4 * CW, Y_GRILLE, TAPIS, noms_douzaines[k], 13,
               "douzaine", k + 1)  # la case de la douzaine

# ----- La ligne du bas : 1-18, Even, rouge, noir, Odd, 19-36 -----
lb = 2 * CW  # chaque case du bas fait 2 colonnes de large
creer_case(COL_X0, Y_BAS, COL_X0 + lb, Y_BAS + DH, TAPIS, "1-18", 12, "manque", None)  # les petits numéros
creer_case(COL_X0 + lb, Y_BAS, COL_X0 + 2 * lb, Y_BAS + DH, TAPIS, "EVEN", 12, "pair", None)  # les numéros pairs
creer_case(COL_X0 + 2 * lb, Y_BAS, COL_X0 + 3 * lb, Y_BAS + DH, TAPIS, "", 12,
           "rouge", None, losange=ROUGE)  # rouge (losange rouge)
creer_case(COL_X0 + 3 * lb, Y_BAS, COL_X0 + 4 * lb, Y_BAS + DH, TAPIS, "", 12,
           "noir", None, losange="black")  # noir (losange noir)
creer_case(COL_X0 + 4 * lb, Y_BAS, COL_X0 + 5 * lb, Y_BAS + DH, TAPIS, "ODD", 12, "impair", None)  # les numéros impairs
creer_case(COL_X0 + 5 * lb, Y_BAS, COL_X0 + 6 * lb, Y_BAS + DH, TAPIS, "19-36", 12, "passe", None)  # les grands numéros

# ----- Textes sous la table : mise totale et gains -----
texte_total = canvas.create_text(CENTRE_TABLE, 440, text="Total bet: 0 / " + str(MISE_MAX),  # texte de la mise totale
                                 font=(POLICE, 14, "bold"), fill="white")  # police grasse blanche
canvas.create_text(CENTRE_TABLE, 463, text="Number x36  |  Dozen x3  |  Other bets x2  |  0 = house wins",
                   font=(POLICE, 11), fill=OR)  # rappel des gains

# ----- Les boutons : UNDO, lancer et CLEAR -----
bouton_annuler = tk.Button(fenetre, text="UNDO", font=(POLICE, 11, "bold"),
                           bg=OR, fg="black", width=8, command=annuler)  # retire le dernier jeton
canvas.create_window(CENTRE_TABLE - 190, 505, window=bouton_annuler)  # place le bouton UNDO à gauche
bouton_lancer = tk.Button(fenetre, text="LANCER LA ROUE", font=(POLICE, 18, "bold"),  # gros texte gras
                          bg=OR, fg="black", width=18, command=lancer)  # bouton doré qui appelle lancer
canvas.create_window(CENTRE_TABLE, 505, window=bouton_lancer)  # place le gros bouton au milieu
bouton_effacer = tk.Button(fenetre, text="CLEAR", font=(POLICE, 11, "bold"),
                           bg=OR, fg="black", width=8, command=effacer)  # retire tous les jetons
canvas.create_window(CENTRE_TABLE + 190, 505, window=bouton_effacer)  # place le bouton CLEAR à droite

# ----- Le sélecteur de jetons en bas -----
dessiner_selecteur()  # dessine les 6 jetons (1, 5, 25, 100, 500, 1k)

# ----- Lancement de la fenêtre -----
fenetre.mainloop()  # garde la fenêtre ouverte et écoute les clics
