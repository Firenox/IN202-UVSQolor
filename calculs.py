import numpy as np

def table_sepia(r, g, b):
    l = np.array([[r, g, b],[r, g, b],[r, g, b]])
    l[0] = l[0] / (np.sum(l[0]) / r)
    l[1] = l[1]* g / (np.sum(l[1]) / g)
    l[2] = l[2]* b / (np.sum(l[2]) / b)

    return l
