'''
Fichier Tkinter.
'''
import traitements

import tkinter as tk
from tkinter import PhotoImage, Label, filedialog
import numpy as np
from tkinter import filedialog
from PIL import Image, ImageTk 

global matrice_pixel, image, pil_image


def afficher_image():
    global pil_image, image, canvas, imageP
    # Placer canvas orange comme détour de l'image
    pil_image = Image.open(image)
    info_image = (pil_image.format, pil_image.size, pil_image.mode)
    canvas = tk.Canvas(root, width=info_image[1][0]+20, height=info_image[1][1]+20, bg="orange")
    canvas.place(x = 50, y = 90, anchor="nw")

    # Placer l'image()
    image1 = Label(root, image=imageP)
    image1.image = imageP
    image1.place(x= 60, y= 100, anchor="nw")



def filtre_vert():
    global imageP, pil_image
    matrice_pixel = traitements.filtre_vert(pil_image)
    imageP = traitements.passer_en_image(matrice_pixel)
    afficher_image()



def ouvrir():
    global imageP, pil_image, image
    image = tk.filedialog.askopenfilename() # https://www.pythontutorial.net/tkinter/tkinter-open-file-dialog/
    
    # Image adapté à Pillow
    pil_img = Image.open(image)

    # Image adapté à Tkinter
    imageP = ImageTk.PhotoImage(pil_img)
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

    root.mainloop()

fenetre_principale()