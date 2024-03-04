import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sympy as sp

class AcceleratedNewton:

    def __init__(self, equation, initial, interv, multiplicity=1, iterat=100, error=1e-7):
        self.equation = equation
        self.initial = initial
        self.interv = interv
        self.multiplicity = multiplicity
        self.iterat = iterat
        self.error = error
        self.x = sp.symbols('x')
        self.func = self.convert()
        self.func_prime = self.derivative()
        self.symbolic_derivative = self.derivative_symbolic()

    def convert(self):
        symbolic_expr = sp.sympify(self.equation)
        func = sp.lambdify(self.x, symbolic_expr, "numpy")
        return func

    def derivative(self):
        symbolic_expr = sp.sympify(self.equation)
        derivative_expr = sp.diff(symbolic_expr, self.x)
        func_prime = sp.lambdify(self.x, derivative_expr, "numpy")
        return func_prime
    
    def derivative_symbolic(self):
        symbolic_expr = sp.sympify(self.equation)
        derivative_expr = sp.diff(symbolic_expr, self.x)
        return derivative_expr

    def solve(self, print_table=False):
        xn = self.initial
        data = []
        errors = [np.inf]

        for i in range(self.iterat):
            fxn = self.func(xn)
            f_prime_xn = self.func_prime(xn)
            if f_prime_xn == 0:
                print("Derivative equals zero. The method cannot proceed.")
                break

            xn_next = xn - self.multiplicity * fxn / f_prime_xn
            error = abs(xn_next - xn)

            if error < self.error or abs(fxn) < self.error:
                print(f"Root found within the interval with x approximated to {xn} is with an error less than {self.error}")
                xn = xn_next
                break

            data.append([i+1, xn, fxn, f_prime_xn, xn_next, error])
            errors.append(error)
            xn = xn_next

        if print_table:
            df = pd.DataFrame(data, columns=['Iteration', 'xn', 'f(xn)', "f'(xn)", 'xn+1', 'Error'])
            print(df)
            print(f"The symbolic derivative of the function is: {self.symbolic_derivative}")

        return xn, errors

    def graf(self, print_table=False):
        root, errors = self.solve(print_table=print_table)
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

        # Plotting the convergence
        plt.subplot(1, 2, 2)
        plt.semilogy(range(1, len(errors)), errors[1:], '-o', label='Error per iteration')
        plt.xlabel('Iteration')
        plt.ylabel('Logarithmic Error')
        plt.title('Convergence')
        plt.grid(True)
        plt.legend()

        plt.tight_layout()
        plt.show()
