from vectorObject import Vector_Object as vt
from structures import Structures as st

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Graphication:
    def __init__(self, structures):
        # Cargar los arrays desde la instancia de structures
        self.structures = structures
        self.distArray = structures.distArray
        self.forceArray = structures.forceArray
        self.momentArray = structures.momentArray

    def prom(self):
        def average_coords(array):
            total = sum(vec.coords for vec in array)
            return total / len(array) if array.size else np.zeros(3)
        
        avg_dist = average_coords(self.distArray)
        avg_force = average_coords(self.forceArray)
        avg_moment = average_coords(self.momentArray)

        return avg_dist, avg_force, avg_moment

    def graf(self, Multpdf= 1/10, Multpdm = 1/12):
        promD, promF, promM = self.prom()
        forceMultp = (Multpdf * promD) / promF if np.any(promF) else np.zeros(3)
        momMultp = ( Multpdm * promD) / promM if np.any(promM) else np.zeros(3)

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Encontrar las dimensiones máximas y mínimas para los ejes
        all_vectors = np.concatenate((self.distArray, self.forceArray, self.momentArray))
        max_coords = np.max([vec.coords for vec in all_vectors], axis=0)
        min_coords = np.min([vec.coords for vec in all_vectors], axis=0)

        # Graficar ejes extendidos como líneas punteadas más gruesas
        ax.plot([min_coords[0], max_coords[0]], [0, 0], [0, 0], 'k--', linewidth=3, label='Eje X')
        ax.plot([0, 0], [min_coords[1], max_coords[1]], [0, 0], 'k--', linewidth=3, label='Eje Y')
        ax.plot([0, 0], [0, 0], [min_coords[2], max_coords[2]], 'k--', linewidth=3, label='Eje Z')

        # Parámetros de flechas
        arrow_params = {
            'arrow_length_ratio': 0.05,#proporcion cabeza flecha
            'linewidth': 1.5, #grosor            
                    }

        # Graficar distArray
        for vec in self.distArray:
            ax.quiver(0, 0, 0, vec.coords[0], vec.coords[1], vec.coords[2], color='r', **arrow_params)

        # Graficar forceArray con posición escalada
        for vec in self.forceArray:
            position = vec.next.coords
            scaled_force = vec.coords * forceMultp
            ax.quiver(position[0], position[1], position[2], scaled_force[0], scaled_force[1], scaled_force[2], color='g', **arrow_params)

        # Graficar momentArray con posición escalada
        for vec in self.momentArray:
            position = vec.next.coords
            scaled_moment = vec.coords * momMultp
            ax.quiver(position[0], position[1], position[2], scaled_moment[0], scaled_moment[1], scaled_moment[2], color='b', **arrow_params)

        # Añadir leyendas
        ax.scatter([], [], [], color='r', label='Distancias')
        ax.scatter([], [], [], color='g', label=f'Fuerzas (mult: {forceMultp})')
        ax.scatter([], [], [], color='b', label=f'Momentos (mult: {momMultp})')

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        plt.legend()
        plt.show()
