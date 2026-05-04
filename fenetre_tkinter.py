'''
Fichier Tkinter.
'''
import traitements

import tkinter as tk
from tkinter import PhotoImage, Label, filedialog
import numpy as np
from PIL import Image, ImageTk 

global pil_image, canvas, original, retablir_liste, annuler_liste, image_importee
canvas = False
pil_image = None
annuler_liste = [None, None, None]
retablir_liste = [None, None, None]
image_importee = ((None, None))

# Original permet de modifier l'origial pour le filtre luminosité

'''
Undo
'''
def annuler():
    global retablir_liste, annuler_liste, pil_image, imageP
    if annuler_liste[2] != None:
        retablir_liste[0], retablir_liste[1], retablir_liste[2] = retablir_liste[1], retablir_liste[2], pil_image
        pil_image = annuler_liste[2]
        annuler_liste[0],annuler_liste[1],annuler_liste[2] = None, annuler_liste[0], annuler_liste[1]
        
        imageP = ImageTk.PhotoImage(pil_image)
        afficher_image()


def retablir():
    global retablir_liste, annuler_liste, pil_image, imageP
    if retablir_liste[2] != None:
        annuler_liste[0],annuler_liste[1],annuler_liste[2] = annuler_liste[1], annuler_liste[2], pil_image        
        pil_image = retablir_liste[2]
        retablir_liste[0], retablir_liste[1], retablir_liste[2] = None, retablir_liste[0], retablir_liste[1]

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
        annuler_liste[0],annuler_liste[1],annuler_liste[2] = annuler_liste[1], annuler_liste[2], pil_image
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


def fermer_erreur():
    global erreur
    erreur.destroy()


def erreur_ratio():
    global erreur
    
    erreur = tk.Toplevel(root)
    erreur.title("Erreur")
    erreur.geometry("380x70")
    
    titre = tk.Label(erreur, text="Les deux images n'ont pas la même taille", font=(100))
    titre.grid()

    bouton = tk.Button(erreur, text="D'accord", command=fermer_erreur)
    bouton.grid()


'''
Filtres
'''
def filtre_vert():
    global imageP, pil_image, annuler_liste
    if error_verif() :
        annuler_liste[0],annuler_liste[1],annuler_liste[2] = annuler_liste[1], annuler_liste[2], pil_image
        imageP, pil_image = traitements.filtre_couleur(pil_image, 0)

        afficher_image()


def filtre_rouge():
    global imageP, pil_image, annuler_liste
    if error_verif() :
        annuler_liste[0],annuler_liste[1],annuler_liste[2] = annuler_liste[1], annuler_liste[2], pil_image
        imageP, pil_image = traitements.filtre_couleur(pil_image, 1)

        afficher_image()


def filtre_bleu():
    global imageP, pil_image, annuler_liste
    if error_verif() :
        annuler_liste[0],annuler_liste[1],annuler_liste[2] = annuler_liste[1], annuler_liste[2], pil_image
        imageP, pil_image = traitements.filtre_couleur(pil_image, 2)

        afficher_image()


def filtre_sepia():
    global imageP, pil_image

    if error_verif() :
        annuler_liste[0],annuler_liste[1],annuler_liste[2] = annuler_liste[1], annuler_liste[2], pil_image
        imageP, pil_image = traitements.filtre_sepia(pil_image, 1.3, 1.2, 1.0)

        afficher_image()


def correction_gamma(valeur):
    global pil_image, imageP, original
    imageP, pil_image = traitements.correction_gamma(original, float(valeur))
    afficher_image()


def applique_effet():
    global annuler_liste
    dialogue_effet.destroy()


def annule_effet():
    global pil_image, original, imageP, imageOG

    pil_image = original
    imageP = imageOG

    afficher_image()
    dialogue_effet.destroy()


def luminosite():
    global original, pil_image, imageOG

    if error_verif() :
        annuler_liste[0],annuler_liste[1],annuler_liste[2] = annuler_liste[1], annuler_liste[2], pil_image

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

        bouton_appliquer = tk.Button(frame_boutons, text="Appliquer", command=applique_effet)
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

        bouton_appliquer = tk.Button(frame_boutons, text="Appliquer", command=applique_effet)
        bouton_appliquer.pack(side=tk.LEFT, padx=10)

        bouton_annuler = tk.Button(frame_boutons, text="Annuler", command=annule_effet)
        bouton_annuler.pack(side=tk.LEFT, padx=10)

        frame_boutons = tk.Frame(dialogue_effet)
        frame_boutons.pack(side=tk.BOTTOM, pady=10)

        bouton_appliquer = tk.Button(frame_boutons, text="Afficher", command=correction_contraste)
        bouton_appliquer.pack(side=tk.LEFT, padx=10)


def flou():
    global imageP, pil_image, annuler_liste

    if error_verif() :
        annuler_liste[0],annuler_liste[1],annuler_liste[2] = annuler_liste[1], annuler_liste[2], pil_image
        imageP, pil_image = traitements.filtre_flou(pil_image)
        afficher_image()


def nettete():
    global imageP, pil_image, annuler_liste

    if error_verif() :
        annuler_liste[0],annuler_liste[1],annuler_liste[2] = annuler_liste[1], annuler_liste[2], pil_image
        imageP, pil_image = traitements.filtre_nettete(pil_image)
        afficher_image()
    

def fusion():
    global imageP, pil_image, annuler_liste

    if error_verif() :
        imageP2, pil_image2 = ouvrir_2eme()
        if imageP2 != None :
            annuler_liste[0],annuler_liste[1],annuler_liste[2] = annuler_liste[1], annuler_liste[2], pil_image
            imageP, pil_image = traitements.filtre_fusion(pil_image, pil_image2)

        if pil_image == None :
            erreur_ratio()
        else :
            afficher_image()


def ouvrir():
    global imageP, pil_image, image_importee
    image = tk.filedialog.askopenfilename() # https://www.pythontutorial.net/tkinter/tkinter-open-file-dialog/

    if image != "":
        # Image adapté à Pillow
        pil_image = Image.open(image)
        # .convert Important car certaines images ont le A = alpha, la transparance
        pil_image = pil_image.convert('RGB') # https://stackoverflow.com/questions/51923503
        # Image adapté à Tkinter
        imageP = ImageTk.PhotoImage(pil_image)
        afficher_image()

        image_importee = ((imageP, pil_image))


def ouvrir_2eme():
    # 2ème image pour la fusion
    image = tk.filedialog.askopenfilename()
    if image != "":
        pil_image2 = Image.open(image)
        pil_image2 = pil_image2.convert('RGBA')
        imageP2 = ImageTk.PhotoImage(pil_image2)
        return ((imageP2, pil_image2))


def fenetre_principale() :
    global root
    root = tk.Tk()
    root.title("Adobe PhotoCrash 2026")
    root.geometry("1200x750") 

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

    Couleur.add_command(label="Vert", command=filtre_vert)
    Couleur.add_command(label="Rouge", command=filtre_rouge)
    Couleur.add_command(label="Bleu", command=filtre_bleu)

    Effets.add_command(label="Filtre Sepia", command=filtre_sepia)
    Effets.add_command(label="Luminosité", command=luminosite)
    Effets.add_command(label="Contraste", command=contraste)
    Effets.add_command(label="Flou", command=flou)
    Effets.add_command(label="Netteté", command=nettete)
    Effets.add_command(label="Fusion", command=fusion)

    root.mainloop()