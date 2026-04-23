'''
Traitements des images
'''

import numpy as np
from PIL import Image, ImageTk 
global pil_image, canvas, imageP

def filtre_vert(pil_image):
    passer_en_matrice(pil_image)
    nblig = matrice_pixel.shape[0]
    nbcol = matrice_pixel.shape[1]
    for i in range(nblig):
        for j in range(nbcol):
            matrice_pixel[i, j] = (0, matrice_pixel[i, j, 1], 0, 255)
    return matrice_pixel


def passer_en_matrice(pil_image):
    global matrice_pixel
    matrice_pixel = np.array(pil_image)


def passer_en_image(image):
    global pil_image, matrice_pixel
    pil_image = Image.fromarray(matrice_pixel)
    image = ImageTk.PhotoImage(pil_image) # https://stackoverflow.com/questions/18369936
    return image