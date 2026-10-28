# jeu blackjack + histoire (si je suis assez motive) 
#l'utilisation de l'ia est note avec des commentaires + j'ai utilise l'ia pour comprendre le fonctionnement du jeu blackjack
#les libraries dont on a besoin 
import random
#import pygame
#import math

# variables boolennes qu'on va utiliser apres
perdu = False
gagne = True # pas besoin 

#les differentes cartes   
cartes = [2, 3, 4, 5, 6, 7, 8, 9, 10, "As", "Valet", "Roi", "Dame"]


# Valeur des cartes qui ne sont pas un int, on va definir les variables dans ce dictionnaire
# le as vaut soit 1 soit 11, on va devoir completer cela 
valeurs_cartes = {"Valet": 10, "Dame": 10,  "Roi": 10,  "As": 11}


#cette partie jusqu'a return x est faite a l'aide de l'IA, j'ai eu du mal a attribuer 2 valeurs a l'as 
def calculer_points(cartes_main_joueur):
    x = 0
    nombre_as = 0

    for carte in cartes_main_joueur:
        if isinstance(carte, int):              #isinstance verifie si la carte est un int
            x += carte                          #ajoute a x la valeur de la carte (addition)
        elif carte == "As":                     #si la carte est un as,
            x += 11                             # on ajoute 11                                    
            nombre_as += 1                      # 0 + 1 = 1 donc le nombre as vaut 1 
        else:                                                                     
            x += valeurs_cartes[carte]          # on donne a x une valeur de valeurs_cartes 
    while x > 21 and nombre_as > 0:             
        x -= 10                                 #retire 10 pts pour faire passer un as de 11 a 1
        nombre_as -= 1                          #diminue nombre_as de 1 -1 
    return x                                    


#on va donner l'option au joueur de rejouer 
rejouer = "oui" 

while rejouer == "oui":                   #toute autre valeur que oui va arreter la boucle.


    

    #la totalite des 52 cartes du paquet 
    paquet_52_cartes = [2, 3, 4, 5, 6, 7, 8, 9, 10, "As", "Valet", "Roi", "Dame"]*4 


    # ca melange les cartes avec .shuffle() 
    random.shuffle(paquet_52_cartes)

    # on doit donner 2 cartes au joueur. j ajoute une carte a la main du joueur en l enlevant du paquet avec pop 
    main_joueur = []
    main_joueur.append(paquet_52_cartes.pop())
    main_joueur.append(paquet_52_cartes.pop())


    #on va distribuer 2 cartes du paquet au croupier 
    main_croupier = []
    main_croupier.append(paquet_52_cartes.pop())
    main_croupier.append(paquet_52_cartes.pop())


    # montrer les cartes du joueur + les points du joueur
    print("Tes cartes :", main_joueur)
    print("Tes points :", calculer_points(main_joueur))

    #demander au joueur si il veut hit ou stand et on utilise .lower pour mettre l'input en minuscule pour eviter des erreurs 
    choix = input("Tu veux hit ou stand ? ").lower()

    while choix not in ["hit", "stand"]:                # Utilisation 
        print("Choix invalide !")                       # IA
        choix = input("Tu veux hit ou stand ? ").lower()# cela sert a accepter que les mots hit ou stand et rejeter toutes les autres input


    while choix == "hit":
        main_joueur.append(paquet_52_cartes.pop())
    
        print("Tes cartes :", main_joueur)
        points = calculer_points(main_joueur)
        print("Tes points :", points)
        # on ne doit pas depasser 21 points pour gagner en tant que joueur. 
        if points > 21:
            print("ahahah tu as perdu.")
            perdu = True            
            break #arreter la boucle

        choix = input("Tu veux hit ou stand ? ").lower()

        while choix not in ["hit", "stand"]:                # partie IA utilise auparavant 
            print("Choix invalide !")                       #
            choix = input("Tu veux hit ou stand ? ").lower()#

    if choix == "stand" and not perdu: # continuer SSI  perdu = false 
        print("hm ok tu restes")
        points_croupier = calculer_points(main_croupier)
        print("Points du croupier :", points_croupier)
        #les points du croupier ne doivent pas depasser 17 c'est une regle de jeu
    
        while points_croupier < 17:
            main_croupier.append(paquet_52_cartes.pop())
            points_croupier = calculer_points(main_croupier)
         

    # maintenant on va determiner le gagnant 
    # la variable points c'est les points du joueur et points_croupier les points du croupier
    points = calculer_points(main_joueur)
    points_croupier = calculer_points(main_croupier)


    # celui qui a le plus de points mais qui ne depasse pas 21 gagne
    if perdu:
        pass    # si on a perdu on arrete simplement
    elif points > 21:
        print("trop nul")
    elif points_croupier > 21:
        print("Yooo, tu as gagne !")
    elif points > points_croupier:
        print('Yooo, tu as gagne !')
    elif points < points_croupier:
        print("trop nul")
    else:
        print("Egalite !")

    # demander au joueur s'il veut rejouer
    rejouer = input("Tu veux rejouer ? ").lower()
