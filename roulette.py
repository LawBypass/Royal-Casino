# -*- coding: utf-8 -*-
# =============================================================================
#  ROULETTE DE CASINO (roulette européenne) — en Python avec Tkinter
# =============================================================================
#  Ce programme est un jeu de roulette avec une interface graphique (une fenêtre).
#  Il est écrit SANS AUCUNE CLASSE : seulement des variables et des fonctions.
#
#  Structures de données utilisées :
#    - des TUPLES        : ROUE (l'ordre des numéros sur la roue), ROUGES (les
#                          numéros rouges), JETONS (les valeurs des jetons), les
#                          polices d'écriture, les rectangles (x1, y1, x2, y2)...
#    - des DICTIONNAIRES : etat (l'état du jeu), mises (les mises posées),
#                          PARIS (tous les paris possibles), ZONES (où se trouve
#                          chaque pari sur le tapis), COULEURS, ui (les widgets)...
#    - des LISTES        : historique (les derniers numéros sortis) et les listes
#                          de numéros fabriquées pour les douzaines, colonnes...
#
#  Comment jouer :
#    1. Choisis la valeur d'un jeton (1, 5, 10, 25 ou 100 €).
#    2. Clic GAUCHE sur le tapis vert pour poser un jeton, clic DROIT pour l'enlever.
#    3. Appuie sur « LANCER » (ou sur la barre ESPACE) pour faire tourner la roue.
#
#  Pour lancer le programme :   python roulette.py
# =============================================================================


# -----------------------------------------------------------------------------
#  1) LES IMPORTS : on charge les bibliothèques dont on a besoin
# -----------------------------------------------------------------------------
import tkinter as tk  # tkinter = la bibliothèque d'interface graphique livrée avec Python (on l'appelle "tk" pour écrire moins)
import random  # random = pour tirer au hasard le numéro gagnant
import math  # math = pour cos() et sin(), qui servent à placer des choses en cercle (la roue)


# -----------------------------------------------------------------------------
#  2) LES CONSTANTES : des valeurs qui ne changent jamais pendant le jeu
#     (par convention, on les écrit en MAJUSCULES)
# -----------------------------------------------------------------------------

# --- Les règles du jeu ---
SOLDE_DEPART = 1000  # l'argent que le joueur reçoit au début d'une partie (en euros)
TAILLE_HISTORIQUE = 10  # combien de numéros sortis on garde en mémoire pour l'historique

# TUPLE : l'ordre RÉEL des 37 numéros sur une roue européenne, en tournant dans le sens des aiguilles d'une montre.
# On utilise un tuple (entre parenthèses) car cet ordre ne doit jamais être modifié.
ROUE = (0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10,  # première moitié de la roue
        5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26)  # deuxième moitié de la roue

# TUPLE : les 18 numéros rouges (les 18 autres, de 1 à 36, sont noirs ; le 0 est vert)
ROUGES = (1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36)  # liste officielle des numéros rouges

# TUPLE : les valeurs des jetons que le joueur peut choisir
JETONS = (1, 5, 10, 25, 100)  # du plus petit au plus grand (l'ordre compte, voir couleur_jeton())

# DICTIONNAIRE : à chaque valeur de jeton (la clé) on associe une couleur (la valeur)
COULEURS_JETONS = {  # les couleurs sont écrites en hexadécimal : "#RRVVBB" (rouge, vert, bleu)
    1: "#ecf0f1",  # jeton de 1 € : blanc
    5: "#e74c3c",  # jeton de 5 € : rouge
    10: "#2e86de",  # jeton de 10 € : bleu
    25: "#27ae60",  # jeton de 25 € : vert
    100: "#2d2d2d",  # jeton de 100 € : noir
}  # fin du dictionnaire des couleurs de jetons

# DICTIONNAIRE : toutes les couleurs de l'interface, rangées par nom (plus facile à retenir qu'un code "#....")
COULEURS = {  # début du dictionnaire
    "rouge": "#c0392b",  # couleur des cases rouges
    "noir": "#1c1c1c",  # couleur des cases noires
    "vert": "#1e8449",  # couleur de la case du 0
    "tapis": "#0b6b30",  # vert du tapis de jeu
    "fond": "#063d1c",  # vert foncé du fond de la fenêtre
    "or": "#d4af37",  # doré (titres, bordures, pointeur)
    "bois": "#5c3317",  # marron du bois de la roue
    "bois_clair": "#8b5a2b",  # marron plus clair (centre de la roue)
    "piste": "#2b1a0e",  # marron très foncé : la piste où roule la bille
    "survol": "#f9e79f",  # jaune pâle : pour montrer la zone sous la souris
    "texte": "#ffffff",  # blanc : couleur du texte
}  # fin du dictionnaire des couleurs

# TUPLES : une police d'écriture se décrit avec un tuple (nom de la police, taille, style)
POLICE_TITRE = ("Georgia", 26, "bold")  # pour le grand titre "ROULETTE"
POLICE_INFO = ("Segoe UI", 14, "bold")  # pour le solde et la mise
POLICE_TEXTE = ("Segoe UI", 11)  # pour les messages
POLICE_PETITE = ("Segoe UI", 9)  # pour l'aide en bas
POLICE_BOUTON = ("Segoe UI", 11, "bold")  # pour les boutons
POLICE_RESULTAT = ("Georgia", 26, "bold")  # pour le grand numéro gagnant
POLICE_ROUE = ("Segoe UI", 10, "bold")  # pour les numéros écrits sur la roue
POLICE_TAPIS = ("Segoe UI", 12, "bold")  # pour les numéros écrits sur le tapis
POLICE_JETON = ("Segoe UI", 8, "bold")  # pour le montant écrit sur un jeton

# --- Dimensions de la roue (en pixels) ---
TAILLE_ROUE = 380  # la zone de dessin de la roue est un carré de 380 x 380 pixels
CENTRE = TAILLE_ROUE // 2  # le centre de la roue est au milieu du carré (// = division entière)
R_BOIS = 186  # rayon du cercle en bois tout autour
R_PISTE = 172  # rayon de la piste où roule la bille au début
R_CASES = 157  # rayon extérieur des cases colorées
R_TEXTE = 140  # à quelle distance du centre on écrit les numéros
R_MOYEU = 100  # rayon du centre en bois (le "moyeu")
R_BILLE_DEPART = 165  # la bille commence sur la piste extérieure...
R_BILLE_ARRIVEE = 115  # ...et finit dans une case, près du centre
RAYON_BILLE = 7  # taille de la bille

# --- Animation de la roue ---
NB_IMAGES = 160  # nombre d'images dans l'animation d'un lancer
DELAI_IMAGE = 25  # temps entre deux images en millisecondes (160 x 25 ms = 4 secondes)
TOURS_COMPLETS = 5  # nombre de tours complets que fait la roue avant de s'arrêter
VITESSE_BILLE = 1.7  # la bille tourne 1,7 fois plus vite que la roue (et dans l'autre sens)

# --- Dimensions du tapis de jeu (en pixels) ---
MARGE = 12  # espace vide autour du tapis
CASE_L = 58  # largeur d'une case de numéro
CASE_H = 46  # hauteur d'une case de numéro
BANDE_H = 40  # hauteur des bandes du bas (douzaines et chances simples)
LARGEUR_TAPIS = 2 * MARGE + 14 * CASE_L  # 14 colonnes : le 0 + 12 colonnes de numéros + la colonne "2 à 1"
HAUTEUR_TAPIS = 2 * MARGE + 3 * CASE_H + 2 * BANDE_H  # 3 lignes de numéros + 2 bandes en dessous
RAYON_JETON_TAPIS = 15  # taille d'un jeton posé sur le tapis
RAYON_JETON_CHOIX = 21  # taille d'un jeton dans le sélecteur de jetons


# -----------------------------------------------------------------------------
#  3) LES VARIABLES DU JEU (elles changent pendant la partie)
#     Comme on n'utilise pas de classe, on range tout dans des dictionnaires et
#     des listes. Avantage : une fonction peut MODIFIER leur contenu sans avoir
#     besoin du mot-clé "global".
# -----------------------------------------------------------------------------

# DICTIONNAIRE : l'état complet du jeu à un instant donné
etat = {  # début du dictionnaire d'état
    "solde": SOLDE_DEPART,  # l'argent que le joueur a encore en poche (hors mises posées)
    "jeton": 10,  # la valeur du jeton actuellement sélectionné
    "en_rotation": False,  # True pendant que la roue tourne (on ne peut plus miser)
    "angle_roue": 90.0,  # l'angle actuel de la roue, en degrés
    "angle_depart": 0.0,  # l'angle de la roue au début du lancer
    "angle_cible": 0.0,  # l'angle où la roue doit s'arrêter
    "angle_bille": 90.0,  # l'angle actuel de la bille, en degrés
    "rayon_bille": R_BILLE_DEPART,  # la distance actuelle entre la bille et le centre
    "bille_visible": False,  # la bille n'apparaît qu'à partir du premier lancer
    "image": 0,  # numéro de l'image actuelle de l'animation
    "numero_tire": None,  # le numéro que le hasard a choisi pour ce lancer
    "dernier_numero": None,  # le dernier numéro sorti (encadré en doré sur le tapis)
    "survol": None,  # le pari qui se trouve sous la souris (None = aucun)
    "tours": 0,  # combien de lancers ont été faits dans cette partie
}  # fin du dictionnaire d'état

# DICTIONNAIRE : les mises posées sur le tapis.  clé = nom du pari, valeur = montant en euros.
# Exemple : {"17": 10, "rouge": 25}  veut dire 10 € sur le 17 et 25 € sur le rouge.
mises = {}  # au début, il n'y a aucune mise

# DICTIONNAIRE : une copie des mises du tour précédent (pour le bouton « Remiser »)
derniere_mise = {}  # vide tant qu'on n'a pas joué

# LISTE : les derniers numéros sortis, le plus récent en premier (une liste car elle change souvent)
historique = []  # vide au début

# DICTIONNAIRE : tous les paris possibles. clé = nom court du pari, valeur = un petit dictionnaire d'infos
PARIS = {}  # rempli par la fonction construire_paris()

# DICTIONNAIRE : où se trouve chaque pari sur le tapis. clé = nom du pari, valeur = TUPLE (x1, y1, x2, y2)
ZONES = {}  # rempli aussi par la fonction construire_paris()

# DICTIONNAIRE : on y range les éléments de l'interface (fenêtre, zones de dessin, textes...)
# pour pouvoir les retrouver depuis n'importe quelle fonction.
ui = {}  # rempli par la fonction creer_interface()


# -----------------------------------------------------------------------------
#  4) FONCTIONS "OUTILS" : des petites fonctions utilisées un peu partout
# -----------------------------------------------------------------------------

def couleur_du_numero(numero):  # reçoit un numéro de 0 à 36
    """Renvoie "vert", "rouge" ou "noir" selon le numéro."""  # docstring : explique à quoi sert la fonction
    if numero == 0:  # le 0 est le seul numéro vert
        return "vert"  # on renvoie le nom de la couleur
    if numero in ROUGES:  # "in" vérifie si le numéro se trouve dans le tuple ROUGES
        return "rouge"  # il y est : c'est un numéro rouge
    return "noir"  # sinon c'est forcément un numéro noir


def decrire_numero(numero):  # reçoit un numéro de 0 à 36
    """Fabrique une phrase qui décrit un numéro, par exemple : « 17 NOIR, impair, manque »."""  # docstring
    if numero == 0:  # le 0 n'est ni pair, ni impair, ni manque, ni passe (au casino)
        return "0 VERT"  # donc on le décrit simplement
    couleur = couleur_du_numero(numero).upper()  # .upper() met le mot en majuscules : "rouge" -> "ROUGE"
    if numero % 2 == 0:  # % donne le reste de la division : reste 0 en divisant par 2 = nombre pair
        parite = "pair"  # le numéro est pair
    else:  # sinon...
        parite = "impair"  # ...il est impair
    if numero <= 18:  # de 1 à 18 on dit "manque"
        moitie = "manque"  # première moitié
    else:  # de 19 à 36 on dit "passe"
        moitie = "passe"  # deuxième moitié
    return f"{numero} {couleur}, {parite}, {moitie}"  # f-string : les {..} sont remplacés par les valeurs


def total_mises():  # pas de paramètre : elle lit le dictionnaire "mises"
    """Renvoie la somme de toutes les mises posées sur le tapis."""  # docstring
    total = 0  # on part de 0
    for montant in mises.values():  # .values() donne tous les montants du dictionnaire
        total = total + montant  # on les additionne un par un
    return total  # on renvoie la somme


def couleur_jeton(montant):  # reçoit un montant en euros
    """Choisit la couleur du plus gros jeton qui ne dépasse pas ce montant."""  # docstring
    couleur = COULEURS_JETONS[JETONS[0]]  # par défaut : la couleur du plus petit jeton
    for valeur in JETONS:  # on parcourt les valeurs de jetons, de la plus petite à la plus grande
        if montant >= valeur:  # si le montant atteint cette valeur...
            couleur = COULEURS_JETONS[valeur]  # ...on prend sa couleur (la dernière trouvée sera la plus grande)
    return couleur  # on renvoie la couleur trouvée


def texte_montant(montant):  # reçoit un montant en euros
    """Écrit un montant en version courte pour qu'il tienne sur un jeton (1500 -> "1.5k")."""  # docstring
    if montant >= 1000:  # à partir de 1000 € le nombre est trop long pour le petit jeton
        return f"{montant / 1000:.1f}k"  # :.1f = un seul chiffre après la virgule, "k" = mille
    return str(montant)  # sinon on écrit le nombre tel quel (str() transforme un nombre en texte)


def cercle(canevas, x, y, rayon, **options):  # **options récupère toutes les options en plus (fill=..., outline=...)
    """Dessine un cercle de centre (x, y) : Tkinter, lui, demande le carré qui entoure le cercle."""  # docstring
    return canevas.create_oval(x - rayon, y - rayon, x + rayon, y + rayon, **options)  # coin haut-gauche puis coin bas-droit


def dessiner_jeton(canevas, x, y, montant, rayon):  # où dessiner, position, montant affiché, taille
    """Dessine un jeton de casino rond avec le montant écrit dessus."""  # docstring
    fond = couleur_jeton(montant)  # la couleur dépend du montant
    cercle(canevas, x + 2, y + 2, rayon, fill="#000000", outline="")  # une ombre noire décalée de 2 pixels
    cercle(canevas, x, y, rayon, fill=fond, outline="#ffffff", width=2)  # le jeton lui-même, bordé de blanc
    cercle(canevas, x, y, rayon - 5, fill="", outline="#ffffff", dash=(3, 3))  # le liseré en pointillés
    if fond == COULEURS_JETONS[1]:  # sur le jeton blanc, un texte blanc serait invisible...
        couleur_texte = "#000000"  # ...donc on écrit en noir
    else:  # sur tous les autres jetons...
        couleur_texte = "#ffffff"  # ...on écrit en blanc
    canevas.create_text(x, y, text=texte_montant(montant), fill=couleur_texte, font=POLICE_JETON)  # le montant au centre


def message(texte):  # reçoit le texte à afficher
    """Affiche un message au joueur dans le panneau de droite."""  # docstring
    ui["message"].config(text=texte)  # .config() change une option d'un widget déjà créé (ici son texte)


# -----------------------------------------------------------------------------
#  5) LA LISTE DE TOUS LES PARIS POSSIBLES ET LEUR PLACE SUR LE TAPIS
# -----------------------------------------------------------------------------

def ajouter_pari(cle, texte, nom, numeros, paiement, sorte, rectangle):  # toutes les infos d'un pari
    """Enregistre un pari dans PARIS et sa position (un rectangle) dans ZONES."""  # docstring
    PARIS[cle] = {  # on crée un petit dictionnaire d'informations pour ce pari
        "texte": texte,  # ce qui est écrit sur le tapis (ex : "PAIR")
        "nom": nom,  # le nom complet pour les messages (ex : "le PAIR")
        "numeros": tuple(numeros),  # les numéros qui font gagner ce pari (convertis en tuple car ils ne changent plus)
        "paiement": paiement,  # combien le pari rapporte pour 1 € misé (35 pour un numéro plein)
        "sorte": sorte,  # la sorte de pari : "numero", "colonne", "douzaine" ou "chance"
    }  # fin du petit dictionnaire
    ZONES[cle] = rectangle  # le rectangle (x1, y1, x2, y2) est un tuple de 4 nombres


def construire_paris():  # pas de paramètre
    """Remplit PARIS et ZONES avec les 49 paris du tapis : 37 numéros, 3 colonnes, 3 douzaines, 6 chances simples."""  # docstring
    # --- Le zéro : une grande case verte à gauche, haute comme 3 cases ---
    rectangle_zero = (MARGE, MARGE, MARGE + CASE_L, MARGE + 3 * CASE_H)  # TUPLE (x1, y1, x2, y2)
    ajouter_pari("0", "0", "le 0", [0], 35, "numero", rectangle_zero)  # le 0 paie 35 fois la mise

    # --- Les 36 numéros : 12 colonnes de 3 numéros ---
    for colonne in range(12):  # range(12) donne 0, 1, 2, ..., 11
        for ligne in range(3):  # 0 = ligne du haut, 1 = ligne du milieu, 2 = ligne du bas
            numero = 3 * colonne + (3 - ligne)  # en haut 3, 6, 9... au milieu 2, 5, 8... en bas 1, 4, 7...
            x1 = MARGE + CASE_L * (colonne + 1)  # +1 car la première colonne est occupée par le 0
            y1 = MARGE + CASE_H * ligne  # chaque ligne est plus basse que la précédente
            rectangle = (x1, y1, x1 + CASE_L, y1 + CASE_H)  # TUPLE : le rectangle de la case
            ajouter_pari(str(numero), str(numero), f"le {numero}", [numero], 35, "numero", rectangle)  # un numéro plein paie 35 contre 1

    # --- Les 3 colonnes "2 à 1", tout à droite ---
    for ligne in range(3):  # une case "2 à 1" au bout de chaque ligne
        reste = (3 - ligne) % 3  # ligne du haut : multiples de 3 (reste 0), milieu : reste 2, bas : reste 1
        numeros = []  # LISTE vide qu'on va remplir avec les numéros de la colonne
        for n in range(1, 37):  # on teste tous les numéros de 1 à 36
            if n % 3 == reste:  # si le reste de la division par 3 correspond...
                numeros.append(n)  # ...le numéro fait partie de la colonne : on l'ajoute à la liste
        numero_colonne = 3 - ligne  # la colonne du bas est la 1re, celle du haut est la 3e
        x1 = MARGE + CASE_L * 13  # 13 cases après la marge : tout au bout du tapis
        y1 = MARGE + CASE_H * ligne  # même hauteur que la ligne de numéros
        rectangle = (x1, y1, x1 + CASE_L, y1 + CASE_H)  # TUPLE : le rectangle de la case
        ajouter_pari(f"colonne{numero_colonne}", "2 à 1", f"la colonne {numero_colonne}",
                     numeros, 2, "colonne", rectangle)  # une colonne paie 2 contre 1

    # --- Les 3 douzaines, sous les numéros ---
    textes_douzaines = ("1re 12", "2e 12", "3e 12")  # TUPLE : ce qu'on écrit sur chaque douzaine
    for d in range(3):  # d = 0, 1, 2
        premier = 12 * d + 1  # premier numéro de la douzaine : 1, 13 ou 25
        dernier = 12 * d + 12  # dernier numéro de la douzaine : 12, 24 ou 36
        numeros = list(range(premier, dernier + 1))  # LISTE des 12 numéros (range s'arrête AVANT la fin, d'où le +1)
        x1 = MARGE + CASE_L * (1 + 4 * d)  # chaque douzaine fait 4 cases de large
        y1 = MARGE + 3 * CASE_H  # juste sous les 3 lignes de numéros
        rectangle = (x1, y1, x1 + 4 * CASE_L, y1 + BANDE_H)  # TUPLE : le rectangle de la douzaine
        ajouter_pari(f"douzaine{d + 1}", textes_douzaines[d], f"la {textes_douzaines[d]} ({premier}-{dernier})",
                     numeros, 2, "douzaine", rectangle)  # une douzaine paie 2 contre 1

    # --- Les 6 chances simples, tout en bas ---
    tous = range(1, 37)  # tous les numéros de 1 à 36 (le 0 fait perdre les chances simples)
    chances = (  # TUPLE de TUPLES : (clé, texte sur le tapis, nom complet, LISTE des numéros gagnants)
        ("manque", "1 - 18", "MANQUE (1-18)", [n for n in tous if n <= 18]),  # [.. for .. if ..] = liste en compréhension : les n de 1 à 18
        ("pair", "PAIR", "PAIR", [n for n in tous if n % 2 == 0]),  # les numéros pairs
        ("rouge", "ROUGE", "ROUGE", [n for n in tous if n in ROUGES]),  # les numéros rouges
        ("noir", "NOIR", "NOIR", [n for n in tous if n not in ROUGES]),  # les numéros noirs (pas rouges)
        ("impair", "IMPAIR", "IMPAIR", [n for n in tous if n % 2 == 1]),  # les numéros impairs
        ("passe", "19 - 36", "PASSE (19-36)", [n for n in tous if n >= 19]),  # les numéros de 19 à 36
    )  # fin du tuple des chances simples
    for i in range(len(chances)):  # len() donne le nombre d'éléments : ici 6
        cle, texte, nom, numeros = chances[i]  # on "déballe" le tuple en 4 variables d'un coup
        x1 = MARGE + CASE_L * (1 + 2 * i)  # chaque chance simple fait 2 cases de large
        y1 = MARGE + 3 * CASE_H + BANDE_H  # sous la bande des douzaines
        rectangle = (x1, y1, x1 + 2 * CASE_L, y1 + BANDE_H)  # TUPLE : le rectangle de la chance simple
        ajouter_pari(cle, texte, nom, numeros, 1, "chance", rectangle)  # une chance simple paie 1 contre 1


def trouver_pari(x, y):  # reçoit la position de la souris sur le tapis
    """Renvoie le nom du pari qui se trouve à la position (x, y), ou None s'il n'y en a pas."""  # docstring
    for cle in ZONES:  # on passe en revue toutes les zones du tapis
        x1, y1, x2, y2 = ZONES[cle]  # on déballe le tuple du rectangle
        if x1 <= x < x2 and y1 <= y < y2:  # la souris est-elle à l'intérieur de ce rectangle ?
            return cle  # oui : on renvoie le nom du pari tout de suite
    return None  # aucune zone trouvée (la souris est dans la marge)


# -----------------------------------------------------------------------------
#  6) LES DESSINS : la roue, le tapis, les jetons, l'historique
# -----------------------------------------------------------------------------

def dessiner_roue():  # pas de paramètre : tout est lu dans le dictionnaire "etat"
    """Efface puis redessine entièrement la roue (appelée à chaque image de l'animation)."""  # docstring
    roue = ui["roue"]  # on récupère la zone de dessin de la roue
    roue.delete("all")  # on efface tout ce qui était dessiné avant
    pas = 360 / len(ROUE)  # chaque case occupe 360° / 37 ≈ 9,7 degrés

    cercle(roue, CENTRE, CENTRE, R_BOIS, fill=COULEURS["bois"], outline=COULEURS["or"], width=3)  # le bois autour
    cercle(roue, CENTRE, CENTRE, R_PISTE, fill=COULEURS["piste"], outline=COULEURS["or"])  # la piste de la bille

    for i in range(len(ROUE)):  # on dessine les 37 cases une par une
        numero = ROUE[i]  # le numéro de la case n°i
        milieu = etat["angle_roue"] - i * pas  # angle du milieu de la case (le "-" fait tourner les numéros dans le sens des aiguilles d'une montre)
        roue.create_arc(CENTRE - R_CASES, CENTRE - R_CASES, CENTRE + R_CASES, CENTRE + R_CASES,  # le carré qui entoure le cercle
                        start=milieu - pas / 2, extent=pas,  # la part commence une demi-case avant le milieu et fait "pas" degrés
                        fill=COULEURS[couleur_du_numero(numero)], outline=COULEURS["or"])  # couleur de la case, bord doré
        angle = math.radians(milieu)  # cos() et sin() veulent des radians, pas des degrés
        x = CENTRE + R_TEXTE * math.cos(angle)  # position horizontale du numéro (trigonométrie)
        y = CENTRE - R_TEXTE * math.sin(angle)  # position verticale ("-" car sur un écran l'axe y descend)
        roue.create_text(x, y, text=str(numero), fill=COULEURS["texte"], font=POLICE_ROUE,  # le numéro...
                         angle=milieu - 90)  # ...tourné pour que le haut du chiffre regarde vers l'extérieur

    cercle(roue, CENTRE, CENTRE, R_MOYEU, fill=COULEURS["bois"], outline=COULEURS["or"], width=2)  # le moyeu en bois
    cercle(roue, CENTRE, CENTRE, R_MOYEU - 35, fill=COULEURS["bois_clair"], outline="")  # un cercle plus clair au centre
    for k in range(4):  # la croix dorée du centre a 4 branches
        angle = math.radians(etat["angle_roue"] + 90 * k)  # une branche tous les 90°, qui tourne avec la roue
        x1 = CENTRE + 14 * math.cos(angle)  # début de la branche (près du centre)
        y1 = CENTRE - 14 * math.sin(angle)  # même chose en vertical
        x2 = CENTRE + 55 * math.cos(angle)  # fin de la branche (plus loin du centre)
        y2 = CENTRE - 55 * math.sin(angle)  # même chose en vertical
        roue.create_line(x1, y1, x2, y2, fill=COULEURS["or"], width=6, capstyle="round")  # la branche, aux bouts arrondis
    cercle(roue, CENTRE, CENTRE, 14, fill=COULEURS["or"], outline="#8a6d1c", width=2)  # le bouton doré au milieu

    if etat["bille_visible"]:  # on ne dessine la bille qu'après le premier lancer
        angle = math.radians(etat["angle_bille"])  # angle de la bille en radians
        x = CENTRE + etat["rayon_bille"] * math.cos(angle)  # position horizontale de la bille
        y = CENTRE - etat["rayon_bille"] * math.sin(angle)  # position verticale de la bille
        cercle(roue, x, y, RAYON_BILLE, fill="#fdfefe", outline="#9e9e9e")  # la bille blanche
        cercle(roue, x - 2, y - 2, 2, fill="#ffffff", outline="")  # un petit reflet pour faire "brillant"

    roue.create_polygon(CENTRE - 11, 2, CENTRE + 11, 2, CENTRE, 26,  # les 3 sommets du triangle en haut de la roue
                        fill=COULEURS["or"], outline="#000000")  # le pointeur doré qui montre le numéro gagnant


def dessiner_tapis():  # pas de paramètre
    """Efface puis redessine le tapis : les cases, la surbrillance, le dernier numéro et les jetons posés."""  # docstring
    tapis = ui["tapis"]  # on récupère la zone de dessin du tapis
    tapis.delete("all")  # on efface tout

    for cle in PARIS:  # pour chaque pari du dictionnaire PARIS...
        pari = PARIS[cle]  # ...on récupère ses informations
        x1, y1, x2, y2 = ZONES[cle]  # ...et son rectangle
        if pari["sorte"] == "numero":  # une case de numéro prend la couleur du numéro
            fond = COULEURS[couleur_du_numero(pari["numeros"][0])]  # [0] = le seul numéro de ce pari
        elif cle == "rouge" or cle == "noir":  # les cases ROUGE et NOIR sont coloriées aussi
            fond = COULEURS[cle]  # la clé "rouge" ou "noir" sert directement de nom de couleur
        else:  # toutes les autres cases (colonnes, douzaines, pair...) ...
            fond = COULEURS["tapis"]  # ... sont vert tapis
        tapis.create_rectangle(x1, y1, x2, y2, fill=fond, outline="#ffffff", width=2)  # la case avec un bord blanc
        tapis.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=pari["texte"],  # le texte au milieu de la case...
                          fill=COULEURS["texte"], font=POLICE_TAPIS)  # ...en blanc

    if etat["survol"] is not None:  # si la souris est au-dessus d'un pari...
        numeros_couverts = PARIS[etat["survol"]]["numeros"]  # ...on regarde quels numéros il couvre
        for numero in numeros_couverts:  # pour chacun de ces numéros...
            x1, y1, x2, y2 = ZONES[str(numero)]  # ...on retrouve sa case
            tapis.create_rectangle(x1 + 3, y1 + 3, x2 - 3, y2 - 3,  # un cadre un peu plus petit que la case
                                   outline=COULEURS["survol"], width=3)  # en jaune pâle
        x1, y1, x2, y2 = ZONES[etat["survol"]]  # la zone survolée elle-même...
        tapis.create_rectangle(x1, y1, x2, y2, outline=COULEURS["survol"], width=3)  # ...reçoit aussi un cadre

    if etat["dernier_numero"] is not None:  # s'il y a eu un lancer...
        x1, y1, x2, y2 = ZONES[str(etat["dernier_numero"])]  # ...on retrouve la case du numéro sorti
        tapis.create_rectangle(x1, y1, x2, y2, outline=COULEURS["or"], width=5)  # gros cadre doré autour

    for cle in mises:  # pour chaque mise posée...
        x1, y1, x2, y2 = ZONES[cle]  # ...on retrouve la zone du pari
        dessiner_jeton(tapis, (x1 + x2) / 2, (y1 + y2) / 2, mises[cle], RAYON_JETON_TAPIS)  # jeton au centre de la zone


def dessiner_selecteur_jetons():  # pas de paramètre
    """Dessine les 5 jetons qu'on peut choisir ; celui qui est choisi est entouré d'un anneau doré."""  # docstring
    zone = ui["jetons"]  # la zone de dessin du sélecteur
    zone.delete("all")  # on efface tout
    for i in range(len(JETONS)):  # pour chacun des 5 jetons...
        valeur = JETONS[i]  # ...sa valeur
        x = 30 + i * 56  # position horizontale : un jeton tous les 56 pixels
        y = 30  # position verticale : tous à la même hauteur
        if valeur == etat["jeton"]:  # si c'est le jeton sélectionné...
            cercle(zone, x, y, RAYON_JETON_CHOIX + 5, fill="", outline=COULEURS["or"], width=3)  # ...anneau doré
        dessiner_jeton(zone, x, y, valeur, RAYON_JETON_CHOIX)  # le jeton lui-même


def dessiner_historique():  # pas de paramètre
    """Dessine les derniers numéros sortis sous forme de petites pastilles colorées."""  # docstring
    zone = ui["historique"]  # la zone de dessin de l'historique
    zone.delete("all")  # on efface tout
    if len(historique) == 0:  # si on n'a encore rien joué...
        zone.create_text(4, 17, text="Aucun numéro sorti", anchor="w",  # anchor="w" : le texte commence au point donné (w = ouest = gauche)
                         fill="#a9cfb5", font=POLICE_TEXTE)  # ...on l'écrit en vert clair
        return  # et on s'arrête là
    for i in range(len(historique)):  # pour chaque numéro de l'historique...
        numero = historique[i]  # ...le numéro (historique[0] est le plus récent)
        x = 16 + i * 30  # une pastille tous les 30 pixels
        cercle(zone, x, 17, 13, fill=COULEURS[couleur_du_numero(numero)], outline="#ffffff")  # pastille colorée
        zone.create_text(x, 17, text=str(numero), fill="#ffffff", font=POLICE_JETON)  # le numéro dedans


def mettre_a_jour_affichage():  # pas de paramètre
    """Remet à jour toute l'interface (textes, tapis, jetons, boutons) après un changement."""  # docstring
    ui["solde"].config(text=f"Solde : {etat['solde']} €")  # le solde (dans une f-string, on met 'solde' entre apostrophes)
    ui["mise"].config(text=f"Mise : {total_mises()} €")  # le total des mises posées
    ui["tours"].config(text=f"Tour n°{etat['tours'] + 1}")  # le numéro du prochain tour
    if etat["dernier_numero"] is None:  # pas encore de résultat...
        ui["resultat"].config(text="–", bg=COULEURS["tapis"])  # ...on affiche un tiret sur fond vert
    else:  # sinon...
        numero = etat["dernier_numero"]  # ...le dernier numéro sorti
        ui["resultat"].config(text=str(numero), bg=COULEURS[couleur_du_numero(numero)])  # ...dans sa couleur
    if etat["en_rotation"]:  # pendant que la roue tourne...
        etat_boutons = "disabled"  # ...les boutons sont grisés (on ne peut pas cliquer)
    else:  # sinon...
        etat_boutons = "normal"  # ...ils marchent normalement
    for nom in ("lancer", "effacer", "remiser", "nouvelle"):  # TUPLE des noms des 4 boutons
        ui["bouton_" + nom].config(state=etat_boutons)  # on change l'état de chaque bouton
    dessiner_tapis()  # on redessine le tapis (les jetons ont peut-être changé)
    dessiner_selecteur_jetons()  # on redessine le sélecteur (le jeton choisi a peut-être changé)
    dessiner_historique()  # on redessine l'historique


# -----------------------------------------------------------------------------
#  7) LES ACTIONS DU JOUEUR : clics de souris, clavier et boutons
# -----------------------------------------------------------------------------

def clic_gauche_tapis(evenement):  # Tkinter donne un "événement" qui contient la position du clic
    """Pose un jeton sur le pari qui a été cliqué."""  # docstring
    if etat["en_rotation"]:  # pendant que la roue tourne...
        message("Rien ne va plus ! Attends la fin du lancer.")  # ...on n'a plus le droit de miser
        return  # on sort de la fonction
    cle = trouver_pari(evenement.x, evenement.y)  # quel pari se trouve sous la souris ?
    if cle is None:  # aucun (clic dans la marge)...
        return  # ...on ne fait rien
    valeur = etat["jeton"]  # la valeur du jeton sélectionné
    if valeur > etat["solde"]:  # le joueur n'a pas assez d'argent pour ce jeton
        message(f"Pas assez d'argent pour un jeton de {valeur} € ! Choisis un jeton plus petit.")  # on le prévient
        return  # et on ne pose rien
    etat["solde"] = etat["solde"] - valeur  # l'argent quitte la poche du joueur...
    mises[cle] = mises.get(cle, 0) + valeur  # ...et va sur le tapis (.get(cle, 0) donne 0 si rien n'était encore misé ici)
    message(f"+{valeur} € sur {PARIS[cle]['nom']}  (total ici : {mises[cle]} €)")  # on confirme au joueur
    mettre_a_jour_affichage()  # on rafraîchit l'écran


def clic_droit_tapis(evenement):  # même principe que le clic gauche
    """Enlève la mise posée sur le pari cliqué et rend l'argent au joueur."""  # docstring
    if etat["en_rotation"]:  # pendant que la roue tourne...
        return  # ...on ne peut rien retirer
    cle = trouver_pari(evenement.x, evenement.y)  # quel pari se trouve sous la souris ?
    if cle is None or cle not in mises:  # pas de pari ici, ou rien n'est misé dessus...
        return  # ...rien à faire
    rendu = mises.pop(cle)  # .pop() enlève la clé du dictionnaire ET renvoie le montant qui y était
    etat["solde"] = etat["solde"] + rendu  # l'argent revient dans la poche du joueur
    message(f"{rendu} € retirés de {PARIS[cle]['nom']}.")  # on confirme au joueur
    mettre_a_jour_affichage()  # on rafraîchit l'écran


def survol_tapis(evenement):  # appelée à chaque mouvement de la souris sur le tapis
    """Retient le pari sous la souris pour montrer en jaune les numéros qu'il couvre."""  # docstring
    cle = trouver_pari(evenement.x, evenement.y)  # le pari sous la souris (ou None)
    if cle != etat["survol"]:  # on ne redessine que si la souris a changé de zone (sinon ce serait trop lent)
        etat["survol"] = cle  # on retient la nouvelle zone
        dessiner_tapis()  # et on redessine le tapis


def sortie_tapis(evenement):  # appelée quand la souris quitte le tapis
    """Enlève la surbrillance quand la souris sort du tapis."""  # docstring
    etat["survol"] = None  # plus aucune zone survolée
    dessiner_tapis()  # on redessine sans la surbrillance


def clic_selecteur_jetons(evenement):  # clic dans la zone des jetons à choisir
    """Sélectionne le jeton sur lequel on a cliqué."""  # docstring
    for i in range(len(JETONS)):  # on teste chaque jeton
        x = 30 + i * 56  # même position que dans dessiner_selecteur_jetons()
        y = 30  # même hauteur aussi
        distance = math.hypot(evenement.x - x, evenement.y - y)  # hypot = distance entre le clic et le centre du jeton (Pythagore)
        if distance <= RAYON_JETON_CHOIX + 4:  # le clic est dans le jeton (avec un peu de marge)
            etat["jeton"] = JETONS[i]  # on retient la nouvelle valeur
            message(f"Jeton de {JETONS[i]} € sélectionné.")  # on prévient le joueur
            dessiner_selecteur_jetons()  # on redessine pour déplacer l'anneau doré
            return  # inutile de tester les autres jetons


def touche_espace(evenement):  # appelée quand on appuie sur la barre espace
    """La barre ESPACE fait la même chose que le bouton LANCER."""  # docstring
    lancer()  # on lance simplement la roue


def effacer_mises():  # appelée par le bouton « Effacer »
    """Retire toutes les mises du tapis et rend l'argent au joueur."""  # docstring
    if etat["en_rotation"]:  # pas pendant que la roue tourne
        return  # on sort
    etat["solde"] = etat["solde"] + total_mises()  # on rend tout l'argent misé
    mises.clear()  # .clear() vide complètement le dictionnaire
    message("Toutes les mises ont été retirées.")  # on prévient le joueur
    mettre_a_jour_affichage()  # on rafraîchit l'écran


def remiser():  # appelée par le bouton « Remiser »
    """Repose exactement les mêmes mises qu'au tour précédent."""  # docstring
    if etat["en_rotation"]:  # pas pendant que la roue tourne
        return  # on sort
    if len(derniere_mise) == 0:  # on n'a encore jamais joué
        message("Il n'y a pas encore de mise précédente à rejouer.")  # on prévient le joueur
        return  # on sort
    prix = 0  # combien coûte la mise précédente
    for montant in derniere_mise.values():  # on additionne tous ses montants
        prix = prix + montant  # un par un
    argent_disponible = etat["solde"] + total_mises()  # ce qu'on aurait si on reprenait les mises actuelles
    if prix > argent_disponible:  # pas assez d'argent...
        message(f"Pas assez d'argent pour remiser {prix} €.")  # ...on prévient le joueur
        return  # et on sort
    etat["solde"] = argent_disponible - prix  # on reprend les mises actuelles et on paie la mise précédente
    mises.clear()  # on enlève les mises actuelles du tapis
    mises.update(derniere_mise)  # .update() recopie toutes les paires clé/valeur de derniere_mise dans mises
    message(f"Même mise que le tour précédent : {prix} €.")  # on confirme
    mettre_a_jour_affichage()  # on rafraîchit l'écran


def nouvelle_partie():  # appelée par le bouton « Nouvelle partie »
    """Remet le jeu à zéro avec l'argent de départ."""  # docstring
    if etat["en_rotation"]:  # pas pendant que la roue tourne
        return  # on sort
    etat["solde"] = SOLDE_DEPART  # on redonne l'argent de départ
    etat["dernier_numero"] = None  # plus de dernier numéro
    etat["tours"] = 0  # on recommence au tour 1
    mises.clear()  # plus de mises sur le tapis
    derniere_mise.clear()  # plus de mise précédente
    historique.clear()  # l'historique est vidé (une liste a aussi une méthode .clear())
    message(f"Nouvelle partie ! Tu as {SOLDE_DEPART} €. Pose tes jetons puis appuie sur LANCER.")  # message d'accueil
    mettre_a_jour_affichage()  # on rafraîchit l'écran


# -----------------------------------------------------------------------------
#  8) LE LANCER : on tire le numéro, on anime la roue, puis on paie les gains
# -----------------------------------------------------------------------------

def lancer():  # appelée par le bouton « LANCER » ou la barre espace
    """Tire le numéro gagnant au hasard et démarre l'animation de la roue."""  # docstring
    if etat["en_rotation"]:  # si la roue tourne déjà...
        return  # ...on ne relance pas par-dessus
    if total_mises() == 0:  # personne n'a misé...
        message("Pose au moins un jeton sur le tapis avant de lancer !")  # ...on prévient le joueur
        return  # et on ne lance pas
    numero = random.randint(0, 36)  # LE TIRAGE : un nombre entier au hasard entre 0 et 36 (inclus)
    etat["numero_tire"] = numero  # on le garde pour la fin de l'animation
    pas = 360 / len(ROUE)  # taille d'une case en degrés
    position = ROUE.index(numero)  # .index() donne la place du numéro dans le tuple ROUE
    angle_gagnant = 90 + position * pas  # angle de roue qui met ce numéro sous le pointeur (le pointeur est en haut, à 90°)
    ecart = (angle_gagnant - etat["angle_roue"]) % 360  # combien il faut tourner pour y arriver (entre 0 et 360°)
    etat["angle_depart"] = etat["angle_roue"]  # on note d'où part la roue
    etat["angle_cible"] = etat["angle_roue"] + ecart + 360 * TOURS_COMPLETS  # on ajoute des tours complets pour le spectacle
    etat["image"] = 0  # l'animation commence à l'image 0
    etat["bille_visible"] = True  # on fait apparaître la bille
    etat["dernier_numero"] = None  # on enlève le cadre doré du numéro précédent
    etat["en_rotation"] = True  # la roue tourne : plus personne ne mise
    message("Les jeux sont faits... Rien ne va plus !")  # la phrase du croupier
    mettre_a_jour_affichage()  # on grise les boutons
    animer()  # on démarre l'animation


def animer():  # appelée une fois par image de l'animation
    """Calcule une image de l'animation, la dessine, puis se rappelle elle-même 25 ms plus tard."""  # docstring
    etat["image"] = etat["image"] + 1  # on passe à l'image suivante
    t = etat["image"] / NB_IMAGES  # t va de 0 (début) à 1 (fin) : c'est l'avancement de l'animation
    ralenti = 1 - (1 - t) ** 3  # formule de "ralentissement" : ça va vite au début et doucement à la fin (** = puissance)
    depart = etat["angle_depart"]  # angle de départ de la roue
    cible = etat["angle_cible"]  # angle d'arrivée de la roue
    etat["angle_roue"] = depart + (cible - depart) * ralenti  # l'angle de la roue pour cette image
    reste = cible - etat["angle_roue"]  # combien de degrés il reste à tourner
    etat["angle_bille"] = 90 + reste * VITESSE_BILLE  # la bille tourne à l'envers et arrive pile en haut (90°) quand reste = 0
    if t < 0.65:  # pendant les 65 premiers pourcents de l'animation...
        etat["rayon_bille"] = R_BILLE_DEPART  # ...la bille roule sur la piste extérieure
    else:  # ensuite...
        chute = (t - 0.65) / 0.35  # ...elle "tombe" vers les cases : chute va de 0 à 1
        etat["rayon_bille"] = R_BILLE_DEPART - (R_BILLE_DEPART - R_BILLE_ARRIVEE) * chute  # le rayon diminue petit à petit
    dessiner_roue()  # on dessine cette image
    if etat["image"] < NB_IMAGES:  # s'il reste des images à montrer...
        ui["fenetre"].after(DELAI_IMAGE, animer)  # ...on demande à Tkinter de rappeler animer() dans 25 ms
    else:  # sinon l'animation est finie...
        fin_du_lancer()  # ...on passe aux résultats


def fin_du_lancer():  # appelée quand la roue s'est arrêtée
    """Calcule les gains, met à jour le solde et l'historique, puis prépare le tour suivant."""  # docstring
    numero = etat["numero_tire"]  # le numéro gagnant
    mise_totale = total_mises()  # tout ce que le joueur avait misé ce tour-ci
    rendu = 0  # l'argent que la banque va rendre au joueur
    paris_gagnants = []  # LISTE des noms des paris gagnants, pour le message
    for cle in mises:  # on regarde chaque mise posée
        pari = PARIS[cle]  # les infos du pari
        if numero in pari["numeros"]:  # le numéro sorti fait partie des numéros du pari : GAGNÉ !
            rendu = rendu + mises[cle] * (pari["paiement"] + 1)  # on rend la mise + le gain (35 contre 1 -> mise x 36)
            paris_gagnants.append(pari["nom"])  # on ajoute ce pari à la liste des gagnants
    etat["solde"] = etat["solde"] + rendu  # l'argent gagné arrive dans la poche du joueur
    bilan = rendu - mise_totale  # le gain (ou la perte) réel de ce tour

    historique.insert(0, numero)  # .insert(0, ...) ajoute le numéro au DÉBUT de la liste
    if len(historique) > TAILLE_HISTORIQUE:  # si la liste est trop longue...
        historique.pop()  # ...on enlève le dernier élément (le plus ancien)

    derniere_mise.clear()  # on oublie l'ancienne "dernière mise"...
    derniere_mise.update(mises)  # ...et on retient celle de ce tour (pour le bouton Remiser)
    mises.clear()  # le croupier ramasse tous les jetons du tapis

    etat["dernier_numero"] = numero  # le numéro sorti sera encadré en doré
    etat["en_rotation"] = False  # la roue est arrêtée : on peut de nouveau miser
    etat["angle_roue"] = etat["angle_roue"] % 360  # on ramène l'angle entre 0 et 360 (même position, nombre plus petit)
    etat["tours"] = etat["tours"] + 1  # un tour de plus a été joué

    texte = f"Le {decrire_numero(numero)} !\n"  # \n = retour à la ligne
    if bilan > 0:  # le joueur a gagné plus qu'il n'a misé
        texte = texte + f"GAGNÉ : +{bilan} €  ({', '.join(paris_gagnants)})"  # ', '.join(liste) colle les éléments de la liste avec des virgules
    elif rendu > 0:  # il a récupéré un peu d'argent, mais moins que sa mise
        texte = texte + f"Tu récupères {rendu} €, mais tu perds {-bilan} € sur ce tour."  # -bilan rend le nombre positif
    else:  # aucun pari gagnant
        texte = texte + f"Perdu : -{mise_totale} €. Retente ta chance !"  # perte totale de la mise
    if etat["solde"] == 0:  # plus un sou...
        texte = texte + "\nTu es ruiné ! Clique sur « Nouvelle partie »."  # ...partie terminée
    message(texte)  # on affiche le message
    mettre_a_jour_affichage()  # on rafraîchit tout l'écran


# -----------------------------------------------------------------------------
#  9) LA CRÉATION DE LA FENÊTRE ET DE TOUS SES ÉLÉMENTS
# -----------------------------------------------------------------------------

def creer_bouton(parent, texte, action, couleur):  # pour ne pas répéter 4 fois le même code
    """Crée un bouton du panneau de droite avec un style commun."""  # docstring
    bouton = tk.Button(parent, text=texte, command=action,  # command = la fonction appelée quand on clique (sans parenthèses !)
                       font=POLICE_BOUTON, bg=couleur, fg="#ffffff",  # police, couleur de fond, couleur du texte
                       activebackground=COULEURS["or"], activeforeground="#000000",  # couleurs quand on appuie dessus
                       relief="flat", padx=10, pady=4,  # bouton plat, avec un peu d'espace autour du texte
                       cursor="hand2", takefocus=0)  # curseur en forme de main ; takefocus=0 évite que ESPACE "clique" le bouton
    bouton.pack(side="left", padx=4)  # on range les boutons de gauche à droite
    return bouton  # on renvoie le bouton pour pouvoir le ranger dans "ui"


def creer_interface():  # pas de paramètre
    """Crée la fenêtre, la roue, le panneau d'informations, les boutons et le tapis."""  # docstring
    fenetre = tk.Tk()  # la fenêtre principale du programme
    fenetre.title("Roulette de casino")  # le titre dans la barre de la fenêtre
    fenetre.configure(bg=COULEURS["fond"])  # couleur de fond de la fenêtre
    fenetre.resizable(False, False)  # on interdit de redimensionner la fenêtre (sinon le dessin serait décalé)
    ui["fenetre"] = fenetre  # on la range dans le dictionnaire ui

    # --- Partie du haut : la roue à gauche, le panneau d'informations à droite ---
    haut = tk.Frame(fenetre, bg=COULEURS["fond"])  # un Frame est une "boîte" invisible qui regroupe des éléments
    haut.pack(side="top", fill="x", padx=10, pady=(10, 0))  # en haut de la fenêtre, avec des marges

    ui["roue"] = tk.Canvas(haut, width=TAILLE_ROUE, height=TAILLE_ROUE,  # un Canvas est une zone où l'on peut dessiner
                           bg=COULEURS["fond"], highlightthickness=0)  # même fond que la fenêtre, sans bordure
    ui["roue"].pack(side="left")  # la roue à gauche

    panneau = tk.Frame(haut, bg=COULEURS["fond"])  # la boîte du panneau d'informations
    panneau.pack(side="left", fill="both", expand=True, padx=(16, 0))  # à droite de la roue, prend toute la place restante

    tk.Label(panneau, text="ROULETTE", font=POLICE_TITRE,  # un Label affiche un texte
             fg=COULEURS["or"], bg=COULEURS["fond"]).pack(anchor="w")  # le titre doré, collé à gauche (w = ouest)
    tk.Label(panneau, text="Roulette européenne · 37 numéros (0 à 36)", font=POLICE_PETITE,  # un sous-titre
             fg="#a9cfb5", bg=COULEURS["fond"]).pack(anchor="w", pady=(0, 8))  # en vert clair, sous le titre

    ligne_infos = tk.Frame(panneau, bg=COULEURS["fond"])  # une ligne pour le solde, la mise et le tour
    ligne_infos.pack(anchor="w", fill="x")  # sous le titre
    ui["solde"] = tk.Label(ligne_infos, font=POLICE_INFO, fg="#ffffff", bg=COULEURS["fond"])  # le solde (le texte est mis plus tard)
    ui["solde"].pack(side="left")  # à gauche
    ui["mise"] = tk.Label(ligne_infos, font=POLICE_INFO, fg=COULEURS["or"], bg=COULEURS["fond"])  # la mise en jeu
    ui["mise"].pack(side="left", padx=20)  # à côté du solde
    ui["tours"] = tk.Label(ligne_infos, font=POLICE_TEXTE, fg="#a9cfb5", bg=COULEURS["fond"])  # le numéro du tour
    ui["tours"].pack(side="right")  # tout à droite

    ligne_resultat = tk.Frame(panneau, bg=COULEURS["fond"])  # une ligne pour le résultat et l'historique
    ligne_resultat.pack(anchor="w", fill="x", pady=8)  # sous les infos
    ui["resultat"] = tk.Label(ligne_resultat, text="–", font=POLICE_RESULTAT, width=3,  # width=3 : place pour 3 caractères
                              fg="#ffffff", bg=COULEURS["tapis"],  # texte blanc sur fond vert
                              relief="ridge", bd=3)  # une bordure en relief
    ui["resultat"].pack(side="left")  # le grand numéro à gauche
    boite_historique = tk.Frame(ligne_resultat, bg=COULEURS["fond"])  # une boîte pour le titre + les pastilles
    boite_historique.pack(side="left", padx=12)  # à droite du grand numéro
    tk.Label(boite_historique, text="Derniers numéros :", font=POLICE_PETITE,  # petit titre
             fg="#a9cfb5", bg=COULEURS["fond"]).pack(anchor="w")  # au-dessus des pastilles
    ui["historique"] = tk.Canvas(boite_historique, width=TAILLE_HISTORIQUE * 30, height=34,  # assez large pour 10 pastilles
                                 bg=COULEURS["fond"], highlightthickness=0)  # même fond, sans bordure
    ui["historique"].pack(anchor="w")  # sous le petit titre

    ui["message"] = tk.Label(panneau, text="", font=POLICE_TEXTE, fg="#ffffff",  # la zone des messages
                             bg="#0a5226", justify="left", anchor="nw",  # texte aligné en haut à gauche
                             wraplength=420, height=3, padx=8, pady=6)  # retour à la ligne automatique, 3 lignes de haut
    ui["message"].pack(fill="x", pady=(0, 8))  # prend toute la largeur du panneau

    tk.Label(panneau, text="Choisis ton jeton :", font=POLICE_TEXTE,  # titre du sélecteur de jetons
             fg="#ffffff", bg=COULEURS["fond"]).pack(anchor="w")  # collé à gauche
    ui["jetons"] = tk.Canvas(panneau, width=len(JETONS) * 56 + 6, height=60,  # assez large pour les 5 jetons
                             bg=COULEURS["fond"], highlightthickness=0, cursor="hand2")  # curseur en forme de main
    ui["jetons"].pack(anchor="w")  # sous le titre
    ui["jetons"].bind("<Button-1>", clic_selecteur_jetons)  # .bind() : quand on clique (bouton 1 = gauche), appeler cette fonction

    ligne_boutons = tk.Frame(panneau, bg=COULEURS["fond"])  # une ligne pour les 4 boutons
    ligne_boutons.pack(anchor="w", pady=(6, 4))  # sous le sélecteur de jetons
    ui["bouton_lancer"] = creer_bouton(ligne_boutons, "LANCER", lancer, "#b7950b")  # le bouton principal, doré
    ui["bouton_effacer"] = creer_bouton(ligne_boutons, "Effacer", effacer_mises, "#7b241c")  # rouge foncé
    ui["bouton_remiser"] = creer_bouton(ligne_boutons, "Remiser", remiser, "#1f618d")  # bleu
    ui["bouton_nouvelle"] = creer_bouton(ligne_boutons, "Nouvelle partie", nouvelle_partie, "#4d5656")  # gris

    tk.Label(panneau, text="Clic gauche : poser un jeton · Clic droit : le retirer · Espace : lancer",  # aide
             font=POLICE_PETITE, fg="#a9cfb5", bg=COULEURS["fond"]).pack(anchor="w")  # en petit, en vert clair

    # --- Partie du bas : le tapis de jeu ---
    ui["tapis"] = tk.Canvas(fenetre, width=LARGEUR_TAPIS, height=HAUTEUR_TAPIS,  # la zone de dessin du tapis
                            bg=COULEURS["tapis"], highlightthickness=2,  # fond vert tapis
                            highlightbackground=COULEURS["or"], cursor="hand2")  # bordure dorée, curseur en main
    ui["tapis"].pack(side="top", padx=10, pady=10)  # sous la partie du haut
    ui["tapis"].bind("<Button-1>", clic_gauche_tapis)  # clic gauche = poser un jeton
    ui["tapis"].bind("<Button-3>", clic_droit_tapis)  # clic droit = retirer (Windows et Linux)
    ui["tapis"].bind("<Button-2>", clic_droit_tapis)  # sur Mac, le clic droit s'appelle parfois "Button-2"
    ui["tapis"].bind("<Motion>", survol_tapis)  # la souris bouge sur le tapis
    ui["tapis"].bind("<Leave>", sortie_tapis)  # la souris sort du tapis

    fenetre.bind("<space>", touche_espace)  # la barre espace lance la roue, où que soit la souris


def main():  # la fonction principale : c'est elle qui démarre tout
    """Prépare les paris, crée la fenêtre, dessine tout et lance la boucle du jeu."""  # docstring
    construire_paris()  # 1. on remplit les dictionnaires PARIS et ZONES
    creer_interface()  # 2. on crée la fenêtre et ses éléments
    dessiner_roue()  # 3. on dessine la roue une première fois
    message(f"Bienvenue au casino ! Tu as {SOLDE_DEPART} €. Choisis un jeton, "  # 4. le message d'accueil...
            "pose-le sur le tapis, puis appuie sur LANCER.")  # ...(deux textes collés l'un à l'autre font un seul texte)
    mettre_a_jour_affichage()  # 5. on affiche le solde, le tapis, les jetons...
    ui["fenetre"].mainloop()  # 6. la "boucle principale" : Tkinter attend les clics jusqu'à ce qu'on ferme la fenêtre


if __name__ == "__main__":  # cette condition est vraie seulement quand on lance CE fichier directement (pas quand on l'importe)
    main()  # on démarre le jeu
