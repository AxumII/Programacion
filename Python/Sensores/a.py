# Gráfica con eje X en kΩ (escala lineal)

import numpy as np
import matplotlib.pyplot as plt

def x(R1,R2,C1,C2,Rs,Rx):
    R1_t = 1/((1/R1)+(1/(Rs + Rx))) 
    return 1 / np.sqrt(R1_t*R2*C1*C2)

# Unidades
k = 1e3
n = 1e-9

# Parámetros fijos
R1 = 15.8*k
R2 = 15.8*k
C1 = 10*n
C2 = 10*n
Rx = 200*k

# Barrido lineal de Rs (100 Ω a 1 MΩ)
Rs_values = np.linspace(5*k, 50*k, 1000)

# Frecuencia (Hz)
frecuencia = x(R1, R2, C1, C2, Rs_values, Rx) / (2*np.pi)

# Eje X en kΩ
Rs_kohm = Rs_values / 1e3

plt.figure(figsize=(7,5))
plt.plot(Rs_kohm, frecuencia)
plt.xlabel('Rs (kΩ)')
plt.ylabel('Frecuencia (Hz)')
plt.title('Frecuencia vs Rs (eje en kΩ, escala lineal)')
plt.grid(True, ls=':')
plt.tight_layout()
plt.show()



