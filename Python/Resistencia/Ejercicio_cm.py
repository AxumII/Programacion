import sympy as sp

def calcular_wd_en_terminos_de_theta():
    # Definir variables simbólicas
    vb, vd, wb, wd, theta = sp.symbols('vb vd wb wd theta')
    md, mb, r, theta_init, k, l = sp.symbols('md mb r theta_init k l')

    # Constantes
    g = 9.81
    Ib = (1/12) * mb * l**2
    Id = (1/2) * md * r**2

    # Ecuación de conservación de energía
    eq1 = (1/2) * mb * g * l * sp.sin(theta_init) + (1/2) * k * l**2 * sp.sin(theta_init)**2 - \
          (1/2) * (mb * vb**2 + Ib * wb**2 + md * vd**2 + Id * wd**2 + mb * g * l * sp.sin(theta) + k * l**2 * sp.sin(theta)**2)

    # Otras ecuaciones del sistema
    eq2 = 0.5 * l * wb - vb
    eq3 = r * wd - vd
    eq4 = vb * sp.sin(theta) - vd

    # Definir el sistema de ecuaciones
    eqs = [eq1, eq2, eq3, eq4]

    # Resolver el sistema para (vb, vd, wb, wd)
    solucion = sp.solve(eqs, (vb, vd, wb, wd))

    # Verificar si la solución es un diccionario antes de extraer wd
    if isinstance(solucion, dict):  
        wd_theta = solucion[wd]  
    elif isinstance(solucion, list) and solucion and isinstance(solucion[0], (tuple, list)):  
        index_wd = (vb, vd, wb, wd).index(wd)  # Obtener el índice de wd
        wd_theta = solucion[0][index_wd]  # Extraer el valor correcto
    else:
        wd_theta = "No se encontró solución"

    print("\n✅ Expresión de wd en términos de θ:")
    sp.pprint(sp.simplify(wd_theta))

# Llamar a la función
calcular_wd_en_terminos_de_theta()
