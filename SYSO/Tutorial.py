import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np
from sympy import *
from scipy.integrate import solve_ivp

def grafFuncionBasica():
    #define vectores como las variables
    x = np.linspace(0, 10, 100)#es la independiente
    y = np.sin(2 * x)#es la dependiente

    # Crear una figura vacía, en sí es el lienzo
    fig = plt.figure()

    # Agregar un conjunto de ejes (subplots) a la figura, ax es un subplot
    ax1 = fig.add_subplot(1, 1, 1)  # 1 fila, 1 columna, primer subplot

    # Trazar los datos en los ejes
    ax1.plot(x, y, linewidth=2.0, label="leyenda", color="red", linestyle="dashdot")

    # el metodo set permite modificar varias cosas en el plot ax
    # x lim y y lim permiten limitar hasta qué número se grafica
    ax1.set(xlim=(0, 8), ylim=(-8, 8))

    ax1.set_title("Titulo principal")
    ax1.set_xlabel("Titulo Eje X", fontsize=12, fontstyle="italic")
    ax1.set_ylabel("Titulo Eje Y", fontsize=12, fontstyle="italic")

    # Crea una malla para ver la escala mejor
    ax1.grid(True)

    # muestra un punto, pone una flecha
    ax1.annotate("Punto Interesante", 
                 xy=(4, 0.5),       # Coordenadas del punto de datos
                 xytext=(3, 2),     # Coordenadas del texto de la anotación
                 arrowprops=dict(facecolor="black", shrink=0.1, width=0.5, headwidth=8),#shrink es cuanto se encoje la flecha, width es el ancho
                 fontsize=10,       # Tamaño de fuente del texto de la anotación
                 color="blue",      # Color del texto de la anotación
                 horizontalalignment="left",  # Alineación horizontal del texto
                 verticalalignment="bottom",   # Alineación vertical del texto
                 bbox=dict(boxstyle="round,pad=0.3", edgecolor="gray", facecolor="lightgray"))  # Estilo del cuadro alrededor del texto

    # Añadir un punto en la punta de la flecha
    ax1.plot(4, 0.5, marker="o", markersize=4, color="black")

    # Permite guardar la gráfica
    # fig.savefig("grafico_seno.png", dpi=300)  # Guardar como PNG con 300 dpi

    ax1.legend(fontsize=10, loc="upper right")
    plt.show()

def opb():
    a = np.array([1, 2, 3])
    b = np.array([4, 5, 6])
    suma = a + b
    resta = a - b
    producto = a * b
    division = a / b
    print(suma, resta, producto, division)

def deriv():
    x, y, z = symbols('x y z')#las define como variables

    #derivada basica de primer orden
    dv1 = diff(cos(x),x)
    #derivada basica de n orden
    n = 2
    dv2 = diff(cos(x),x,n)
    #derivada en varias variables, se ponen despues de la expresion las variables con las que se desea derivar
    dv3 = diff((y**4)*cos(x),x,y)
    #esta forma no la evalua pero no se si esta bien escrita
    dv4 = Derivative((y**4)*cos(x),x,y)
    
    print(dv1)
    print(dv2)
    print(dv3)
    print(dv4)
    
def integ():
    x, y, z = symbols('x y z')#las define como variables   
    
    #integral basica indefinida
    i1 = integrate(x**2,x)
    #integral basica definida
    i2 = integrate(x**2,(x,0,50))
    #integral iterada de varias variables
    i3 = integrate((x*(y**2)*exp(-x),(y,0,5),(x,1,oo)))
    
    print(i1)
    print(i2)
    print(i3)
    
    
    
def EDO():
    def eom(x, y):
        y1, y2 = y
        dy1dx = y2
        dy2dx = 2 * y2 - y1 + np.cos(x)
        return [dy1dx, dy2dx]

    # Condiciones iniciales
    initial_conditions = [1, 0]
    x_range = (0, 10)  # Rango de valores de x donde se resolverá la EDO

    # Resolver la EDO
    sol = solve_ivp(eom, x_range, initial_conditions, t_eval=np.linspace(x_range[0], x_range[1], 1000))
     
#para laplace, scipy tiene es para SYS, sympy para laplace pura.
def laplaceSympy():
    
    # Definir las variables simbólicas y la variable 's' de la transformada de Laplace
    t, s = sp.symbols('t s')

    # Definir la función original en el dominio del tiempo
    f_original = sp.exp(-2 * t)

    # Calcular la transformada de Laplace de la función
    laplace_transform = sp.laplace_transform(f_original, t, s)

    # Imprimir el resultado de la transformada de Laplace
    print("Transformada de Laplace de la función:")
    print(laplace_transform)
   
#para escalon e impulso numpy tienen librerias 
def escalonUnit():
    def heaviside(x):
        return np.heaviside(x, 1)

    valor = -1
    resultado = heaviside(valor)
    print(f"Heaviside({valor}) = {resultado}")
      
"""
#buscar con numpy, toca ponerlo, luego se me olvida
def impulsoUnit():
   print("falta terminar")

   
def complejos():  
    # 1. Expresar un número complejo
    z = 3 + 4j
    print("Número complejo:", z)

    # 2. Expresar en forma exponencial y trigonométrica
    magnitude = np.abs(z)
    angle_rad = np.angle(z)
    exponential_form = magnitude * np.exp(1j * angle_rad)
    cos_form = magnitude * np.cos(angle_rad) + 1j * (magnitude * np.sin(angle_rad))

    print("Forma exponencial:", exponential_form)
    print("Forma sen-cos:", cos_form)

    # 3. Operaciones básicas con números complejos
    w = 1 - 2j

    # Suma
    sum_result = z + w
    print("Suma:", sum_result)

    # Resta
    sub_result = z - w
    print("Resta:", sub_result)

    # Multiplicación
    mul_result = z * w
    print("Multiplicación:", mul_result)

    # División
    div_result = z / w
    print("División:", div_result)
    
  """    
#########################################################################################################
"""grafFuncionBasica()"""


integ()