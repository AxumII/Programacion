import numpy as np

#Recordar que Rk es para edos de 1 orden, asi que se descompone

class RK4:
    def __init__(self, Un_init , x, dudx):
        self.Un_init = Un_init  #Vector de valores iniciales
        self.x = x  # Array de valores de independiente
        self.dudx = dudx  # Función derivativa derivada
        #dydx es yb array de funciones de n variables
        self.h = x[1] - x[0]  # Paso
        self.U = np.array()
        for i in range(0,np.len(Un_init)):
            self.U[i] = np.append(Un_init[i])
            
        self.solve()
        
    def solve(self):
        
         # Iterar sobre los valores de x, excluyendo el último para evitar salida de rango
        for xi in self.x[:-1]:
            ui : float
            # Cálculo de los coeficientes de Runge-Kutta (k1, k2, k3, k4)
            for fn in self.dudx:
                k1 = self.h * self.dudx[fn(xi,ui)]
                k2 = self.h * self.dudx[fn]
                
                
                
                
                k2 = self.h * self.dudx(fn(xi + 0.5 * self.h, ui + 0.5 * k1))
                k3 = self.h * self.dudx(fn(xi + 0.5 * self.h, yi + 0.5 * k2))
                k4 = self.h * self.dudx(fn(xi + self.h, yi + k3))
            
            
            
            
            
                
                
            #aca va el init temporal
            
            
            yi = self.y[-1]  # Último valor de y calculado
            
            # Cálculo de los coeficientes de Runge-Kutta (k1, k2, k3, k4)
            k1 = self.h * self.dydx(xi, yi)
            k2 = self.h * self.dydx(xi + 0.5 * self.h, yi + 0.5 * k1)
            k3 = self.h * self.dydx(xi + 0.5 * self.h, yi + 0.5 * k2)
            k4 = self.h * self.dydx(xi + self.h, yi + k3)
            
            # Calcular el siguiente valor de y usando la fórmula de RK4
            y_next = yi + (k1 + 2 * k2 + 2 * k3 + k4) / 6.0
            
            # Añadir el nuevo valor de y al array
            self.y = np.append(self.y, y_next)