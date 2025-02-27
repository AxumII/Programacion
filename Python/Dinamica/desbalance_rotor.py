import numpy as np
import sympy as sp

class desb:
    def __init__(self, w_t = 1, alpha = 0, r_ctr_d = 0.038):
        self.w_t = w_t
        self.alpha = alpha
        L_n = []
        self.L = np.sum(np.array(L_n))
        self.r_ctr_d= r_ctr_d
        D1_existencia = [1, 0, 1, 1]
        D1_masa = [10.5, 5.0, 8.3, 7.2]

        D2_existencia = [0, 1, 1, 0]
        D2_masa = [6.4, 7.1, 9.2, 3.3]

        D3_existencia = [1, 1, 0, 1]
        D3_masa = [12.7, 8.8, 4.5, 11.3]


    def circulo(self, theta_init = 0, n = 100):
        theta = np.linspace(0 + theta_init, 2*np.pi + theta_init, n)
        x = self.r_ctr_d*np.cos(theta)
        y = self.r_ctr_d*np.sen(theta)
        return x,y
    
    


    def pIn_disco(self, D ,x ,y ,l ):
        Ixz = 0
        Iyz = 0
        for i in D:
            Ixz += D[i]*x*l 
            Iyz += D[i]*y*l 

        


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
        
        Ixz_B, Iyz_B = In_B 
        Ay =    (((-1*Ixz_B * self.alpha ) + (Iyz_B * self.w_t**2 )) / self.L)
        Ax =    -1*(((-1*Iyz_B * self.alpha ) + (-1*Ixz_B * self.w_t**2 )) / self.L)

        B = [Bx,By]
        A = [Ax,Ay]
        return A,B
    
    def distancias_desbalance(self):
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