import numpy as np

# Operaciones básicas
def ejemploOperacionesBasicas():
    a = np.array([1, 2, 3])
    b = np.array([4, 5, 6])
    suma = a + b
    resta = a - b
    producto = a * b
    division = a / b
    return suma, resta, producto, division

# Derivada
def ejemploDerivada():
    def f(x):
        return x**2
    
    x = np.linspace(0, 5, 100)
    y = f(x)
    derivada = np.gradient(y, x)
    return x, y, derivada

# Integral
def ejemploIntegral():
    def f(x):
        return x**2
    
    x = np.linspace(0, 5, 100)
    y = f(x)
    integral = np.trapz(y, x)
    return x, y, integral

# Ecuación Diferencial Ordinaria (EDO)
def ejemploEDO():
    from scipy.integrate import odeint
    
    def model(y, t):
        return -2 * y
    
    t = np.linspace(0, 5, 100)
    y0 = 1
    y = odeint(model, y0, t)
    return t, y

# Transformada de Laplace
def ejemploTransformadaLaplace():
    from scipy.signal import step, impulse
    import matplotlib.pyplot as plt
    
    num = [1]
    den = [1, 1, 1]
    t, y = step((num, den))
    t_imp, h = impulse((num, den))
    
    plt.figure()
    plt.plot(t, y, label='Respuesta al escalón')
    plt.plot(t_imp, h, label='Respuesta al impulso')
    plt.legend()
    plt.xlabel('Tiempo')
    plt.ylabel('Amplitud')
    plt.show()

# Funciones específicas
def ejemploFuncionesEspecificas():
    x = np.linspace(-2*np.pi, 2*np.pi, 100)
    escalon = np.heaviside(x, 1)
    impulso = np.zeros_like(x)
    impulso[50] = 1
    sin_func = np.sin(x)
    piecewise_func = np.piecewise(x, [x < 0, x >= 0], [-1, 1])
    return x, escalon, impulso, sin_func, piecewise_func

# Llamadas a las funciones
print("Operaciones básicas:", ejemploOperacionesBasicas())
print("Derivada:", ejemploDerivada())
print("Integral:", ejemploIntegral())
print("EDO:", ejemploEDO())
print("Transformada de Laplace:")
ejemploTransformadaLaplace()
print("Funciones específicas:", ejemploFuncionesEspecificas())


###################################################################################################################################

import numpy as np
from scipy.integrate import odeint
from scipy.signal import step, impulse
import matplotlib.pyplot as plt

# Operaciones básicas
def ejemploOperacionesBasicas():
    a = np.array([1, 2, 3])
    b = np.array([4, 5, 6])
    suma = a + b
    resta = a - b
    producto = a * b
    division = a / b
    return suma, resta, producto, division

# Derivada
def ejemploDerivada():
    def f(x):
        return x**2
    
    x = np.linspace(0, 5, 100)
    y = f(x)
    derivada = np.gradient(y, x)
    return x, y, derivada

# Integral
def ejemploIntegral():
    def f(x):
        return x**2
    
    x = np.linspace(0, 5, 100)
    y = f(x)
    integral = np.trapz(y, x)
    return x, y, integral

# Ecuación Diferencial Ordinaria (EDO)
def ejemploEDO():
    def model(y, t):
        return -2 * y
    
    t = np.linspace(0, 5, 100)
    y0 = 1
    y = odeint(model, y0, t)
    return t, y

# Transformada de Laplace
def ejemploTransformadaLaplace():
    num = [1]
    den = [1, 1, 1]
    t, y = step((num, den))
    t_imp, h = impulse((num, den))
    
    plt.figure()
    plt.plot(t, y, label='Respuesta al escalón')
    plt.plot(t_imp, h, label='Respuesta al impulso')
    plt.legend()
    plt.xlabel('Tiempo')
    plt.ylabel('Amplitud')
    plt.show()

# Funciones específicas
def ejemploFuncionesEspecificas():
    x = np.linspace(-2*np.pi, 2*np.pi, 100)
    escalon = np.heaviside(x, 1)
    impulso = np.zeros_like(x)
    impulso[50] = 1
    sin_func = np.sin(x)
    piecewise_func = np.piecewise(x, [x < 0, x >= 0], [-1, 1])
    return x, escalon, impulso, sin_func, piecewise_func

# Llamadas a las funciones
print("Operaciones básicas:", ejemploOperacionesBasicas())
print("Derivada:", ejemploDerivada())
print("Integral:", ejemploIntegral())
print("EDO:", ejemploEDO())
print("Transformada de Laplace:")
ejemploTransformadaLaplace()
print("Funciones específicas:", ejemploFuncionesEspecificas())
