import numpy as np
from vectorObject import Vector_Object as vt
from rigidStaticCalculator import RigidStaticCalculator as RSC
from wrench import Wrench as wr
from graphication import Graphication as graf

# Test VectorObject de casos
"""
# Caso 0: Completo
coords0 = [1, 1, 1]
angles0 = [np.sqrt(1/3), np.sqrt(1/3), np.sqrt(1/3)]
magn0 = np.sqrt(3)
position0 = [0, 0, 0]
angle_format0 = 'cdir'

vector0 = vt(coords=coords0, angles=angles0, magn=magn0, position=position0, angle_format=angle_format0)
print("Vector 0 - Caso Completo")
print("Coords:", vector0.get_coords())
print("Angles:", vector0.get_angles())
print("Magnitude:", vector0.get_magn())
print("Position:", vector0.get_position())
print()

# Caso 1: Solo faltan ángulos
coords1 = [1, 1, 1]
angles1 = [np.nan, np.nan, np.nan]
magn1 = np.sqrt(3)
position1 = [0, 0, 0]
angle_format1 = 'cdir'

vector1 = vt(coords=coords1, angles=angles1, magn=magn1, position=position1, angle_format=angle_format1)
print("Vector 1 - Solo faltan ángulos")
print("Coords:", vector1.get_coords())
print("Angles:", vector1.get_angles())
print("Magnitude:", vector1.get_magn())
print("Position:", vector1.get_position())
print()

# Caso 2: Solo faltan coordenadas
coords2 = [np.nan, np.nan, np.nan]
angles2 = [0.1, 0.5, 0.4]
magn2 = 10
position2 = [0, 0, 0]
angle_format2 = 'cdir'

vector2 = vt(coords=coords2, angles=angles2, magn=magn2, position=position2, angle_format=angle_format2)
print("Vector 2 - Solo faltan coordenadas")
print("Coords:", vector2.get_coords())
print("Angles:", vector2.get_angles())
print("Magnitude:", vector2.get_magn())
print("Position:", vector2.get_position())
print()

# Caso 3: Dos coordenadas y magnitud
coords3 = [2, 10, np.nan]
angles3 = [np.nan, np.nan, np.nan]
magn3 = 15
position3 = [0, 0, 0]
angle_format3 = 'cdir'

vector3 = vt(coords=coords3, angles=angles3, magn=magn3, position=position3, angle_format=angle_format3)
print("Vector 3 - Dos coordenadas y magnitud")
print("Coords:", vector3.get_coords())
print("Angles:", vector3.get_angles())
print("Magnitude:", vector3.get_magn())
print("Position:", vector3.get_position())
print()

# Caso 4: Angulo, coordenada y Magnitud
coords4 = [4, np.nan, np.nan]
angles4 = [np.nan, 0.25, np.nan]
magn4 = 7
position4 = [0, 0, 0]
angle_format4 = 'cdir'

vector4 = vt(coords=coords4, angles=angles4, magn=magn4, position=position4, angle_format=angle_format4)
print("Vector 4 - Ángulo y coordenada")
print("Coords:", vector4.get_coords())
print("Angles:", vector4.get_angles())
print("Magnitude:", vector4.get_magn())
print("Position:", vector4.get_position())
print()

# Caso 5: Dos coordenadas y un ángulo
coords5 = [1, 3, np.nan]
angles5 = [0.25, np.nan, np.nan]
magn5 = np.nan
position5 = [0, 0, 0]
angle_format5 = 'cdir'

vector5 = vt(coords=coords5, angles=angles5, magn=magn5, position=position5, angle_format=angle_format5)
print("Vector 5 - Dos coordenadas y un ángulo")
print("Coords:", vector5.get_coords())
print("Angles:", vector5.get_angles())
print("Magnitude:", vector5.get_magn())
print("Position:", vector5.get_position())
print()

# Caso 8: Dos ángulos y una coordenada
coords8 = [1, np.nan, np.nan]
angles8 = [0.25, 0.5, np.nan]
magn8 = np.nan
position8 = [0, 0, 0]
angle_format8 = 'cdir'

vector8 = vt(coords=coords8, angles=angles8, magn=magn8, position=position8, angle_format=angle_format8)
print("Vector 8 - Dos ángulos y una coordenada")
print("Coords:", vector8.get_coords())
print("Angles:", vector8.get_angles())
print("Magnitude:", vector8.get_magn())
print("Position:", vector8.get_position())
print()

# Caso 9: Dos ángulos y magnitud
coords9 = [np.nan, np.nan, np.nan]
angles9 = [0.25, 0.25, np.nan]
magn9 = 10
position9 = [0, 0, 0]
angle_format9 = 'cdir'

vector9 = vt(coords=coords9, angles=angles9, magn=magn9, position=position9, angle_format=angle_format9)
print("Vector 9 - Un ángulo y todas las coordenadas son NaN")
print("Coords:", vector9.get_coords())
print("Angles:", vector9.get_angles())
print("Magnitude:", vector9.get_magn())
print("Position:", vector9.get_position())
print()

# Caso 10: Todas las coordenadas definidas y los ángulos son NaN
coords10 = [3,4,12]
angles10 = [np.nan, np.nan, np.nan]
magn10 = np.nan
position10 = [0, 0, 0]
angle_format10 = 'cdir'

vector10 = vt(coords=coords10, angles=angles10, magn=magn10, position=position10, angle_format=angle_format10)
print("Vector 10 - Todas las coordenadas definidas y los ángulos son NaN")
print("Coords:", vector10.get_coords())
print("Angles:", vector10.get_angles())
print("Magnitude:", vector10.get_magn())
print("Position:", vector10.get_position())
print()
"""
####################################################################################
#Test Vector Object de errores

"""



#Indet Type 8 (2 angulos y 1 coord no intersecantes)
coords_indet = [3, np.nan, np.nan]
angles_indet = [np.nan,0.2, 0.3]
magn_indet = np.nan
position_indet = [0, 0, 0]
angle_format_indet = 'cdir'

vector_indet = vt(coords=coords_indet, angles=angles_indet, magn=magn_indet, position=position_indet, angle_format=angle_format_indet)
print("Vector Indeterminado")
print("Coords:", vector_indet.get_coords())
print("Angles:", vector_indet.get_angles())
print("Magnitude:", vector_indet.get_magn())
print("Position:", vector_indet.get_position())
print()


#Indet Type 5 (1 angulo y 2 coord no intersecantes)
coords_indet = [np.nan, 3, 4]
angles_indet = [0.8, np.nan, np.nan]
magn_indet = np.nan
position_indet = [0, 0, 0]
angle_format_indet = 'cdir'

vector_indet = vt(coords=coords_indet, angles=angles_indet, magn=magn_indet, position=position_indet, angle_format=angle_format_indet)
print("Vector Indeterminado")
print("Coords:", vector_indet.get_coords())
print("Angles:", vector_indet.get_angles())
print("Magnitude:", vector_indet.get_magn())
print("Position:", vector_indet.get_position())
print()

#Indet Type 4 (1 magn, 1  coord y 1 angulo, coincidentes)
coords_indet = [1, np.nan, np.nan]
angles_indet = [0.5, np.nan, np.nan]
magn_indet = 4
position_indet = [0, 0, 0]
angle_format_indet = 'cdir'

vector_indet = vt(coords=coords_indet, angles=angles_indet, magn=magn_indet, position=position_indet, angle_format=angle_format_indet)
print("Vector Indeterminado")
print("Coords:", vector_indet.get_coords())
print("Angles:", vector_indet.get_angles())
print("Magnitude:", vector_indet.get_magn())
print("Position:", vector_indet.get_position())
print()

# Conversor implementa: Probando la conversión automática a cosenos directores
coords_conv = [np.nan, np.nan, np.nan]
angles_conv = [60, 50, np.nan]
magn_conv = 7
position_conv = [0, 0, 0]
angle_format_conv = 'degrees'

vector_conv = vt(coords=coords_conv, angles=angles_conv, magn=magn_conv, position=position_conv, angle_format=angle_format_conv)
print("Vector Conversor (de grados a cosenos directores)")
print("Coords:", vector_conv.get_coords())
print("Angles:", vector_conv.get_angles())
print("Magnitude:", vector_conv.get_magn())
print("Position:", vector_conv.get_position())
print()

# Conversor implementa: Probando la conversión automática de radianes a cosenos directores
coords_conv2 = [np.nan, np.nan, np.nan]
angles_conv2 = [np.pi / 4, np.nan , 1]
magn_conv2 = 10
position_conv2 = [0, 0, 0]
angle_format_conv2 = 'rad'

vector_conv2 = vt(coords=coords_conv2, angles=angles_conv2, magn=magn_conv2, position=position_conv2, angle_format=angle_format_conv2)
print("Vector Conversor (de radianes a cosenos directores)")
print("Coords:", vector_conv2.get_coords())
print("Angles:", vector_conv2.get_angles())
print("Magnitude:", vector_conv2.get_magn())
print("Position:", vector_conv2.get_position())
print()
"""


# Test RSC

# Create instance of RSC
rsc = RSC()

# Definición de las variables para d1
coordsd1 = [3, 4, 12]
# Llamada a la función vt para d1
d1 = vt(coords=coordsd1)

# Definición de las variables para d2
coordsd2 = [4,-5,20]
# Llamada a la función vt para d2
d2 = vt(coords=coordsd2)

#######################################################################

# Definición de las variables para f1
coordsf1 = [9,2,-6]
# Llamada a la función vt para f1
f1 = vt(coords=coordsf1, next = d1)

# Definición de las variables para f2
coordsf2 = [1,-12,-12]
# Llamada a la función vt para f2
f2 = vt(coords=coordsf2, next = d1)

# Definición de las variables para f3
coordsf3 = [8,9,12]
# Llamada a la función vt para f3
f3 = vt(coords=coordsf3, next = d2)

####################################################################################
# Definición de las variables para m1
coordsm1 = [13,13,13]
# Llamada a la función vt para m1
m1 = vt(coords=coordsm1)
#####################################################################################################
#Variable inutil de prueba
xd = vt(coords = [1000,1000,1000])


#########################################################################
rsc.add_distance(d1)
rsc.add_distance(d2)

rsc.add_distance(vt(coords = [-7,0,0]))

rsc.add_force(f1)
rsc.add_force(f2)
rsc.add_force(f3)

rsc.add_moment(m1)

print("Mostrar Distancias",rsc.read_all_distances())
print("Mostrar Fuerzas",rsc.read_all_forces())
print("Mostrar Momentoss",rsc.read_all_moments())
"""
rsc.add_distance(xd)
rsc.add_force(xd)
rsc.add_moment(xd)

print("Mostrar Distancias",rsc.read_all_distances())
print("Mostrar Fuerzas",rsc.read_all_forces())
print("Mostrar Momentoss",rsc.read_all_moments())

rsc.delete_distance(2)
rsc.delete_force(3)
rsc.delete_moment(1)

print("Mostrar Distancias",rsc.read_all_distances())
print("Mostrar Fuerzas",rsc.read_all_forces())
print("Mostrar Momentoss",rsc.read_all_moments())
"""

rsc.calculate_moments()

print("Fuerza Total",rsc.totalF)
print("Momento Total",rsc.totalM)

print("Mostrar Distancias",rsc.read_all_distances())
print("Mostrar Fuerzas",rsc.read_all_forces())
print("Mostrar Momentoss",rsc.read_all_moments())

###########################################################################
#Test Wrench

llave = wr(totalF = rsc.totalF, totalM = rsc.totalM)
print("II momento", llave.IIMoment)
print("T momento", llave.TMoment)
print("Posiciones",llave.positions)
print("Posiciones Verificadas", llave.valid_positions)

###########################################################################
#Test graficacion

g = graf(rsc,llave)
print("promedios", g.avg())
print("max_min", g.max_min())
g.graf_dfm()
g.graf_wr()


   
    

