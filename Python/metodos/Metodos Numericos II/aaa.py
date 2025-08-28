import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import BarycentricInterpolator

# Definir la función de Runge
def runge_function(x):
    return 1 / (1 + 25 * x**2)

# Generar puntos equiespaciados
n = 10
x_equi = np.linspace(-1, 1, n+1)
y_equi = runge_function(x_equi)

# Interpolación polinómica con puntos equiespaciados
poly_equi = BarycentricInterpolator(x_equi, y_equi)

# Generar puntos de Chebyshev
x_cheb = np.cos((2 * np.arange(n+1) + 1) * np.pi / (2 * (n+1)))
y_cheb = runge_function(x_cheb)

# Interpolación polinómica con puntos de Chebyshev
poly_cheb = BarycentricInterpolator(x_cheb, y_cheb)

# Puntos para graficar
x_plot = np.linspace(-1, 1, 1000)
y_true = runge_function(x_plot)
y_equi_interp = poly_equi(x_plot)
y_cheb_interp = poly_cheb(x_plot)

# Graficar los resultados
plt.figure(figsize=(14, 7))

# Interpolación con puntos equiespaciados
plt.subplot(1, 2, 1)
plt.plot(x_plot, y_true, 'k-', label='Función de Runge $f(x)$')
plt.plot(x_plot, y_equi_interp, 'r--', label='Interpolación Equiespaciada $P_{10}(x)$')
plt.plot(x_equi, y_equi, 'bo', label='Puntos Equiespaciados')
plt.title('Interpolación Polinómica con Puntos Equiespaciados')
plt.xlabel('$x$')
plt.ylabel('$y$')
plt.legend()
plt.grid()

# Interpolación con puntos de Chebyshev
plt.subplot(1, 2, 2)
plt.plot(x_plot, y_true, 'k-', label='Función de Runge $f(x)$')
plt.plot(x_plot, y_cheb_interp, 'r--', label='Interpolación Chebyshev $P_{10}(x)$')
plt.plot(x_cheb, y_cheb, 'bo', label='Puntos de Chebyshev')
plt.title('Interpolación Polinómica con Puntos de Chebyshev')
plt.xlabel('$x$')
plt.ylabel('$y$')
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()
