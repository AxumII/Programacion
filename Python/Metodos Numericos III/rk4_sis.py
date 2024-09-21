import numpy as np
import matplotlib.pyplot as plt


class RK4:
    def __init__(self, Un_init, x, dudx):
        """
        Un_init: Array con los valores iniciales de cada función del sistema.
        x: Array de valores de la variable independiente (ej. tiempo).
        dudx: Array de funciones que describen las derivadas de cada variable dependiente.
        """
        self.Un_init = np.array(Un_init)  # Vector de valores iniciales para cada variable dependiente
        self.x = np.array(x)  # Array de valores de la variable independiente
        self.dudx = dudx  # Array de funciones derivativas (cada una corresponde a una variable dependiente)
        self.h = x[1] - x[0]  # Paso entre valores de la variable independiente
        self.U = np.zeros((len(x), len(Un_init)))  # Matriz para guardar las soluciones de cada variable en cada paso
        self.U[0, :] = Un_init  # Asignar las condiciones iniciales
        
        self.solve()

    def solve(self):
        """
        Resolver el sistema de ecuaciones diferenciales usando el método RK4.
        """
        # Iterar sobre los valores de x, excluyendo el último valor
        for i in range(1, len(self.x)):
            xi = self.x[i - 1]
            Ui = self.U[i - 1, :]  # Vector de soluciones en el paso anterior
            
            k1 = np.zeros(len(Ui))
            k2 = np.zeros(len(Ui))
            k3 = np.zeros(len(Ui))
            k4 = np.zeros(len(Ui))
            
            # Cálculo de los coeficientes k1, k2, k3, k4 para cada ecuación del sistema
            for j in range(len(Ui)):  # Para cada ecuación en el sistema
                k1[j] = self.h * self.dudx[j](xi, Ui)
            
            for j in range(len(Ui)):
                k2[j] = self.h * self.dudx[j](xi + 0.5 * self.h, Ui + 0.5 * k1)
            
            for j in range(len(Ui)):
                k3[j] = self.h * self.dudx[j](xi + 0.5 * self.h, Ui + 0.5 * k2)
            
            for j in range(len(Ui)):
                k4[j] = self.h * self.dudx[j](xi + self.h, Ui + k3)
            
            # Calcular el siguiente valor de las variables dependientes
            self.U[i, :] = Ui + (k1 + 2 * k2 + 2 * k3 + k4) / 6.0

    def get_solution(self):
        """
        Devolver la matriz de soluciones. Cada fila corresponde a un valor de x
        y cada columna a una variable dependiente del sistema.
        """
        return self.U
    

# Definir la matriz del sistema lineal
A = np.array([[1, 2], [3, 4]])

# Definir las derivadas del sistema lineal
def du1_dt(t, U):
    u1, u2 = U
    return A[0, 0] * u1 + A[0, 1] * u2

def du2_dt(t, U):
    u1, u2 = U
    return A[1, 0] * u1 + A[1, 1] * u2

# Condiciones iniciales: u1(0) = 1, u2(0) = 0
Un_init = [1, 0]
t = np.arange(0, 5, 0.1)  # Tiempo de simulación

# Resolver el sistema con RK4
solver = RK4(Un_init, t, [du1_dt, du2_dt])
soluciones = solver.get_solution()

# Extraer las soluciones numéricas
u1_numerica = soluciones[:, 0]
u2_numerica = soluciones[:, 1]

# Soluciones analíticas exactas
# Cálculo de autovalores y autovectores de la matriz A
valores_propios, vectores_propios = np.linalg.eig(A)
lambda1, lambda2 = valores_propios

# Cálculo de coeficientes para las soluciones exactas usando condiciones iniciales
C = np.linalg.solve(vectores_propios, Un_init)

# Solución analítica exacta para u1 y u2
def u1_analitica(t):
    return C[0] * vectores_propios[0, 0] * np.exp(lambda1 * t) + C[1] * vectores_propios[0, 1] * np.exp(lambda2 * t)

def u2_analitica(t):
    return C[0] * vectores_propios[1, 0] * np.exp(lambda1 * t) + C[1] * vectores_propios[1, 1] * np.exp(lambda2 * t)

# Calcular las soluciones analíticas para cada t
u1_exacta = u1_analitica(t)
u2_exacta = u2_analitica(t)

# Graficar las soluciones numéricas y analíticas
plt.figure(figsize=(10, 6))
plt.plot(t, u1_numerica, label='u1 numérica (RK4)', linestyle='--')
plt.plot(t, u2_numerica, label='u2 numérica (RK4)', linestyle='--')
plt.plot(t, u1_exacta, label='u1 analítica exacta', linestyle='-')
plt.plot(t, u2_exacta, label='u2 analítica exacta', linestyle='-')
plt.legend()
plt.xlabel('Tiempo')
plt.ylabel('Valor de u')
plt.title('Sistema Lineal: Comparación entre soluciones numéricas y analíticas')
plt.grid()
plt.show()


# Definir la EDO de segundo orden como sistema de primer orden
# EDO original: d^2y/dx^2 = -y - 0.2(dy/dx)
def dudx1(x, U):
    # U[0] = y, U[1] = dy/dx
    return U[1]

def dudx2(x, U):
    # U[0] = y, U[1] = dy/dx
    return -U[0] - 0.2 * U[1]

# Valores iniciales
Un_init = [1.0, 0.0]  # [y(0), dy/dx(0)]
x = np.arange(0, 5, 0.000001)  # Valores de x

# Lista de funciones que definen el sistema de EDOs
dudx = [dudx1, dudx2]

# Crear instancia de RK4
rk4_solver = RK4(Un_init, x, dudx)

# Obtener la solución
solution = rk4_solver.get_solution()

# Definir la solución analítica
def analytical_solution(x):
    C1 = 1
    C2 = 0.05038
    omega = np.sqrt(0.99)
    return np.exp(-0.1 * x / 2) * (C1 * np.cos(omega * x) + C2 * np.sin(omega * x))

# Calcular la solución analítica
y_analytical = analytical_solution(x)

# Graficar la solución numérica y analítica
plt.plot(x, solution[:, 0], label='RK4 Numérica', linestyle='dashed')
plt.plot(x, y_analytical, label='Solución Analítica')
plt.legend()
plt.xlabel('x')
plt.ylabel('y(x)')
plt.title('Comparación de la solución RK4 y la solución analítica')
plt.grid()
plt.show()