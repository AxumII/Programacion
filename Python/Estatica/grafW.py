import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from wrench import Wrench as wr

class Graphication:
    def __init__(self, TotalF, TotalM, TMoment, IIMoment, vPos):
        self.TotalF = TotalF
        self.TotalM = TotalM
        self.TMoment = TMoment
        self.IIMoment = IIMoment
        self.vPos = vPos

        
    def graf(self):
        

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Encontrar las dimensiones máximas y mínimas para los ejes
        all_vectors = np.concatenate((self.distArray, self.forceArray, self.momentArray))
        max_coords = np.max([vec.coords for vec in all_vectors], axis=0)
        min_coords = np.min([vec.coords for vec in all_vectors], axis=0)

        # Graficar ejes extendidos como líneas punteadas más gruesas
        ax.plot([min_coords[0], max_coords[0]], [0, 0], [0, 0], 'k--', linewidth=3, label='Eje X')
        ax.plot([0, 0], [min_coords[1], max_coords[1]], [0, 0], '--', color=(0.35, 0, 0.35), linewidth=3, label='Eje Y')  # Morado oscuro
        ax.plot([0, 0], [0, 0], [min_coords[2], max_coords[2]], '--', color=(0.4, 0.1, 0.1), linewidth=3, label='Eje Z')  # Café


        # Parámetros de flechas
        arrow_params = {
            'arrow_length_ratio': 0.05,#proporcion cabeza flecha
            'linewidth': 1.5, #grosor            
                    }
        
