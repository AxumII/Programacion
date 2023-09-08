import numpy as np
import matplotlib.pyplot as plt

def senal(k, b, t):
    x = k * np.cos(2 * np.pi * b * t)
    return x

t = np.arange(-5, 5, 0.0001)

# Definir señales
s1 = senal(-4.05, 1, t)
s2 = senal(-0.45, 3, t)
s3 = senal(-0.162, 5, t)
s4 = senal(-0.082, 7, t)
################################
s5 = senal(5, 1, t)
s6 = senal(2.12, 2, t)
s7 = senal(-0.424, 4, t)
s8 = senal(0.181, 6, t)
###########################################
s9 = senal(6.36, 1, t)
s10 = senal(-2.12, 3, t)
s11 = senal(1.272, 5, t)
s12 = senal(0.907, 7, t)
#################################################

# Sumas
sum1 = s1 + s2 + s3 + s4
sum2 = s5 + s6 + s7 + s8
sum3 = s9 + s10 + s11 + s12

# Graficar señales individuales
plt.figure(figsize=(12, 6))
# Graficar sumas
plt.subplot(1, 1, 1)
plt.plot(t, sum1, label='Suma 1 (s1+s2+s3+s4)')
plt.plot(t, sum2, label='Suma 2 (s5+s6+s7+s8)')
plt.plot(t, sum3, label='Suma 2 (s9+s10+s11+s12)')
plt.title('Sumas de Señales')
plt.xlabel('Tiempo')
plt.ylabel('Amplitud')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
