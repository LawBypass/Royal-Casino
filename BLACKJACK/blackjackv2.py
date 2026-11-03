# jeu blackjack + histoire (si je suis assez motive)
# j'ai utilise l'ia pour comprendre le fonctionnement du blackjack
# et pour m'aider a creer l'interface graphique et bcp de choses avec pygame surtout les modules.
#presence excessive de commentaires en raison de la difficulte de comprehension

import random
import pygame
#import math (pas besoin pour le moment)


#initialise les modules de pygame necessaires au fonctionnement du jeu.
pygame.init()



# creer la fenetre 1000x700
LARGEUR = 1000
HAUTEUR = 700
#surface jeu par la variable ecran
ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))

#titre du jeu avec la fonction .set_caption
pygame.display.set_caption("Jeu blackjack")

# chaque couleur est definie par 3 nombres, rouge vert bleu.
#definit les couleurs utilisees dans le jeu avec les valeurs rouge vert bleu
VERT = (20, 110, 60)
VERT_FONCE = (12, 75, 42)
BLANC = (255, 255, 255)
NOIR = (20, 20, 20)
OR = (240, 190, 70)
BLEU = (40, 80, 160)

# les polices
# arial = nom de la police, 48 la taille, bold = gras
police_titre = pygame.font.SysFont("arial", 48, bold=True) 

police_texte = pygame.font.SysFont("arial", 27)

police_carte = pygame.font.SysFont("arial", 27, bold=True)

police_resultat = pygame.font.SysFont("arial", 32, bold=True)

police_bouton = pygame.font.SysFont("arial", 25, bold=True)


# cree une horloge pour limiter la frequence de la boucle principale (on va utiliser cela apres)
horloge = pygame.time.Clock() 

# les differentes cartes
#liste les valeurs possibles des cartes dans le jeu
cartes = [
    2, 3, 4, 5, 6, 7, 8, 9, 10,
    "As", "Valet", "Roi", "Dame"
]

# valeur des cartes qui ne sont pas un int
#associe un int aux cartes qui sont des variables 
valeurs_cartes = {
    "Valet": 10,
    "Dame": 10,
    "Roi": 10,
    "As": 11
}

# multiplicateurs des gains selon les cartes et le resultat.
# 2 = mise rendue + meme somme gagnee ; 2.5 = blackjack naturel (gain de 3:2).
multiplicateurs_gains = {
    "victoire": 2,
    "blackjack": 2.5,
    "egalite": 1,
    "defaite": 0
}

# fonction pour calculer les points
# l'as peut valoir 1 ou 11

#fonction qui calcule le total des points d'une main
def calculer_points(main):          #le calcul des points pour la main du joueur
    x = 0               #valeur de depart
    nombre_as = 0       #valeur de depart

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


# les boutons de l'interface
#.rect = rectangle(position horizontale x, position verticale y,largeur,hauteur)
#cree le rectangle du bouton pour hit, stand, rejouer
bouton_hit = pygame.Rect(300, 615, 170, 55)
bouton_stand = pygame.Rect(530, 615, 170, 55)
bouton_rejouer = pygame.Rect(280, 640, 200, 50) # recommencer en repassant par le choix de mise
bouton_menu = pygame.Rect(520, 640, 200, 50) # revenir au menu principal
bouton_jouer = pygame.Rect(390, 500, 220, 55) # valider la mise et commencer


#  def fonction pour dessiner un bouton avec le texte, le rect. (position et dimension) + la couleur
    #fonction qui dessine un bouton avec son texte sa position et sa couleur
def dessiner_bouton(texte, rectangle, couleur):

    #on dessine le rect. avec pygame.draw. border radius arrondit les coins du rectangle
    pygame.draw.rect(ecran, couleur, rectangle, border_radius=12)
    # le contour est blanc et le nombre 2 signifie l'epaisseur en pixels. 
    pygame.draw.rect(ecran, BLANC, rectangle, 2, border_radius=12)

    #cette ligne transforme le texte en une surface graphique que pygame peut afficher.
    surface_texte = police_bouton.render(texte, True, BLANC)
    #cette instruction calcule un rectangle correspondant au texte,
    # puis place son centre au meme endroit que le centre du bouton.
    position = surface_texte.get_rect(center=rectangle.center)
    # blit permet de dessiner une surface sur une autre. le programme affiche le texte sur la fenetre
    ecran.blit(surface_texte, position)


# fonction pour dessiner une carte
def dessiner_carte(x, y, valeur, cachee=False):     #dessiner la carte blanche sur l'ecran avec ses coordonnees, la valeur de la carte et en indiquant si la carte doit etre cachee
    largeur_carte = 90                              #hauteur et largeur carte en pixels
    hauteur_carte = 125         

    rectangle = pygame.Rect(                    
        x, y, largeur_carte, hauteur_carte     #definition de la variable rectangle
    )

    pygame.draw.rect(                             #on dessine la carte 
        ecran,                                     #on dessine sur la fenetre ecran
        BLANC if not cachee else BLEU,              #blanc si visible sinon bleu 
        rectangle,                                  #correspond a la variable precedente 
        border_radius=8                             #arrondit les coins 
    )

    pygame.draw.rect(   
        ecran,                                  #idem 
        NOIR if not cachee else OR,             # noir si visible sinon or ( la couleur)
        rectangle,                               #correspond a la variable precedente 
        2,                                       #2 pixels de large pour les contours
        border_radius=8                         #arrondit les coins 
    )
    # si la carte est cachee, on affiche un point d'interrogation
    if cachee:                  
        texte = police_carte.render("?", True, OR)     
    # sinon on affiche la valeur de la carte en noir

    else:
        texte = police_carte.render(str(valeur), True, NOIR) #str transforme la valeur de la carte en texte car render attend du texte 
    #blit permet de placer un element sur l'ecran. on place la variable texte qu'on vient de creer de 8 pixels sur les 2 axes x,y
    ecran.blit(texte, (x + 8, y + 8))

    if cachee:              #si la carte est cachee 
        pygame.draw.line(   # .line: (surface, color, start pos, end pos, width)
                            #donc ecran, or puis le point d'arrive et fin et enfin l'epaisseur de 3 pixels
            ecran, OR,      
            (x + 15, y + 45),
            (x + 75, y + 100), 3    # 3 correspond a l epaisseur 
        )
        pygame.draw.line(
            ecran, OR,              #idem qu'avant
            (x + 75, y + 45),
            (x + 15, y + 100), 3
        )


# def fonction pour afficher toutes les cartes d'une main
def dessiner_main(main, y, cacher_deuxieme=False):      #y = pos verticale et la 2e carte n'est pas cache
    largeur_carte = 90
    espace = 105        #les cartes sont espacees de 105 pixels au depart.

    if len(main) > 1: #si le nb de cartes > 1 dans la main
        espace = min(      #choisit la valeur la plus petite des 2 valeurs pour eviter que les cartes soient trop espacees 
            105,
            (840 - largeur_carte) // (len(main) - 1) #CALCULE l'espace maximal entre les cartes pour qu'elles rentrent dans une zone de 840 pixels
        )

    largeur_totale = largeur_carte + espace * (len(main) - 1)   #calcule la largeur occupe par toutes les cartes + l'espace entre elles 
    depart_x = (LARGEUR - largeur_totale) // 2                  #calcule la largeur occupe par toutes les cartes pour centrer la main sur l'ecran

    for i, carte in enumerate(main):             #enumerate prend la valeur de la carte et son numero                         
        cachee = cacher_deuxieme and i == 1      # verifie si la carte doit etre cachee cacher_deuxieme doit etre vrai et i doit valoir 1
                                                # i == 1 signifie qu'on est sur la deuxieme carte car ca commence a 0

        dessiner_carte(
            depart_x + i * espace,  # calcule la position horizontale de la carte
            y,                       # donne la position verticale de la carte
            carte,                   # indique la valeur de la carte a afficher
            cachee                   # indique si la carte doit etre cachee ou visible
        )


# variable du jeu (boolenne)
# Cette variable permet de continuer la boucle tant que la fenetre est ouverte.
jeu_en_cours = True
etat = "menu"                 # indique si on est dans le menu, le tour du joueur ou la fin
solde = 2000                  # argent fictif de depart du joueur (2000 maximum)
mise = "100"                  # mise saisie au clavier ; elle reste du texte dans le menu
gain_regle = False            # verifie si les gains ont deja ete calcules
message_menu = ""             # message affiche dans le menu en cas de mise invalide
message_gain = ""             # phrase qui explique les gains a la fin de la partie


# demarrer une nouvelle partie
def nouvelle_partie():
    # global permet de modifier les variables creees en dehors de cette fonction.
    # Ici, on remet aussi le paiement a zero pour la nouvelle partie.
    global paquet_52_cartes #global permet d'utiliser et de modifier la carte en dehors de la fonction 
    global main_joueur, main_croupier
    global etat, resultat, perdu, gain_regle, message_gain

    # chaque nouvelle partie doit pouvoir regler ses gains une seule fois
    gain_regle = False
    message_gain = ""
    perdu = False
    resultat = "" #

    # les 52 cartes du paquet = les 13 cartes x 4 
    paquet_52_cartes = cartes * 4
    #melange le paquet
    random.shuffle(paquet_52_cartes)

    # distribuer deux cartes au joueur
    main_joueur = [
        paquet_52_cartes.pop(),
        paquet_52_cartes.pop()
    ]

    # distribuer deux cartes au croupier
    main_croupier = [
        paquet_52_cartes.pop(),
        paquet_52_cartes.pop()
    ]

    # le joueur commence
    etat = "joueur"         # indique que c'est au joueur de jouer

    # verifier si le joueur a depasse 21
    if calculer_points(main_joueur) > 21:
        perdu = True
        etat = "fin"            #fin du jeu 
        resultat = "Tu as depasse 21 !"


# determiner le gagnant
    #fonction qui compare les points du joueur et du croupier pour definir le resultat
def determiner_resultat():
    # Cette fonction compare les points des deux mains et termine la partie.
    global resultat, etat  #global permet d'utiliser et de modifier la carte en dehors de la fonction 

    points = calculer_points(main_joueur)      #on calcule les points de la main du joueur 
    points_croupier = calculer_points(main_croupier) #on calcule les points de la main du croupier 

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

    etat = "fin" #fin du jeu 


# tour du croupier
    #fonction qui gere le tour du croupier
def tour_croupier():
    # Le croupier pioche jusqu'a atteindre au moins 17 points.
    global etat, resultat #global permet d'utiliser et de modifier la carte en dehors de la fonction  TRESS UTILE

    points = calculer_points(main_joueur)

    if points > 21:
        determiner_resultat()
        return

    # le croupier tire tant qu'il a moins de 17 points
    while calculer_points(main_croupier) < 17:
        if len(paquet_52_cartes) == 0: #si le paquet de carte est vide
            break #fin de la while loop / on arrete

        main_croupier.append(paquet_52_cartes.pop()) #on ajoute une carte a la main du croupier/ on enleve une carte du paquet

    determiner_resultat() # compare les points du joueur et du croupier pour determiner le gagnant (voir def determiner_resultat)


# lancer la premiere partie
# le joueur choisit sa mise dans le menu avant de commencer


# boucle principale de pygame
#repete la boucle principale tant que le jeu est ouvert
# boucle principale de pygame
while jeu_en_cours:  # repete le code tant que le jeu est ouvert

    for evenement in pygame.event.get():
        # recupere les evenements de pygame

        if evenement.type == pygame.QUIT:
            jeu_en_cours = False  # arreter la boucle principale si le joueur ferme la fenetre

        # detecter les clics de souris
        if evenement.type == pygame.MOUSEBUTTONDOWN and evenement.button == 1:
            position_souris = evenement.pos

            if etat == "menu":
                # Dans le menu, le joueur peut lancer une partie avec la mise saisie.
                if bouton_jouer.collidepoint(position_souris):
                    # On accepte uniquement un nombre entre 1 et 2000,
                    # et le joueur ne peut pas miser plus que son solde.
                    if mise.isdigit() and 1 <= int(mise) <= 2000 and int(mise) <= solde:
                        message_menu = ""
                        mise = int(mise)       # transforme le texte saisi en nombre
                        solde -= mise           # la mise est retiree avant de jouer
                        nouvelle_partie()      # distribue les cartes et lance la partie
                    else:
                        message_menu = "Mise invalide : entre 1 et 2000, sans depasser ton solde."
                elif bouton_menu.collidepoint(position_souris):
                    # Le bouton dans le menu remet simplement la mise proposee par defaut.
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

        # choisir la mise avec le clavier dans le menu
        # Retour arriere efface le dernier chiffre ; les chiffres sont limites a 4 caracteres.
        if evenement.type == pygame.KEYDOWN and etat == "menu":
            if evenement.key == pygame.K_BACKSPACE:
                mise = mise[:-1]
            elif evenement.unicode.isdigit() and len(mise) < 4:
                mise += evenement.unicode  # ajoute le chiffre a la fin de la mise

    # PARTIE AFFICAGE DU JEU

    # dessiner le fond vert
    ecran.fill(VERT)

    if etat == "menu":
        titre = police_titre.render("BLACKJACK", True, OR)
        ecran.blit(titre, titre.get_rect(center=(LARGEUR // 2, 150)))

        # Le menu montre l'argent disponible avant de choisir la mise.
        texte_solde = police_texte.render("Ton solde : " + str(solde) + " euros", True, BLANC)
        ecran.blit(texte_solde, texte_solde.get_rect(center=(LARGEUR // 2, 260)))

        # La mise est encore du texte ici, car le joueur la tape au clavier.
        texte_mise = police_texte.render("Choisis ta mise (1 a 2000, solde maximum 2000) : " + str(mise), True, BLANC)
        ecran.blit(texte_mise, texte_mise.get_rect(center=(LARGEUR // 2, 330)))

        texte_clavier = police_texte.render("Tape le montant, efface avec Retour arriere, puis clique sur JOUER", True, BLANC)
        ecran.blit(texte_clavier, texte_clavier.get_rect(center=(LARGEUR // 2, 390)))

        dessiner_bouton("JOUER", bouton_jouer, BLEU)
        if message_menu:
            texte_erreur = police_texte.render(message_menu, True, OR)
            ecran.blit(texte_erreur, texte_erreur.get_rect(center=(LARGEUR // 2, 570)))

    else:
        # regler les gains une seule fois a la fin de la partie
        # gain_regle evite de donner les gains a chaque tour de la boucle principale.
        if etat == "fin" and not gain_regle:
            # On choisit le multiplicateur selon le resultat et les cartes du joueur.
            if resultat == "Egalite !":
                type_gain = "egalite"
            elif resultat in ("Le croupier depasse 21 : tu gagnes !", "Bravo, tu as gagne !"):
                if len(main_joueur) == 2 and calculer_points(main_joueur) == 21:
                    type_gain = "blackjack"  # As + carte valant 10 des les deux premieres cartes
                else:
                    type_gain = "victoire"
            else:
                type_gain = "defaite"

            # Formule unique : mise x multiplicateur, sans depasser le solde maximum.
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


        # dessiner le fond vert
        ecran.fill(VERT) #.fill sert a remplir l'ecran

        # afficher le titre
        titre = police_titre.render("BLACKJACK", True, OR)   # on affiche le titre "blackhack" avec la couleur comme background "or"
        ecran.blit(titre, titre.get_rect(center=(LARGEUR // 2, 50)))   #affiche le titre blackjack en le placant au centre de l'ecran (largeur // 2) puis 50 pixel de haut 

        # afficher le solde et la mise
        # Le solde a deja ete diminue du montant mise au debut de la partie.
        texte_argent = police_texte.render("Solde : " + str(solde) + " euros   Mise : " + str(mise) + " euros", True, BLANC)
        ecran.blit(texte_argent, (20, 80))

        # afficher le croupier
        texte_croupier = police_texte.render("Croupier", True, BLANC)   #on affiche Croupier avec le background en blanc
        ecran.blit(texte_croupier, (50, 130)) #afficher le texte_croupier sur l'ecran aux coords 50 130 

        # cacher la deuxieme carte du croupier pendant le tour du joueur
        cacher_carte = etat == "joueur"
        dessiner_main(main_croupier, 180, cacher_carte) #affiche les cartes du croupier à partir de la position verticale 180.

        # afficher les points du croupier
        if etat == "joueur": #si le joueur joue 
            points_croupier = calculer_points([main_croupier[0]])   #on prend la 1ere carte de la main et on calcule les points avec la fonction calculer_points
        else:
            points_croupier = calculer_points(main_croupier)       #sinon on calcule les points de la main du croupier

        texte_points_croupier = police_texte.render(                #on montre les points du crouper
            "Points : " + str(points_croupier),                     # on affiche points: (les points du croupier) !!!! str transforme le nombre en texte pour pouvoir l'afficher
            True,                                                   #anti aliasing == rend les contours et lettres plus lisses
            BLANC                                                    #couleur background
        )
        ecran.blit(texte_points_croupier, (50, 320))                # on render les txt_pts_crouper aux coords (50,320)

        # afficher le joueur
        texte_joueur = police_texte.render("Joueur", True, BLANC)       #on render "Joueur" avec antialiasing en blanc 
        ecran.blit(texte_joueur, (50, 370))  #montre le txt_joueur aux coords (50,370)
        #affiche les cartes du joueur aux coords y = 420 
        dessiner_main(main_joueur, 420) 

        # afficher les points du joueur
        points_joueur = calculer_points(main_joueur) #calcul des points de la main du joueur 
        texte_points_joueur = police_texte.render(              # idem que pour le croupier
            "Points : " + str(points_joueur),
            True,
            BLANC
        )
        ecran.blit(texte_points_joueur, (50, 560))          #on montre le txt_pts_joueurs aux coords (50,560)

        # afficher les boutons si le joueur peut jouer
        if etat == "joueur":                            
            dessiner_bouton("HIT", bouton_hit, BLEU) #on utilise la fonction dessiner_bouton pour dessiner le bouton hit en bleu
            dessiner_bouton("STAND", bouton_stand, VERT_FONCE) #idem

        # afficher le resultat si la partie est terminee
        else:
            texte_resultat = police_resultat.render(resultat, True, OR) #on utilis la police resultat pour montrer le resultat , avec l'antialiasing et le background en couleur or
            ecran.blit(
                texte_resultat,
                texte_resultat.get_rect(center=(LARGEUR // 2, 570)) # place le resultat au centre de l ecran
            )
            texte_gain = police_texte.render(message_gain, True, BLANC)
            ecran.blit(texte_gain, texte_gain.get_rect(center=(LARGEUR // 2, 605)))
            # REJOUER renvoie au menu pour choisir une nouvelle mise.
            dessiner_bouton("REJOUER", bouton_rejouer, BLEU) #si le joueur a perdu, on lui donne l'option de rejouer en dessinant le bouton rejouer
            dessiner_bouton("MENU PRINCIPAL", bouton_menu, VERT_FONCE)

    # actualiser l'affichage avec .flip, pour montrer tous les dessins qui viennent d'etre affichees
    pygame.display.flip()

    # limiter la vitesse a 60 fps
    horloge.tick(60) #on a cree la variable horologe en debut de programme.

# fermer pygame une seule fois, quand la boucle du jeu est terminee
pygame.quit()
