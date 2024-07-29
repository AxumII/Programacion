from vectorObject import Vector_Object as vt
from structures import Structures as st
import numpy as np

class Rigid_Static_Calculator:
    def __init__(self, structures):
        # Cargar los arrays desde la instancia de structures
        self.structures = structures
        self.distArray = structures.distArray
        self.forceArray = structures.forceArray
        self.momentArray = structures.momentArray
        self.vlist = []
    
    def momento(self, dist, force):
        return np.cross(dist.get_coords(), force.get_coords())
    
    def clasif(self):
        for dist in self.distArray:
            temp_forces = []
            #print(f"Checking dist: {dist.get_coords()}")
            for force in self.forceArray:
                if force.next is dist:  # Comprobar referencia del objeto
                    temp_forces.append(force)
                    #print(f"Matching force found: {force.get_coords()}")
            if temp_forces:
                total_force = np.sum([f.get_coords() for f in temp_forces], axis=0)
                #print(f"Total force for {dist.get_coords()}: {total_force}")
                moment_coords = self.momento(dist, vt(coords=total_force))
                moment = vt(coords=moment_coords)
                moment.next = dist
                self.structures.momentArray = np.append(self.structures.momentArray, moment)
                #print(f"Added moment: {moment_coords}")