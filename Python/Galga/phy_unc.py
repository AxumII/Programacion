import numpy as np
import pandas as pd
import sympy as sp

from unc import Type_A as T_A
from unc import Type_B as T_B

class T_B_Total(T_B):
    def __init__(self, resol, calib, temp, name=None, f_c_calib=3):
        super().__init__(resol, calib, name, f_c_calib)  # Hereda el constructor de Type_B
        
    def unc_gen_function(self,num_values_gen):
        delta_V, Vi, GF, RL, RG = sp.symbols('delta_V Vi GF RL RG')    
        epsilon = (-4 * (delta_V / Vi)) / (GF * (1 + 2 * (delta_V / Vi))) * (1 + RL / RG)

        #Se crea un objeto por cada medicion de variable
        #Vi
        Type_B_Vi = T_B(calib=1, name = "Voltaje Input")
        Type_B_Vi.coef_sens(i_var = 1 , equation= 1, num_values= 1)
        Type_B_Vi.unc_calib()
            
        #GF 
        Type_B_GF = T_B(calib=1, name = "Gauge Factor")
        Type_B_GF.coef_sens(i_var = 1 , equation= 1, num_values= 1)
        Type_B_GF.unc_calib()
        #RL
        Type_B_RL = T_B(calib=1, name = "Wire Resistence")
        Type_B_RL.coef_sens(i_var = 1 , equation= 1, num_values= 1)
        Type_B_RL.unc_calib()
        #RG
        Type_B_RG = T_B(calib=1, name = "Gauge Resistence",equation = 1, num_values= 1)
        Type_B_RG.unc_calib()
        #delta_V

    def unc_misagnl(self,num_values_misagnl):
        v, phi = sp.symbols('v phi')

        error = ((1 - v + (1 + v)*sp.cos(2*phi)) / 2) - 1
        #phi
        Type_B_ms_a = T_B(calib=1, name = "Misalignment Angle")
        Type_B_ms_a.coef_sens(i_var = 1 , equation= 1, num_values= 1)
        Type_B_ms_a.unc_calib()
        
    def unc_curvature(self,num_values_curv):
        h , r, E, b,h,F,L,x = sp.symbols('h r E b h F L x')
        
        error = h/((E*(b*(h**3))/12)/(F*(L-x)))
        
        #h
        Type_B_h = T_B(calib=1, name = "Gauge und Surface Distance")
        Type_B_h.coef_sens(i_var = 1 , equation= 1, num_values= 1)
        Type_B_h.unc_calib()
        
        