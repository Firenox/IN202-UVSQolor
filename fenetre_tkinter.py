'''
Fichier Tkinter.
'''
import traitements

import tkinter as tk
from tkinter import PhotoImage, Label, filedialog
import numpy as np
from PIL import Image, ImageTk 

global pil_image, canvas

canvas = False


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
    global imageP, pil_image
    imageP = traitements.filtre_vert(pil_image)
    afficher_image()

def filtre_sepia():
    global imageP, pil_image
    imageP = traitements.filtre_sepia(pil_image, 1.3, 1.2, 1.0)
    afficher_image()

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
    root.mainloop()

fenetre_principale()