from vectorObject import Vector_Object as vt
from structures import Structures as st
from rigidCalculator import Rigid_Static_Calculator as rsc
from graf import Graphication as graph  

# Crear instancia de Structures
structures = st()

# Agregar vectores de prueba a distArray sin punteros
vector1 = vt(coords=[1, 2, 3])
vector2 = vt(coords=[4, 5, 6])
vector3 = vt(coords=[7, 8, 9])
vector4 = vt(coords=[2, 3, 4])
vector5 = vt(coords=[5, 6, 7])

structures.add_distance(vector1)
structures.add_distance(vector2)
structures.add_distance(vector3)
structures.add_distance(vector4)
structures.add_distance(vector5)

# Agregar vectores de prueba a forceArray con punteros
force1 = vt(coords=[1, 0, 0], next=vector1)
force2 = vt(coords=[0, 1, 0], next=vector2)
force3 = vt(coords=[0, 0, 1], next=vector3)
force4 = vt(coords=[1, 1, 0], next=vector1)
force5 = vt(coords=[0, 1, 1], next=vector3)
force6 = vt(coords=[1, 0, 1], next=vector2)
force7 = vt(coords=[1, -1, 0], next=vector1)
force8 = vt(coords=[0, -1, 1], next=vector3)
force9 = vt(coords=[-1, 0, 1], next=vector2)

structures.add_force(force1)
structures.add_force(force2)
structures.add_force(force3)
structures.add_force(force4)
structures.add_force(force5)
structures.add_force(force6)
structures.add_force(force7)
structures.add_force(force8)
structures.add_force(force9)

# Crear instancia de Rigid_Static_Calculator
calculator = rsc(structures)

# Ejecutar el método clasif
print("Ejecutando clasif()")
calculator.clasif()

print("Calculando totales")
structures.calculate_totals()

# Verificar resultados
print("\nDistArray:")
for dist in structures.distArray:
    print(dist.get_coords())

print("\nForceArray:")
for force in structures.forceArray:
    print(force.get_coords())

print("\nTotalForceArray:")
for force in structures.totalforce:
    print(force.get_coords())

print("\nMomentArray:")
for moment in structures.momentArray:
    print(moment.get_coords())

print("\nTotalMomentArray:")
for moment in structures.totalmoment:
    print(moment.get_coords())

structures.sum_f_m()
print("\nSumas:")
print("Total F:", structures.totalSumForce, "\n")
print("Total M", structures.totalSumMoment, "\n")

# Graficar los resultados
grapher = graph(structures)
grapher.graf(Multpdf= 1/10, Multpdm = 1/12)
