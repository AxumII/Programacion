import numpy as np
import sympy as sp

class desb:
    def __init__(self, k = 40, w_t = 1, alpha = 0, r_ctr_d = 0.038, L = 0.1):
        self.w_t = w_t
        self.alpha = alpha
        self.k = k
        L_n = []
        self.L = np.sum(np.array(L_n))
        self.r_ctr_d= r_ctr_d
        
        #Propiedades Discos
        # Matriz de D1
        self.D1 = np.array([
            [1, 0, 1, 1],  # Existencia
            [10.5, 5.0, 8.3, 7.2],  # Masa
            [self.circulo(0), self.circulo(90), self.circulo(-90), self.circulo(180)]  # Posiciones
        ])

        # Matriz de D2
        self.D2 = np.array([
            [0, 1, 1, 0],  # Existencia
            [6.4, 7.1, 9.2, 3.3],  # Masa
            [self.circulo(0), self.circulo(90), self.circulo(-90), self.circulo(180)]  # Posiciones
        ])

        # Matriz de D3
        self.D3 = np.array([
            [1, 1, 0, 1],  # Existencia
            [12.7, 8.8, 4.5, 11.3],  # Masa
            [self.circulo(0), self.circulo(90), self.circulo(-90), self.circulo(180)]  # Posiciones
        ])


    def circulo(self, theta_init = 0, n = 180):
        #Permmite mapear un circulo con coordenadas rectngulares y un angulo inicial
        theta = np.linspace(0 + theta_init, 2*np.pi + theta_init, n)
        x = self.r_ctr_d*np.cos(theta)
        y = self.r_ctr_d*np.sin(theta)
        return x,y
    

    def pIn_disco(self,D,l):
        #Se obtiene cada masa con su distancia respectiva y se suman los pdInercia
        Ixz = 0
        Iyz = 0
        for i in range(D.shape[1]):
            existencia = D[0, i]
            masa = D[1, i]
            x, y = D[2, i]
            Ixz += existencia * masa * x * l
            Iyz += existencia * masa * y * l
            
        return Ixz, Iyz
    
    def Inercia(self):
        Ixz_d1, Iyz_d1 = self.pIn_disco(D = self.D1, l = 0.06)
        Ixz_d2, Iyz_d2 =  self.pIn_disco(D = self.D2, l = 0.12)
        Ixz_d3, Iyz_d3 =  self.pIn_disco(D = self.D3, l = 0.18)
        Ixz = Ixz_d1 + Ixz_d2 + Ixz_d3
        Iyz = Iyz_d1 + Iyz_d2 + Iyz_d3
        
        return Ixz, Iyz


    def solve_reacciones_din(self, In_A, In_B, Iz):
        """Se tienen dos apoyos, A y B siendo A el izquierdo y B el derecho
        Ya estan en equilibrio estatico, por lo que solo interesan las fuerzas dinamicas
        El eje Z es en el que rota el eje
        A---------------D1------------------D2------------------D3-----------------B
        Se tienen dos puntos de referencia, A para calcular las reacciones en B , B para calcular las reacciones en A
        #En A, L es positivo, pero respecto a B, L es negativo ya que apunta hacia A
        """
        #Sistema de Referencia en A
        Ixz_A, Iyz_A = In_A
        By =   -1*(((-1*Ixz_A * self.alpha ) + (Iyz_A * self.w_t**2 )) / self.L)
        Bx =    (((-1*Iyz_A * self.alpha ) + (-1*Ixz_A * self.w_t**2 )) / self.L)

        #Sistema de Referencia en B
        
<<<<<<< HEAD
        Ixz_B, Iyz_B = In_B 
        Ay =    (((-1*Ixz_B * self.alpha ) + (Iyz_B * self.w_t**2 )) / self.L)
        Ax =    -1*(((-1*Iyz_B * self.alpha ) + (-1*Ixz_B * self.w_t**2 )) / self.L)
=======
        M = np.array([[1,1], [0,self.L]])
        S = np.array([self.W_peso,self.W_peso*self.L_ctr ])
        return  np.linalg.solve(M,S)
>>>>>>> 4deb2acecce37bfc164f5670703a8c371ed9e553

        B = [Bx,By]
        A = [Ax,Ay]
        return A,B
    
    def distancias_desbalance(self, Bx, By, Ax, Ay):
        """
        Aca ya se conocen las reacciones dinamicas y estaticas, por lo que se procede a calcular la desviacion
        en cada apoyo en cada eje
        
        En el eje x, solo actuan las reacciones estaticas laterales y las reacciones dinamicas laterales, no hay fuerzas externas, el resorte no presenta deformacion (no hay fuerzas en x)
        ya que todas son por el peso que no esta en este eje y momentos minimos. por lo que estos resortes no estaran deformados
        
        En el eje y, actuan las reacciones estaticas verticuales y las dinamicas verticales. Las dinamicas ya las tenemos por calculo, mas las estaticas
        tienen en cuenta el peso de todo el sistema repartido en ambos apoyos. Esto implica que en estatico los resortes ya presentan una deformacion inicial de modo que toca tenerla en cuenta
        """

        X_b = 2*Bx / self.k
        Y_b = 2*By / self.k
        X_a = 2*Ax / self.k
        Y_a = 2*Ay / self.k
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
      
