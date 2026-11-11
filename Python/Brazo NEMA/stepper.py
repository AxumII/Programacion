import numpy as np
import pandas as pd

class StepperAnalysis:
    def __init__(self, I_ph, R, L, T_h_motor, ratio, J_motor=50e-7, V=24, 
                     l_arm=0.32, m_load=0.5, m_arm = 140, J_gearbox=1.5e-5, backlash = 3/60):
            # Parámetros Eléctricos y del Motor
            self.I_ph = I_ph             
            self.R = R                   
            self.L = L                   
            self.V = V                   
            self.T_h_motor = T_h_motor   # Torque base del motor sin caja en Nm
            self.eff = 0.96              
            self.ratio = ratio           
            self.p = 50                
            
            # Parámetros Mecánicos Articulacion de Test de Torque
            self.l_arm = l_arm  
            self.m_load = m_load    
            self.m_arm = m_arm   
            self.J_gb = J_gearbox    # Inercia de la caja referida al motor (kg*m^2)
            self.backlash = backlash  
            
    def electrical_analysis(self, rpm_motor_array):