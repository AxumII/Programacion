import numpy as np

class Vector_Object:
    def __init__(self, coord=[np.nan, np.nan, np.nan], angles=[np.nan, np.nan, np.nan], magn=np.nan, position=[0, 0, 0]):
        self.coord = np.array(coord)
        self.angles = np.array(angles)
        self.magn = float(magn)
        self.position = np.array(position)

    def get_coord(self, index=None):
        if index is None:
            return self.coord
        else:
            return self.coord[index]

    def set_coord(self, new_coord, index=None):
        if index is None:
            self.coord = np.array(new_coord)
        else:
            self.coord[index] = new_coord

    def get_angles(self, index=None):
        if index is None:
            return self.angles
        else:
            return self.angles[index]

    def set_angles(self, new_angles, index=None):
        if index is None:
            self.angles = np.array(new_angles)
        else:
            self.angles[index] = new_angles

    def get_magn(self):
        return self.magn

    def set_magn(self, new_magn):
        self.magn = float(new_magn)

    def get_position(self, index=None):
        if index is None:
            return self.position
        else:
            return self.position[index]

    def set_position(self, new_position, index=None):
        if index is None:
            self.position = np.array(new_position)
        else:
            self.position[index] = new_position

    def del_coord(self, index=None):
        if index is None:
            self.coord = np.array([np.nan, np.nan, np.nan])
        else:
            self.coord[index] = np.nan

    def del_angles(self, index=None):
        if index is None:
            self.angles = np.array([np.nan, np.nan, np.nan])
        else:
            self.angles[index] = np.nan

    def del_position(self, index=None):
        if index is None:
            self.position = np.array([np.nan, np.nan, np.nan])
        else:
            self.position[index] = np.nan






# Ejemplo de uso:
vector_obj = Vector_Object([1, 2, 3], [45, 45, 45], 5.0)
print("Coordenada específica (índice 1):", vector_obj.get_coord(1))
vector_obj.set_coord(10, 1)
print("Coordenada actualizada (índice 1):", vector_obj.get_coord(1))
vector_obj.del_coord(1)
print("Coordenada después de eliminar (índice 1):", vector_obj.get_coord(1))

