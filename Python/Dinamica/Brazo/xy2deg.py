import numpy as np

class XYtoDeg:
    def __init__(self, l1, l2):
        self.l1 = l1
        self.l2 = l2
        
    def ik(self, x, y):
        # 1. Distancia al objetivo
        magn2 = x**2 + y**2
        magn = np.sqrt(magn2)

        # Verificación de alcance
        if magn > (self.l1 + self.l2) or magn < abs(self.l1 - self.l2):
            print(f"Error: Punto ({x}, {y}) fuera de alcance")
            return None

        # 2. Ley de cosenos para theta2, D = cos(theta2)
        D = (magn2 - self.l1**2 - self.l2**2) / (2.0 * self.l1 * self.l2)
        
        # usar negativo para codo arriba
        theta2 = np.arctan2(-np.sqrt(1 - D**2), D)
        
        # 3. Ángulo theta1
        alpha = np.arctan2(y, x)
        beta = np.arctan2(self.l2 * np.sin(theta2), self.l1 + self.l2 * np.cos(theta2))
        theta1 = alpha - beta
        
        # Retornar en grados
        return np.degrees(theta1), np.degrees(theta2)
    
########
if __name__ == "__main__":
    l1 = 106.0
    l2 = 97.0
    xy2ang = XYtoDeg(l1, l2)
    
    x_target = 100.0
    y_target = 0.0
    angles = xy2ang.ik(x_target, y_target)
    if angles:  
        print(f"Ángulos para alcanzar ({x_target}, {y_target}): θ1 = {angles[0]:.2f}°, θ2 = {angles[1]:.2f}°")      
    
