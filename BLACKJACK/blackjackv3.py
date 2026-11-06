import random
import pygame

# Initialisation de Pygame
pygame.init()

# Création de la fenêtre
LARGEUR = 1000
HAUTEUR = 700
ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Jeu blackjack")

# Couleurs
VERT = (20, 110, 60)
VERT_FONCE = (12, 75, 42)
BLANC = (255, 255, 255)
NOIR = (20, 20, 20)
OR = (240, 190, 70)
BLEU = (40, 80, 160)

# Polices d'écriture
police_titre = pygame.font.SysFont("arial", 48, bold=True)
police_texte = pygame.font.SysFont("arial", 27)
police_carte = pygame.font.SysFont("arial", 27, bold=True)
police_resultat = pygame.font.SysFont("arial", 32, bold=True)
police_bouton = pygame.font.SysFont("arial", 25, bold=True)

horloge = pygame.time.Clock()

# Liste des cartes et valeurs des figures
cartes = [
    2, 3, 4, 5, 6, 7, 8, 9, 10,
    "As", "Valet", "Roi", "Dame"
]

valeurs_cartes = {
    "Valet": 10,
    "Dame": 10,
    "Roi": 10,
    "As": 11
}

# Multiplicateurs des gains selon le résultat
multiplicateurs_gains = {
    "victoire": 2,
    "blackjack": 2.5,
    "egalite": 1,
    "defaite": 0
}


# Fonction qui calcule les points d'une main
def calculer_points(main):
    x = 0
    nombre_as = 0

    for carte in main:
        if isinstance(carte, int):
            x += carte
        elif carte == "As":
            x += 11
            nombre_as += 1
        else:
            x += valeurs_cartes[carte]

    # L'as passe de 11 à 1 si le joueur dépasse 21
    while x > 21 and nombre_as > 0:
        x -= 10
        nombre_as -= 1

    return x


# Création des boutons
bouton_hit = pygame.Rect(300, 615, 170, 55)
bouton_stand = pygame.Rect(530, 615, 170, 55)
bouton_rejouer = pygame.Rect(280, 640, 200, 50)
bouton_menu = pygame.Rect(520, 640, 200, 50)
bouton_jouer = pygame.Rect(390, 500, 220, 55)


# Fonction pour dessiner les boutons
def dessiner_bouton(texte, rectangle, couleur):
    pygame.draw.rect(ecran, couleur, rectangle, border_radius=12)
    pygame.draw.rect(ecran, BLANC, rectangle, 2, border_radius=12)

    surface_texte = police_bouton.render(texte, True, BLANC)
    position = surface_texte.get_rect(center=rectangle.center)
    ecran.blit(surface_texte, position)


# Fonction pour dessiner une carte
def dessiner_carte(x, y, valeur, cachee=False):
    largeur_carte = 90
    hauteur_carte = 125

    rectangle = pygame.Rect(x, y, largeur_carte, hauteur_carte)

    pygame.draw.rect(
        ecran,
        BLANC if not cachee else BLEU,
        rectangle,
        border_radius=8
    )

    pygame.draw.rect(
        ecran,
        NOIR if not cachee else OR,
        rectangle,
        2,
        border_radius=8
    )

    if cachee:
        texte = police_carte.render("?", True, OR)
    else:
        texte = police_carte.render(str(valeur), True, NOIR)

    ecran.blit(texte, (x + 8, y + 8))

    if cachee:
        pygame.draw.line(ecran, OR, (x + 15, y + 45), (x + 75, y + 100), 3)
        pygame.draw.line(ecran, OR, (x + 75, y + 45), (x + 15, y + 100), 3)


# Fonction pour afficher toutes les cartes d'une main
def dessiner_main(main, y, cacher_deuxieme=False):
    largeur_carte = 90
    espace = 105

    if len(main) > 1:
        espace = min(
            105,
            (840 - largeur_carte) // (len(main) - 1)
        )

    largeur_totale = largeur_carte + espace * (len(main) - 1)
    depart_x = (LARGEUR - largeur_totale) // 2

    for i, carte in enumerate(main):
        cachee = cacher_deuxieme and i == 1

        dessiner_carte(
            depart_x + i * espace,
            y,
            carte,
            cachee
        )


# Variables principales du jeu
jeu_en_cours = True
etat = "menu"
solde = 2000
mise = "100"
gain_regle = False
message_menu = ""
message_gain = ""


# Fonction qui démarre une nouvelle partie
def nouvelle_partie():
    global paquet_52_cartes
    global main_joueur, main_croupier
    global etat, resultat, perdu, gain_regle, message_gain

    gain_regle = False
    message_gain = ""
    perdu = False
    resultat = ""

    # Création et mélange du paquet de 52 cartes
    paquet_52_cartes = cartes * 4
    random.shuffle(paquet_52_cartes)

    # Distribution des cartes
    main_joueur = [
        paquet_52_cartes.pop(),
        paquet_52_cartes.pop()
    ]

    main_croupier = [
        paquet_52_cartes.pop(),
        paquet_52_cartes.pop()
    ]

    etat = "joueur"

    if calculer_points(main_joueur) > 21:
        perdu = True
        etat = "fin"
        resultat = "Tu as depasse 21 !"


# Fonction qui détermine le gagnant
def determiner_resultat():
    global resultat, etat

    points = calculer_points(main_joueur)
    points_croupier = calculer_points(main_croupier)

    if points > 21:
        resultat = "Tu as depasse 21 !"
    elif points_croupier > 21:
        resultat = "Le croupier depasse 21 : tu gagnes !"
    elif points > points_croupier:
        resultat = "Bravo, tu as gagne !"
    elif points < points_croupier:
        resultat = "Le croupier a gagne !"
    else:
        resultat = "Egalite !"

    etat = "fin"


# Fonction qui gère le tour du croupier
def tour_croupier():
    global etat, resultat

    points = calculer_points(main_joueur)

    if points > 21:
        determiner_resultat()
        return

    # Le croupier pioche jusqu'à atteindre 17 points
    while calculer_points(main_croupier) < 17:
        if len(paquet_52_cartes) == 0:
            break

        main_croupier.append(paquet_52_cartes.pop())

    determiner_resultat()


# Boucle principale du jeu
while jeu_en_cours:

    for evenement in pygame.event.get():

        if evenement.type == pygame.QUIT:
            jeu_en_cours = False

        # Gestion des clics de souris
        if evenement.type == pygame.MOUSEBUTTONDOWN and evenement.button == 1:
            position_souris = evenement.pos

            if etat == "menu":
                if bouton_jouer.collidepoint(position_souris):
                    if mise.isdigit() and 1 <= int(mise) <= 2000 and int(mise) <= solde:
                        message_menu = ""
                        mise = int(mise)
                        solde -= mise
                        nouvelle_partie()
                    else:
                        message_menu = "Mise invalide : entre 1 et 2000, sans depasser ton solde."

                elif bouton_menu.collidepoint(position_souris):
                    mise = "100"

            elif etat == "joueur":
                if bouton_hit.collidepoint(position_souris):
                    if len(paquet_52_cartes) > 0:
                        main_joueur.append(paquet_52_cartes.pop())
                        points = calculer_points(main_joueur)

                        if points > 21:
                            perdu = True
                            resultat = "Tu as depasse 21 !"
                            etat = "fin"

                elif bouton_stand.collidepoint(position_souris):
                    tour_croupier()

            elif etat == "fin":
                if bouton_rejouer.collidepoint(position_souris):
                    etat = "menu"
                    mise = "100"
                    message_menu = ""

                elif bouton_menu.collidepoint(position_souris):
                    etat = "menu"
                    mise = "100"
                    message_menu = ""

        # Saisie de la mise avec le clavier
        if evenement.type == pygame.KEYDOWN and etat == "menu":
            if evenement.key == pygame.K_BACKSPACE:
                mise = mise[:-1]
            elif evenement.unicode.isdigit() and len(mise) < 4:
                mise += evenement.unicode

    # Affichage du menu
    ecran.fill(VERT)

    if etat == "menu":
        titre = police_titre.render("BLACKJACK", True, OR)
        ecran.blit(titre, titre.get_rect(center=(LARGEUR // 2, 150)))

        texte_solde = police_texte.render("Ton solde : " + str(solde) + " euros", True, BLANC)
        ecran.blit(texte_solde, texte_solde.get_rect(center=(LARGEUR // 2, 260)))

        texte_mise = police_texte.render("Choisis ta mise (1 a 2000, solde maximum 2000) : " + str(mise), True, BLANC)
        ecran.blit(texte_mise, texte_mise.get_rect(center=(LARGEUR // 2, 330)))

        texte_clavier = police_texte.render("Tape le montant, efface avec Retour arriere, puis clique sur JOUER", True, BLANC)
        ecran.blit(texte_clavier, texte_clavier.get_rect(center=(LARGEUR // 2, 390)))

        dessiner_bouton("JOUER", bouton_jouer, BLEU)

        if message_menu:
            texte_erreur = police_texte.render(message_menu, True, OR)
            ecran.blit(texte_erreur, texte_erreur.get_rect(center=(LARGEUR // 2, 570)))

    else:
        # Gestion des gains à la fin de la partie
        if etat == "fin" and not gain_regle:
            if resultat == "Egalite !":
                type_gain = "egalite"
            elif resultat in ("Le croupier depasse 21 : tu gagnes !", "Bravo, tu as gagne !"):
                if len(main_joueur) == 2 and calculer_points(main_joueur) == 21:
                    type_gain = "blackjack"
                else:
                    type_gain = "victoire"
            else:
                type_gain = "defaite"

            argent_rendu = min(int(mise * multiplicateurs_gains[type_gain]), 2000 - solde)
            solde += argent_rendu

            if type_gain == "defaite":
                message_gain = "Partie perdue : tu perds ta mise de " + str(mise) + " euros."
            elif type_gain == "egalite":
                message_gain = "Egalite : tes " + str(argent_rendu) + " euros te sont rendus."
            elif type_gain == "blackjack":
                message_gain = "Blackjack ! Tu recuperes " + str(argent_rendu) + " euros, mise incluse."
            else:
                message_gain = "Bravo ! Tu recuperes " + str(argent_rendu) + " euros, mise incluse."

            gain_regle = True

        # Affichage de la partie
        ecran.fill(VERT)

        titre = police_titre.render("BLACKJACK", True, OR)
        ecran.blit(titre, titre.get_rect(center=(LARGEUR // 2, 50)))

        texte_argent = police_texte.render("Solde : " + str(solde) + " euros   Mise : " + str(mise) + " euros", True, BLANC)
        ecran.blit(texte_argent, (20, 80))

        texte_croupier = police_texte.render("Croupier", True, BLANC)
        ecran.blit(texte_croupier, (50, 130))

        cacher_carte = etat == "joueur"
        dessiner_main(main_croupier, 180, cacher_carte)

        if etat == "joueur":
            points_croupier = calculer_points([main_croupier[0]])
        else:
            points_croupier = calculer_points(main_croupier)

        texte_points_croupier = police_texte.render(
            "Points : " + str(points_croupier),
            True,
            BLANC
        )
        ecran.blit(texte_points_croupier, (50, 320))

        texte_joueur = police_texte.render("Joueur", True, BLANC)
        ecran.blit(texte_joueur, (50, 370))

        dessiner_main(main_joueur, 420)

        points_joueur = calculer_points(main_joueur)
        texte_points_joueur = police_texte.render(
            "Points : " + str(points_joueur),
            True,
            BLANC
        )
        ecran.blit(texte_points_joueur, (50, 560))

        if etat == "joueur":
            dessiner_bouton("HIT", bouton_hit, BLEU)
            dessiner_bouton("STAND", bouton_stand, VERT_FONCE)

        else:
            texte_resultat = police_resultat.render(resultat, True, OR)
            ecran.blit(
                texte_resultat,
                texte_resultat.get_rect(center=(LARGEUR // 2, 570))
            )

            texte_gain = police_texte.render(message_gain, True, BLANC)
            ecran.blit(texte_gain, texte_gain.get_rect(center=(LARGEUR // 2, 605)))

            dessiner_bouton("REJOUER", bouton_rejouer, BLEU)
            dessiner_bouton("MENU PRINCIPAL", bouton_menu, VERT_FONCE)

    pygame.display.flip()
    horloge.tick(60)

# Fermeture de Pygame
pygame.quit()
