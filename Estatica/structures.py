import numpy as np
from vectorObject import Vector_Object as vt

class Structures:
    def __init__(self):
        self.distArray = np.array([], dtype=vt)
        self.forceArray = np.array([], dtype=vt)
        self.momentArray = np.array([], dtype=vt)
        self.totalmoment = 0
        self.totalforce = 0
        self.sum_f_m()

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
        self.totalforce = np.sum([vector.get_coords() for vector in self.forceArray], axis=0)
        self.totalmoment = np.sum([vector.get_coords() for vector in self.momentArray], axis=0)
