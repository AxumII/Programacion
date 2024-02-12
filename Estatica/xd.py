import numpy as np

class VectorConfig:
    def __init__(self, tipo, coord=None, cosdir=None, magnitude=None, angle=False):
        # Convertir None a np.nan para facilitar la identificación de datos faltantes
        self.coord = np.array([np.nan if x is None else x for x in (coord or [None, None, None])], dtype=float)
        self.cosdir = np.array([np.nan if x is None else x for x in (cosdir or [None, None, None])], dtype=float)
        self.magnitude = magnitude
        self.tipo = tipo
        self.angle = angle
        self.convert(tipo)

    def convert(self, tipo):
        if tipo == 0:  # 3 componentes cartesianas
            pass  # Ya manejado en __init__

        elif tipo == 1:  # 2 componentes cartesianas y la magnitud
            miss_i, other_i = self.find_index(self.coord)

            if len(miss_i) != 1 or len(other_i) != 2:
                print("Error: Debe haber exactamente dos componentes conocidas y una desconocida.")
                return
            
            sum_squares = np.nansum(self.coord[other_i] ** 2)
            if self.magnitude**2 < sum_squares:
                print("Error: Los valores proporcionados no cumplen con la desigualdad triangular.")
                return

            self.coord[miss_i] = np.sqrt(max(self.magnitude**2 - sum_squares, 0))

        elif tipo == 2:  # 2 componentes cartesianas y 1 ángulo o coseno director
            if self.angle:
                self.angle_to_cos()
            itsc = np.where(~np.isnan(self.coord) & ~np.isnan(self.cosdir))[0]

            if len(itsc) != 1:
                print("Error: Debe haber exactamente un componente común entre coordenadas y cosenos directores.")
                return

            self.magnitude = self.coord[itsc[0]] / self.cosdir[itsc[0]]
            miss_i_c, _ = self.find_index(self.coord)
            self.coord[miss_i_c] = self.magnitude * self.cosdir[miss_i_c]

        elif tipo == 3:  # 1 ángulo o coseno director, la magnitud y una componente
            if self.angle:
                self.angle_to_cos()

            miss_i_c, other_i_c = self.find_index(self.coord)
            miss_i_o, other_i_o = self.find_index(self.cosdir)

            if np.array_equal(other_i_c, other_i_o):
                print("No es posible armar el vector, deben ser de distinto eje el ángulo y la componente")
                return

            self.coord[other_i_o] = self.magnitude * self.cosdir[other_i_o]
            sum_squares = np.nansum(self.coord ** 2)
            self.coord[miss_i_c] = np.sqrt(max(self.magnitude**2 - sum_squares, 0))

        elif tipo == 4:  # 2 ángulos o cosenos directores y la magnitud (coordenadas esféricas)
            miss_i, _ = self.find_index(self.cosdir)
            if len(miss_i) != 1:
                print("Error: Debe haber exactamente un coseno director desconocido.")
                return
            # Calculamos el coseno director faltante usando la relación entre los cosenos directores y la magnitud.
            self.cosdir[miss_i] = np.sqrt(1 - np.nansum(self.cosdir**2))
            # Actualizamos las coordenadas usando los cosenos directores y la magnitud.
            self.coord = self.cosdir * self.magnitude

        elif tipo == 5:  # 3 ángulos o cosenos directores y la magnitud
            if self.angle:
                self.angle_to_cos()
            self.coord = self.cosdir * self.magnitude

        elif tipo == 6:  # 3 ángulos o cosenos directores y una componente
            if self.angle:
                self.angle_to_cos()
        
            known_i = np.where(~np.isnan(self.coord))[0]  # Índice de la componente conocida
            if len(known_i) != 1:
                print("Error: Debe haber exactamente una componente conocida.")
                return
            
            known_i = known_i[0]  # Extraemos el índice como un entero
            
            # Calculamos la magnitud del vector a partir de la componente conocida y su coseno director correspondiente
            self.magnitude = abs(self.coord[known_i] / self.cosdir[known_i])
            
            # Calculamos las componentes desconocidas utilizando la magnitud y los cosenos directores
            for i in range(3):
                if np.isnan(self.coord[i]):
                    self.coord[i] = self.magnitude * self.cosdir[i]


    def angle_to_cos(self):
        # Convertir ángulo (en grados) a coseno director si es necesario
        self.cosdir = np.radians(self.cosdir)
        self.cosdir = np.cos(self.cosdir)

    def find_index(self, vector):
        miss_index = np.where(np.isnan(vector))[0]
        other_index = np.where(~np.isnan(vector))[0]
        return miss_index, other_index

# Función para imprimir los detalles de un vector
def print_vector_details(vector, title):
    print(f"{title}:")
    print(f"  Coordenadas: {vector.coord}")


vector_tipo_0 = VectorConfig(tipo=0, coord=[1, 2, 3])
print_vector_details(vector_tipo_0, "Vector Tipo 0")

vector_tipo_1 = VectorConfig(tipo=1, coord=[3, 4, None], magnitude=7)
print_vector_details(vector_tipo_1, "Vector Tipo 1")

vector_tipo_2 = VectorConfig(tipo=2, coord=[3, 4, None], cosdir=[0.4, None, 0.5], angle=False)
print_vector_details(vector_tipo_2, "Vector Tipo 2")

vector_tipo_3 = VectorConfig(tipo=3, coord=[None, None, 4], cosdir=[None, 0.6, None], magnitude=5, angle=False)
print_vector_details(vector_tipo_3, "Vector Tipo 3")

vector_tipo_4 = VectorConfig(tipo=4, cosdir=[0.5, 0.1, None], magnitude=10)
print_vector_details(vector_tipo_4, "Vector Tipo 4")

vector_tipo_5 = VectorConfig(tipo=5, cosdir=[0.4, 0.577, 0.98], magnitude=5, angle=False)
print_vector_details(vector_tipo_5, "Vector Tipo 5")

vector_tipo_6 = VectorConfig(tipo=6, coord=[None, 10, None], cosdir=[0.3, 0.3, 0.3])
print_vector_details(vector_tipo_6, "Vector Tipo 6")
