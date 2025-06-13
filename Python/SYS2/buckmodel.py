from scipy.signal import StateSpace, initial
import numpy as np
import matplotlib.pyplot as plt


class BuckModel:
    def __init__(self, L, C, R):
        A = np.array([[0, -1/L],[1/C, -1/(R*C)]])
        C = np.array([0, 1])
        D = np.array([0])

    def stateon(self,X0,T0):
        B = np.array([1/self.L , 0])
        Syson = StateSpace(self.A, B, self.C, self.D)
        T,Y,X = initial(Syson, T = T, X0 = X0)
        return T,Y,X

    def stateoff(self,X0,T0):
        B = np.array([ 0, 0])
        Sysoff = StateSpace(self.A, B, self.C, self.D)
        T,Y,X = initial(Sysoff, T = T, X0 = X0)
        return T,Y,X

    def completesystem(self,w_conm):
        T_arr = np.linspace(0,15,1000)

        conmutation_state = 0

        if conmutation_state == 1:
            self.stateon(X0,T0)

        if conmutation_state == 0:
            self.stateoff(X0,T0)