import numpy as np
from vectorObject import Vector_Object as vt
from rigidStaticCalculator import RigidStaticCalculator as RSC
from scipy.linalg import solve

class Wrench:
    def __init__(self,totalF,totalM):
        self.totalF = np.array(totalF).flatten()
        self.totalM = np.array(totalM).flatten()
        self.IIMoment = None
        self.TMoment = None        
        self.valid_positions =  []
        self.__tol = 1e-8

        self.find_wrench()
        self.positions = self.position_solver(self.totalF, self.TMoment)
        self.verify_positions()



    def find_wrench(self):
        try:
            UnitF = self.totalF / np.linalg.norm(self.totalF)
        except ZeroDivisionError:
            UnitF = np.zeros_like(self.totalF)
        

        Lambda = np.dot(UnitF, self.totalM)
        self.IIMoment = Lambda * UnitF
        self.TMoment = self.totalM - self.IIMoment


    def position_solver(self, F, M):
        results = []
        if np.all(F == 0):
            return results

        # Caso 1: x = 0, resolver para y y z
        A1 = np.array([
            [0, F[0]],    # Ecuación My: término de z
            [-F[0], 0]    # Ecuación Mz: término de y
        ])
        b1 = np.array([M[1], M[2]])
        try:
            solution1 = (np.linalg.solve(A1, b1))
            results.append(np.array([0, solution1[0], solution1[1]]))  
        except np.linalg.LinAlgError:
            print("Matriz singular en caso 1")

        # Caso 2: y = 0, resolver para x y z
        A2 = np.array([
            [-F[1], 0],   # Mx equation
            [0, F[1]]     # Mz equation
        ])
        b2 = np.array([M[0], M[2]])
        try:
            solution2 = (np.linalg.solve(A2, b2))
            results.append(np.array([solution2[1], 0, solution2[0]]))  # [x, 0, z]
        except np.linalg.LinAlgError:
            print("Matriz singular en caso 2")

        # Caso 3: z = 0, resolver para x y y
        A3 = np.array([
            [0, F[2]],    # Ecuación Mx: término de y
            [-F[2], 0]    # Ecuación My: término de x
        ])
        b3 = np.array([M[0], M[1]])
        try:
            solution3 = (np.linalg.solve(A3, b3))
            results.append(np.array([solution3[0], solution3[1], 0]))  
        except np.linalg.LinAlgError:
            print("Matriz singular en caso 3")

        return results
    






    def verify_positions(self):        
        for pos in self.positions:
            calculated_moment = np.cross(pos,self.totalF)
            if np.allclose(calculated_moment, self.TMoment, atol=self.__tol, rtol=1e-3):
                self.valid_positions.append(pos)
            # Impresión para depuración            
            #print("Posición: {}, Momento Calculado: {}, Momento Objetivo: {}".format(pos, calculated_moment, self.TMoment))
           
        
    