from vectorObject import Vector_Object as vt
from rigidStaticCalculator import RigidStaticCalculator as RSC
from wrench import Wrench as wr

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Graphication:
    def __init__(self, RSC_instance, Wrench_instance):
        # Cargar los arrays desde las instancias
        self.distArray = RSC_instance.distArray
        self.forceArray = RSC_instance.forceArray
        self.momentArray = RSC_instance.momentArray
        self.totalForces = RSC_instance.totalForces
        self.totalF = Wrench_instance.totalF
        self.totalM = Wrench_instance.totalM
        self.IIMoment = Wrench_instance.IIMoment
        self.TMoment = Wrench_instance.TMoment
        self.valid_positions = Wrench_instance.valid_positions

    def graf_dfm(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Obtener promedios y fijar tamaño de ejes
        avg_dist, avg_force, avg_moment = self.avg()
        max_coords, min_coords = self.max_min(self.distArray)

        ax.plot([min_coords[0], max_coords[0]], [0, 0], [0, 0], 'k--', linewidth=3, label='Eje X')
        ax.plot([0, 0], [min_coords[1], max_coords[1]], [0, 0], '--', color=(0.35, 0, 0.35), linewidth=3, label='Eje Y')
        ax.plot([0, 0], [0, 0], [min_coords[2] - 2, max_coords[2]], '--', color=(0.4, 0.1, 0.1), linewidth=3, label='Eje Z')

        ForceScale = 1
        MomentScale = 1

        if np.linalg.norm(avg_force) / np.linalg.norm(avg_dist) >= 1:
            print("Fuerza es mayor")
            ForceScale = np.linalg.norm(avg_dist) / np.linalg.norm(avg_force) * 0.1
        else:
            print("Fuerza es menor")
            ForceScale = np.linalg.norm(avg_force) / np.linalg.norm(avg_dist) * 0.1

        if np.linalg.norm(avg_moment) / np.linalg.norm(avg_dist) >= 1:
            print("Momento es mayor")
            MomentScale = np.linalg.norm(avg_dist) / np.linalg.norm(avg_moment) * 0.1
        else:
            print("Momento es menor")
            MomentScale = np.linalg.norm(avg_moment) / np.linalg.norm(avg_dist) * 0.1

        arrow_params = {
            'arrow_length_ratio': 0.05,  # proporción cabeza flecha
            'linewidth': 1.5,  # grosor
        }

        # Graficar distArray
        for vec in self.distArray:
            coords = vec.get_coords()
            ax.quiver(0, 0, 0, coords[0], coords[1], coords[2], color='r', **arrow_params)

        # Graficar forceArray con posición escalada
        for vec in self.forceArray:
            position = vec.next.get_coords()
            scaled_force = vec.get_coords() * ForceScale
            ax.quiver(position[0], position[1], position[2], scaled_force[0], scaled_force[1], scaled_force[2], color='g', **arrow_params)

        # Graficar momentArray con posición escalada
        for vec in self.momentArray:
            if vec.next is not None:
                position = vec.next.get_coords()
            else:
                position = np.array([0, 0, 0])
            scaled_moment = vec.get_coords() * MomentScale
            ax.quiver(position[0], position[1], position[2], scaled_moment[0], scaled_moment[1], scaled_moment[2], color='b', **arrow_params)

        # Añadir leyendas
        ax.scatter([], [], [], color='r', label='Distancias')
        ax.scatter([], [], [], color='g', label=f'Fuerzas (escala: {ForceScale})')
        ax.scatter([], [], [], color='b', label=f'Momentos (escala: {MomentScale})')

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        plt.legend()
        plt.show()

    def graf_wr(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Obtener los máximos y mínimos
        max_vals, min_vals = self.max_min([self.totalF, self.totalM, self.TMoment, self.IIMoment] + list(self.valid_positions), vector_type=False)

        # Graficar los ejes con tope en los máximos y mínimos
        ax.plot([min_vals[0], max_vals[0]], [0, 0], [0, 0], 'k--', linewidth=3, label='Eje X')
        ax.plot([0, 0], [min_vals[1], max_vals[1]], [0, 0], '--', color=(0.35, 0, 0.35), linewidth=3, label='Eje Y')
        ax.plot([0, 0], [0, 0], [min_vals[2], max_vals[2]], '--', color=(0.4, 0.1, 0.1), linewidth=3, label='Eje Z')

        arrow_params = {
            'arrow_length_ratio': 0.05,  # proporción cabeza flecha
            'linewidth': 1.5,  # grosor
        }

        # Graficar Fuerza Total
        totalF = self.totalF
        ax.quiver(0, 0, 0, totalF[0], totalF[1], totalF[2], color='g', **arrow_params)

        # Graficar Momento Total
        totalM = self.totalM
        ax.quiver(0, 0, 0, totalM[0], totalM[1], totalM[2], color='b', **arrow_params)

        # Graficar T Momento
        TMoment = self.TMoment
        ax.quiver(0, 0, 0, TMoment[0], TMoment[1], TMoment[2], color='m', **arrow_params)

        # Graficar II Momento
        IIMoment = self.IIMoment
        ax.quiver(0, 0, 0, IIMoment[0], IIMoment[1], IIMoment[2], color='c', **arrow_params)

        # Graficar valid_positions
        valid_positions = np.array([pos for pos in self.valid_positions])
        ax.scatter(valid_positions[:, 0], valid_positions[:, 1], valid_positions[:, 2], color='k', label='Posiciones válidas', s=30)

        # Ajustar límites de los ejes basados en los máximos y mínimos
        ax.set_xlim([min_vals[0], max_vals[0]])
        ax.set_ylim([min_vals[1], max_vals[1]])
        ax.set_zlim([min_vals[2], max_vals[2]])

        # Sombrear planos X, Y, Z
        x = np.linspace(min_vals[0], max_vals[0], 100)
        y = np.linspace(min_vals[1], max_vals[1], 100)
        z = np.linspace(min_vals[2], max_vals[2], 100)
        X, Y = np.meshgrid(x, y)
        Z = np.zeros_like(X)
        ax.plot_surface(X, Y, Z, color='r', alpha=0.2)
        X, Z = np.meshgrid(x, z)
        Y = np.zeros_like(X)
        ax.plot_surface(X, Y, Z, color='g', alpha=0.2)
        Y, Z = np.meshgrid(y, z)
        X = np.zeros_like(Y)
        ax.plot_surface(X, Y, Z, color='b', alpha=0.2)

        # Añadir leyendas
        ax.scatter([], [], [], color='g', label='Fuerza Total')
        ax.scatter([], [], [], color='b', label='Momento Total')
        ax.scatter([], [], [], color='m', label='T Momento')
        ax.scatter([], [], [], color='c', label='II Momento')
        ax.scatter([], [], [], color='k', label='Posiciones válidas')

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        plt.legend()
        plt.show()

    def avg(self):
        avg_dist = np.mean([vector.get_coords() for vector in self.distArray], axis=0)
        avg_force = np.mean([vector.get_coords() for vector in self.forceArray], axis=0)
        avg_moment = np.mean([vector.get_coords() for vector in self.momentArray], axis=0)
        return avg_dist, avg_force, avg_moment


    def max_min(self, data, vector_type=True):
        if vector_type:
            all_coords = np.array([vector.get_coords() for vector in data])
        else:
            all_coords = np.array(data)
        max_vals = np.max(all_coords, axis=0)
        min_vals = np.min(all_coords, axis=0)
        return max_vals, min_vals
