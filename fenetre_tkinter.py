'''
Fichier Tkinter.
'''
import traitements

import tkinter as tk
from tkinter import PhotoImage, Label, filedialog
import numpy as np
from PIL import Image, ImageTk 

canvas = False
pil_image = None
image_importee = ((None, None))


'''
Undo
'''
# On glisse de droite à gauche
def annuler():
    global pil_image, imageP
    if traitements.annuler_liste[2] != None:
        traitements.retablir_liste[0], traitements.retablir_liste[1], traitements.retablir_liste[2] = traitements.retablir_liste[1], traitements.retablir_liste[2], pil_image
        pil_image = traitements.annuler_liste[2]
        traitements.annuler_liste[0],traitements.annuler_liste[1],traitements.annuler_liste[2] = None, traitements.annuler_liste[0], traitements.annuler_liste[1]
        
        imageP = ImageTk.PhotoImage(pil_image)
        afficher_image()


def retablir():
    global pil_image, imageP
    if traitements.retablir_liste[2] != None:
        traitements.annuler_liste[0],traitements.annuler_liste[1],traitements.annuler_liste[2] = traitements.annuler_liste[1], traitements.annuler_liste[2], pil_image        
        pil_image = traitements.retablir_liste[2]
        traitements.retablir_liste[0], traitements.retablir_liste[1], traitements.retablir_liste[2] = None, traitements.retablir_liste[0], traitements.retablir_liste[1]

        imageP = ImageTk.PhotoImage(pil_image)
        afficher_image()


'''
Verif Image
'''
def error_verif():
    global pil_image

    if pil_image == None:
        error()
    
    if pil_image == None:
        return False

    return True


def error_destroy():
    global rootE
    rootE.destroy()
    ouvrir()


def error():
    global rootE
    rootE = tk.Toplevel(root)
    rootE.title("Adobe PhotoCrash 2026 ERROR")
    rootE.geometry("300x70")

    titre = tk.Label(rootE, text="Veillez choisir une image.", font=(100))
    bouton_valider = tk.Button(rootE, text='Compris.', command=error_destroy)
    titre.pack()
    bouton_valider.pack()

    # Mettre en pause les fonctions principales car il n'y a plus de mainloop
    rootE.grab_set()
    rootE.wait_window() #https://stackoverflow.com/questions/78171468


def image_importee_restaurer():
    global image_importee, pil_image, imageP
    if image_importee[0] != None :
        imageP = image_importee[0]
        pil_image = image_importee[1]
        afficher_image()

def afficher_image():
    global pil_image, canvas, imageP, image1
    if canvas != False :
        canvas.destroy()
        image1.destroy()
    
    # Placer canvas orange comme détour de l'image
    info_image = (pil_image.format, pil_image.size, pil_image.mode)
    canvas = tk.Canvas(root, width=info_image[1][0]+25, height=info_image[1][1]+25, bg="orange")
    canvas.place(x = 50, y = 90, anchor="nw")

    # Placer l'image()
    image1 = Label(root, image=imageP)
    image1.image = imageP
    image1.place(x= 60, y= 100, anchor="nw")


'''
Filtres callback
'''
def filtre_rgb(couleur):
    global imageP, pil_image
    if error_verif() :
        
        imageP, pil_image = traitements.filtre_couleur(pil_image, couleur)

        afficher_image()


def gris():
    global imageP, pil_image
    if error_verif():
        imageP, pil_image = traitements.filtre_gris(pil_image)
        afficher_image()

def bords():
    global imageP, pil_image
    if error_verif():
        imageP, pil_image = traitements.filtre_bords(pil_image)
        afficher_image()


def filtre_sepia():
    global imageP, pil_image

    if error_verif() :
        imageP, pil_image = traitements.filtre_sepia(pil_image, 1.3, 1.2, 1.0)

        afficher_image()


def correction_gamma(valeur):
    global pil_image, imageP, original
    imageP, pil_image = traitements.correction_gamma(original, float(valeur))
    afficher_image()


def annule_effet():
    global pil_image, original, imageP, imageOG

    pil_image = original
    imageP = imageOG

    afficher_image()
    dialogue_effet.destroy()


def luminosite():
    global original, pil_image, imageOG

    if error_verif() :

        imageOG = imageP
        original = pil_image

        global dialogue_effet
        
        dialogue_effet = tk.Toplevel(root)
        dialogue_effet.title("Luminosité")
        dialogue_effet.geometry("300x150")
        dialogue_effet.grab_set()
        slider = tk.Scale(dialogue_effet, from_=0.05, to=0.95, orient=tk.HORIZONTAL, length=200, resolution=0.01, digits=2, command=correction_gamma)
        slider.set(0.50)
        slider.pack(pady=20)

        frame_boutons = tk.Frame(dialogue_effet)
        frame_boutons.pack(side=tk.BOTTOM, pady=10)

        bouton_appliquer = tk.Button(frame_boutons, text="Appliquer", command=lambda : dialogue_effet.destroy())
        bouton_appliquer.pack(side=tk.LEFT, padx=10)

        bouton_annuler = tk.Button(frame_boutons, text="Annuler", command=annule_effet)
        bouton_annuler.pack(side=tk.LEFT, padx=10)


def correction_contraste(): # error sans valeur
    # https://python-course.eu/tkinter/sliders-in-tkinter.php
    global pil_image, imageP, original, slider, slider2
    imageP, pil_image = traitements.correction_contraste(original, 2**float(slider.get()), float(slider2.get()))
    afficher_image()


def contraste():
    global original, pil_image, imageOG, slider, slider2

    if error_verif() :

        imageOG = imageP
        original = pil_image

        global dialogue_effet
        
        dialogue_effet = tk.Toplevel(root)
        dialogue_effet.title("Contraste")
        dialogue_effet.geometry("300x250")
        dialogue_effet.grab_set()

        # c
        slider = tk.Scale(dialogue_effet, from_=-0.99, to=0.99, orient=tk.HORIZONTAL, length=200, resolution=0.01, digits=2)
        slider.set(0)
        slider.pack(pady=10)

        # p
        slider2 = tk.Scale(dialogue_effet, from_=0.01, to=0.99, orient=tk.HORIZONTAL, length=200, resolution=0.01, digits=2)
        slider2.set(0.5)
        slider2.pack(pady=10)

        frame_boutons = tk.Frame(dialogue_effet)
        frame_boutons.pack(side=tk.BOTTOM, pady=10)

        bouton_appliquer = tk.Button(frame_boutons, text="Appliquer", command=lambda: dialogue_effet.destroy())
        bouton_appliquer.pack(side=tk.LEFT, padx=10)

        bouton_annuler = tk.Button(frame_boutons, text="Annuler", command=annule_effet)
        bouton_annuler.pack(side=tk.LEFT, padx=10)

        frame_boutons = tk.Frame(dialogue_effet)
        frame_boutons.pack(side=tk.BOTTOM, pady=10)

        bouton_appliquer = tk.Button(frame_boutons, text="Afficher", command=correction_contraste)
        bouton_appliquer.pack(side=tk.LEFT, padx=10)


def flou_appel(valeur):
    global imageP, pil_image, original
    imageP, pil_image = traitements.filtre_flou(original, float(valeur))
    afficher_image()


def flou():
    global original, pil_image, imageOG

    if error_verif() :

        imageOG = imageP
        original = pil_image

        global dialogue_effet
        
        dialogue_effet = tk.Toplevel(root)
        dialogue_effet.title("Flou")
        dialogue_effet.geometry("300x150")
        dialogue_effet.grab_set()
        slider = tk.Scale(dialogue_effet, from_=0, to=1, orient=tk.HORIZONTAL, length=200, resolution=0.01, digits=2, command=flou_appel)
        slider.set(0.50)
        slider.pack(pady=20)

        frame_boutons = tk.Frame(dialogue_effet)
        frame_boutons.pack(side=tk.BOTTOM, pady=10)

        bouton_appliquer = tk.Button(frame_boutons, text="Appliquer", command=lambda : dialogue_effet.destroy())
        bouton_appliquer.pack(side=tk.LEFT, padx=10)

        bouton_annuler = tk.Button(frame_boutons, text="Annuler", command=annule_effet)
        bouton_annuler.pack(side=tk.LEFT, padx=10)

def nettete():
    global imageP, pil_image

    if error_verif() :
        imageP, pil_image = traitements.filtre_nettete(pil_image)
        afficher_image()
    

def fusion():
    global imageP, pil_image

    if error_verif() :
        image_tuple = ouvrir_2eme()
        if image_tuple != None : # Aucune image choisie ?
            imageP, pil_image = traitements.filtre_fusion(pil_image, image_tuple[1])
            afficher_image()


def ouvrir():
    global imageP, pil_image, image_importee, longeur_coef, largeur_coef
    image = tk.filedialog.askopenfilename() # https://www.pythontutorial.net/tkinter/tkinter-open-file-dialog/

    if image != "":
        # Image adapté à Pillow
        pil_image = Image.open(image)

        # Ne pas sortir du cadre, on regarde le plus grand et on crée un coefficient de zoom
        longeur = pil_image.size[0]
        largeur = pil_image.size[1]

        if 800/longeur < 1200/largeur : # On cherche le plus hors du cadre
            coefficient = 800/longeur
        else :
            coefficient = 1200/largeur

        # Pour fusion on enregistre
        longeur_coef = longeur*coefficient
        largeur_coef = largeur*coefficient
        pil_image = pil_image.resize((int(longeur_coef), int(largeur_coef)))


        # .convert Important car certaines images ont le A = alpha, la transparance
        pil_image = pil_image.convert('RGB') # https://stackoverflow.com/questions/51923503
        # Image adapté à Tkinter
        imageP = ImageTk.PhotoImage(pil_image)
        afficher_image()

        image_importee = ((imageP, pil_image))


def ouvrir_2eme():
    global longeur_coef, largeur_coef # Même taille que l'image précédente
    # 2ème image pour la fusion
    image = tk.filedialog.askopenfilename()
    if image != "":
        pil_image2 = Image.open(image)
        pil_image2 = pil_image2.resize((int(longeur_coef), int(largeur_coef)))
        pil_image2 = pil_image2.convert('RGBA')
        imageP2 = ImageTk.PhotoImage(pil_image2)
        return ((imageP2, pil_image2))


def fenetre_principale() :
    global root
    root = tk.Tk()
    root.title("Adobe PhotoCrash 2026")
    root.geometry("1250x660") 

    # Fond
    fond = PhotoImage(file = "Medias/fond.png")
    fond1 = Label(root, image=fond)
    fond1.image = fond
    fond1.place(x=-5, y= -5, anchor="nw")

    titre = tk.Label(root, text="Adobe PhotoCash 2026", font=(100))
    titre.place(x = 50, y = 50)

    # Menu
    menubar = tk.Menu()
    root.config(menu=menubar)
    Fichier = tk.Menu(menubar, tearoff=False)
    menubar.add_cascade(menu=Fichier, label="Fichier")
  
    Fichier.add_command(label="Ouvrir", command=ouvrir)


    Edition = tk.Menu(menubar, tearoff=False)
    Effets = tk.Menu(menubar, tearoff=False)
    Couleur = tk.Menu(menubar, tearoff=False)

    menubar.add_cascade(menu=Edition, label="Édition")
    menubar.add_cascade(menu=Effets, label="Effets")
    Effets.add_cascade(menu=Couleur, label="Filtre couleur")

    Edition.add_command(label="Annuler", command=annuler)
    Edition.add_command(label="Rétablir", command=retablir)
    Edition.add_command(label="Tout annuler", command=image_importee_restaurer)

    Couleur.add_command(label="Vert", command=lambda : filtre_rgb(0))
    Couleur.add_command(label="Rouge", command=lambda : filtre_rgb(1))
    Couleur.add_command(label="Bleu", command=lambda : filtre_rgb(2))
    Couleur.add_command(label="Gris", command=lambda : filtre_rgb(3))

    Effets.add_command(label="Filtre Sepia", command=filtre_sepia)
    Effets.add_command(label="Luminosité", command=luminosite)
    Effets.add_command(label="Contraste", command=contraste)
    Effets.add_command(label="Flou", command=flou)
    Effets.add_command(label="Netteté", command=nettete)
    Effets.add_command(label="Fusion", command=fusion)
    Effets.add_command(label="Détection de bords", command=bords)

    root.mainloop()