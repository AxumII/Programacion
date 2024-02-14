import numpy as np

# Define una función para encontrar la posición de intersección
def encontrar_interseccion(v1, v2):
    # Encuentra los índices donde ambos vectores tienen valores numéricos (no NaN)
    indices_con_valores = np.where(~np.isnan(v1) & ~np.isnan(v2))[0]
    
    # Verifica si hay intersecciones
    if len(indices_con_valores) == 0:
        return None, "No hay intersección."
    elif len(indices_con_valores) > 1:
        return indices_con_valores[0], "Hay más de una intersección, retornando la primera posición."
    else:
        return indices_con_valores[0], "Hay una intersección."

# Ejemplo 1
v1 = np.array([2, np.nan, 3])
v2 = np.array([np.nan, np.nan, 5])
posicion, mensaje = encontrar_interseccion(v1, v2)
print(f"Ejemplo 1: Posición = {posicion}, Mensaje = {mensaje}")

# Ejemplo 2
v1 = np.array([np.nan, 7, np.nan])
v2 = np.array([np.nan, 6, np.nan])
posicion, mensaje = encontrar_interseccion(v1, v2)
print(f"Ejemplo 2: Posición = {posicion}, Mensaje = {mensaje}")
