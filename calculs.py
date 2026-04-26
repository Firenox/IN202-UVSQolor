import numpy as np

def table_sepia(r, g, b):
    l = np.array([[r, g, b], [r, g, b], [r, g, b]])
    
    # On normalise (comme pour les logiciels de son)
    l[0] = l[0] * r / np.sum(l[0])
    l[1] = l[1] * g / np.sum(l[1])
    l[2] = l[2] * b / np.sum(l[2])
    return l
