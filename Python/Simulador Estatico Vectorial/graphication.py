import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Graphication:
    def __init__(self, RSC_instance, Wrench_instance, Ffs=1, Fms=1):
        self.distArray = RSC_instance.distArray
        self.forceArray = RSC_instance.forceArray
        self.momentArray = RSC_instance.momentArray
        self.totalForces = RSC_instance.totalForces
        self.totalF = Wrench_instance.totalF
        self.totalM = Wrench_instance.totalM
        self.IIMoment = Wrench_instance.IIMoment
        self.TMoment = Wrench_instance.TMoment
        self.valid_positions = Wrench_instance.valid_positions
        self.Ffs = Ffs
        self.Fms = Fms

    def graf_dfm(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        avg_dist, avg_force, avg_moment = self.avg()
        max_coords, min_coords = self.max_min(self.distArray)

        FactorForceScale = 1
        FactorMomentScale = 1

        if np.linalg.norm(avg_force) / np.linalg.norm(avg_dist) >= 1:
            FactorForceScale = np.linalg.norm(avg_dist) / np.linalg.norm(avg_force) * self.Ffs
        else:
            FactorForceScale = np.linalg.norm(avg_force) / np.linalg.norm(avg_dist) * self.Ffs

        if np.linalg.norm(avg_moment) / np.linalg.norm(avg_dist) >= 1:
            FactorMomentScale = np.linalg.norm(avg_dist) / np.linalg.norm(avg_moment) * self.Fms
        else:
            FactorMomentScale = np.linalg.norm(avg_moment) / np.linalg.norm(avg_dist) * self.Fms

        FactorForceScale = round(FactorForceScale, 4)
        FactorMomentScale = round(FactorMomentScale, 4)

        # Recalcular los límites con las fuerzas y momentos escalados
        all_coords = np.vstack([
            vec.get_coords() for vec in self.distArray] +
            [vec.next.get_coords() + vec.get_coords() * FactorForceScale for vec in self.forceArray] +
            [vec.next.get_coords() + vec.get_coords() * FactorMomentScale for vec in self.momentArray if vec.next is not None]
        )

        max_range = np.max(np.abs(all_coords))
        ax.set_xlim([-max_range, max_range])
        ax.set_ylim([-max_range, max_range])
        ax.set_zlim([-max_range, max_range])

        ax.plot([-max_range, max_range], [0, 0], [0, 0], 'k--', linewidth=3, label='Eje X')
        ax.plot([0, 0], [-max_range, max_range], [0, 0], '--', color=(0.35, 0, 0.35), linewidth=3, label='Eje Y')
        ax.plot([0, 0], [0, 0], [-max_range, max_range], '--', color=(0.4, 0.1, 0.1), linewidth=3, label='Eje Z')

        arrow_params = {
            'arrow_length_ratio': 0.05,
            'linewidth': 1.5,
        }

        for vec in self.distArray:
            coords = vec.get_coords()
            ax.quiver(0, 0, 0, coords[0], coords[1], coords[2], color='r', **arrow_params)

        for vec in self.forceArray:
            pos = vec.next.get_coords()
            Force_scaled = vec.get_coords() * FactorForceScale
            ax.quiver(pos[0], pos[1], pos[2], Force_scaled[0], Force_scaled[1], Force_scaled[2], color='g', **arrow_params)

        for vec in self.momentArray:
            pos = vec.next.get_coords() if vec.next is not None else np.array([0, 0, 0])
            Moment_scaled = vec.get_coords() * FactorMomentScale
            ax.quiver(pos[0], pos[1], pos[2], Moment_scaled[0], Moment_scaled[1], Moment_scaled[2], color='b', **arrow_params)

        ax.scatter([], [], [], color='r', label='Distancias')
        ax.scatter([], [], [], color='g', label=f'Fuerzas (escala: {FactorForceScale})')
        ax.scatter([], [], [], color='b', label=f'Momentos (escala: {FactorMomentScale})')

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        plt.legend()
        plt.show()

    def graf_wr(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        max_vals, min_vals = self.max_min([self.totalF, self.totalM, self.TMoment, self.IIMoment] + list(self.valid_positions), vector_type=False)

        # Unificar la escala de los ejes
        max_range = np.array([max_vals[0] - min_vals[0], max_vals[1] - min_vals[1], max_vals[2] - min_vals[2]]).max()
        mid_x = (max_vals[0] + min_vals[0]) * 0.5
        mid_y = (max_vals[1] + min_vals[1]) * 0.5
        mid_z = (max_vals[2] + min_vals[2]) * 0.5

        ax.set_xlim(mid_x - max_range / 2, mid_x + max_range / 2)
        ax.set_ylim(mid_y - max_range / 2, mid_y + max_range / 2)
        ax.set_zlim(mid_z - max_range / 2, mid_z + max_range / 2)

        ax.plot([min_vals[0], max_vals[0]], [0, 0], [0, 0], 'k--', linewidth=3, label='Eje X')
        ax.plot([0, 0], [min_vals[1], max_vals[1]], [0, 0], '--', color=(0.35, 0, 0.35), linewidth=3, label='Eje Y')
        ax.plot([0, 0], [0, 0], [min_vals[2], max_vals[2]], '--', color=(0.4, 0.1, 0.1), linewidth=3, label='Eje Z')

        arrow_params = {
            'arrow_length_ratio': 0.05,
            'linewidth': 1.5,
        }

        totalF = self.totalF
        ax.quiver(0, 0, 0, totalF[0], totalF[1], totalF[2], color='g', **arrow_params)

        totalM = self.totalM
        ax.quiver(0, 0, 0, totalM[0], totalM[1], totalM[2], color='b', **arrow_params)

        TMoment = self.TMoment
        ax.quiver(0, 0, 0, TMoment[0], TMoment[1], TMoment[2], color='m', **arrow_params)

        IIMoment = self.IIMoment
        ax.quiver(0, 0, 0, IIMoment[0], IIMoment[1], IIMoment[2], color='c', **arrow_params)

        valid_positions = np.array([pos for pos in self.valid_positions])
        ax.scatter(valid_positions[:, 0], valid_positions[:, 1], valid_positions[:, 2], color='k', label='Posiciones válidas', s=30)

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
