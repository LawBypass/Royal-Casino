#MACHINE A SOUS CODE 

from math import* # importe toutes les fonctions du module maths sans avoir à les appeler
from random import* # == pour le module random
from time import* # == pour le module time

gains = 2000 # temporaire car l'utilisateur va soit en gagner soit en perdre
restart = True # variable vérifiant si le joueur souhaite rejouer

while restart == True : # le code s'execute seulement si restart = True

    mise = int(input(f"Combien voulez vous miser ? (max {gains} ) : ")) # mise temporaire
    while mise > gains: # vérifier que le joueur mets un nombre inférieur
        print("Vous n'avez pas assez de monnaie !")
        mise = int(input(f"Combien voulez vous miser ? (max {gains} ) : "))  #utilisation du fstring pour ajouter la variable
    else :
        gains = gains = gains - mise

    #PARTIE A/ LANCER LA MACHINE : C'est la partie qui va aboutir au lancement du jeu elle est essentielle pour le code. 

    #1. Variable ; booléene : start_game (variable permettant de lancer le jeu) --> False donne l'information qu'au départ la variable à pour valeur Faux! 

    start_game = False 

    #2. demander à l'utilisateur de lancer la machine --> action (variable qui détermine s'il faut lancer le jeu) input permet dee demander quelque chose dans la console entre "". 

    action = input("Tapez 'a' et appuyez sur Entrée pour jouer : ") 

    #3. Vérification --> if = si, action ( donc on appelle la variable ) .lower (Transforme majuscule en minuscule évitant les erreurs) == : égal "A" alors la variable start_game prend la valeur : True (Vraie).

    if action.lower() == "a": start_game = True 

    #4. Début du jeu --> if start_game revient à si la variable à pour valeur True. alors écrire "" dans la console pour informer l'utilisateur que le jeu se lance else = sinon : le jeu ne se lance pas.

    if start_game: print("Bouton activé ! Le jeu commence...") 

    else: print("Action annulée ou incorrecte.") 

    #PARTIE B/ INITIALISATION DES SYMBOLES : cette partie initialise les différents symboles qui sont succeptibles d'être "choisi" par hasard. 

    #1. Initialisation : ICI 8 SYMBOLES QUI SERONT CHOISIS ALEATOIREMENT
    symboles = ["gem", "7", "coin", "grape", "cherry", "key", "star", "diamond"] 

    #2. Abondance : Cela détermine le nombre de fois où un symbole apparait sur 40 par exemple, sur 40 symboles, il y a 6 fois le symbole "key" autrement dit la probabilité d'obtenir la clé sur un rouleau est de 6aa/40.
    symboles = ["7"] * 1 + ["coin"] * 3 + ["gem"] * 5 + ["star"] * 4 + ["key"] * 6+ ["cherry"] * 9 + ["grape"] * 10 + ["diamond"]*2

    #PARTIE C / TIRAGE DES ROULEAUX : Cette partie est essentielle puisque c'est la base même du jeu, le tirage des symboles. 

    #1. L'aléatoire : on fait un bloc conditionel qui tire aléatoirement les symboles prenant compte de leurs abondances.

    if start_game: #si la variable est vraie : c'est à ditre si le jeu est bien lancé
        rouleau_1 = choice(symboles) #rouleau_1 (variable) = symbole aléatoire
        rouleau_2 = choice(symboles)
        rouleau_3 = choice(symboles)
    else :
        pass # si le jeu n'est pas lancé : pass permet d'effectuer aucune action 
        
    #2. Affichage des résultats : On affiche à la suite les 3 symboles obtenus.
    sleep(4) # attendre 4 seconde grâce au module time.
    print(rouleau_1, rouleau_2, rouleau_3)

    # PARTIE D / Vérifications : obtentions des gains. Cette partie est la plus complexe du code, car il faut tester de multiples conditions, et qu'il y a beaucoup de situations différentes où les gains sont différents

    #1. Transformer en dictionnaire : en effet pour se simplifier la tâche je vais non pas écrire une ligne par mais créer un dictionnaire nommé abondance.

    abondance = {"7": 1, "coin" : 3, "gem" : 5, "star" : 4, "key" : 6, "cherry": 9, "grape" : 10, "diamond" : 2}

    #2. Vérifications et gains : elles vont permettre de savoir si on a 0,2 ou 3 éléments identiques, puis donner les gains
    sleep(2)
    if rouleau_1 == rouleau_2 == rouleau_3 :
        print("Bravo vous avez gagné le gros lot : 3 éléments identiques")
        if rouleau_1 == "7":
            print("Bravo : c'est le JACKPOT : vous gagnez 3 fois votre mise en plus de la récupérer !!!!!")
            nb_abondance = abondance["7"]
            gains = gains + mise + (1/ nb_abondance) * mise * 3
            gains = round(gains) #permet d'arrondir les gains
            sleep(1)
            print("Voici vos nouveau gains", gains , "unités de monnaie.")
        else :
        # On récupère l'abondance du symbole (ex: 12 pour grape)
            nb_abondance = abondance[rouleau_1]
        
        # On applique ta formule : (1 / abondance) * mise * nombre_de_symboles (ici 3)
            gains = gains + mise + (1 / nb_abondance) * mise * 3
            gains = round(gains)
            sleep(1)
            print("Voici vos nouveau gains", gains , "unités de monnaie.")
        
    elif rouleau_1 == rouleau_2 or rouleau_2 == rouleau_3 or rouleau_1 == rouleau_3:
        print("Bravo vous avez gagné : 2 éléments identiques")
        # On identifie quel est le symbole qui fait la paire
        if rouleau_1 == rouleau_2 or rouleau_1 == rouleau_3:
            symbole_double = rouleau_1
        else:
            symbole_double = rouleau_2
            
        # On récupère son abondance
        nb_abondance = abondance[symbole_double]
        
        # Si le symbole fait partie de notre liste spéciale, il récupère sa mise en plus !
        if symbole_double in ["7", "diamond", "coin"]:
            gains = gains + mise + (1 / nb_abondance) * mise * 2
            gains = round(gains)
            sleep(1)
            print("Bonus spécial : tu récupères ta mise en plus du gain !, Voici tes nouveaux gains :", gains)
        else:
            # Pour les autres symboles : gain * 2 sans reprendre la mise
            gains = gains + (1 / nb_abondance) * mise * 2
            gains = round(gains)
        sleep(1)    
        print("Voici vos gains :", gains, "unités de monnaie.")
    else :
        print("VOUS AVEZ PERDU ! RETENTEZ VOTRE CHANCE !")
        sleep(1)
        print("Vos gains actuels sont", gains)
    
    if gains <= 0:
        sleep(1)
        restart = False
        print("Vous n'avez plus aucun gains, vous avez perdu, veuillez remettre une mise dans le menu principal")


    action_restart = input("Tapez b si vous voulez rejouer : ")
        
    if action_restart.lower() == "b":
        restart = True
        print("C'est reparti pour un tour !\n")
    else:
        restart = False
        print("Merci d'avoir joué, à bientôt !")
   