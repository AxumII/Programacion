import numpy as np

class rk42s:
    def __init__(self, x, u1_init, u2_init, du1dx, du2dx):
        self.x = x
        self.u1_init = u1_init
        self.u2_init = u2_init
        self.du1dx = du1dx
        self.du2dx = du2dx
        self.h = x[1] - x[0]
        self.u1 = np.array([u1_init])  # Inicializar el array con el valor inicial
        self.u2 = np.array([u2_init])  # Inicializar el array con el valor inicial
        self.solve()

    def solve(self):
        for i in range(len(self.x) - 1):
            k1 = self.du1dx(self.x[i], self.u1[i], self.u2[i])
            j1 = self.du2dx(self.x[i], self.u1[i], self.u2[i])

            k2 = self.du1dx(self.x[i] + (self.h/2), self.u1[i] + (self.h/2)*k1, self.u2[i] + (self.h/2)*j1)
            j2 = self.du2dx(self.x[i] + (self.h/2), self.u1[i] + (self.h/2)*k1, self.u2[i] + (self.h/2)*j1)

            k3 = self.du1dx(self.x[i] + (self.h/2), self.u1[i] + (self.h/2)*k2, self.u2[i] + (self.h/2)*j2)
            j3 = self.du2dx(self.x[i] + (self.h/2), self.u1[i] + (self.h/2)*k2, self.u2[i] + (self.h/2)*j2)

            k4 = self.du1dx(self.x[i] + self.h, self.u1[i] + self.h*k3, self.u2[i] + self.h*j3)
            j4 = self.du2dx(self.x[i] + self.h, self.u1[i] + self.h*k3, self.u2[i] + self.h*j3)

            u1i = self.u1[i] + (self.h/6) * (k1 + 2*k2 + 2*k3 + k4)
            u2i = self.u2[i] + (self.h/6) * (j1 + 2*j2 + 2*j3 + j4)

            # Agregar los nuevos valores calculados a los arrays u1 y u2
            self.u1 = np.append(self.u1, u1i)
            self.u2 = np.append(self.u2, u2i)
