import numpy as np
from graf import graf as graf


class RK4:
    def __init__(self, y_init, x, dydx):
        self.y_init = y_init  # Valor inicial de y
        self.x = x  # Array de valores de x
        self.dydx = dydx  # Función para calcular dy/dx
        self.h = x[1] - x[0]  # Paso de integración (diferencia entre valores consecutivos de x)
        self.y = np.array([y_init])  # Inicializa y con el valor inicial
        self.solve()

    def solve(self):
        # Iterar sobre los valores de x, excluyendo el último para evitar salida de rango
        for xi in self.x[:-1]:
            yi = self.y[-1]  # Último valor de y calculado
            
            # Cálculo de los coeficientes de Runge-Kutta (k1, k2, k3, k4)
            k1 = self.h * self.dydx(xi, yi)
            k2 = self.h * self.dydx(xi + 0.5 * self.h, yi + 0.5 * k1)
            k3 = self.h * self.dydx(xi + 0.5 * self.h, yi + 0.5 * k2)
            k4 = self.h * self.dydx(xi + self.h, yi + k3)
            
            # Calcular el siguiente valor de y usando la fórmula de RK4
            y_next = yi + (k1 + 2 * k2 + 2 * k3 + k4) / 6.0
            
            # Añadir el nuevo valor de y al array
            self.y = np.append(self.y, y_next)

    def get_solution(self):
        # Devuelve los valores de x e y
        return  self.y











# Ejemplo de uso:
# Definir la función dydx
def dydx(x, y):
    return (y*(x**2) - 1.2*y)

# Definir valores iniciales y pasos
x = np.arange(0, 2.5, 0.1)
y_init = 1

# Crear una instancia de la clase RK4 y resolver la EDO
solver = RK4(y_init, x, dydx)

# Obtener la solución
y_vals = solver.get_solution()

yn = np.array([y_vals, (np.exp(((x**3)/3) - 1.2*x   ))])
graf(x = x,yn = yn, title = "(x**2 -1)/y**2 con y(0) = 2", function_at = [{"label":"Solucion RK4"},{"label":"Solucion Analitica"}])




