

import numpy as np
from Vector_operation import Vector_operation 


    

class Vector_definition:
    def __init__(self, tipo, coord=None, cosdir=None, magnitude=None, angle=False):
        self.tipo = tipo
        self.angle = angle 
        self.coord = np.array([np.nan if x is None else x for x in (coord or [None, None, None])], dtype=float)
        self.cosdir = np.array([np.nan if x is None else x for x in (cosdir or [None, None, None])], dtype=float)
        self.magnitude = magnitude

        # Crear una instancia de Vector_operation y asignarla a self.vop
        self.vop = Vector_operation()  # Esta es la línea que necesitas agregar

        self.convert(tipo)  # Asegúrate de llamar convert después de inicializar todos los atributos

   



    def convert(self, tipo):
        if tipo == 0:  # 3 componentes cartesianas, no se necesita conversión
            if not self.vop.validate_components(self.coord):
                print("Error en el tipo 0: Todas las componentes no pueden ser NaN.")

        elif tipo == 1:  # 2 componentes cartesianas y la magnitud
            self.coord = self.vop.find_miss(self.coord, self.magnitude)

        elif tipo == 2:  # 2 componentes cartesianas y 1 ángulo o coseno director
            pass

        elif tipo == 3:  # 1 ángulo o coseno director, la magnitud y una componente
            pass

        elif tipo == 4:  # 2 ángulos o cosenos directores y la magnitud (coordenadas esféricas)
            pass

        elif tipo == 5:  # 3 ángulos o cosenos directores y la magnitud
            pass

        elif tipo == 6:  # 3 ángulos o cosenos directores y una componente
            pass




# Ejemplos
def print_vector_details(vector, title):
    print(f"{title}:")
    print(f"  Coordenadas: {vector.coord}")
    print(f"  Magnitud: {vector.magnitude}")

vector_tipo_0 = Vector_definition(tipo=0, coord=[1, 2, 3])
print_vector_details(vector_tipo_0, "Vector Tipo 0")

vector_tipo_1 = Vector_definition(tipo=1, coord=[3, 4, None], magnitude=5)
print_vector_details(vector_tipo_1, "Vector Tipo 1")



