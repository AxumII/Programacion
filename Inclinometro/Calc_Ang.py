import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from vectorObject import Vector_Object as vt

class Inclinometro:
    def __init__(self, gvect, tol=0.5):
        self.gvect = gvect
        g = vt(coords=[0, 0, -9.81])
        self.g = g
        self.tol = tol

    def calculate(self):
        self.magnitude_difference = abs(self.gvect.get_magn() - self.g.get_magn())
        if self.magnitude_difference < (self.tol * self.g.get_magn()):            
            angulos = np.arccos(self.gvect.get_angles())
            angulos = np.degrees(angulos)

            # Corregir el ángulo respecto al eje Z
            angulos[2] = 180 - angulos[2]

            self.angulos = angulos

            # Calcular el ángulo con respecto al plano XY
            xy_projection = np.array([self.gvect.coords[0], self.gvect.coords[1], 0])
            xy_magn = np.linalg.norm(xy_projection)
            self.angle_xy = np.degrees(np.arccos(np.dot(self.gvect.coords, xy_projection) / (self.gvect.get_magn() * xy_magn)))

            #print("Diferencia de magnitud frente a g",self.magnitude_difference, "\n")
             # Calcular ángulos complementarios
            self.complementary_angles = 90 - self.angulos
            self.complementary_angle_xy = 90 - self.angle_xy


            return self.complementary_angles ,  self.complementary_angle_xy


        else:
            print("Corrija el vector, la magnitud no es g o cercano en la tolerancia")

    def graf(self):
        fig = plt.figure(figsize=(15, 15))  
        ax = fig.add_subplot(111, projection='3d')

        # Graficar ejes extendidos como líneas punteadas más gruesas
        ax.plot([-10, 10], [0, 0], [0, 0], 'k--', linewidth=5, label='Eje X')
        ax.plot([0, 0], [-10, 10], [0, 0], 'k--', linewidth=3, label='Eje Y')
        ax.plot([0, 0], [0, 0], [-10, 1], 'k--', linewidth=3, label='Eje Z')

        #Graficar g

        ax.quiver(0, 0, 0, self.g.coords[0], self.g.coords[1], self.g.coords[2], color='b', label='Vector g', length=1.5)
        
        # Graficar el vector gvect 
        ax.quiver(0, 0, 0, self.gvect.coords[0], self.gvect.coords[1], self.gvect.coords[2], color='r', label=f'Vector gvect ({self.gvect.coords[0]}, {self.gvect.coords[1]}, {self.gvect.coords[2]})', length=1.5)

        # Plano sombreado en XY
        xx, yy = np.meshgrid(range(-10, 11), range(-10, 11))
        zz = np.zeros_like(xx)
        xy_plane = ax.plot_surface(xx, yy, zz, color='g', alpha=0.2)

        # Mostrar los ángulos 
        if hasattr(self, 'angulos'):
            # Ángulos con respecto a los ejes
            ax.text(self.gvect.coords[0], 0, 0, f'θx: {self.angulos[0]:.2f}°', color='b')
            ax.text(0, self.gvect.coords[1], 0, f'θy: {self.angulos[1]:.2f}°', color='b')
            ax.text(0, 0, self.gvect.coords[2], f'θz: {self.angulos[2]:.2f}°', color='b')

            # Ángulo con respecto al plano XY
            ax.text(-self.gvect.coords[0], -self.gvect.coords[1], 0, f'θxy: {self.angle_xy:.2f}°', color='g')

           
            ax.plot([], [], ' ', label=f'Ángulos: θx: {self.angulos[0]:.2f}°, θy: {self.angulos[1]:.2f}°, θz: {self.angulos[2]:.2f}°, θxy: {self.angle_xy:.2f}°')

        plt.legend(loc='upper right')
        plt.show()


"""
# Uso de la clase Inclinometro
gvect1 = vt(coords=[0.1, 0.1, -9.8])
print(gvect1.get_magn())

inclinometro = Inclinometro(gvect1)
inclinometro.calculate()
inclinometro.graf()
"""