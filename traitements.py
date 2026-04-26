'''
Traitements des images
'''
import numpy as np
from PIL import Image, ImageTk 
import calculs


def filtre_vert(pil_image):
    matrice_pixel = passer_en_matrice(pil_image)
    nblig = matrice_pixel.shape[0]
    nbcol = matrice_pixel.shape[1]
    for i in range(nblig):
        for j in range(nbcol):
            matrice_pixel[i, j] = (0, matrice_pixel[i, j, 1], 0, matrice_pixel[i, j, 3])
    return passer_en_image(np.clip(matrice_pixel, 0, 255))


# LENT, UTILISER DOT
def filtre_sepia(pil_image, r1, g1, b1): # RGB : choisir l'intencité
    table_sepia = calculs.table_sepia(r1, g1, b1)
    matrice_pixel = passer_en_matrice(pil_image)
    print(table_sepia)
    for i in range(matrice_pixel.shape[0]):
        for j in range(matrice_pixel.shape[1]):
            r2, g2, b2, a2 = (matrice_pixel[i, j])
            
            r3 = int(r2 * table_sepia[0][0] + g2 * table_sepia[0][1] + b2 * table_sepia[0][2])
            g3 = int(r2 * table_sepia[1][0] + g2 * table_sepia[1][1] + b2 * table_sepia[1][2])
            b3 = int(r2 * table_sepia[2][0] + g2 * table_sepia[2][1] + b2 * table_sepia[2][2])
            matrice_pixel[i, j] = [np.clip(r3, 0, 255), np.clip(g3, 0, 255), np.clip(b3, 0, 255), a2]
    return passer_en_image(matrice_pixel)


def correction_gamma(pil_image, facteur):
    matrice_pixel = passer_en_matrice(pil_image)
    
    gamma = 2**(-facteur)
    max_value = float(np.iinfo(matrice_pixel.dtype).max)
    matrice_gamma = matrice_pixel.astype(np.float64)
    matrice_gamma = max_value*(matrice_gamma/max_value)**gamma
    matrice_gamma = matrice_gamma.astype(np.uint8)
    #img_ajustee = Image.fromarray(matrice_gamma)
    
    return passer_en_image(matrice_gamma)


def passer_en_matrice(pil_image):
    return np.array(pil_image)


def passer_en_image(matrice_pixel):
    pil_image = Image.fromarray(matrice_pixel)
    a = (ImageTk.PhotoImage(pil_image), pil_image) # https://stackoverflow.com/questions/18369936
    return a

