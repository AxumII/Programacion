import numpy as np
import sympy as sp

class Desbalance:
    def __init__(self, k_h=80, k_v = 80, w_t=1, alpha=0, r_ctr_d=1,  L_n=[0.0739, 0.1546, 0.235], L=2, W_peso = -1, L_ctr =1,
                 D1_ex=[0, 0, 0, 0], D1_m=[0, 0, 0, 0], 
                 D2_ex=[0, 1, 0, 0], D2_m=[0, 1, 0, 0], 
                 D3_ex=[0, 0, 0, 0], D3_m=[0, 0, 0, 0], 
                 theta_init=45):
        self.theta_init = 0
        self.w_t = w_t #Frecuencia Forzada (Rev/s)
        self.alpha = alpha #Aceleracion Angular (requiere torque e Iz)
        self.L_n = L_n  # Distancias de D1, D2 y D3 respecto a A
        self.L = L  # Longitud total
        self.L_ctr = L_ctr #Distancia desde A al centroide total
        self.r_ctr_d = r_ctr_d  # Radio de círculo centroidal de masas
        self.k_h = k_h  # Constante de rigidez resortes horizontales
        self.k_v = k_v  # Constante de rigidez resortes verticales
        self.W_peso = W_peso
        # Generar posiciones automáticamente a partir del ángulo inicial
        self.posiciones = [self.circulo(theta_init), self.circulo(theta_init + 90), 
                           self.circulo(theta_init - 90), self.circulo(theta_init + 180)]

        # Definir estructuras de D1, D2, y D3 con posiciones generadas
        self.D1 = np.array([D1_ex, D1_m, self.posiciones], dtype=object)
        self.D2 = np.array([D2_ex, D2_m, self.posiciones], dtype=object)
        self.D3 = np.array([D3_ex, D3_m, self.posiciones], dtype=object)


    def circulo(self, theta_init):
        """ Retorna la posición (x, y) de un punto en el círculo. """
        theta = np.radians(theta_init)
        x = float(self.r_ctr_d * np.cos(theta))  # Asegurar valores escalares
        y = float(self.r_ctr_d * np.sin(theta))
        return (x, y)
    
    def pIn_disco(self, D, l):
        """
        Calcula Ixz e Iyz para un conjunto de masas y posiciones D (puede ser D1, D2 o D3).
        Ixz = masa * posición_x * l
        Iyz = masa * posición_y * l
        """
        Ixz, Iyz = 0, 0
        
        existencia, masa, posiciones = D[0], D[1], D[2]

        # Sumar contribuciones de cada elemento si existe
        for i in range(len(existencia)):
            if existencia[i] == 1:  # Si el elemento existe
                x, y = posiciones[i]  # Extraer x, y de la posición
                Ixz += masa[i] * x * l
                Iyz += masa[i] * y * l
        return Ixz, Iyz

    def Inercia(self):
        # Respecto a A
        Ixz_d1_A, Iyz_d1_A = self.pIn_disco(self.D1 , self.L_n[0])
        Ixz_d2_A, Iyz_d2_A = self.pIn_disco(self.D2 , self.L_n[1])
        Ixz_d3_A, Iyz_d3_A = self.pIn_disco(self.D3 , self.L_n[2])
        """
        print("Ixz A Calculado en el disco 1", Ixz_d1_A)
        print("Iyz A Calculado en el disco 1", Iyz_d1_A)
        print("Ixz A Calculado en el disco 2", Ixz_d2_A)  
        print("Iyz A Calculado en el disco 2", Iyz_d2_A)  
        print("Ixz A Calculado en el disco 3", Ixz_d3_A) 
        print("Iyz A Calculado en el disco 3", Iyz_d3_A)  
        """
        # Respecto a B (Invirtiendo las distancias)
        Ixz_d1_B, Iyz_d1_B = self.pIn_disco(self.D3 , - self.L +  self.L_n[2])
        Ixz_d2_B, Iyz_d2_B = self.pIn_disco(self.D2 , - self.L +  self.L_n[1])
        Ixz_d3_B, Iyz_d3_B = self.pIn_disco(self.D1 , - self.L +  self.L_n[0])
        """
        print("Ixz B Calculado en el disco 1", Ixz_d1_B)
        print("Iyz B Calculado en el disco 1", Iyz_d1_B)
        print("Ixz B Calculado en el disco 2", Ixz_d2_B)  
        print("Iyz B Calculado en el disco 2", Iyz_d2_B)  
        print("Ixz B Calculado en el disco 3", Ixz_d3_B) 
        print("Iyz B Calculado en el disco 3", Iyz_d3_B)  
        """
        # Sumar los valores para cada punto
        In_A = (Ixz_d1_A + Ixz_d2_A + Ixz_d3_A, Iyz_d1_A + Iyz_d2_A + Iyz_d3_A)
        In_B = (Ixz_d1_B + Ixz_d2_B + Ixz_d3_B, Iyz_d1_B + Iyz_d2_B + Iyz_d3_B)

    


        return In_A, In_B

    def solve_reacciones_din(self):
        """Se tienen dos apoyos, A y B siendo A el izquierdo y B el derecho
        Ya estan en equilibrio estatico, por lo que solo interesan las fuerzas dinamicas
        El eje Z es en el que rota el eje
        A---------------D1------------------D2------------------D3-----------------B
        Se tienen dos puntos de referencia, A para calcular las reacciones en B , B para calcular las reacciones en A
        #En A, L es positivo, pero respecto a B, L es negativo ya que apunta hacia A
        """
        In_A, In_B = self.Inercia()

        # Sistema de Referencia en A
        Ixz_A, Iyz_A = In_A
        By = (((Ixz_A * self.alpha ) - (Iyz_A * self.w_t ** 2 )) / self.L)
        Bx = (((-Iyz_A * self.alpha ) + (-Ixz_A * self.w_t ** 2 )) / self.L)

        # Sistema de Referencia en B
        Ixz_B, Iyz_B = In_B 
        Ay = (((-Ixz_B * self.alpha ) + (Iyz_B * self.w_t ** 2 )) / self.L)
        Ax = -(((-Iyz_B * self.alpha ) + (-Ixz_B * self.w_t ** 2 )) / self.L)

        return [Ax, Ay], [Bx, By]
    
    def solver_reacciones_est(self):
        
        M = np.array([[1,1], [0,self.L]])
        S = np.array([self.W_peso,self.W_peso*self.L_ctr ])
        return  np.linalg.solve(M,S)

    def distancias_desbalance(self):
        """
        Aca ya se conocen las reacciones dinamicas y estaticas, por lo que se procede a calcular la desviacion
        en cada apoyo en cada eje
        
        En el eje x, solo actuan las reacciones estaticas laterales y las reacciones dinamicas laterales, no hay fuerzas externas, el resorte no presenta deformacion (no hay fuerzas en x)
        ya que todas son por el peso que no esta en este eje y momentos minimos. por lo que estos resortes no estaran deformados
        
        En el eje y, actuan las reacciones estaticas verticuales y las dinamicas verticales. Las dinamicas ya las tenemos por calculo, mas las estaticas
        tienen en cuenta el peso de todo el sistema repartido en ambos apoyos. Esto implica que en estatico los resortes ya presentan una deformacion inicial de modo que toca tenerla en cuenta
        """
        [Ax_D, Ay_D], [Bx_D, By_D] = self.solve_reacciones_din()
        Ay_E, By_E = self.solver_reacciones_est()
        Ax = Ax_D 
        Ay = Ay_D + Ay_E
        Bx = Bx_D
        By = By_D + By_E
        

        X_a = 2 * Ax / self.k_h
        Y_a = 2 * Ay / self.k_v
        X_b = 2 * Bx / self.k_h
        Y_b = 2 * By / self.k_v
        
        return [X_a, Y_a], [X_b, Y_b]

    def cal_k(self):
        #se usa para saber cuanto se debe elongar el resorte con un K dado con una masa en mm
        #W = k*y
        #y = w/k
        m = 0.25
        return 9.81*m /self.k_h  *1000  , 9.81*m /self.k_v  *1000 


"""

#Ejemplos
default = Desbalance()
print(default.Inercia())
print(default.solve_reacciones_din())
#################################################################################################################
libro = Desbalance( w_t=125.7, alpha=3000, r_ctr_d=0.05, L_n=[0.15, 0.3, 0.45], L=0.6, theta_init=0, 
                 D1_ex=[0, 0, 0, 1], D1_m=[0, 0, 0, 0.3], 
                 D2_ex=[0, 1, 0, 0], D2_m=[0, 0.3, 0, 0], 
                 D3_ex=[0, 0, 0, 0], D3_m=[0, 0, 0, 0])
print("\nInercia en A y B (custom):", libro.Inercia())
print("Reacciones dinámicas en A y B (custom):", libro.solve_reacciones_din())
"""

"""
k_h = 500
k_v = 700
m_tornillo = 8/1000 #Gramos
L_t = 0.31
masa_t = (3*(36)) + (0.18) + ((15) + (15)) +((6)* (m_tornillo))  #3discos + Eje + 2 rodamientos + n Masas  EN GRAMOS
g = -9.81
W_peso_t = (masa_t*g)/1000
w_t  = (500)*(np.pi/30) #rpm


print("masa total gramos", masa_t)
print("peso total N", W_peso_t)
rotor = Desbalance(k_h=k_h, k_v=k_v ,w_t=w_t, alpha=0, r_ctr_d=0.035, L_n=[0.0739, 0.1546, 0.235], L= L_t, theta_init=0, L_ctr= L_t / 2, W_peso = W_peso_t,
                    D1_ex=[0, 1, 1, 1], D1_m=[0, m_tornillo, m_tornillo, m_tornillo], 
                    D2_ex=[0, 1, 0, 0], D2_m=[0, m_tornillo, 0, 0], 
                    D3_ex=[1, 0, 1, 0], D3_m=[m_tornillo, 0, m_tornillo, 0])

    # Calcular la inercia en A y B
inercia_rotor = rotor.Inercia()
print("\nInercia en A y B (rotor):", inercia_rotor)

    # Calcular las reacciones dinámicas en A y B
reacciones_din_rotor = rotor.solve_reacciones_din()
print("Reacciones dinámicas en A y B (rotor):", reacciones_din_rotor)

    # Calcular las reacciones Estaticas en A y B
reacciones_est_rotor = rotor.solver_reacciones_est()
print("Reacciones Estaticas en A y B (rotor):", reacciones_est_rotor)

    # Calcular las distancias de desbalance
desbalance_rotor = rotor.distancias_desbalance()
print("Distancias de desbalance en A y B (rotor): (x,y), Metros", desbalance_rotor)
desbalance_rotor * 1000
print("Distancias de desbalance en A y B (rotor): (x,y), Milímetros", [[x * 1000 for x in desbalance_rotor[0]], [y * 1000 for y in desbalance_rotor[1]]])


    #Distancia de elongacion de resorte para fabricacion
elongacion = rotor.cal_k()
print("La elongacion en mm es", elongacion)


"""
      