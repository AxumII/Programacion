import numpy as np
from vectorObject import Vector_Object as vt
from rigidStaticCalculator import RigidStaticCalculator as RSC
from wrench import Wrench as wr
from graphication import Graphication as graf


#x,y,z, en el libro seria i,k,j
#Ejercicio 3.140

rsc = RSC()

var = 1
P = 1
A = vt(coords=[0 , 18*var, 0])
B = vt(coords=[0 , 0 , 24*var])
C = vt(coords=[15*var, 0, 0])
D = vt(coords=[0 , 0 , 20*var])
E = vt(coords=[-9*var, -12*var, 0 ])


rsc.add_distance(A)
rsc.add_distance(C)
rsc.add_distance(E)


dir1 = vt(coords=np.subtract(A.get_coords(), B.get_coords()))  # A-B
dir2 = vt(coords=np.subtract(C.get_coords(), D.get_coords()))  # C-D
dir3 = vt(coords=np.subtract(E.get_coords(), D.get_coords()))  # E-D



f1 = vt(coords= np.array(dir1.get_angles()*P), next = A )
f2 = vt(coords= np.array(dir2.get_angles()*P), next = C )
f3 = vt(coords= np.array(dir3.get_angles()*P), next = E )

rsc.add_force(f1)
rsc.add_force(f2)
rsc.add_force(f3)

rsc.calculate_moments()

print("Mostrar Distancias",rsc.read_all_distances())
print("Mostrar Fuerzas",rsc.read_all_forces())
print("Mostrar Momentoss",rsc.read_all_moments())



print("Fuerza Total",rsc.totalF)
print("Momento Total",rsc.totalM)


llave = wr(totalF = rsc.totalF, totalM = rsc.totalM)
print("II momento", llave.IIMoment)
print("T momento", llave.TMoment)
print("Posiciones",llave.positions)
print("Posiciones Verificadas", llave.valid_positions)

g = graf(rsc,llave,Ffs = 1.5, Fms = 0.5)
g.graf_dfm()
g.graf_wr()

