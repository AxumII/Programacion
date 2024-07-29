import sympy as sp
import numpy as np

class F_Transferencia:

    def __init__(self):
            # Definir símbolos como atributos
            self.t, self.s = sp.symbols('t s')   #Variables generales         
            self.X, self.Y = sp.symbols('X Y')   #Funciones laplace como simbolos
            self.R1, self.R2, self.R3, self.R4, self.C = sp.symbols('R1 R2 R3 R4 C')#Elementos electricos como variables
            self.w, self.A = sp.symbols('w A')
            
            
            # Definir funciones como atributos
            self.V_In = sp.Function('V_In')(self.t)
            self.V_Out = sp.Function('V_Out')(self.t)
            self.V_A = sp.Function('V_A')(self.t)
            self.V_B = sp.Function('V_B')(self.t)         
            
    
    def FTP1(self, R1_value, R2_value, R3_value, C_value):
        
        #Aca ya se plantea desde laplace
        """
        Recordando propiedades de Laplace

        L[diff(f,t)] = s*L[]
        L[integ(f,t)] = F(s)/s
        """
        # x = L[V_in]
        # y = L[V_out]
        
        VnL = (-1/(self.C*self.R1))*(self.Y/self.s)        
        print("Ecuacion Nodo:", VnL," En numerico: " , VnL.subs({self.C : C_value, self.R1: R1_value}), "\n")
        
        I1L = ((self.X - VnL) / self.R3)        
        print("Ecuacion I1:",I1L," En numerico: " , I1L.subs({self.C : C_value, self.R1: R1_value, self.R3: R3_value}), "\n")
        
        I2L = (VnL / self.R2)        
        print("Ecuacion I2:",I2L," En numerico: " , I2L.subs({self.C : C_value, self.R1: R1_value, self.R2: R2_value}), "\n")
        
        
        IC1L = (self.C *self.s*(VnL- self.Y))        
        print("Ecuacion I3:",IC1L," En numerico: " , IC1L.subs({self.C : C_value, self.R1: R1_value}), "\n")

        
        IC2L = (self.C*VnL*self.s)        
        print("Ecuacion I4:",IC2L,"En numerico: " , IC2L.subs({self.C : C_value, self.R1: R1_value}), "\n")
        
        # Ecuación en Laplace
        eq1 = sp.Eq(I1L, I2L + IC1L + IC2L)
        Y_as_X = sp.solve(eq1, self.Y)

        # Si H es la función de transferencia
        H = Y_as_X[0] / self.X
        
        valores = {self.R1 : R1_value, self.R2 : R2_value, self.R3: R3_value, self.C : C_value}
        H_num = H.subs(valores)
        

        return H_num, H, 
        
    def FTP2(self, R1_value, R2_value, R3_value, R4_value, C_value):
        eq1 = sp.Eq(self.Y , (-1*( (self.R3*self.C*self.R2*self.R4*self.C*(self.s**2) ) + (self.R2*self.R4*self.C*self.s ) - ( self.R3*self.C*self.R4*self.C*(self.R1+self.R2)*(self.s**2))- (self.R1*self.R3*self.C*self.s) - (self.R1) )  / ( self.R1 + (self.s *((self.R3*self.C*self.R1) + (self.R4*self.C*self.R1)) )  + ((self.s**2)* self.R1*self.R3*self.C*self.R4*self.C ) )))
        Y_as_X = sp.solve(eq1, self.Y)

        # Si H es la función de transferencia
        H = Y_as_X[0] 
        
        valores = {self.R1 : R1_value, self.R2 : R2_value, self.R3: R3_value, self.R4 : R4_value, self.C : C_value}
        H_num = H.subs(valores)

        return H_num, H
    
    def Design1(self, w_val, A_val, R1_val, R2_val, R3_val):
    
        #sea a,b,c los terminos que acompañan los polinomios
        a = self.R1*self.R2*self.R3*self.C**2
        b = 2*self.R2*self.R3*self.C
        c = self.R2 + self.R3

        eqn1 = sp.Eq(self.w, sp.sqrt((c) / (a))) #Ecuacion para resonancia
        
        eqn1_subs = eqn1.subs({self.w: w_val,self.R1: R1_val, self.R2: R2_val , self.R3: R3_val})
        
        solutions = sp.solve([eqn1_subs], (self.C))
        return np.array(solutions)

    def Design2(self,w_val,R1_val,R2_val,R3_val,R4_val):
        
        a = self.R1*(self.R3*self.R4*self.C**2)
        b = self.R1*(self.C*(self.R3+self.R4))
        c = self.R1
        
        eqn1 = sp.Eq(self.w, sp.sqrt((c) / (a))) #Ecuacion para resonancia
        
        eqn1_subs = eqn1.subs({self.w: w_val, self.R2: R2_val, self.R1: R1_val, self.R3: R3_val, self.R4: R4_val})

        solutions = sp.solve([eqn1_subs], (self.C))
        return np.array(solutions)
    
    
    def C_Amort(self, H):
        polos = sp.solve(H.as_numer_denom()[1],self.s)
        
        Coef = [-pole.as_real_imag()[0]/abs(pole) for pole in polos if (pole) != 0]

        #Si es complejo, halla el coeficiente a partir de los polos
        #Si no es complejo, el coef es 1
        
        return np.array(Coef)
    
    
#####################################################################################################################################################################################
    

