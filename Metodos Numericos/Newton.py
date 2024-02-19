import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
import pandas as pd  # Importar pandas

class Newton:

    def __init__(self, equation, initial, interv, iterat=100, error=1e-7):
        self.equation = equation
        self.initial = initial
        self.interv = interv  # Intervalo para graficar
        self.iterat = iterat
        self.error = error
        self.x = sp.symbols('x')
        self.func = self.convert()
        self.func_prime = self.derivative()

    def convert(self):
        symbolic_expr = sp.sympify(self.equation)
        func = sp.lambdify(self.x, symbolic_expr, "numpy")
        return func

    def derivative(self):
        symbolic_expr = sp.sympify(self.equation)
        derivative_expr = sp.diff(symbolic_expr, self.x)
        func_prime = sp.lambdify(self.x, derivative_expr, "numpy")
        return func_prime

    def solve(self, print_table=False):
        xn = self.initial
        data = []

        for i in range(self.iterat):
            fxn = self.func(xn)
            f_prime_xn = self.func_prime(xn)

            if f_prime_xn == 0:
                print("Derivada igual a cero. El método no puede continuar.")
                break

            xn_next = xn - fxn / f_prime_xn

            if abs(fxn) < self.error or abs(xn_next - xn) < self.error:
                print(f"La raíz hallada en el intervalo con x aproximado a {xn} es con un error menor a {self.error}")
                xn = xn_next
                break

            data.append([i+1, xn, fxn, f_prime_xn, xn_next])
            xn = xn_next

        if print_table:
            df = pd.DataFrame(data, columns=['Iteración', 'xn', 'f(xn)', "f'(xn)", 'xn+1'])
            print(df)

        
        return xn

    def graf(self):
        root = self.solve()
        x_values = np.linspace(self.interv[0], self.interv[1], 400)
        y_values = self.func(x_values)

        plt.figure(figsize=(8, 6))
        plt.plot(x_values, y_values, label='Función')
        plt.plot(root, self.func(root), 'ro', label=f'Raíz aproximada: {root}')
        plt.axvline(root, color='red', linestyle='--', lw=0.5)
        plt.axhline(0, color='black', lw=0.5)
        plt.legend()
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.grid(True)
        plt.show()

# Ejemplo de uso
eq = "exp(2*x) +3*x -4"
ini = 0.6
intervalo = (-10, 10)
iteraciones = 100  
error_tol = 1e-5

newton = Newton(eq, ini, intervalo, iteraciones, error_tol)
root = newton.solve(print_table=True)
newton.graf()


# Ejemplo de uso
eq = "-506146776.192*x**2 + 1086618240*x - 265000000 "
ini = 100
intervalo = (0, 10)
iteraciones = 100  
error_tol = 1e-5

newton2 = Newton(eq, ini, intervalo, iteraciones, error_tol)
root2 = newton.solve(print_table=True)
newton2.graf()


# Ejemplo de uso
eq = "(2414707.2*x*(450-0.822*x*(255))) - 265000000  "
ini = 100
intervalo = (0, 10)
iteraciones = 100  
error_tol = 1e-5

newton3 = Newton(eq, ini, intervalo, iteraciones, error_tol)
root2 = newton.solve(print_table=True)
newton3.graf()