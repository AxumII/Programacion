import numpy as np
import matplotlib.pyplot as plt
import random

# Definir las funciones con las pendientes especificadas
def funcion_pendiente_2(x):
    return -2 * x

def funcion_pendiente_4(x):
    return 4 * x

def funcion_pendiente_1(x):
    return -x

# Crear un rango de valores x
x = np.linspace(-20, 20, 100)

# Calcular los valores y para cada función
y_pendiente_2 = funcion_pendiente_2(x)
y_pendiente_4 = funcion_pendiente_4(x)
y_pendiente_1 = funcion_pendiente_1(x)

# Crear subplots
fig, axs = plt.subplots(2, 2, figsize=(10, 8))

# Graficar las funciones en subplots individuales
axs[0, 0].plot(x, y_pendiente_4, label='Vi/Vo', color = 'red')
axs[0, 0].set_title('Funcion de Transferencia de no Inversor')
axs[0, 0].set_xlabel('V in')
axs[0, 0].set_ylabel('V out')

axs[0, 1].plot(x, y_pendiente_2, label='Vi/Vo', color = 'green')
axs[0, 1].set_title('Funcion de Transferencia de Inversor')
axs[0, 1].set_xlabel('V in')
axs[0, 1].set_ylabel('V out')

axs[1, 0].plot(x, y_pendiente_1, label='Vi/Vo Input', color =  'orange')
axs[1, 0].set_title('Funcion de Transferencia de Inversor (Entrada Individual)')
axs[1, 0].set_xlabel('V in')
axs[1, 0].set_ylabel('V out')

# Calcular y graficar la suma de las funciones con pendiente 1
y_suma_pendiente_1 = y_pendiente_1 + y_pendiente_1

# Agregar un número aleatorio entre -0.08 y 0.08 a la suma de funciones
random_noise = np.random.normal(-0.08, 0.08, len(x))
y_suma_pendiente_1 += random_noise

axs[1, 1].plot(x, y_suma_pendiente_1, label='Vi/Vo Sumador', linestyle='dashed', color = 'purple')
axs[1, 1].set_title('Funcion de Transferencia de Sumador')
axs[1, 1].set_xlabel('V in (Sumado)')
axs[1, 1].set_ylabel('V out')

# Agregar etiquetas y leyendas
for ax in axs.flat:
    ax.legend()
    ax.grid(True)

# Ajustar el diseño de los subplots
plt.tight_layout()

# Mostrar los subplots
plt.show()
