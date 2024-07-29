import numpy as np
class Vector_Object:
    def __init__(self, coords=[np.nan, np.nan, np.nan], angles=[np.nan, np.nan, np.nan], magn=np.nan, position=[0, 0, 0], angle_format='cdir', next=None):
        self.__coords = np.array(coords)
        self.__angles = np.array(angles)
        self.__magn = float(magn)
        self.__position = np.array(position)
        self.angle_format = angle_format
        self.next = next
        self.identifier()

        
        

        
#####################################################################################
    # CRUD Methods

    # Coords
    def get_coords(self, index=None):
        if index is None:
            return self.__coords
        else:
            return self.__coords[index]

    def set_coords(self, new_coords, index=None):
        if index is None:
            self.__coords = np.array(new_coords)
        else:
            self.__coords[index] = new_coords

    # Angles
    def get_angles(self, index=None):
        if index is None:
            return self.__angles
        else:
            return self.__angles[index]

    def set_angles(self, new_angles, index=None):
        if index is None:
            self.__angles = np.array(new_angles)
        else:
            self.__angles[index] = new_angles

    # Magnitude
    def get_magn(self):
        return self.__magn

    def set_magn(self, new_magn):
        self.__magn = float(new_magn)

    # Position
    def get_position(self, index=None):
        if index is None:
            return self.__position
        else:
            return self.__position[index]

    def set_position(self, new_position, index=None):
        if index is None:
            self.__position = np.array(new_position)
        else:
            self.__position[index] = new_position

    # Pointer

    # clear
    def clear(self):
        self.__coords = np.array([np.nan, np.nan, np.nan])
        self.__angles = np.array([np.nan, np.nan, np.nan])
        self.__magn = np.nan
        self.__position = np.array([0, 0, 0])
        self.next = None
#########################################################################################
    # Conversor
    
    def angle_conversor(self):
        if self.angle_format == 'cdir':
            pass  # Si ya está en cosenos directores, no se requiere conversión

        elif self.angle_format == 'rad':
            valid_angles = self.__angles[~np.isnan(self.__angles)]
            if np.all(valid_angles >= 0) and np.all(valid_angles <= 2 * np.pi):
                self.__angles[~np.isnan(self.__angles)] = np.cos(valid_angles)
                self.angle_format = 'cdir'
            else:
                print("Radianes mal implementados")

        elif self.angle_format == 'degrees':
            valid_angles = self.__angles[~np.isnan(self.__angles)]
            if np.all(valid_angles >= 0) and np.all(valid_angles <= 360):
                print("Converting angles from degrees to cosenos directores")
                radians = np.radians(valid_angles)
                self.__angles[~np.isnan(self.__angles)] = np.cos(radians)
                self.angle_format = 'cdir'
            else:
                print("Angulos mal implementados")

        else:
            print("No reconoce el formato del ángulo")

##################################################################################
    # Cases according to the diagram

    def Type0(self): # Complete case
        if np.isclose(self.__magn, np.sqrt(np.sum(self.__coords**2))) and np.isclose(self.__coords / self.__magn, self.__angles).all():
            pass
        else:
            print("Data inconsistency, recalculating...")
            self.__magn = np.nan
            self.__angles = np.array([np.nan, np.nan, np.nan])
            self.Type10()

    def Type1(self): # Only angles are missing        
        calculated_magn = np.sqrt(np.sum(self.__coords**2))
        if not np.isclose(self.__magn, calculated_magn):
            print(f"The current magnitude {self.__magn} is incorrect, recalculating...")
            self.__magn = calculated_magn

        self.__angles = self.__coords / self.__magn
        self.Type0()

    def Type2(self): # Only coordinates are missing
        self.__coords = self.__magn * self.__angles
        self.Type0()

    def Type3(self): # Two coordinates and magnitude
        sum_squares = np.nansum(self.__coords ** 2)
        if self.__magn**2 >= sum_squares:
            last = np.sqrt(self.__magn**2 - sum_squares)
        else:
            print("It is not possible to calculate a missing component with the provided data.")

        nan_index = np.where(np.isnan(self.__coords))[0][0]        
        self.__coords[nan_index] = last
        self.Type1()

    def Type4(self):
        angle_index = np.where(~np.isnan(self.__angles))[0][0]
        self.__coords[angle_index] = self.__magn * self.__angles[angle_index]
        self.__angles[:] = np.nan
        self.Type3()

    def Type5(self): # Two coordinates and an angle
        angle_index = np.where(~np.isnan(self.__angles))[0][0]
        self.__magn = self.__coords[angle_index] / self.__angles[angle_index]
        self.__angles[:] = np.nan
        self.Type3()

    def Type6(self):
        shared_indices = np.where(~np.isnan(self.__angles) & ~np.isnan(self.__coords))[0]
        if len(shared_indices) > 1:
            self.__angles[shared_indices[1]] = np.nan
        elif len(shared_indices) == 1:
            all_angle_indices = np.where(~np.isnan(self.__angles))[0]
            next_angle_index = all_angle_indices[all_angle_indices != shared_indices[0]][0]
            self.__angles[next_angle_index] = np.nan
            self.Type5()

    def Type7(self):
        angle_index = np.where(~np.isnan(self.__angles))[0][0]
        self.__magn = self.__coords[angle_index] / self.__angles[angle_index]
        self.__coords[:] = np.nan
        self.Type2()

    def Type8(self): # Two angles and one coordinate
        angle_index = np.where(~np.isnan(self.__angles))[0][0]
        self.__magn = self.__coords[angle_index] / self.__angles[angle_index]
        self.__coords[:] = np.nan
        self.Type9()

    def Type9(self): # Two angles and one magnitude
        angle_indices = np.where(~np.isnan(self.__angles))[0]
        if len(angle_indices) == 2:
            sum_squares = np.sum(self.__angles[angle_indices] ** 2)
            missing_angle = np.sqrt(1 - sum_squares)
            missing_index = np.setdiff1d([0, 1, 2], angle_indices)[0]
            self.__angles[missing_index] = missing_angle
            self.Type2()

    def Type10(self): # Only three coordinates
        self.__magn = np.sqrt(np.sum(self.__coords ** 2))
        self.Type1()
##############################################################################
    # Identifier
    # Types 6 and 7 are not implemented
    def identifier(self):

        
        self.angle_conversor()
        if np.all(~np.isnan(self.__coords)) and np.all(~np.isnan(self.__angles)) and not np.isnan(self.__magn):
            print("ya esta todo definido")
            self.Type0()
            

        elif not np.isnan(self.__magn):
            nan_count_angles = np.sum(np.isnan(self.__angles))
            nan_count_coords = np.sum(np.isnan(self.__coords))

            if nan_count_angles == 0 and np.all(np.isnan(self.__coords)):
                self.Type2()
            elif nan_count_angles == 1 and np.all(np.isnan(self.__coords)):
                self.Type9()
            elif nan_count_coords == 0 and np.all(np.isnan(self.__angles)):
                self.Type1()
            elif nan_count_coords == 1 and np.all(np.isnan(self.__angles)):
                self.Type3()

            elif nan_count_coords == 2 and nan_count_angles == 2:
                index_coord_nan = np.where(~np.isnan(self.__coords))[0][0]
                index_angle_nan = np.where(~np.isnan(self.__angles))[0][0]
                if index_coord_nan != index_angle_nan:
                    self.Type4()
                else:
                    print("Indeterminación de type 4")
            
        elif np.all(~np.isnan(self.__coords)) and np.all(np.isnan(self.__angles)):
            self.Type10()

        elif np.any(~np.isnan(self.__coords)) and np.any(~np.isnan(self.__angles)):
            index_coords_exist = np.where(~np.isnan(self.__coords))[0]
            index_angles_exist = np.where(~np.isnan(self.__angles))[0]
            coords_nan_count = len(index_coords_exist)
            angles_nan_count = len(index_angles_exist)

            if coords_nan_count == 1 and angles_nan_count == 2:
                if set(np.where(self.__coords)[0]).intersection(set(np.where(self.__angles)[0])):
                    self.Type8()
                else:
                    print("Indeterminación 3")

            elif coords_nan_count == 2 and angles_nan_count == 1:
                if set(np.where(self.__coords)[0]).intersection(set(np.where(self.__angles)[0])):
                    self.Type5()
                else:
                    print("Indeterminación 4")
            else:
                print("Indeterminación")

        else:
            print("Indeterminación, no encontró ningún caso")
