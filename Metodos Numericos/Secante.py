import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sympy as sp

class Secante:

    def __init__(self, equation, initial_guesses, interv, iterat=100, error=1e-7):
        self.equation = equation
        self.initial_guesses = initial_guesses  # Almacena las dos conjeturas iniciales
        self.interv = interv
        self.iterat = int(iterat)
        self.error = error
        self.x = sp.symbols('x')
        self.func = self.convert()


    def convert(self):
        symbolic_expr = sp.sympify(self.equation)
        func = sp.lambdify(self.x, symbolic_expr, "numpy")
        return func

    def solve(self, print_table=False):
        x0, x1 = self.initial_guesses  # Usa correctamente initial_guesses
        data = []
        errors = [np.inf]
        error_ratios = []

        for i in range(self.iterat):
            fx0 = self.func(x0)
            fx1 = self.func(x1)
            if fx1 - fx0 == 0:
                print("Division by zero. The method cannot proceed.")
                break

            x2 = x1 - fx1 * (x1 - x0) / (fx1 - fx0)
            error = abs(x2 - x1)
            error_ratio = error / errors[-1] if i > 0 else np.nan

            if error < self.error or abs(self.func(x2)) < self.error:
                print(f"Root found within the interval with x approximated to {x2} is with an error less than {self.error}")
                x1 = x2
                break

            data.append([i+1, x0, x1, fx0, fx1, x2, error, error_ratio])
            errors.append(error)
            error_ratios.append(error_ratio)
            x0, x1 = x1, x2

        if print_table:
            df = pd.DataFrame(data, columns=['Iteration', 'x0', 'x1', 'f(x0)', 'f(x1)', 'x2', 'Error', '|En|/|En-1|'])
            print(df)

        # Calculating the order of convergence
        if len(errors) > 2:
            p = np.log(errors[-1]/errors[-2])/np.log(errors[-2]/errors[-3])
        else:
            p = None
        
        return x2, errors, error_ratios, p

    def graf(self, print_table=False):
        root, errors, error_ratios, p = self.solve(print_table=print_table)
        x_values = np.linspace(self.interv[0], self.interv[1], 400)
        y_values = self.func(x_values)

        plt.figure(figsize=(12, 6))

        # Plotting the function and the approximate root
        plt.subplot(1, 2, 1)
        plt.plot(x_values, y_values, label='Function')
        plt.plot(root, self.func(root), 'ro', label=f'Approximate Root: {root}')
        plt.axvline(root, color='red', linestyle='--', lw=0.5)
        plt.axhline(0, color='black', lw=0.5)
        plt.legend()
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.grid(True)
        plt.title('Function and Approximate Root')

        # Plotting the convergence speed
        plt.subplot(1, 2, 2)
        plt.semilogy(range(1, len(errors)), errors[1:], '-o', label='Error per iteration')
        plt.xlabel('Iteration')
        plt.ylabel('Logarithmic Error')
        convergence_order = f"Convergence Order: {p:.2f}" if p is not None else "Convergence Order: N/A"
        plt.title(f'Convergence Speed - {convergence_order}')
        plt.grid(True)
        plt.legend()

        plt.tight_layout()
        plt.show()

        if p is not None:
            print(f"The calculated convergence order is {p:.2f}.")
        else:
            print("Convergence order could not be calculated.")
