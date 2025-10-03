import scipy.signal as sg
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


class UNMotor:
    def __init__(self,Ra,La,y,J,N,B, u):
        
        A11 = 
        A12 = 
        A21 = 
        A22 = 
        self.A = np.array([[A11, A12],
                           [A21, A22]], dtype=float)
        self.B = [1/La, 0]
        self.C = [0,1]
        self.D = np.zeros((1,1))

        self.alpha =    u/((u**2) + B*Ra) 
        self.tao = (J*N*Ra)/((u**2) + B*Ra) 

    def ss(self):
        return sg.StateSpace(self.A, self.B, self.C, self.D)

    def ss_out(self, t_sim=0.01, fs=1e5, x0=None):
        # condiciones iniciales
        if x0 is None:
            x0 = np.array([1.0, 0.0])
        else:
            x0 = np.asarray(x0, dtype=float)
            if x0.shape != (2,):
                raise ValueError("x0 debe ser un vector de longitud 2.")

        npts = int(t_sim * fs)
        t = np.linspace(0.0, float(t_sim), npts)
        u = np.zeros_like(t)  # entrada cero
        tout, y, x = sg.lsim(self.ss(), U=u, T=t, X0=x0)
        return tout, y.squeeze(), x
    
    def tf_omega(self):
        num = [self.alpha]
        den = [self.tao, 1]
        return 
    
    def tf_theta(self):
        num = [self.alpha]
        den = [self.tao, 1,0]
        return 
    
    