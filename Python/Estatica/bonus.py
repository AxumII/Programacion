import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import quad
import sympy as sp

# Define the symbolic variable and functions
x_sym = sp.symbols('x')
f1_sym = -1/3 * x_sym**2
f2_sym = -1/3 * x_sym**2 + 3
f3_sym = (-x_sym + 6)**2

# Define numeric integration for each segment
def integral_numeric(f, a, b):
    result, _ = quad(f, a, b)
    return result

# Calculate numeric integrals for each segment
area1 = integral_numeric(lambda x: -1/3 * x**2, 0, 1.5)
area2 = integral_numeric(lambda x: -1/3 * x**2 + 3, 1.5, 4.5)
area3 = integral_numeric(lambda x: (-x + 6)**2, 4.5, 6)

# Calculate symbolic integrals for each segment
integral1_sym = sp.integrate(f1_sym, (x_sym, 0, 1.5))
integral2_sym = sp.integrate(f2_sym, (x_sym, 1.5, 4.5))
integral3_sym = sp.integrate(f3_sym, (x_sym, 4.5, 6))

# Create x values for cumulative integral plots
x_total = np.linspace(0, 6, 500)
y_integral = np.zeros_like(x_total)

# Numeric cumulative integral
for i, x_val in enumerate(x_total):
    if x_val <= 1.5:
        y_integral[i] = integral_numeric(lambda x: -1/3 * x**2, 0, x_val)
    elif 1.5 < x_val <= 4.5:
        y_integral[i] = area1 + integral_numeric(lambda x: -1/3 * x**2 + 3, 1.5, x_val)
    else:
        y_integral[i] = area1 + area2 + integral_numeric(lambda x: (-x + 6)**2, 4.5, x_val)

# Plot symbolic and numeric integrals
plt.figure(figsize=(10, 6))

# Numeric integral plot
plt.plot(x_total, y_integral, label="Integral de la fuerza cortante", color="green")


# Add labels, legend, and grid
plt.xlabel("Distancia : m")
plt.ylabel("Momento Flector: kN*m")
plt.title("Momento Flector en la viga")
plt.legend()
plt.grid()
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.show()

# Display symbolic integral values
integral1_sym, integral2_sym, integral3_sym
