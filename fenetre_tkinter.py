'''
Fichier Tkinter.
'''
import traitements

import tkinter as tk
from tkinter import PhotoImage, Label, filedialog
import numpy as np
from PIL import Image, ImageTk 

global pil_image, canvas, original
canvas = False
pil_image = None
# Original permet de modifier l'origial pour le filtre luminosité


def error_verif():
    global pil_image
    if pil_image == None:
        error()
    return True


def error_destroy():
    global rootE
    rootE.destroy()
    ouvrir()


def error():
    global rootE
    rootE = tk.Toplevel(root)
    rootE.title("Adobe PhotoCrash 2026 ERROR")
    rootE.geometry("300x100")

    titre = tk.Label(rootE, text="Veillez choisir une image.", font=(100))
    bouton_valider = tk.Button(rootE, text='Compris.', command=error_destroy)
    titre.pack()
    bouton_valider.pack()

    # Mettre en pause les fonctions principales car il n'y a plus de mainloop
    rootE.grab_set()
    rootE.wait_window() #https://stackoverflow.com/questions/78171468


def afficher_image():
    global pil_image, canvas, imageP, image1
    if canvas != False :
        canvas.destroy()
        image1.destroy()
    
    # Placer canvas orange comme détour de l'image
    info_image = (pil_image.format, pil_image.size, pil_image.mode)
    canvas = tk.Canvas(root, width=info_image[1][0]+20, height=info_image[1][1]+20, bg="orange")
    canvas.place(x = 50, y = 90, anchor="nw")

    # Placer l'image()
    image1 = Label(root, image=imageP)
    image1.image = imageP
    image1.place(x= 60, y= 100, anchor="nw")


def filtre_vert():
    global imageP, pil_image, original

    error_verif()
    imageP, pil_image = traitements.filtre_vert(pil_image)
    afficher_image()


def filtre_sepia():
    global imageP, pil_image, original

    error_verif()
    imageP, pil_image = traitements.filtre_sepia(pil_image, 1.3, 1.2, 1.0)

    # Sepia pert le canal alpha, on le remet pour les autres filtres
    pil_image = pil_image.convert('RGBA') # https://stackoverflow.com/questions/51923503

    afficher_image()


def correction_gamma(valeur):
    global pil_image, imageP, original
    imageP, pil_image = traitements.correction_gamma(original, float(valeur))
    afficher_image()


def applique_effet():
    dialogue_effet.destroy()
    original = pil_image


def annule_effet():
    global pil_image, original, imageP, imageOG

    pil_image = original
    imageP = imageOG

    afficher_image()
    dialogue_effet.destroy()


def luminosite():
    global original, pil_image, imageOG

    error_verif()

    imageOG = imageP
    original = pil_image
    
    '''
    global rootl, lumi_valeur, slider, original

    rootl = tk.Tk()
    rootl.title("Adobe PhotoCrash 2026")
    rootl.geometry("300x100")

    lumi_valeur = '' # https://www.geeksforgeeks.org/python/python-tkinter-scale-widget/
    slider = tk.Scale(rootl, from_=1, to=100 , orient="horizontal") # https://stackoverflow.com/questions/73161883
    slider.pack()
    bouton_valider = tk.Button(rootl, text='Valider', command=luminosite_valide)
    bouton_valider.pack() 
    rootl.mainloop()
    '''

    global dialogue_effet
    
    dialogue_effet = tk.Toplevel(root)
    dialogue_effet.title("Luminosité")
    dialogue_effet.geometry("300x150")
    dialogue_effet.grab_set()
    slider = tk.Scale(dialogue_effet, from_=0.05, to=0.95, orient=tk.HORIZONTAL, length=200, resolution=0.1, digits=2, command=correction_gamma)
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

    error_verif()

    imageOG = imageP
    original = pil_image

    global dialogue_effet
    
    dialogue_effet = tk.Toplevel(root)
    dialogue_effet.title("Contraste")
    dialogue_effet.geometry("300x250")
    dialogue_effet.grab_set()

    # c
    slider = tk.Scale(dialogue_effet, from_=-0.9, to=0.90, orient=tk.HORIZONTAL, length=200, resolution=0.01, digits=2)
    slider.set(0)
    slider.pack(pady=10)

    # p
    slider2 = tk.Scale(dialogue_effet, from_=0.1, to=0.9, orient=tk.HORIZONTAL, length=200, resolution=0.1, digits=2)
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




def ouvrir():
    global imageP, pil_image
    image = tk.filedialog.askopenfilename() # https://www.pythontutorial.net/tkinter/tkinter-open-file-dialog/
    
    # Image adapté à Pillow
    pil_image = Image.open(image)
    # .convert Important car certaines images ont le A = alpha soit la transparance
    pil_image = pil_image.convert('RGBA') # https://stackoverflow.com/questions/51923503
    # Image adapté à Tkinter
    imageP = ImageTk.PhotoImage(pil_image)
    afficher_image()


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

    Fichier = tk.Menu(menubar, tearoff=False)
    menubar.add_cascade(menu=Fichier, label="Fichier")
    root.config(menu=menubar)
    Fichier.add_command(label="Ouvrir", command=ouvrir)

    Effets = tk.Menu(menubar, tearoff=False)
    menubar.add_cascade(menu=Effets, label="Effets")
    Effets.add_command(label="Filtre Vert", command=filtre_vert)
    Effets.add_command(label="Filtre Sepia", command=filtre_sepia)
    Effets.add_command(label="Luminosité", command=luminosite)
    Effets.add_command(label="Contraste", command=contraste)
    root.mainloop()

fenetre_principale()