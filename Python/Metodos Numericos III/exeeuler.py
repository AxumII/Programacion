from euler import Euler as euler
from graf import graf as graf
import numpy as np



# Ejemplo de uso:

def ej1vd():
    # Definir la función dydx
    def dydx(x, y):
        return (x**2 -1)/y**2  # Ejemplo: dy/dx = x + y

    # Definir valores iniciales y pasos
    x = np.arange(0, 2, 0.2)  # 11 puntos de 0 a 1
    y_init = 2  # Valor inicial de y

    # Crear una instancia de la clase Euler y resolver la EDO
    y = euler(y_init, x, dydx)

    # Obtener la solución
    print(y)
    yn = np.array([y(), (x**3 - 3*x + 8)**(1/3)])
    graf(x = x,yn = yn, title = "(x**2 -1)/y**2 con y(0) = 2", function_at = [{"label":"Solucion Euler"},{"label":"Solucion Analitica"}])


def ejcl1_h1():
    def dydx(x,y):
        return (y*(x**2) - 1.2*y)

    x = np.arange(0, 2.5, 0.5)
    y_init = 1

    y = euler(y_init, x, dydx)
    print(y)
   
    yn = np.array([y(), (np.exp(((x**3)/3) - 1.2*x   ))])
    graf(x = x,yn = yn, title = "(x**2 -1)/y**2 con y(0) = 2", function_at = [{"label":"Solucion Euler"},{"label":"Solucion Analitica"}])


def ejcl1_h2():
    def dydx(x,y):
        return (y*(x**2) - 1.2*y)

    x = np.arange(0, 2.25, 0.25)
    y_init = 1

    y = euler(y_init, x, dydx)
    print(y)

    yn = np.array([y(), (np.exp(((x**3)/3) - 1.2*x   ))])
    graf(x = x,yn = yn, title = "(x**2 -1)/y**2 con y(0) = 2", function_at = [{"label":"Solucion Euler"},{"label":"Solucion Analitica"}])


#ej1vd()
ejcl1_h1()
ejcl1_h2()
