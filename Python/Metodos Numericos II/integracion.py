import numpy as np

class Integration():
    def __init__(self, x=np.array([]), y=np.array([])):
        self.x = x
        self.y = y
        self.h = self.x[1] - self.x[0]
    
    def trapz(self):
        integral = 0.0
        for i in range(1, len(self.x)):
            integral += 0.5 * self.h * (self.y[i] + self.y[i - 1])
        return integral
    
    def tercioSimpson(self):
        integral = 0.0
        if len(self.x) < 3 or (len(self.x) - 1) % 2 != 0:
            raise ValueError("Se necesitan al menos tres puntos y un número de intervalos divisible por 2 para aplicar la regla del tercio de Simpson.")
        for i in range(0, len(self.x) - 2, 2):
            integral += (self.y[i] + 4*self.y[i + 1] + self.y[i + 2]) * (self.h / 3)
        return integral
    
    def octSimpson(self):
        integral = 0.0
        if len(self.x) < 4 or (len(self.x) - 1) % 3 != 0:
            raise ValueError("Se necesitan al menos cuatro puntos y un número de intervalos divisible por 3 para aplicar la regla de 3/8 de Simpson.")
        for i in range(0, len(self.x) - 3, 3):
            integral += (self.y[i] + 3*self.y[i + 1] + 3*self.y[i + 2] + self.y[i + 3]) * (3 * self.h / 8)
        return integral
    
    def Boole(self):
        integral = 0.0
        if len(self.x) < 5 or (len(self.x) - 1) % 4 != 0:
            raise ValueError("Se necesitan al menos cinco puntos y un número de intervalos divisible por 4 para aplicar la regla de Boole.")
        for i in range(0, len(self.x) - 4, 4):
            integral += (7*self.y[i] + 32*self.y[i + 1] + 12*self.y[i + 2] + 32*self.y[i + 3] + 7*self.y[i + 4]) * (2 * self.h / 45)
        return integral


def func(x):
    return (np.cos(x))/np.exp(x)

x_vals = np.linspace(0, 1.25*np.pi, num = 25)
y_vals = func(x_vals)
ig = Integration(x_vals, y_vals)
print(ig.Boole())



