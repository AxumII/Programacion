from euler import Euler as Eu
from rk4 import RK4 as RK4
from rk4_2s import rk42s as rk4_2s
from df import df as df
from euler_2s import euler2s as euler2s
import numpy as np
import matplotlib.pyplot as plt
def ej2():
    h = 0.1
    x = np.arange(0,4+h, h)
    
    #u1 = x
    #u2 = y

    def du1dx(x, u1, u2):
        return -3*u2
    def du2dx(x, u1, u2):
        return (1/3)*u1

    u1_init = 0
    u2_init = 1

    sol = rk4_2s(u1_init= u1_init, u2_init= u2_init, x = x, du1dx= du1dx, du2dx= du2dx)
    print("solucion u1 o x(t)",sol.u1)
    print("solucion u2 o y(t)",sol.u2)

    print("ultimos", 2.27, -0.65)

def ej3():
    h = 0.25
    x = np.arange(0,1+h,h)
    u1_init = 1
    u2_init = 0

    def du1dx(x,u1,u2):
        return u1 - u2 + 2*x - x**2 - x**3 
    def du2dx(x,u1,u2):
        return u1 + u2 -4*(x**2) + x**3
    
    sole = euler2s(x = x, u1_init= u1_init, u2_init= u2_init, du1dx= du1dx, du2dx= du2dx)
    sol4 = rk4_2s(x = x, u1_init= u1_init, u2_init= u2_init, du1dx= du1dx, du2dx= du2dx)
    print("comparacion euler y rk4 S1""\n", "Euler", sole.u1,"\n" ,"Rk4", sol4.u1)
    plt.plot(x,sole.u1)
    plt.plot(x,sol4.u1)
    plt.grid()
    plt.show()

    print("comparacion euler y rk4 S2""\n", "Euler", sole.u2, "\n","Rk4", sol4.u2)
    plt.plot(x,sole.u2)
    plt.plot(x,sol4.u2)
    plt.grid()
    plt.show()
    
def ejshoot():
    h = 0.2  # Tamaño de paso según el ejemplo
    x = np.arange(0, 4 + h, h)  # Puntos de discretización
    print(x)
    u1_init = 1.25
    u1_fin = -0.95
    u2_init = 0  # Derivada inicial es 0 por requisito de disparo lineal

    # Primer sistema (u)
    def du1dx(x, u1, u2):
        return u2

    def du2dx(x, u1, u2):
        return (2 * x / (1 + x**2)) * u2 - (2 / (1 + x**2)) * u1 + 1

    sole = rk4_2s(x=x, u1_init=u1_init, u2_init=u2_init, du1dx=du1dx, du2dx=du2dx)
    u1 = sole.u1
    print("Soluciones u1(t):", sole.u1)
    print("Soluciones u2(t):", sole.u2)

    # Segundo sistema (v)
    def du1dx_v(x, u1, u2):
        return u2

    def du2dx_v(x, u1, u2):
        return (2 * x / (1 + x**2)) * u2 - (2 / (1 + x**2)) * u1

    sole2 = rk4_2s(x=x, u1_init=0, u2_init=1, du1dx=du1dx_v, du2dx=du2dx_v)
    v1 = sole2.u1
    print("Soluciones v1(t):", sole2.u1)
    print("Soluciones v2(t):", sole2.u2)

    # Cálculo de c
    c = (u1_fin - u1[-1]) / v1[-1]
    print("Valor de c:", c)
    print("Solución final para x(t):", u1 + c * v1)

def ejrk4single():
    def dydx(x, y):
        return (y*(x**2) - 1.2*y)

    # Definir valores iniciales y pasos
    x = np.arange(0, 2.5, 0.1)
    y_init = 1

    # Crear una instancia de la clase RK4 y resolver la EDO
    solver = RK4(y_init, x, dydx)

    print("Solucion RK4",solver.y)

    def realSol(x):
        return (np.exp(((x**3)/3) - 1.2*x   ))
    
    plt.plot(x, solver.y)
    plt.plot(x, realSol(x))
    plt.grid()
    plt.show()
    
def ejeulersingle():
    def dydx(x, y):
        return (y*(x**2) - 1.2*y)

    # Definir valores iniciales y pasos
    x = np.arange(0, 2.5, 0.1)
    y_init = 1

    # Crear una instancia de la clase RK4 y resolver la EDO
    solver = Eu(y_init, x, dydx)

    print("Solucion Euler",solver.y)

    def realSol(x):
        return (np.exp(((x**3)/3) - 1.2*x   ))
    
    plt.plot(x, solver.y)
    plt.plot(x, realSol(x))
    plt.grid()
    plt.show()



    
    








#ej2()
#ej3()
#ejshoot()
#ejrk4single()
#ejeulersingle()
