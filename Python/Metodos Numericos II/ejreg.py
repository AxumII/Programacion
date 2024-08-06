from regresion import Regresion
import numpy as np

def ej1():
    
    A = np.array    ([[10, 36],
                    [36, 195.02]])

    # Vector de términos independientes
    B = np.array([38, 193.61])
    
    print(np.linalg.solve(A,B))


    
    
    x            = np.array([0.1, 0.5, 1, 2, 3, 4, 5, 6, 7, 7.4])
    y_lineal     = np.array([0.4, 1.3, 1.5, 2.7, 3.4, 4.2, 4.7, 6, 6.5, 7.3])
    y_potencial  = np.array([0.01, 0.3, 1, 4.7, 12.1, 16.2, 26.1, 34.2, 50, 58.76])
   
    # Crear instancia de la clase Regresion
    reg = Regresion()

    # Regresión lineal
    coeff_lineal = reg.lineal(x, y_lineal)
    y_pred_lineal = coeff_lineal[0] * x + coeff_lineal[1]
    print(f"Coeficientes de regresión lineal: {coeff_lineal}")
    reg.plot_regression(x, y_lineal, y_pred_lineal, 'Regresión Lineal')

   
    # Ajuste potencial
    M = 2
    A_pot, M_pot = reg.ajuste_potencial(x, y_potencial, M)
    y_pred_potencial = A_pot * x**M_pot
    print(f"Coeficientes de ajuste potencial: A={A_pot}, M={M_pot}")
    reg.plot_regression(x, y_potencial, y_pred_potencial, 'Ajuste Potencial')


ej1()