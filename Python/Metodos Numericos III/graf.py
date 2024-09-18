import matplotlib.pyplot as plt
import numpy as np

class graf:
    def __init__(self, x=np.array([]), yn=np.array([]), function_at=None, I=None, title=''):
        self.x = x
        self.yn = yn
        self.title = title
        self.I = I  # Configuración de una línea para marcar x = k o y = k

        # Configuración de los atributos de los arrays
        self.function_at = function_at or [{'label': f'Función {i+1}', 'linestyle': '-', 'color': None}
                                           for i in range(self.yn.shape[0] if self.yn.ndim == 2 else 1)]
        
        self.plot()

    def plot(self):
        plt.figure(figsize=(12, 6))
        
        # Graficar múltiples arrays 
        if self.yn.ndim == 2:  # Caso de múltiples funciones
            for y, attr in zip(self.yn, self.function_at):
                plt.plot(self.x, y, **attr)
        else:  # Caso de una sola función
            plt.plot(self.x, self.yn, **self.function_at[0])

        # Añadir línea de referencia punteada si se especifica
        if self.I:
            val = self.I.get('valor', 0)
            if self.I.get('orientacion') == 'v':
                plt.axvline(x=val, linestyle='--', color='purple', label=f'x = {val}')
            elif self.I.get('orientacion') == 'h':
                plt.axhline(y=val, linestyle='--', color='purple', label=f'y = {val}')

        plt.xlabel('Eje X')
        plt.ylabel('Eje Y')
        plt.title(self.title)
        plt.grid(True)
        plt.legend()
        plt.show()
"""
# Ejemplo de uso
x = np.linspace(0, 10, 100)
yn = np.array([20*np.sin(x), 10*np.cos(x), np.exp(x**0.5), 0.1*x**2 + 1])  # Múltiples funciones

# Configuraciones personalizadas para cada función
function_at = [
    {'label': '20*sin(x)', 'linestyle': '-', 'color': 'blue'},
    {'label': '10*cos(x)', 'linestyle': '--', 'color': 'red'},
    {'label': 'exp(sqrt(x))', 'linestyle': '-.', 'color': 'green'},
    {'label': '0.1*x^2 + 1', 'linestyle': ':', 'color': 'purple'}
]

# Configuración de una línea de referencia vertical
I = {'orientacion': 'v', 'valor': 5}

# Crear instancia de la clase graf con configuraciones personalizadas y un título específico
grafica = graf(x, yn, function_at, I, title='Funciones Matemáticas Ejemplares')

# Crear otra instancia de la clase graf con las dimensiones correctas
x2 = np.linspace(0, 1000, 1000)
yn2 = x2**2 + 3*x2 - 5  # Define `yn2` usando `x2` para que coincidan las dimensiones
graf2 = graf(x=x2, yn=yn2, title="Prueba Singular", function_at=[{'label' : "XD"}])
"""