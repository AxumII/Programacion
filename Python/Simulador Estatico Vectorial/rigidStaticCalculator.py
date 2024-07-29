import numpy as np
from vectorObject import Vector_Object as vt

class RigidStaticCalculator:
    def __init__(self):
        self.distArray = np.array([], dtype=vt)
        self.forceArray = np.array([], dtype=vt)
        self.momentArray = np.array([], dtype=vt)
        self.totalForces = np.array([], dtype=vt)        
        self.totalF= 0
        self.totalM = 0

##############################################################################
#CRUD


    #####################################################
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


    ######################################################
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


    ##############################################################
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
    

#####################################################################################
#Analisis

    def sum_f_m(self):
        self.totalF = np.sum([vector.get_coords() for vector in self.forceArray], axis=0)
        self.totalM = np.sum([vector.get_coords() for vector in self.momentArray], axis=0)

    def calculate_moments(self):
        def momento(dist, force):
            return np.cross(dist.get_coords(), force.get_coords())
        
        for dist in self.distArray:
            temp_forces = []
            for force in self.forceArray:
                if force.next is dist:  
                    temp_forces.append(force)

            if temp_forces:
                total_force = np.sum([f.get_coords() for f in temp_forces], axis=0)
                moment_coords = momento(dist, vt(coords=total_force))
                moment = vt(coords=moment_coords)
                moment.next = dist

                self.momentArray = np.append(self.momentArray, moment)
                self.totalForces = np.append(self.totalForces, vt(coords=total_force))

        self.sum_f_m()
   