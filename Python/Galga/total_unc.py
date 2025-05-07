import numpy as np
import pandas as pd
import sympy as sp

from unc import Type_A as T_A
from unc import Type_B as T_B


class Total_unc:
    def __init__(self,datos_delta_V):
        self.datos_delta_V = datos_delta_V
        self.resol_delta_V

    def calculate():
        #Dado a que estoy calculando la deformacion , implica que calculo la
        #incertidumbre tanto de la formula general como los errores, teniend
        #cada factor fisico su propia incertidumbre
        
        #Formula general
        delta_V, Vi, GF, RL, RG = sp.symbols('delta_V Vi GF RL RG')    
        epsilon = (-4 * (delta_V / Vi)) / (GF * (1 + 2 * (delta_V / Vi))) * (1 + RL / RG)

        #Delta_V
        #Tipo A
        t_a_delta_V = T_A(muestra = self.datos_delta_V, name="Voltage Difference")
        u_a_delta_V = t_a_delta_V.des_est()
        #Tipo B
        #Resolucion (EL adc no tiene calibracion)
        
        t_b_delta_V = T_B(resol = self.resol_delta_V, name= "Voltage Difference", sensitivity =  )
        sens_delta_V = t_b_delta_V.coef_sens(i_var = delta_V, equation=epsilon, num_values= num_values_gen)
        t_b_delta_V.unc_resol()
        t_b_delta_V.add()
        u_b_delta_V = t_b_delta_V.df_unc
        
        #Vi
        u_a_vi = T_A()
        
        
        
        
        
        pass
    