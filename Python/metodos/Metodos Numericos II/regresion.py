import numpy as np
from scipy.linalg import lstsq
import matplotlib.pyplot as plt

class Regresion:
    def __init__(self) -> None:
        pass

    def lineal(self, x, y):
        # Construcción de la matriz de diseño
        A = np.vstack([x, np.ones(len(x))]).T
        # Resolución del sistema de ecuaciones
        coeff, _, _, _ = lstsq(A, y)
        return coeff#Devuelve B y luego A

    def exponencial(self, x, y):
        # Aplicar logaritmo a y
        log_y = np.log(y)
        # Construcción de la matriz de diseño
        A = np.vstack([x, np.ones(len(x))]).T
        # Resolución del sistema de ecuaciones
        coeff, _, _, _ = lstsq(A, log_y)
        return np.exp(coeff[1]), coeff[0]  # Retornar A y B

    def ajuste_potencial(self, x, y, M):
        # Aplicar logaritmo a y y x
        log_y = np.log(y)
        log_x = np.log(x)
        # Construcción de la matriz de diseño
        A = np.vstack([log_x, np.ones(len(log_x))]).T
        # Resolución del sistema de ecuaciones
        coeff, _, _, _ = lstsq(A, log_y)
        return np.exp(coeff[1]), M  # Retornar A y M

    def comb_lin(self, x, y, bases):
        # Construcción de la matriz de diseño
        F = np.column_stack([b(x) for b in bases])
        # Resolución del sistema de ecuaciones
        coeff, _, _, _ = lstsq(F, y)
        return coeff

    # Funciones base para la combinación lineal
    @staticmethod
    def f1(x):
        return np.sin(x)

    @staticmethod
    def f2(x):
        return np.cos(x)

    # Función para graficar
    @staticmethod
    def plot_regression(x, y, y_pred, title):
        plt.scatter(x, y, color='blue', label='Datos originales')
        plt.plot(x, y_pred, color='red', label='Ajuste')
        plt.title(title)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.legend()
        plt.show()

# Ejemplo de uso
if __name__ == "__main__":
    # Datos de ejemplo
    x = np.array([0.1, 0.5, 1, 1.5, 2])
    y_lineal = np.array([1, 2, 3, 4, 5])
    y_exponencial = np.array([1, 2.718, 7.389, 20.085, 54.598])
    y_potencial = np.array([1, 0.7, 0.5, 0.4, 0.3])
    y_comb = np.array([1, 0.707, 0, -0.707, -1])

    # Crear instancia de la clase Regresion
    reg = Regresion()

    # Regresión lineal
    coeff_lineal = reg.lineal(x, y_lineal)
    y_pred_lineal = coeff_lineal[0] * x + coeff_lineal[1]
    print(f"Coeficientes de regresión lineal: {coeff_lineal}")
    reg.plot_regression(x, y_lineal, y_pred_lineal, 'Regresión Lineal')

    # Regresión exponencial
    A_exp, B_exp = reg.exponencial(x, y_exponencial)
    y_pred_exponencial = A_exp * np.exp(B_exp * x)
    print(f"Coeficientes de regresión exponencial: A={A_exp}, B={B_exp}")
    reg.plot_regression(x, y_exponencial, y_pred_exponencial, 'Regresión Exponencial')

    # Ajuste potencial
    A_pot, M_pot = reg.ajuste_potencial(x, y_potencial, 0.5)
    y_pred_potencial = A_pot * x**M_pot
    print(f"Coeficientes de ajuste potencial: A={A_pot}, M={M_pot}")
    reg.plot_regression(x, y_potencial, y_pred_potencial, 'Ajuste Potencial')

    # Combinación lineal de funciones base
    bases = [reg.f1, reg.f2]
    coeff_comb_lin = reg.comb_lin(x, y_comb, bases)
    y_pred_comb_lin = coeff_comb_lin[0] * reg.f1(x) + coeff_comb_lin[1] * reg.f2(x)
    print(f"Coeficientes de combinación lineal: {coeff_comb_lin}")
    reg.plot_regression(x, y_comb, y_pred_comb_lin, 'Combinación Lineal de Funciones Base')
