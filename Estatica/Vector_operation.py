import numpy as np

class Vector_operation:
    def __init__(self) -> None:
        pass

    def angle_to_cos(self, cosdir):
        # Convierte ángulos a cosenos directores
        return np.cos(np.radians(cosdir))

    def cos_to_angle(self, cos):
        # Convierte cosenos directores a ángulos en grados
        return np.degrees(np.arccos(cos))

    def find_index(self, vector):
        # Encuentra índices de componentes faltantes y presentes
        miss_index = np.where(np.isnan(vector))[0]
        other_index = np.where(~np.isnan(vector))[0]
        return miss_index, other_index

    def validate_components(self, coord):
        # Valida que no todas las componentes sean NaN
        if np.isnan(coord).all():
            print("Error: Todas las componentes son NaN.")
            return False
        return True

    def find_mag(self, components):
        # Calcula la magnitud de un vector con componentes válidas
        if components is not None:
            valid_components = [c for c in components if not np.isnan(c)]
            if valid_components:
                return np.sqrt(np.sum(np.array(valid_components) ** 2))
        return np.nan

    def find_miss(self, vector, magn):
        # Encuentra el componente faltante de un vector dado su magnitud
        miss_i, other_i = self.find_index(vector)

        if len(miss_i) != 1 or len(other_i) != 2:
            print("Error: Debe haber exactamente dos componentes conocidas y una desconocida.")
            return

        sum_squares = np.nansum(vector[other_i] ** 2)

        if magn**2 < sum_squares:
                print("Error: Los valores proporcionados no cumplen con la desigualdad triangular.")
                return

        vector[miss_i] = np.sqrt(max(magn**2 - sum_squares, 0))

        return vector

    def find_inter(self,vector,cosdir):
        # Encuentra los índices donde ambos vectores tienen valores numéricos (no NaN)
        indices_con_valores = np.where(~np.isnan(vector) & ~np.isnan(cosdir))[0]
        
        # Verifica si hay intersecciones
        if len(indices_con_valores) == 0:
            return None  # "No hay intersección."
        elif len(indices_con_valores) > 1:
            return indices_con_valores[0] # "Hay más de una intersección, retornando la primera posición."
        else:
            return indices_con_valores[0] # "Hay una intersección."