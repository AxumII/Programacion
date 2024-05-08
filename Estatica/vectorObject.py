import numpy as np

class Vector_Object:
    def __init__(self, coords=[np.nan, np.nan, np.nan], angles=[np.nan, np.nan, np.nan], magn=np.nan, position=[0, 0, 0]):
        self.coords = np.array(coords)
        self.angles = np.array(angles)
        self.magn = float(magn)
        self.position = np.array(position)
        self.identifier()


#########################################################
#CRUD
    def get_coords(self, index=None):
        if index is None:
            return self.coords
        else:
            return self.coords[index]

    def set_coords(self, new_coords, index=None):
        if index is None:
            self.coords = np.array(new_coords)
        else:
            self.coords[index] = new_coords

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

    def del_coords(self, index=None):
        if index is None:
            self.coords = np.array([np.nan, np.nan, np.nan])
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
#############################################################

#Identificador
    def identifier(self):
        if np.all(~np.isnan(self.coords)) and np.all(~np.isnan(self.angles)) and not np.isnan(self.magn):
            self.Type0()
            #########################
        elif not np.isnan(self.magn):
            nan_count_angles = np.sum(np.isnan(self.angles))
            nan_count_coords = np.sum(np.isnan(self.coords))

            if nan_count_angles == 3 and np.all(np.isnan(self.coords)):
                self.Type2()
            elif nan_count_angles == 2 and np.all(np.isnan(self.coords)):
                self.Type9()
            elif nan_count_coords == 3 and np.all(np.isnan(self.angles)):
                self.Type1()
            elif nan_count_coords == 2 and np.all(np.isnan(self.angles)):
                self.Type3()
            elif nan_count_coords == 1 and nan_count_angles == 1:
                index_coord_nan = np.where(np.isnan(self.coords))[0][0]
                index_angle_nan = np.where(np.isnan(self.angles))[0][0]
                if index_coord_nan != index_angle_nan:
                    self.Type4()
                else:
                    print("indeterminacion")
            else:
                print("indeterminacion")
            #########################################################
        if np.all(~np.isnan(self.coords)) and np.all(np.isnan(self.angles)):
            self.Type10()
        ##############################################################
        elif np.all(~np.isnan(self.coords)) and np.all(~np.isnan(self.angles)):
            index_coords_nan = np.where(np.isnan(self.coords))[0]
            index_angles_nan = np.where(np.isnan(self.angles))[0]
            coords_nan_count = len(index_coords_nan)
            angles_nan_count = len(index_angles_nan)

            if coords_nan_count == 1 and angles_nan_count == 2:
                if set(np.where(self.coords)[0]).intersection(set(np.where(self.angles)[0])):
                    self.Type8()
                else:
                    print("Indeterminación")
            elif coords_nan_count == 2 and angles_nan_count == 1:
                if set(np.where(self.coords)[0]).intersection(set(np.where(self.angles)[0])):
                    self.Type5()
                else:
                    print("Indeterminación")
            elif coords_nan_count == 1 and angles_nan_count == 3:
                self.Type7()
            elif coords_nan_count == 2 and angles_nan_count == 2:
                self.Type6()
            else:
                print("Indeterminación")
        else:
            print("Indeterminación")
            

            
                
    
#############################################################
#Casos de acuerdo al diagrama, provisional
    def Type0(self):
        print("Type1 Operation Executed")

    def Type1(self):
        print("Type1 Operation Executed")

    def Type2(self):
        print("Type2 Operation Executed")

    def Type3(self):
        print("Type3 Operation Executed")

    def Type4(self):
        print("Type4 Operation Executed")

    def Type5(self):
        print("Type5 Operation Executed")

    def Type6(self):
        print("Type6 Operation Executed")

    def Type7(self):
        print("Type7 Operation Executed")

    def Type8(self):
        print("Type8 Operation Executed")

    def Type9(self):
        print("Type9 Operation Executed")

    def Type10(self):
        print("Type10 Operation Executed")




# Ejemplo de uso:
vector_obj = Vector_Object([1, 2, 3], [45, 45, 45], 5.0)
print("Coordenada específica (índice 1):", vector_obj.get_coords(1))
vector_obj.set_coords(10, 1)
print("Coordenada actualizada (índice 1):", vector_obj.get_coords(1))
vector_obj.del_coords(1)
print("Coordenada después de eliminar (índice 1):", vector_obj.get_coords(1))

