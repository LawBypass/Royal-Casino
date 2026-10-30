
# jeu blackjack + histoire (si je suis assez motive)
# J'ai utilise l'IA pour comprendre le fonctionnement du blackjack
# et pour m'aider a creer l'interface graphique et bcp de choses avec pygame surtout les modules.

import random
import pygame
import math


#initialise les modules de Pygame necessaires au fonctionnement du jeu.
pygame.init()



# Creer la fenetre 1000x700
LARGEUR = 1000
HAUTEUR = 700
#surface jeu par la variable ecran
ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))

#titre du jeu
pygame.display.set_caption("Jeu blackjack")

# chaque couleur est definie par 3 nombres, rouge vert bleu.
VERT = (20, 110, 60)
VERT_FONCE = (12, 75, 42)
BLANC = (255, 255, 255)
NOIR = (20, 20, 20)
OR = (240, 190, 70)
#GRIS = (190, 190, 190) pas besoin de l'utiliser
BLEU = (40, 80, 160)

# Les polices
# arial = nom de la police, 48 la taille, bold = gras
police_titre = pygame.font.SysFont("arial", 48, bold=True)
police_texte = pygame.font.SysFont("arial", 27)
police_carte = pygame.font.SysFont("arial", 27, bold=True)
police_resultat = pygame.font.SysFont("arial", 32, bold=True)
police_bouton = pygame.font.SysFont("arial", 25, bold=True)


# Cree une horloge pour limiter la frequence de la boucle principale
horloge = pygame.time.Clock() 

# Les differentes cartes
cartes = [
    2, 3, 4, 5, 6, 7, 8, 9, 10,
    "As", "Valet", "Roi", "Dame"
]

# Valeur des cartes qui ne sont pas un int
valeurs_cartes = {
    "Valet": 10,
    "Dame": 10,
    "Roi": 10,
    "As": 11
}

# Fonction pour calculer les points
# L'As peut valoir 1 ou 11 selon la situation.

def calculer_points(main):
    x = 0
    nombre_as = 0

    for carte in main:
        if isinstance(carte, int):  #isinstance verifie si la carte est un int
            x += carte              #ajoute a x la valeur de la carte (addition)
        elif carte == "As":         #si la carte est un as,
            x += 11                 # on ajoute 11        
            nombre_as += 1          # 0 + 1 = 1 donc le nombre as vaut 1 
        else:   
            x += valeurs_cartes[carte] # on donne a x une valeur de valeurs_cartes 

    while x > 21 and nombre_as > 0:
        x -= 10                         #retire 10 pts pour faire passer un as de 11 a 1
        nombre_as -= 1                  #diminue nombre_as de 1 -1             

    return x                            # donne x 


# Les boutons de l'interface
#.rect = rectangle(position horizontale x, position verticale y,largeur,hauteur)
bouton_hit = pygame.Rect(300, 615, 170, 55)
bouton_stand = pygame.Rect(530, 615, 170, 55)
bouton_rejouer = pygame.Rect(390, 615, 220, 55)


# Fonction pour dessiner un bouton avec le texte, le rect. (position et dimension) + la couleur
def dessiner_bouton(texte, rectangle, couleur):
    
    #on dessine le rect. avec pygame.draw. border radius arrondit les coins du rectangle
    pygame.draw.rect(ecran, couleur, rectangle, border_radius=12)
    # le contour est BLANC et le nb 2 signifie l'epaisseur en pixel. 
    pygame.draw.rect(ecran, BLANC, rectangle, 2, border_radius=12)
    
    #Cette ligne transforme le texte en une surface graphique que Pygame peut afficher.
    surface_texte = police_bouton.render(texte, True, BLANC)
    #Cette instruction calcule un rectangle correspondant au texte,
    # puis place son centre au meme endroit que le centre du bouton.
    position = surface_texte.get_rect(center=rectangle.center)
    # blit permet de dessiner une surface sur une autre. le programme affiche le texte sur la fenetre
    ecran.blit(surface_texte, position)


# Fonction pour dessiner une carte
def dessiner_carte(x, y, valeur, cachee=False):     #dessiner une carte sur l'ecran avec ses coordonnees, la valeur de la carte et en indiquant si la carte doit etre cachee
    largeur_carte = 90                              
    hauteur_carte = 125 

    rectangle = pygame.Rect(                    #on dessine le rectangle donc la carte
        x, y, largeur_carte, hauteur_carte      
    )

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
        pygame.draw.line(
            ecran, OR,
            (x + 15, y + 45),
            (x + 75, y + 100), 3
        )
        pygame.draw.line(
            ecran, OR,
            (x + 75, y + 45),
            (x + 15, y + 100), 3
        )


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


# Variables du jeu
rejouer = True
jeu_en_cours = True

# Ajouter le solde et la mise
solde = 100
mise = 10
mise_reglee = False


# Demarrer une nouvelle partie
def nouvelle_partie():
    global paquet_52_cartes
    global main_joueur, main_croupier
    global etat, resultat, perdu
    global solde, mise_reglee

    # Verifier si le joueur a assez d'argent
    if solde < mise:
        etat = "fin"
        resultat = "Solde insuffisant !"
        return

    # Retirer la mise au debut de la partie
    solde -= mise
    mise_reglee = False

    perdu = False
    resultat = ""

    # Les 52 cartes du paquet
    paquet_52_cartes = cartes * 4

    random.shuffle(paquet_52_cartes)

    # Distribuer deux cartes au joueur
    main_joueur = [
        paquet_52_cartes.pop(),
        paquet_52_cartes.pop()
    ]

    # Distribuer deux cartes au croupier
    main_croupier = [
        paquet_52_cartes.pop(),
        paquet_52_cartes.pop()
    ]

    # Le joueur commence
    etat = "joueur"

    # Verifier si le joueur a depasse 21
    if calculer_points(main_joueur) > 21:
        perdu = True
        determiner_resultat()


# Regler la mise a la fin de la partie
def regler_mise():
    global solde, mise_reglee

    if mise_reglee:
        return

    if resultat == "Egalite !":
        solde += mise
    elif resultat in [
        "Bravo, tu as gagne !",
        "Le croupier depasse 21 : tu gagnes !"
    ]:
        solde += mise * 2

    mise_reglee = True


# Determiner le gagnant
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

    # Ajouter les gains ou rendre la mise
    regler_mise()


# Tour du croupier
def tour_croupier():
    global etat, resultat

    points = calculer_points(main_joueur)

    if points > 21:
        determiner_resultat()
        return

    # Le croupier tire tant qu'il a moins de 17 points
    while calculer_points(main_croupier) < 17:
        if len(paquet_52_cartes) == 0:
            break

        main_croupier.append(paquet_52_cartes.pop())

    determiner_resultat()


# Lancer la premiere partie
nouvelle_partie()


# Boucle principale de Pygame
while jeu_en_cours:

    for evenement in pygame.event.get():

        if evenement.type == pygame.QUIT:
            jeu_en_cours = False

        # Detecter les clics de souris
        if evenement.type == pygame.MOUSEBUTTONDOWN:
            if evenement.button == 1:

                position_souris = evenement.pos

                # Le joueur peut jouer son tour
                if etat == "joueur":

                    if bouton_hit.collidepoint(position_souris):
                        if len(paquet_52_cartes) > 0:
                            main_joueur.append(
                                paquet_52_cartes.pop()
                            )

                            points = calculer_points(main_joueur)

                            if points > 21:
                                perdu = True
                                determiner_resultat()

                    elif bouton_stand.collidepoint(position_souris):
                        tour_croupier()

                # Rejouer apres la fin de la partie
                elif etat == "fin":
                    if bouton_rejouer.collidepoint(position_souris):
                        nouvelle_partie()

    # Dessiner le fond
    ecran.fill(VERT)

    # Titre
    titre = police_titre.render("BLACKJACK", True, OR)
    ecran.blit(
        titre,
        titre.get_rect(center=(LARGEUR // 2, 50))
    )

    # Ligne decorative
    pygame.draw.line(
        ecran, OR, (100, 90), (900, 90), 2
    )

    # Afficher le croupier
    texte_croupier = police_texte.render(
        "CROUPIER", True, BLANC
    )
    ecran.blit(texte_croupier, (80, 115))

    # Cacher la deuxieme carte pendant le tour du joueur
    cacher_carte = etat == "joueur"

    dessiner_main(
        main_croupier,
        155,
        cacher_deuxieme=cacher_carte
    )

    # Afficher les points du croupier
    if cacher_carte:
        points_croupier = calculer_points([main_croupier[0]])
        texte_points = "Points visibles : " + str(points_croupier)
    else:
        points_croupier = calculer_points(main_croupier)
        texte_points = "Points : " + str(points_croupier)

    surface_points = police_texte.render(
        texte_points, True, BLANC
    )
    ecran.blit(surface_points, (80, 295))

    # Afficher le joueur
    texte_joueur = police_texte.render(
        "JOUEUR", True, BLANC
    )
    ecran.blit(texte_joueur, (80, 345))

    dessiner_main(main_joueur, 385)

    points_joueur = calculer_points(main_joueur)
    surface_points_joueur = police_texte.render(
        "Tes points : " + str(points_joueur),
        True,
        BLANC
    )
    ecran.blit(surface_points_joueur, (80, 525))

    # Afficher le solde et la mise
    texte_solde = police_texte.render(
        "Solde : " + str(solde) + " euros", True, OR
    )
    ecran.blit(texte_solde, (700, 525))

    texte_mise = police_texte.render(
        "Mise : " + str(mise) + " euros", True, OR
    )
    ecran.blit(texte_mise, (700, 560))

    # Afficher les boutons selon l'etat du jeu
    if etat == "joueur":
        dessiner_bouton("HIT", bouton_hit, BLEU)
        dessiner_bouton("STAND", bouton_stand, VERT_FONCE)

    elif etat == "fin":
        couleur_resultat = OR

        texte_resultat = police_resultat.render(
            resultat, True, couleur_resultat
        )
        position_resultat = texte_resultat.get_rect(
            center=(LARGEUR // 2, 580)
        )
        ecran.blit(texte_resultat, position_resultat)

        dessiner_bouton(
            "REJOUER",
            bouton_rejouer,
            VERT_FONCE
        )

    pygame.display.flip()
    horloge.tick(60)


pygame.quit()
