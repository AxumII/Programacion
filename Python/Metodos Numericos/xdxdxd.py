import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
import pandas as pd  # Importar pandas

class Biseccion:

    def __init__(self, equation, interv, iterat=100, error=1e-5):
        self.equation = equation
        self.interv = interv
        self.iterat = iterat  # Asigna un valor por defecto
        self.error = error  # Asigna un valor por defecto
        self.x = sp.symbols('x')
        self.func = self.convert()

    def convert(self):
        symbolic_expr = sp.sympify(self.equation)  # Convierte la fórmula en una expresión simbólica
        func = sp.lambdify(self.x, symbolic_expr, "numpy")  # Crea una función numpy
        return func

    def solve(self, print_table=False):
        a, b = self.interv
        fa, fb = self.func(a), self.func(b)
        if fa * fb >= 0:
            print("La función debe tener signos opuestos en los extremos del intervalo. No cumple con este requisito.")
            return None

        m = None
        data = []  # Lista para almacenar los datos de cada iteración
        for i in range(self.iterat):
            m = (a + b) / 2
            fm = self.func(m)

            # Almacenar datos de la iteración actual en la lista, incluyendo f(a) y f(b)
            data.append([i+1, a, b, m, fm, fa, fb])

            if abs(fm) < self.error:
                break  # Detiene el bucle si se cumple la condición de error

            if fa * fm < 0:
                b = m
                fb = self.func(b)  # Actualizar f(b) después de cambiar b
            else:
                a = m
                fa = self.func(a)  # Actualizar f(a) después de cambiar a

        if print_table:
            # Crear un DataFrame de pandas con los datos recopilados, incluyendo f(a) y f(b)
            df = pd.DataFrame(data, columns=['Iteración', 'a', 'b', 'm', 'f(m)', 'f(a)', 'f(b)'])
            print(df)  # Imprimir la tabla

        return m

    def graf(self):
        root = self.solve()
        x_values = np.linspace(self.interv[0], self.interv[1], 400)
        y_values = self.func(x_values)

        plt.figure(figsize=(8, 6))
        plt.plot(x_values, y_values, label='Función')

        if root is not None:
            plt.plot(root, self.func(root), 'ro', label=f'Raíz aproximada: {root}')
            plt.axvline(root, color='red', linestyle='--', lw=0.5)
        else:
            plt.title('No se encontró raíz con los criterios dados')
        plt.axhline(0, color='black', lw=0.5)
        plt.legend()
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.grid(True)
        plt.show()

# Ejemplo de uso
eq = "exp(x) - x**4 - 2"
intervalo = (-10, 10)

#a = Biseccion(eq, intervalo)

iteraciones = 100
error_tol = 1e-7
a = Biseccion(eq, intervalo, iteraciones, error_tol)
a.solve(print_table=True)  # Ahora con print_table=True para imprimir la tabla
a.graf()  # Grafica la función y muestra la raíz encontrada


eq = "x*sin(x) - 1"
intervalo = (0, 2)

#b = Biseccion(eq, intervalo)

iteraciones = 100
error_tol = 1e-7
b = Biseccion(eq, intervalo, iteraciones, error_tol)
b.solve(print_table=True)  # Ahora con print_table=True para imprimir la tabla
b.graf()  # Grafica la función y muestra la raíz encontrada
