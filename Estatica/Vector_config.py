import numpy as np

class VectorConfig:
    def __init__(self, tipo, coord=None, cosdir=None, magnitude=None, angle=False):
        self.coord = np.array([np.nan if x is None else x for x in (coord or [None, None, None])], dtype=float)
        self.cosdir = np.array([np.nan if x is None else x for x in (cosdir or [None, None, None])], dtype=float)
        self.magnitude = magnitude if magnitude is not None else self.calculate_magnitude_from_components(coord)
        self.tipo = tipo
        self.angle = angle
        self.validate_and_convert()

    def validate_and_convert(self):
        if self.tipo == 0:
            self.validate_components()
        elif self.tipo in [1, 2, 3, 4, 5, 6]:
            self.convert()
        else:
            print("Error: Tipo no reconocido.")

    def convert(self):
        if self.angle:
            self.angle_to_cos()

        # Reutilizar lógica para diferentes tipos
        if self.tipo == 1:
            self.type_1_logic()
        elif self.tipo == 2:
            self.type_2_logic()
        elif self.tipo == 3:
            self.type_3_logic()
        elif self.tipo == 4:
            self.type_4_logic()
        elif self.tipo == 5 or self.tipo == 6:
            self.type_5_logic()

    def type_1_logic(self):
        miss_i, other_i = self.find_index(self.coord)
        if len(miss_i) != 1 or len(other_i) != 2:
            print("Error: Debe haber exactamente dos componentes conocidas y una desconocida.")
            return
        self.calculate_missing_component(miss_i, other_i)

    def type_2_logic(self):
        self.calculate_magnitude_and_missing_components()

    def type_3_logic(self):
        self.calculate_missing_components_based_on_angle()

    def type_4_logic(self):
        self.calculate_missing_cosdir_and_update_coords()

    def type_5_logic(self):
        self.update_coordinates_based_on_cosdir()

    def angle_to_cos(self):
        self.cosdir = np.cos(np.radians(self.cosdir))

    def find_index(self, vector):
        miss_index = np.where(np.isnan(vector))[0]
        other_index = np.where(~np.isnan(vector))[0]
        return miss_index, other_index

    def validate_components(self):
        if np.isnan(self.coord).all():
            print("Error: Todas las componentes son NaN.")

    def calculate_magnitude_from_components(self, components):
        if components is not None:
            valid_components = [c for c in components if c is not None]
            if valid_components:
                return np.sqrt(np.sum(np.array(valid_components) ** 2))
        return np.nan

    def calculate_missing_component(self, miss_i, other_i):
        sum_squares = np.nansum(self.coord[other_i] ** 2)
        if self.magnitude**2 < sum_squares:
            print("Error: Los valores proporcionados no cumplen con la desigualdad triangular.")
            return
        self.coord[miss_i] = np.sqrt(max(self.magnitude**2 - sum_squares, 0))

    def calculate_magnitude_and_missing_components(self):
        # Implementación específica para el tipo 2
        pass

    def calculate_missing_components_based_on_angle(self):
        # Implementación específica para el tipo 3
        pass

    def calculate_missing_cosdir_and_update_coords(self):
        # Implementación específica para el tipo 4
        pass

    def update_coordinates_based_on_cosdir(self):
        if self.tipo == 6:
            # Recalcular magnitud basada en componente conocida para tipo 6
            known_i = np.where(~np.isnan(self.coord))[0]
            if len(known_i) != 1:
                print("Error: Debe haber exactamente una componente conocida para tipo 6.")
                return
            self.magnitude = self.coord[known_i] / self.cosdir[known_i]
        self.coord = self.cosdir * self.magnitude

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
