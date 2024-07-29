import numpy as np
from vectorObject import Vector_Object as vt

class Structures:
    def __init__(self):
        self.distArray = np.array([], dtype=vt)
        self.forceArray = np.array([], dtype=vt)
        self.momentArray = np.array([], dtype=vt)
        self.totalSumMoment = 0
        self.totalSumForce = 0
        self.totalForces = np.array([], dtype=vt)
        self.totalMoments = np.array([], dtype=vt)
        
        #self.calculate_totals()

    # Distances
    def add_distance(self, vector):
        self.distArray = np.append(self.distArray, vector)

    def delete_distance(self, index):
        self.distArray = np.delete(self.distArray, index)

    def read_distance(self, index):
        try:
            return self.distArray[index].get_coords()
        except IndexError:
            raise IndexError("Index out of range")

    def clear_distances(self):
        self.distArray = np.array([], dtype=vt)

    def read_all_distances(self):
        print("Distancias")
        return [vector.get_coords() for vector in self.distArray]

    # Forces
    def add_force(self, vector):
        self.forceArray = np.append(self.forceArray, vector)

    def delete_force(self, index):
        self.forceArray = np.delete(self.forceArray, index)

    def read_force(self, index):
        try:
            return self.forceArray[index].get_coords()
        except IndexError:
            raise IndexError("Index out of range")

    def clear_forces(self):
        self.forceArray = np.array([], dtype=vt)

    def read_all_forces(self):
        print("Fuerzas")
        return [vector.get_coords() for vector in self.forceArray]

    # Moments
    def add_moment(self, vector):
        self.momentArray = np.append(self.momentArray, vector)

    def delete_moment(self, index):
        self.momentArray = np.delete(self.momentArray, index)

    def read_moment(self, index):
        try:
            return self.momentArray[index].get_coords()
        except IndexError:
            raise IndexError("Index out of range")

    def clear_moments(self):
        self.momentArray = np.array([], dtype=vt)

    def read_all_moments(self):
        print("Momentos")
        return [vector.get_coords() for vector in self.momentArray]

    # Sum Forces and Moments
    def sum_f_m(self):
        self.totalSumForce = np.sum([vector.get_coords() for vector in self.forceArray], axis=0)
        self.totalSumMoment = np.sum([vector.get_coords() for vector in self.momentArray], axis=0)

    # Calculate Totals for Forces and Moments by Common Pointers
            
    def calculate_totals(self):
        total_forces = []
        total_moments = []

        for dist in self.distArray:
            if dist is not None and hasattr(dist, 'coords'):
                dist_coords = np.array(dist.coords, dtype=float)
                if not np.isnan(dist_coords).any():
                    temp_forces = []
                    temp_moments = []

                    # Find forces with the same pointer as dist
                    for force in self.forceArray:
                        if force.next is dist:
                            coords = force.get_coords()
                            if coords is not None:
                                coords = np.array(coords, dtype=float)
                                if not np.isnan(coords).any():
                                    temp_forces.append(coords)

                    # Find moments with the same pointer as dist
                    for moment in self.momentArray:
                        if moment.next is dist:
                            coords = moment.get_coords()
                            if coords is not None:
                                coords = np.array(coords, dtype=float)
                                if not np.isnan(coords).any():
                                    temp_moments.append(coords)

                    if temp_forces:
                        total_force = np.sum(temp_forces, axis=0)
                        if not np.isnan(total_force).any():
                            dist_float = np.array(dist.coords, dtype=float)
                            total_forces.append(vt(total_force, dist_float))

                    if temp_moments:
                        total_moment = np.sum(temp_moments, axis=0)
                        if not np.isnan(total_moment).any():
                            dist_float = np.array(dist.coords, dtype=float)
                            total_moments.append(vt(total_moment, dist_float))

        self.totalforce = np.array(total_forces, dtype=object)
        self.totalmoment = np.array(total_moments, dtype=object)
        self.sum_f_m()

        print("Total Forces Calculated:", self.totalforce)
        print("Total Moments Calculated:", self.totalmoment)
