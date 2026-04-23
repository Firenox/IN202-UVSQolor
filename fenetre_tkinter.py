'''
Fichier Tkinter.
'''

import tkinter as tk
from tkinter import PhotoImage, Label, filedialog


import numpy as np
from tkinter import filedialog
from PIL import Image, ImageTk 


def filtre_vert(mat):
    nbcol = mat.shape[1]
    for i in range(nblig):
        for j in range(nbcol):
            mat[i, j] = (0, mat[i, j, 1], 0)

# https://www.pythontutorial.net/tkinter/tkinter-open-file-dialog/
def ouvrir():
    global pil_image
    image = tk.filedialog.askopenfilename()
    pil_image = Image.open(image)
    info_image = (pil_image.format, pil_image.size, pil_image.mode)
    canvas = tk.Canvas(root, width=info_image[1][0]+20, height=info_image[1][1]+20, bg="orange")
    canvas.place(x = 50, y = 90, anchor="nw")
    print(pil_image)

    image = PhotoImage(file = image)
    image1 = Label(root, image=image)
    image1.image = image
    image1.place(x = 60, y = 100, anchor="nw")

def fenetre_principale() :
    global root
    root = tk.Tk()
    root.title("Adobe PhotoCrash 2026")
    root.geometry("1200x750") 

    fond = PhotoImage(file = "Medias/fond.png")
    fond1 = Label(root, image=fond)
    fond1.image = fond
    fond1.place(x=-5, y= -5, anchor="nw")

    titre = tk.Label(root, text="Adobe PhotoCash 2026", font=(100))
    titre.place(x = 50, y = 50)

    # TD6 : https://pythonassets.com/posts/menubar-in-tk-tkinter/
    menubar = tk.Menu()

    Fichier = tk.Menu(menubar, tearoff=False)
    menubar.add_cascade(menu=Fichier, label="Fichier")
    root.config(menu=menubar)
    Fichier.add_command(label="Ouvrir", command=ouvrir)

    Effets = tk.Menu(menubar, tearoff=False)
    menubar.add_cascade(menu=Effets, label="Effets")
    Effets.add_command(label="Filtre Vert", command=ouvrir)

    root.mainloop()

fenetre_principale()