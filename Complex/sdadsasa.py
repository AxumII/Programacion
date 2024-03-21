from sympy import symbols, exp, lambdify
import numpy as np
import matplotlib.pyplot as plt

# Entrada de texto para la función
funcion_texto = "exp(z)"

# Definir la variable compleja y convertir la cadena de texto en una función sympy
z = symbols('z', complex=True)
funcion = eval(funcion_texto, {"exp": exp, "z": z})

# Convertir la expresión sympy en una función que pueda ser evaluada sobre arrays de numpy
funcion_evaluada = lambdify(z, funcion, "numpy")

# Generar una malla de puntos en el plano complejo y evaluar la función
x = np.linspace(-2, 2, 400)
y = np.linspace(-2, 2, 400)
X, Y = np.meshgrid(x, y)
Z = X + 1j*Y
W = funcion_evaluada(Z)

# Función para graficar el dominio y rango complejo
def graficar_dominio_rango(X, Y, W):
    plt.figure(figsize=(12, 6))

    # Dominio complejo
    plt.subplot(1, 2, 1)
    plt.title('Dominio Complejo')
    plt.xlabel('Re(z)')
    plt.ylabel('Im(z)')
    plt.scatter(X, Y, c=np.angle(Z), cmap='hsv', s=0.5)

    # Rango complejo
    plt.subplot(1, 2, 2)
    plt.title('Rango Complejo')
    plt.xlabel('Re(f(z))')
    plt.ylabel('Im(f(z))')
    plt.scatter(W.real, W.imag, c=np.angle(W), cmap='hsv', s=0.5)

    plt.tight_layout()
    plt.show()

graficar_dominio_rango(X, Y, W)
