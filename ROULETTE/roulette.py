import tkinter as tk  # tkinter is the library used to build the window and the buttons
import math  # math gives us cos, sin and radians to place the numbers on the circle
import random  # random lets the code pick the winning number

# ----- Window size (16/9 format) -----
LARGEUR = 1152  # width of the window in pixels
HAUTEUR = 648  # height of the window in pixels

# ----- Colors and font (same in every file of the casino) -----
FOND = "#14171f"  # anthracite black, used as the background
OR = "#d4af37"  # gold
CLAIR = "#f5d77a"  # light gold
ROUGE = "#c8102e"  # bright red
VERT = "#2ecc71"  # bright green, used for winning messages
TAPIS = "#0b6b3a"  # dark green of the casino table felt
VERT_ZERO = "#0a8f4a"  # green of the zero
POLICE = "DM Sans"  # the DM Sans font must be installed (tkinter uses a default one otherwise)

# ----- The chips: value -> (chip color, text color, ring color) -----
JETONS = {
    1: ("#f2f2f2", "#1b3a6b", "#1b5e9b"),  # chip 1: white with a blue ring
    5: ("#2e9e4f", "white", "white"),  # chip 5: green
    25: ("#d6303a", "white", "white"),  # chip 25: red
    100: ("#1a1a1a", "white", "white"),  # chip 100: black
    500: ("#7b3fb0", "white", "white"),  # chip 500: purple
    1000: ("#e0b020", "#3a2a00", "white"),  # chip 1k: gold
}
VALEURS_JETONS = [1, 5, 25, 100, 500, 1000]  # the chips shown at the bottom, from left to right

# ----- Wheel geometry -----
CX = 230  # x position of the wheel center
CY = 330  # y position of the wheel center
RAYON = 150  # radius of the wheel in pixels
NB_PARTS = 37  # number of slices on the wheel (0 to 36)
ANGLE_PART = 360 / NB_PARTS  # angle of one slice in degrees

# ----- Real order of the numbers around a European roulette wheel -----
ORDRE = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1,
         20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]  # slice i holds the number ORDRE[i]

# ----- Table geometry (the green betting table) -----
TX = 440  # x of the left side of the table (the zero column)
ZW = 50  # width of the zero column
CW = 50  # width of one number cell
CH = 54  # height of one number cell
DH = 40  # height of the dozens row and of the bottom row
Y_DOUZ = 160  # y of the top of the dozens row (1-12, 13-24, 25-36)
Y_GRILLE = Y_DOUZ + DH  # y of the top of the 3 rows of numbers
Y_BAS = Y_GRILLE + 3 * CH  # y of the top of the bottom row (1-18, Even...)
COL_X0 = TX + ZW  # x where the 12 columns of numbers start
CENTRE_TABLE = COL_X0 + 6 * CW  # x of the middle of the table

# ----- Game rules -----
ROUGES = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]  # the red numbers
MISE_MAX = 2000  # the maximum total bet on the table
ARGENT_DEPART = 2000  # the money the player starts with
JETONS_VISIBLES = 10  # maximum number of chips drawn in one stack
DUREE_ANIMATION = 4000  # total duration of the spin in milliseconds
DELAI_IMAGE = 30  # time between two animation frames in milliseconds
TOURS_MINI = 4  # minimum number of full turns the wheel makes

# ----- Game state (global variables, no classes) -----
reserve = ARGENT_DEPART  # the money of the player (later it will come from the menu)
mises = {}  # the bets on the table: (type, value) -> {"x", "y", "jetons": [chip values]}
historique = []  # the order in which chips were placed (used by the UNDO button)
jeton_choisi = 1  # the value of the chip currently selected at the bottom
angle_roue = 0.0  # current rotation of the wheel in degrees
en_rotation = False  # True while the wheel is spinning (blocks bets)
ids_parts = []  # list of the canvas ids of the 37 slices
ids_numeros = []  # list of the canvas ids of the 37 numbers


# ----- Helper functions -----
def couleur_du_numero(n):
    """Return the color of the number n."""  # docstring
    if n == 0:  # the zero
        return VERT_ZERO  # is green
    if n in ROUGES:  # if the number is in the red list
        return ROUGE  # it is red
    return "black"  # otherwise it is black


def texte_jeton(valeur):
    """Shorten big amounts so they fit on a chip (1000 -> 1k, 1500 -> 1.5k)."""  # docstring
    if valeur >= 1000:  # 1000 and more
        if valeur % 1000 == 0:  # a round number of thousands
            return str(valeur // 1000) + "k"  # for example 1k or 2k
        return str(valeur // 100 / 10) + "k"  # for example 1.5k
    return str(valeur)  # small amounts are written fully


def total_mise():
    """Return the total amount of all the chips on the table."""  # docstring
    total = 0  # start at zero
    for cle in mises:  # for each bet on the table
        total = total + sum(mises[cle]["jetons"])  # add all the chips of this bet
    return total  # the total amount


def maj_affichage():
    """Refresh the balance and the total bet texts."""  # docstring
    canvas.itemconfig(texte_reserve, text="Solde monnaie : " + str(reserve))  # refresh the balance
    canvas.itemconfig(texte_total, text="Total bet: " + str(total_mise()) + " / " + str(MISE_MAX))  # refresh the total


def dessiner_jeton(x, y, rayon, valeur, texte, tag, actif):
    """Draw one chip and return the list of its canvas ids."""  # docstring
    fond, couleur_texte, anneau = JETONS[valeur]  # colors of this chip
    etat = "normal" if actif else "disabled"  # "disabled" items ignore the mouse (clicks go through)
    exterieur = canvas.create_oval(x - rayon, y - rayon, x + rayon, y + rayon,
                                   fill=fond, outline=anneau, width=2, tags=tag, state=etat)  # outer disc
    interieur = canvas.create_oval(x - rayon + 5, y - rayon + 5, x + rayon - 5, y + rayon - 5,
                                   fill=fond, outline=anneau, width=1, dash=(3, 2),
                                   tags=tag, state=etat)  # dashed inner ring
    nombre = canvas.create_text(x, y, text=texte, font=(POLICE, int(rayon / 2), "bold"),
                                fill=couleur_texte, tags=tag, state=etat)  # the number on top of the chip
    return [exterieur, interieur, nombre]  # give back the ids (used to bind clicks)


def dessiner_mises():
    """Redraw all the stacks of chips on the table."""  # docstring
    canvas.delete("jeton")  # remove every chip drawn on the table
    for cle in mises:  # for each bet on the table
        pari = mises[cle]  # the data of this bet
        pile = pari["jetons"][-JETONS_VISIBLES:]  # the last chips of the stack (the only ones drawn)
        total = sum(pari["jetons"])  # total amount of this bet
        for k in range(len(pile)):  # from the bottom chip to the top chip
            y = pari["y"] + 6 - k * 4  # each chip is drawn 4 pixels higher than the previous one
            if k == len(pile) - 1:  # the top chip of the stack
                texte = texte_jeton(total)  # shows the total amount of the bet
            else:  # the chips below
                texte = ""  # have no text (they are hidden by the chip above)
            dessiner_jeton(pari["x"], y, 17, pile[k], texte, "jeton", False)  # draw the chip


def dessiner_selecteur():
    """Draw the 6 chips at the bottom (the selected one is raised and has a gold halo)."""  # docstring
    canvas.delete("selecteur")  # remove the old chips of the selector
    for k in range(len(VALEURS_JETONS)):  # for each chip
        valeur = VALEURS_JETONS[k]  # the value of this chip
        x = CENTRE_TABLE + (k - 2.5) * 72  # the chips are spread around the middle of the table
        y = 575  # normal height of the chips
        if valeur == jeton_choisi:  # if this is the selected chip
            y = y - 8  # raise it a little
            canvas.create_oval(x - 31, y - 31, x + 31, y + 31, outline=OR, width=3,
                               tags="selecteur", state="disabled")  # gold halo around it
        ids = dessiner_jeton(x, y, 26, valeur, texte_jeton(valeur), "selecteur", True)  # draw the chip
        for element in ids:  # for each part of the chip
            canvas.tag_bind(element, "<Button-1>", lambda event, v=valeur: choisir_jeton(v))  # click = select it
            canvas.tag_bind(element, "<Enter>", lambda event: canvas.config(cursor="hand2"))  # hand cursor
            canvas.tag_bind(element, "<Leave>", lambda event: canvas.config(cursor=""))  # normal cursor


def choisir_jeton(valeur):
    """Select the chip the player wants to use."""  # docstring
    global jeton_choisi  # we modify the global variable
    jeton_choisi = valeur  # remember the selected chip
    dessiner_selecteur()  # redraw the selector with the new highlighted chip


def placer_roue():
    """Draw every slice and number according to the current angle_roue."""  # docstring
    for i in range(NB_PARTS):  # loop over the 37 slices
        debut = i * ANGLE_PART + angle_roue  # start angle of this slice, shifted by the rotation
        canvas.itemconfig(ids_parts[i], start=debut)  # rotate the slice by changing its start angle
        milieu = math.radians(debut + ANGLE_PART / 2)  # middle of the slice, in radians
        x = CX + 122 * math.cos(milieu)  # x of the number (122 = distance from the center)
        y = CY - 122 * math.sin(milieu)  # y of the number (minus because y goes down on screen)
        canvas.coords(ids_numeros[i], x, y)  # move the number to its new position


def poser_jeton(type_pari, valeur, x, y):
    """Put the selected chip on a cell of the table (chips stack on top of each other)."""  # docstring
    global reserve  # we modify the reserve
    if en_rotation:  # if the wheel is spinning
        return  # we ignore the click, no bet during the spin
    if jeton_choisi > reserve:  # if the player cannot afford this chip
        canvas.itemconfig(texte_resultat, text="Not enough money !", fill=ROUGE)  # warn the player
        return  # stop here
    if total_mise() + jeton_choisi > MISE_MAX:  # if the table would go over the maximum bet
        canvas.itemconfig(texte_resultat, text="Max bet is " + str(MISE_MAX) + " !", fill=ROUGE)  # warn the player
        return  # stop here
    cle = (type_pari, valeur)  # the key that identifies this cell
    if cle not in mises:  # if there is no chip on this cell yet
        mises[cle] = {"x": x, "y": y, "jetons": []}  # create an empty stack for it
    mises[cle]["jetons"].append(jeton_choisi)  # add the chip on top of the stack
    historique.append(cle)  # remember it for the UNDO button
    reserve = reserve - jeton_choisi  # take the chip's value out of the reserve
    canvas.itemconfig(texte_resultat, text="Place your bets !", fill=CLAIR)  # reset the message
    maj_affichage()  # refresh the balance and the total bet
    dessiner_mises()  # redraw the stacks


def annuler():
    """UNDO: remove the last chip that was placed and give its money back."""  # docstring
    global reserve  # we modify the reserve
    if en_rotation or len(historique) == 0:  # during a spin or if there is nothing to remove
        return  # do nothing
    cle = historique.pop()  # the cell of the last chip placed
    valeur = mises[cle]["jetons"].pop()  # take the chip off its stack
    if len(mises[cle]["jetons"]) == 0:  # if the stack is now empty
        del mises[cle]  # remove the bet from the table
    reserve = reserve + valeur  # give the money back
    maj_affichage()  # refresh the balance and the total bet
    dessiner_mises()  # redraw the stacks


def effacer():
    """CLEAR: remove every chip from the table and give all the money back."""  # docstring
    while len(historique) > 0 and not en_rotation:  # while there are chips to remove
        annuler()  # remove the last chip


def multiplicateur(numero, cle):
    """Return how many times a chip is paid back for the bet 'cle' when 'numero' wins."""  # docstring
    type_pari, valeur = cle  # split the key into the type and the value
    if type_pari == "numero":  # bet on one single number
        if valeur == numero:  # the number came out
            return 36  # pays 36 times the stake
        return 0  # otherwise the stake is lost
    if numero == 0:  # the zero makes every other bet lose
        return 0  # the house wins
    if type_pari == "douzaine":  # bet on a dozen
        if (numero - 1) // 12 + 1 == valeur:  # the number is in the chosen dozen (1, 2 or 3)
            return 3  # pays 3 times the stake
        return 0  # otherwise the stake is lost
    if type_pari == "rouge" and numero in ROUGES:  # red bet and a red number
        return 2  # pays 2 times the stake
    if type_pari == "noir" and numero not in ROUGES:  # black bet and a black number
        return 2  # pays 2 times the stake
    if type_pari == "pair" and numero % 2 == 0:  # even bet and an even number
        return 2  # pays 2 times the stake
    if type_pari == "impair" and numero % 2 == 1:  # odd bet and an odd number
        return 2  # pays 2 times the stake
    if type_pari == "manque" and numero <= 18:  # bet on 1-18 and the number is between 1 and 18
        return 2  # pays 2 times the stake
    if type_pari == "passe" and numero >= 19:  # bet on 19-36 and the number is between 19 and 36
        return 2  # pays 2 times the stake
    return 0  # otherwise the player loses the stake


def finir(gagnant):
    """Called when the wheel stops: pay every bet, clear the table and show the result."""  # docstring
    global reserve, en_rotation  # we modify these global variables
    mise = total_mise()  # total amount that was bet
    gain = 0  # total money paid back to the player
    for cle in mises:  # for each bet on the table
        gain = gain + sum(mises[cle]["jetons"]) * multiplicateur(gagnant, cle)  # add what this bet pays
    reserve = reserve + gain  # add the winnings to the reserve
    mises.clear()  # the table is cleared
    historique.clear()  # the history is cleared too
    en_rotation = False  # the wheel is stopped, bets are allowed again
    bouton_lancer.config(state="normal")  # re-enable the big spin button
    bouton_annuler.config(state="normal")  # re-enable the UNDO button
    bouton_effacer.config(state="normal")  # re-enable the CLEAR button
    maj_affichage()  # refresh the balance and the total bet
    dessiner_mises()  # redraw the (now empty) table
    net = gain - mise  # profit (positive) or loss (negative)
    if net > 0:  # the player made a profit
        message = "Number " + str(gagnant) + " - You win " + str(net) + " !"  # winning message
        canvas.itemconfig(texte_resultat, text=message, fill=VERT)  # show it in green
    elif net == 0:  # the player got exactly his money back
        message = "Number " + str(gagnant) + " - You break even"  # neutral message
        canvas.itemconfig(texte_resultat, text=message, fill=CLAIR)  # show it in light gold
    else:  # the player lost money
        message = "Number " + str(gagnant) + " - You lose " + str(-net)  # losing message
        canvas.itemconfig(texte_resultat, text=message, fill="white")  # show it in white
    if reserve <= 0:  # if the player has no money left
        canvas.itemconfig(texte_resultat, text="No money left !", fill=ROUGE)  # game over message


def tourner(etape, total, angle_depart, rotation_totale, gagnant):
    """One frame of the spinning animation (calls itself with after)."""  # docstring
    global angle_roue  # we modify the rotation of the wheel
    t = etape / total  # progress of the animation between 0 and 1
    facile = 1 - (1 - t) ** 3  # ease-out: fast at first, then slows down smoothly
    angle_roue = angle_depart - rotation_totale * facile  # new angle (minus = clockwise turn)
    placer_roue()  # redraw the wheel at this angle
    if etape < total:  # if the animation is not finished
        fenetre.after(DELAI_IMAGE, tourner, etape + 1, total, angle_depart,
                      rotation_totale, gagnant)  # schedule the next frame
    else:  # last frame reached
        finir(gagnant)  # the wheel stopped: pay the bets


def lancer():
    """Spin the wheel (the chips are already paid when placed)."""  # docstring
    global en_rotation  # we modify this global variable
    if en_rotation:  # if the wheel is already spinning
        return  # do nothing
    if len(mises) == 0:  # if there is no chip on the table
        canvas.itemconfig(texte_resultat, text="Place a chip on the table first !", fill=CLAIR)  # warn the player
        return  # stop here

    canvas.itemconfig(texte_resultat, text="No more bets...", fill=OR)  # message during the spin
    en_rotation = True  # block the bets during the spin
    bouton_lancer.config(state="disabled")  # disable the spin button during the spin
    bouton_annuler.config(state="disabled")  # disable the UNDO button during the spin
    bouton_effacer.config(state="disabled")  # disable the CLEAR button during the spin

    gagnant = random.randint(0, 36)  # the code picks the winning number
    index = ORDRE.index(gagnant)  # position of its slice on the wheel
    cible = (90 - (index * ANGLE_PART + ANGLE_PART / 2)) % 360  # angle putting that slice under the pointer (90 = top)
    reste = (angle_roue - cible) % 360  # clockwise distance to reach the target angle
    rotation_totale = reste + 360 * (TOURS_MINI + random.randint(0, 2))  # add several full turns
    total = DUREE_ANIMATION // DELAI_IMAGE  # number of frames in the animation
    tourner(0, total, angle_roue, rotation_totale, gagnant)  # start the animation


def retour():
    fenetre.destroy()  # close the window


def creer_case(x1, y1, x2, y2, couleur, texte, taille, type_pari, valeur, losange=None):
    """Create one clickable cell of the table (rectangle + text or diamond)."""  # docstring
    cx = (x1 + x2) / 2  # x of the center of the cell
    cy = (y1 + y2) / 2  # y of the center of the cell
    elements = []  # list of the canvas items that belong to this cell
    rect = canvas.create_rectangle(x1, y1, x2, y2, fill=couleur, outline="white", width=1)  # the cell itself
    elements.append(rect)  # the rectangle is clickable
    if losange is not None:  # if the cell shows a red or black diamond
        points = [cx, cy - 15, cx + 26, cy, cx, cy + 15, cx - 26, cy]  # the 4 corners of the diamond
        elements.append(canvas.create_polygon(points, fill=losange, outline="white"))  # draw the diamond
    else:  # otherwise the cell shows a text
        elements.append(canvas.create_text(cx, cy, text=texte, font=(POLICE, taille, "bold"),
                                           fill="white"))  # draw the text
    for element in elements:  # for each item of the cell
        canvas.tag_bind(element, "<Button-1>",
                        lambda event: poser_jeton(type_pari, valeur, cx, cy))  # click = put a chip here
        canvas.tag_bind(element, "<Enter>", lambda event: canvas.config(cursor="hand2"))  # hand cursor on hover
        canvas.tag_bind(element, "<Leave>", lambda event: canvas.config(cursor=""))  # normal cursor outside


# ----- The window and the drawing area -----
fenetre = tk.Tk()  # create the main window
fenetre.title("Royal Casino - Roulette")  # title of the window
fenetre.geometry("1152x648")  # size of the window

canvas = tk.Canvas(fenetre, width=LARGEUR, height=HAUTEUR, bg=FOND, highlightthickness=0)  # drawing area
canvas.pack()  # display the canvas in the window

# ----- The frame around the window (gold then red) -----
canvas.create_rectangle(10, 10, LARGEUR - 10, HAUTEUR - 10, outline=OR, width=4)  # gold frame
canvas.create_rectangle(20, 20, LARGEUR - 20, HAUTEUR - 20, outline=ROUGE, width=2)  # red frame

# ----- Top bar: back button on the left, balance on the right -----
bouton_retour = tk.Button(fenetre, text="< Menu", font=(POLICE, 11), command=retour)  # back button
canvas.create_window(80, 45, window=bouton_retour)  # place the back button

canvas.create_rectangle(905, 30, 1105, 62, fill="black", outline=OR, width=2)  # black box for the balance
texte_reserve = canvas.create_text(1005, 46, text="Solde monnaie : " + str(reserve),  # balance text
                                   font=(POLICE, 12, "bold"), fill="white")  # bold white font

# ----- The title -----
canvas.create_text(576, 75, text="ROULETTE", font=(POLICE, 34, "bold"), fill=OR)  # big gold title

# ===== LEFT PART: the wheel =====
canvas.create_oval(CX - RAYON - 8, CY - RAYON - 8, CX + RAYON + 8, CY + RAYON + 8,
                   outline=OR, width=4)  # gold ring around the wheel

for i in range(NB_PARTS):  # create the 37 slices once (they are moved later)
    couleur = couleur_du_numero(ORDRE[i])  # color of the number written on this slice
    part = canvas.create_arc(CX - RAYON, CY - RAYON, CX + RAYON, CY + RAYON,  # box of the circle
                             start=i * ANGLE_PART, extent=ANGLE_PART,  # position and size of the slice
                             fill=couleur, outline=OR, width=1)  # color of the slice and gold border
    ids_parts.append(part)  # keep its id to rotate it later

for i in range(NB_PARTS):  # create the 37 numbers once
    numero = canvas.create_text(0, 0, text=str(ORDRE[i]),  # text created at (0, 0), moved right after
                                font=(POLICE, 9, "bold"), fill="white")  # small bold white font
    ids_numeros.append(numero)  # keep its id to move it later

placer_roue()  # put every slice and number at its starting position

# The center of the wheel
canvas.create_oval(CX - 50, CY - 50, CX + 50, CY + 50, fill="black", outline=OR, width=3)  # black disc
canvas.create_text(CX, CY, text="♠", font=(POLICE, 38), fill=OR)  # gold spade symbol

# The small triangle at the top (it shows the winning number)
canvas.create_polygon(CX - 14, CY - RAYON - 14, CX + 14, CY - RAYON - 14, CX, CY - RAYON + 14,
                      fill=CLAIR, outline="black")  # fixed pointer

# Text under the wheel showing messages and the result of the spin
texte_resultat = canvas.create_text(CX, 525, text="Pick a chip and click on the table !",  # message text
                                    font=(POLICE, 15, "bold"), fill=CLAIR)  # bold light gold font

# ===== RIGHT PART: the green betting table =====
canvas.create_rectangle(TX - 14, Y_DOUZ - 14, COL_X0 + 12 * CW + 14, Y_BAS + DH + 14,
                        fill=TAPIS, outline=OR, width=3)  # the green felt with a gold border

# ----- The zero (on the left, as tall as the 3 rows of numbers) -----
creer_case(TX, Y_GRILLE, TX + ZW, Y_BAS, VERT_ZERO, "0", 16, "numero", 0)  # the 0 cell

# ----- The 36 numbers (3 rows x 12 columns) -----
for n in range(1, 37):  # one cell per number
    colonne = (n - 1) // 3  # column index from 0 to 11 (3 numbers per column)
    ligne = 2 - (n - 1) % 3  # row index: 0 = top (3, 6, 9...), 2 = bottom (1, 4, 7...)
    x1 = COL_X0 + colonne * CW  # left side of the cell
    y1 = Y_GRILLE + ligne * CH  # top side of the cell
    creer_case(x1, y1, x1 + CW, y1 + CH, couleur_du_numero(n), str(n), 14, "numero", n)  # cell of the number n

# ----- The 3 dozens (above the numbers) -----
noms_douzaines = ["1-12", "13-24", "25-36"]  # labels of the 3 dozens
for k in range(3):  # for each dozen
    x1 = COL_X0 + k * 4 * CW  # a dozen is 4 columns wide
    creer_case(x1, Y_DOUZ, x1 + 4 * CW, Y_GRILLE, TAPIS, noms_douzaines[k], 13,
               "douzaine", k + 1)  # the dozen cell

# ----- The bottom row: 1-18, Even, red, black, Odd, 19-36 -----
lb = 2 * CW  # each bottom cell is 2 columns wide
creer_case(COL_X0, Y_BAS, COL_X0 + lb, Y_BAS + DH, TAPIS, "1-18", 12, "manque", None)  # low numbers
creer_case(COL_X0 + lb, Y_BAS, COL_X0 + 2 * lb, Y_BAS + DH, TAPIS, "EVEN", 12, "pair", None)  # even numbers
creer_case(COL_X0 + 2 * lb, Y_BAS, COL_X0 + 3 * lb, Y_BAS + DH, TAPIS, "", 12,
           "rouge", None, losange=ROUGE)  # red (red diamond)
creer_case(COL_X0 + 3 * lb, Y_BAS, COL_X0 + 4 * lb, Y_BAS + DH, TAPIS, "", 12,
           "noir", None, losange="black")  # black (black diamond)
creer_case(COL_X0 + 4 * lb, Y_BAS, COL_X0 + 5 * lb, Y_BAS + DH, TAPIS, "ODD", 12, "impair", None)  # odd numbers
creer_case(COL_X0 + 5 * lb, Y_BAS, COL_X0 + 6 * lb, Y_BAS + DH, TAPIS, "19-36", 12, "passe", None)  # high numbers

# ----- Texts under the table: total bet and payouts -----
texte_total = canvas.create_text(CENTRE_TABLE, 440, text="Total bet: 0 / " + str(MISE_MAX),  # total bet text
                                 font=(POLICE, 14, "bold"), fill="white")  # bold white font
canvas.create_text(CENTRE_TABLE, 463, text="Number x36  |  Dozen x3  |  Other bets x2  |  0 = house wins",
                   font=(POLICE, 11), fill=OR)  # reminder of the payouts

# ----- The buttons: UNDO, SPIN and CLEAR -----
bouton_annuler = tk.Button(fenetre, text="UNDO", font=(POLICE, 11, "bold"),
                           bg=OR, fg="black", width=8, command=annuler)  # removes the last chip
canvas.create_window(CENTRE_TABLE - 190, 505, window=bouton_annuler)  # place the UNDO button on the left
bouton_lancer = tk.Button(fenetre, text="LANCER LA ROUE", font=(POLICE, 18, "bold"),  # big bold text
                          bg=OR, fg="black", width=18, command=lancer)  # gold button that calls lancer
canvas.create_window(CENTRE_TABLE, 505, window=bouton_lancer)  # place the big button in the middle
bouton_effacer = tk.Button(fenetre, text="CLEAR", font=(POLICE, 11, "bold"),
                           bg=OR, fg="black", width=8, command=effacer)  # removes all the chips
canvas.create_window(CENTRE_TABLE + 190, 505, window=bouton_effacer)  # place the CLEAR button on the right

# ----- The chip selector at the bottom -----
dessiner_selecteur()  # draw the 6 chips (1, 5, 25, 100, 500, 1k)

# ----- Start the window -----
fenetre.mainloop()  # keep the window open and listen to the clicks
