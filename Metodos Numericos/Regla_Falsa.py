import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
import pandas as pd  # Importar pandas

class ReglaFalsa:

    def __init__(self, equation, interv, iterat=100, error=1e-5):
        self.equation = equation
        self.interv = interv
        self.iterat = iterat
        self.error = error
        self.x = sp.symbols('x')
        self.func = self.convert()

    def convert(self):
        symbolic_expr = sp.sympify(self.equation)
        func = sp.lambdify(self.x, symbolic_expr, "numpy")
        return func

    def solve(self, print_table=False):
        a, b = self.interv
        fa, fb = self.func(a), self.func(b)
        if fa * fb >= 0:
            print("La función debe tener signos opuestos en los extremos del intervalo. No cumple con el teorema de Bolzano.")
            return None

        m = None
        data = []
        for i in range(self.iterat):
            m = b - (fb * (a - b)) / (fa - fb)  # Cálculo de m usando la fórmula de la regla falsa
            fm = self.func(m)

            data.append([i+1, a, b, m, fm, fa, fb])

            if abs(fm) < self.error:
                break

            if fa * fm < 0:
                b = m
                fb = fm
            else:
                a = m
                fa = fm

        if print_table:
            df = pd.DataFrame(data, columns=['Iteración', 'a', 'b', 'm', 'f(m)', 'f(a)', 'f(b)'])
            print(df)

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
