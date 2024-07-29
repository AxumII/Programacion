import numpy as np
from structures import Structures as st
from vectorObject import Vector_Object as vt
from wrench import Wrench as wr

# Ejemplo de inicialización de Structures con vectores de muestra
v1 = vt(coords=[[32, 36, 14]])
v2 = vt(coords=[[17, 0, 18]])
v3 = vt(coords=[[22, 25, 17]])
v4 = vt(coords=[[31, 35, 11]])
v5 = vt(coords=[[28, 14, 21]])
v6 = vt(coords=[[35, 23, 36]])
v7 = vt(coords=[[ 7, 22, 18]])
v8 = vt(coords=[[27, 14, 13]])
v9 = vt(coords=[[7, 1, 37]])

depot = st()
depot.add_distance(v1)
depot.add_distance(v2)
depot.add_distance(v3)
depot.add_force(v4)
depot.add_force(v5)
depot.add_force(v6)
depot.add_force(v7)
depot.add_moment(v8)
depot.add_moment(v9)

print(depot.read_all_distances())
print(depot.read_all_forces())
print(depot.read_all_moments())


depot.delete_distance(1)
depot.delete_force(3)
depot.delete_moment(0)

print("aca leo el 0 y el 1, deberia solo mostrar el 0")
print(depot.read_distance(0))
print(depot.read_distance(1))

print(depot.read_all_distances())
print(depot.read_all_forces())
print(depot.read_all_moments())

depot.sum_f_m()

print("Sumas")
print(depot.totalForces, depot.totalMoments)



depot.clear_distances()
depot.clear_forces()
depot.clear_moments()

print(depot.read_all_distances())
print(depot.read_all_forces())
print(depot.read_all_moments())



examples = [
    (np.array([3, 4, 5]), np.array([0, 12, -16])),
    (np.array([1, 2, 3]), np.array([7, -3, 2])),
    (np.array([2, 5, 4]), np.array([1, -2, 3])),
    (np.array([0, 1, 0]), np.array([0, 0, 10])),
]

print("inicia WR")
# Ejecutando cada ejemplo y recopilando resultados
for i, (F, M) in enumerate(examples, 1):
    wrench = wr(F, M)
    print(f"Ejemplo {i} - Fuerza: {F}, Momento: {M}")
    positions = wrench.positions
    print(f"Posiciones Calculadas: {positions}")
    valid_positions = wrench.verify_positions()  # Asegúrate de invocar el método con paréntesis
    print("Momento T, objetivo ",wrench.TMoment, "\n")
    print(f"Posiciones Validadas: {valid_positions}\n")