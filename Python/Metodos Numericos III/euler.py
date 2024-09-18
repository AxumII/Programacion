import numpy as np

class Euler:
    def __init__(self, y_init, x, dydx):
        self.y_init = y_init  # Valor inicial de y
        self.x = x  # Array de valores de x
        self.dydx = dydx  # Función para calcular dy/dx
        self.h = x[1] - x[0]  # Paso de integración (diferencia entre valores consecutivos de x)
        self.y = np.array([y_init])  # Inicializa y con el valor inicial
        self.solve()

    def solve(self):
        for i in range(len(self.x) - 1):
            y_next = self.y[i] + self.h * self.dydx(self.x[i], self.y[i])
            self.y = np.append(self.y, y_next)

    def __repr__(self):
        # Devuelve solo la representación de y
        return repr(self.y)

    def __call__(self):
        # Permite usar la instancia directamente como si fuera el array y
        return self.y
