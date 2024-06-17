import numpy as np

class Vector_Object:
    def __init__(self, coords=[np.nan, np.nan, np.nan], angles=[np.nan, np.nan, np.nan], magn=np.nan, position=[0, 0, 0], next=None):
        self.coords = np.array(coords)
        self.angles = np.array(angles)
        self.magn = float(magn)
        self.position = np.array(position)
        self.next = next
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
            self.coords[index] = np.nan

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

    def read_all_asociates(self):         
        return self.extra_list

    def read_from_extra_list(self, index):
        if index < len(self.extra_list):
            return self.extra_list[index]
        else:
            raise IndexError("Índice fuera de rango.")

    def create_asociates(self, item):       
        self.extra_list.append(item)

    def update_asociates(self, index, new_item):
        if index < len(self.extra_list):
            self.extra_list[index] = new_item
        else:
            raise IndexError("Índice fuera de rango.")

    def delete_asociates(self, index):
        if index < len(self.extra_list):
            del self.extra_list[index]
        else:
            raise IndexError("Índice fuera de rango.")
        
    def clear_list(self):
        self.asociates.clear()

#############################################################

#Identificador
    def identifier(self):
        if np.all(~np.isnan(self.coords)) and np.all(~np.isnan(self.angles)) and not np.isnan(self.magn):
            self.Type0()

        #######################################################################

        elif not np.isnan(self.magn):
            nan_count_angles = np.sum(np.isnan(self.angles))
            nan_count_coords = np.sum(np.isnan(self.coords))

            if nan_count_angles == 3 and np.all(np.isnan(self.coords)):
                self.Type2()
            elif nan_count_angles == 1 and np.all(np.isnan(self.coords)):
                self.Type9()
            elif nan_count_coords == 0 and np.all(np.isnan(self.angles)):
                self.Type1()
            elif nan_count_coords == 1 and np.all(np.isnan(self.angles)):
                self.Type3()

            elif nan_count_coords == 2 and nan_count_angles == 2:
                index_coord_nan = np.where(~np.isnan(self.coords))[0][0]
                index_angle_nan = np.where(~np.isnan(self.angles))[0][0]
                if index_coord_nan != index_angle_nan:
                    self.Type4()
                else:
                    print("indeterminacion de type 4")
            
        #########################################################
        elif np.all(~np.isnan(self.coords)) and np.all(np.isnan(self.angles)):
            self.Type10()

        ##############################################################
        elif np.any(~np.isnan(self.coords)) and np.any(~np.isnan(self.angles)):
            index_coords_exist = np.where(~np.isnan(self.coords))[0]
            index_angles_exist = np.where(~np.isnan(self.angles))[0]
            coords_nan_count = len(index_coords_exist)
            angles_nan_count = len(index_angles_exist)

            if coords_nan_count == 1 and angles_nan_count == 2:
                if set(np.where(self.coords)[0]).intersection(set(np.where(self.angles)[0])):
                    self.Type8()
                else:
                    print("Indeterminación 3")
            elif coords_nan_count == 2 and angles_nan_count == 1:
                if set(np.where(self.coords)[0]).intersection(set(np.where(self.angles)[0])):
                    self.Type5()
                else:
                    print("Indeterminación 4")
            else:
                print("Indeterminación xdxxcdxdxdxdxdd")
        
        else:

            print("Indeterminación, no encontro ningun caso")
            

            
                
    
#############################################################
#Casos de acuerdo al diagrama, provisional
    def Type0(self): #Caso completo
        if np.isclose(self.magn, np.sqrt(np.sum(self.coords**2))) and np.isclose(self.coords / self.magn, self.angles).all():
            #print("Ya tiene el vector completo")
            #print("Coordenadas", self.get_coords(), "\nÁngulos en CosDir", self.get_angles(), "\nMagnitud", self.get_magn(), "\n")
            pass
        else:
            print("Inconsistencia en los datos, recalculando...")
            self.magn = np.nan
            self.angles = np.array([np.nan, np.nan, np.nan])
            self.Type10()

    def Type1(self): #Solo faltan angulos        
        calculated_magn = np.sqrt(np.sum(self.coords**2))
        if not np.isclose(self.magn, calculated_magn):
            print(f"La magnitud actual {self.magn} es incorrecta, recalculando...")
            self.magn = calculated_magn

        self.angles = self.coords / self.magn
        self.Type0()

    def Type2(self): #Solo faltan coordenadas
        self.coords = self.magn * self.angles
        self.Type0()

    def Type3(self):#Dos coord y magnitud
        sum_squares = np.nansum(self.coords ** 2)
        if self.magn**2 >= sum_squares:
            last = np.sqrt(self.magn**2 - sum_squares)
            #print("El faltante ya se hallo")
        else:
            print("No es posible calcular un componente faltante con los datos proporcionados.")
        nan_index = np.where(np.isnan(self.coords))[0][0]        
        # Reemplaza el NaN por el componente faltante calculado
        self.coords[nan_index] = last
        self.Type1()

    def Type4(self):
        # Encontrar el índice del único elemento no-NaN en self.angles
        angle_index = np.where(~np.isnan(self.angles))[0][0]

        # Realizar el cálculo y reemplazar el valor correspondiente en self.coords
        self.coords[angle_index] = self.magn * self.angles[angle_index]
        #print(f"Reemplazo realizado en la posición {angle_index} con el valor {self.coords[angle_index]}")
       
        # Configura todos los elementos de self.angles a NaN
        self.angles[:] = np.nan

        self.Type3()

    def Type5(self):#Dos coord y un angulo
        
        # Encuentra el índice del único elemento no-NaN en self.angles
        angle_index = np.where(~np.isnan(self.angles))[0][0]
        self.magn = self.coords[angle_index] / self.angles[angle_index]

        # Configura todos los elementos de self.angles a NaN
        self.angles[:] = np.nan

        self.Type3()

    def Type6(self):
        # Encuentra los índices donde ambos, ángulos y coordenadas, no son NaN
        shared_indices = np.where(~np.isnan(self.angles) & ~np.isnan(self.coords))[0]
        if len(shared_indices) > 1:
            # Configura el segundo ángulo definido (no el compartido) a NaN si hay más de un índice compartido
            self.angles[shared_indices[1]] = np.nan
        elif len(shared_indices) == 1:
            # Configura el próximo ángulo no NaN a NaN si hay exactamente uno compartido
            all_angle_indices = np.where(~np.isnan(self.angles))[0]
            next_angle_index = all_angle_indices[all_angle_indices != shared_indices[0]][0]
            self.angles[next_angle_index] = np.nan
            self.Type5()

    def Type7(self):
        angle_index = np.where(~np.isnan(self.angles))[0][0]
        self.magn = self.coords[angle_index] / self.angles[angle_index]
        # Configura todas las coordenadas a NaN
        self.coords[:] = np.nan
        self.Type2()

    def Type8(self):#Dos angulos y una coordenada
        # Igual que el type 7 pero con solo 2 angulos
        angle_index = np.where(~np.isnan(self.angles))[0][0]
        self.magn = self.coords[angle_index] / self.angles[angle_index]
        # Configura todas las coordenadas a NaN
        self.coords[:] = np.nan
        self.Type9()

    def Type9(self):#Dos angulos y una magnitud
        # Encuentra los índices de los ángulos no-NaN
        angle_indices = np.where(~np.isnan(self.angles))[0]
        if len(angle_indices) == 2:
            # Calcula el ángulo faltante usando la propiedad de que la suma de los cuadrados es 1
            sum_squares = np.sum(self.angles[angle_indices] ** 2)
            missing_angle = np.sqrt(1 - sum_squares)
            missing_index = np.setdiff1d([0, 1, 2], angle_indices)[0]
            self.angles[missing_index] = missing_angle

            self.Type2()

    def Type10(self):#Solo tres coordenadas
        self.magn = np.sqrt(np.sum(self.coords ** 2))
        self.Type1()








#########################################################################################
"""
print("Vector 0")
v0 = Vector_Object(coords=[3, 4, 0], angles=[0.6, 0.8, 0], magn=5)
print("Vector 02")
v02 = Vector_Object(coords=[3, 10, 0], angles=[0.6, 0.8, 0], magn=5)
print("Vector 1")


v1 = Vector_Object(coords=[3, 4, 7], magn=15)
print(v1.get_coords, v1.get_angles, v1.get_magn)


print("XD")

print("Vector 3")
v3 = Vector_Object(coords=[0.5, 0.14, np.nan], magn=30)



print("Vector 4")
v4 = Vector_Object(coords=[5,np.nan, np.nan], angles= [np.nan, 0.4, np.nan], magn= 14)


print("Vector 4false")
v4false = v4 = Vector_Object(coords=[5,np.nan, np.nan], angles= [0.2, np.nan, np.nan], magn= 14)



print("Vector 5")
v5 = Vector_Object(coords=[np.nan, 4 , 7], angles= [np.nan, np.nan, 0.23])


print("Vector 8")
v8 = Vector_Object(coords= [7, np.nan, np.nan], angles = [0.2, 0.4, np.nan])


print("Vector 9")
v9 = Vector_Object(angles = [np.nan, 0.2, 0.4], magn= 10)

print("Vector 10")
v10 = Vector_Object(coords = [3,4,5])

"""


"""


print("Prueba fallo 1")
v11 = Vector_Object()
#corregir, no hay nsercion

#poner exception 
print("Prueba fallo 2")
v12 = Vector_Object(coords = "XDXD")


print("Prueba fallo 3")
v12 = Vector_Object(coords=[3, 4, 7], magn=0)

#corregir el if por suma y poner un corrector 
print("Prueba fallo 4")
v12 = Vector_Object(angles=[3, 4, 7], magn=4)

print("Prueba fallo 5")
v12 = Vector_Object(angles=[3, 4, 7], magn=0)

print("Prueba fallo 6")
v12 = Vector_Object(None)


print("Prueba fallo 7")
v12 = Vector_Object(coords=[3, 4, None], magn=4)

"""