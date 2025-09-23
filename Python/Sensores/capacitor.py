import numpy as np

class Capacitor:
    def __init__(self, d_s=10e-3, A=None, e_d=None):
        self.d_s = float(d_s)
        self.A = np.array(A) if A is not None else np.array([1.0])  # área por defecto
        self.e_d = np.array(e_d) if e_d is not None else np.array([1.0])  # permitividad relativa por defecto

        # Constante
        self.e_0 = 8.854e-12  # permitividad del vacío [F/m]

        # Capacitancia
        self.c = self.cap()

    def cap(self):
        c = 0
        for i in range(self.e_d.size):
            c += (self.A[i] * self.e_0 * self.e_d[i]) / self.d_s
        return c
    
    def t_5tao(self, r):
        return 5 * r * self.c
    
    def f_min(self, r):
        t5 = self.t_5tao(r)
        return 1 / t5  

#--------------------------------------------------------------------------------------------------------------