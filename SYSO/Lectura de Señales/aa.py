import numpy as np
import matplotlib.pyplot as plt

def expon(t, a, b):
    return np.exp(a * t) + b

# Generar valores de t
t = np.linspace(0, 5, 100)  # Cambia los valores según tus necesidades

# Parámetros de la función exponencial
rc = 0.0046389
rc_inv = rc ** -1 

# Calcular los valores de la función exponencial
y = expon(t, rc_inv, -rc_inv)

# Crear el gráfico
plt.figure()
plt.plot(t, y, label='Función Exponencial')
plt.xlabel('t')
plt.ylabel('y')
plt.title('Gráfico de la Función Exponencial')
plt.legend()
plt.grid(True)

# Mostrar el gráfico
plt.show()
