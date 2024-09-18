import numpy as np

class Derivation:
    def __init__(self, x=np.array([]), y=np.array([]), h=0.5):
        self.x = x
        self.y = y
        self.h = h
    
    def center_Oh2(self):
        """
        Derivada centrada de orden O(h^2)
        """
        print(h)
        n = len(self.y)
        dydx = np.zeros(n)
        for i in range(1, n-1):
            dydx[i] = (self.y[i+1] - self.y[i-1]) / (2 * self.h)
        return dydx
    
    def center_Oh4(self):
        """
        Derivada centrada de orden O(h^4)
        """
        n = len(self.y)
        dydx = np.zeros(n)
        for i in range(2, n-2):
            dydx[i] = (-self.y[i+2] + 8*self.y[i+1] - 8*self.y[i-1] + self.y[i-2]) / (12 * self.h)
        return dydx

# Ejemplo de uso
x = np.linspace(0, 20, num = 9)
y = x**2
h = x[1] - x[0]
print(x,y)
deriv = Derivation(x, y, h)
dydx_oh2 = deriv.center_Oh2()
dydx_oh4 = deriv.center_Oh4()

print(dydx_oh2)
print(dydx_oh4)
