'''
Traitements des images
'''
import numpy as np
from PIL import Image, ImageTk 
import calculs
from scipy.signal import convolve2d


# Annuler est dans traitements.py car passer_en_matrice() est utilisée par tous les filtres de fenetre_tkinter
annuler_liste = [None, None, None]
retablir_liste = [None, None, None]


def filtre_couleur(pil_image, couleur):
    matrice_pixel = passer_en_matrice(pil_image)
    nblig = matrice_pixel.shape[0]
    nbcol = matrice_pixel.shape[1]

    if couleur == 0:
        for i in range(nblig):
            for j in range(nbcol):
                matrice_pixel[i, j] = (0, matrice_pixel[i, j, 1], 0)

    if couleur == 1:
        for i in range(nblig):
            for j in range(nbcol):
                matrice_pixel[i, j] = (matrice_pixel[i, j, 0], 0, 0)

    if couleur == 2:
        for i in range(nblig):
            for j in range(nbcol):
                matrice_pixel[i, j] = (0, 0, matrice_pixel[i, j, 2])

    # GRIS
    if couleur == 3: # Gris
        # Calcul de la luminance
        luminance = (matrice_pixel[:, :, 0] * 0.299 + 
                     matrice_pixel[:, :, 1] * 0.587 + 
                     matrice_pixel[:, :, 2] * 0.114)
        
        # Même valeur de gris sur les 3 canaux (RGB)
        for i in range(3):
            matrice_pixel[:, :, i] = luminance

    return passer_en_image(np.clip(matrice_pixel, 0, 255).astype(np.uint8))


# LENT, UTILISER DOT
def filtre_sepia(pil_image, r1, g1, b1): # RGB : choisir l'intencité
    table_sepia = calculs.table_sepia(r1, g1, b1)
    matrice_pixel = passer_en_matrice(pil_image)
    # print(matrice_pixel)

    matrice_pixel = np.dot(matrice_pixel, table_sepia)

    matrice_pixel= np.clip(matrice_pixel, 0, 255)

    # passage en int
    return passer_en_image(matrice_pixel.astype(np.uint8))


def correction_gamma(pil_image, facteur):
    matrice_pixel = passer_en_matrice(pil_image)
    
    gamma = np.log(float(facteur)) / np.log(0.5) # https://stackoverflow.com/questions/10593100
    max_value = float(np.iinfo(matrice_pixel.dtype).max)
    matrice_gamma = matrice_pixel.astype(np.float64)
    matrice_gamma = max_value*(matrice_gamma/max_value)**gamma
    matrice_gamma = matrice_gamma.astype(np.uint8)
    #img_ajustee = Image.fromarray(matrice_gamma)
    
    return passer_en_image(matrice_gamma)


def correction_contraste(pil_image, facteur, p):
    matrice_pixel = passer_en_matrice(pil_image)
    
    max_value = float(np.iinfo(matrice_pixel.dtype).max)
    matrice_contraste = matrice_pixel.astype(np.float64)
    for i in range(matrice_contraste.shape[0]): # Lent
        for j in range(matrice_contraste.shape[1]):
            for k in range(3): #RGB
                x = matrice_contraste[i, j, k]/max_value
                if x <= p:
                    matrice_contraste[i, j, k] = (p*(x/p)**facteur)*max_value
                else :
                    matrice_contraste[i, j, k] = (1 - (1-p)*((1-x)/(1-p))**facteur)*max_value

    
    return passer_en_image(matrice_contraste.astype(np.uint8))


def filtre_flou(pil_image):
    matrice_pixel = passer_en_matrice(pil_image)
    matrice_pixel = matrice_pixel.astype(np.float64)
    matrice_pixel2 = matrice_pixel.copy()
    noyeau = np.array([[1/9, 1/9, 1/9],
                      [1/9, 1/9, 1/9],
                      [1/9, 1/9, 1/9]])

    for i in range(3):
        matrice_pixel2[:,:,i] = convolve2d(matrice_pixel[:,:,i], noyeau, boundary='symm', mode='same')
    return passer_en_image(matrice_pixel2.astype(np.uint8))


def filtre_nettete(pil_image):
    matrice_floue = passer_en_matrice(filtre_flou(pil_image)[1])

    matrice_pixel = passer_en_matrice(pil_image)
    matrice_pixel = matrice_pixel.astype(np.float64)

    nettete = matrice_pixel - matrice_floue
    matrice_pixel = (matrice_pixel + nettete)

    return passer_en_image(np.clip(matrice_pixel, 0, 255).astype(np.uint8))


def filtre_fusion(pil_image, pil_image2): # Les images sont toujours à la même taille
    matrice_pixel = passer_en_matrice(pil_image)
    matrice_pixel = matrice_pixel.astype(np.float64)

    matrice_pixel2 = passer_en_matrice(pil_image2)
    matrice_pixel2 = matrice_pixel2.astype(np.float64)

    image2_alpha = matrice_pixel2[:,:,3]/255

    for i in range(3):
        matrice_pixel[:,:,i] = matrice_pixel[:,:,i] + matrice_pixel2[:,:,i]* image2_alpha

    matrice_pixel = np.clip(matrice_pixel, 0 , 255)
    return passer_en_image(matrice_pixel.astype(np.uint8))


def filtre_bords(pil_image):
    matrice_pixel = passer_en_matrice(pil_image)
    matrice_pixel = matrice_pixel.astype(np.float64)
    
    #Matrice vide de même taille pour stocker le résultat
    matrice_bords = np.zeros_like(matrice_pixel)
    
    # Noyau de convolution pour la détection des contours (Laplacien)
    noyau = np.array([[-1, -1, -1],
                      [-1,  8, -1],
                      [-1, -1, -1]])

    # Application du noyau sur chaque canal RGB
    for i in range(3):
        matrice_bords[:, :, i] = convolve2d(matrice_pixel[:, :, i], noyau, boundary='symm', mode='same')
        
    return passer_en_image(np.clip(matrice_bords, 0, 255).astype(np.uint8))


def passer_en_matrice(pil_image):
    global annuler_liste
    annuler_liste[0],annuler_liste[1],annuler_liste[2] = annuler_liste[1], annuler_liste[2], pil_image
    return np.array(pil_image)


def passer_en_image(matrice_pixel):
    pil_image = Image.fromarray(matrice_pixel)
    a = (ImageTk.PhotoImage(pil_image), pil_image) # https://stackoverflow.com/questions/18369936

    return a