import numpy as np
import matplotlib.pyplot as plt
class df:
    def __init__(self, x, px, qx, rx, fa, fb):
        self.x = x
        self.px = px
        self.qx = qx
        self.rx = rx
        self.fa = fa  # condición inicial en el primer punto
        self.fb = fb  # condición inicial en el último punto
        self.h = x[1] - x[0]  # tamaño del paso
        self.n = len(x)  # número de puntos
        self.fx = np.zeros(self.n)  # solución en cada punto de x
        self.matriz = np.zeros((self.n-2, self.n-2))  # matriz tridiagonal para el sistema lineal
        self.ind = np.zeros(self.n-2)  # vector independiente del sistema lineal
        
        self.solve()

    def solve(self):
        # Calcular términos e0 y en para las condiciones iniciales
        e0 = ((self.h / 2) * self.px[0] + 1) * self.fa
        en = ((self.h / 2) * self.px[-1] + 1) * self.fb

        # Primera fila de la matriz
        self.matriz[0, 0] = ((self.h ** 2) * self.qx[1]) + 2  # k
        self.matriz[0, 1] = (self.h / 2 * self.px[1]) - 1  # k+1
        # Independiente
        self.ind[0] = -1 * self.rx[1] * (self.h ** 2) + e0

        # Última fila de la matriz
        self.matriz[-1, -2] = (-self.h / 2 * self.px[-2]) - 1  # k-1
        self.matriz[-1, -1] = ((self.h ** 2) * self.qx[-2]) + 2  # k
        # Independiente
        self.ind[-1] = -1 * self.rx[-2] * (self.h ** 2) + en

        # Rellenar el resto de la matriz tridiagonal
        for r in range(1, self.n - 3):
            self.matriz[r, r - 1] = (-self.h / 2 * self.px[r]) - 1  # k-1
            self.matriz[r, r] = ((self.h ** 2) * self.qx[r]) + 2  # k
            self.matriz[r, r + 1] = (self.h / 2 * self.px[r]) - 1  # k+1
            # Independiente
            self.ind[r] = -1 * self.rx[r] * (self.h ** 2)

        # Resolver el sistema lineal
        self.fx[1:-1] = np.linalg.solve(self.matriz, self.ind)
        
        self.fx[0] = self.fa
        self.fx[-1] = self.fb
"""
# Ejemplo de uso
h = 0.5
x = np.arange(1, 6, h)  # Intervalo [0, 1] dividido en 11 puntos
def px(x):
    return -(1/x)
def qx(x):
    return -(1 - (1/(4*(x**2))))
def rx(x):
    return np.zeros(len(x))
# Condiciones iniciales
fa = 1 # f(1) = 1
fb = 0  # f(6) = 0


solver = df(x, px(x), qx(x), rx(x), fa, fb)
print("Solución f(x) en cada punto x:")
print(solver.fx)

print(len(x), len(solver.fx))

plt.plot(x,solver.fx)
plt.title("Soluciones")
plt.grid()
plt.show()"""