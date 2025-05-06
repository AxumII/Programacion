import numpy as np
import pandas as pd
import sympy as sp

from unc import Type_A as T_A
from unc import Type_B as T_B

class T_B_Total(T_B):
    def __init__(self, resol, calib, temp, name=None, f_c_calib=3):
        super().__init__(resol, calib, name, f_c_calib)  # Hereda el constructor de Type_B
        
    def unc_gen_function(self,v_num):
        delta_V, Vi, GF, RL, RG = sp.symbols('delta_V Vi GF RL RG')    
        epsilon = (-4 * (delta_V / Vi)) / (GF * (1 + 2 * (delta_V / Vi))) * (1 + RL / RG)

        #Se crea un objeto por cada medicion de variable
        #Vi
        Type_B_Vi = T_B(calib=1, name = "Voltaje Input")
        Type_B_Vi.coef_sens(i_var = 1 , equation= 1, num_values= 1)
        Type_B_Vi.unc_calib()
            
        #GF 
        
        #RL
        
        #RG
        
        #delta_V
