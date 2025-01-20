import sympy as sp

def Punto2():
    # Definir símbolos
    d, G, Tao_max, L1, L2, T, rEng1, rEng2, a = sp.symbols('d G Tao_max L1 L2 T rEng1 rEng2 a', real=True, positive=True)

    # Elementos geométricos
    rab = 2 * d / 2  # Radio externo de la sección AB
    rbc = d / 2      # Radio externo de la sección BC
    b = 2.5 * d      # Lado del área cuadrada

    # Momento polar de inercia (J) para secciones circulares
    Jab = (1 / 2) * sp.pi * rab**4
    Jbc = (1 / 2) * sp.pi * rbc**4

    # Momento polar de inercia (J) para sección cuadrada
    Jde = (1 / 6) * b**4

    # T resultante por engranajes
    T2 = T * (rEng2 / rEng1)

    # Esfuerzo cortante en áreas circulares del eje 1 en función de T
    tao_ab = (T * rab) / Jab  # Esfuerzo cortante en AB
    tao_bc = (T * rbc) / Jbc  # Esfuerzo cortante en BC

    # Esfuerzo cortante en área cuadrada del eje 2
    tao_de = (T2 * (b / 2)) / Jde

    # Calcular factor de seguridad (FS) dado un material y T aplicado
    FS_ab = Tao_max / tao_ab  # Factor de seguridad en AB
    FS_bc = Tao_max / tao_bc  # Factor de seguridad en BC
    FS_de = Tao_max / tao_de  # Factor de seguridad en DE

    # Ángulo de torsión en cada segmento circular
    theta_ab = (T * L1) / (Jab * G)  # Ángulo de torsión en AB
    theta_bc = (T * L2) / (Jbc * G)  # Ángulo de torsión en BC

    # Ángulo de torsión en segmento cuadrado
    theta_de = (T2 * a) / (Jde * G)  # Ángulo de torsión en DE

    #Angulo de torsion relacionando engranajes
    theta_c = theta_de* (rEng2 / rEng1)

    #Angulo de torsion

    # Resultados
    results = {
        'Momento polar de inercia AB (Jab)': Jab,
        'Momento polar de inercia BC (Jbc)': Jbc,
        'Momento polar de inercia DE (Jde)': Jde,
        'Factor de seguridad en AB (FS_ab)': FS_ab,
        'Factor de seguridad en BC (FS_bc)': FS_bc,
        'Factor de seguridad en DE (FS_de)': FS_de,
        'Esfuerzo cortante en AB (tao_ab)': tao_ab,
        'Esfuerzo cortante en BC (tao_bc)': tao_bc,
        'Esfuerzo cortante en DE (tao_de)': tao_de,
        'Ángulo total de torsión (theta_total)': theta_total
    }

    return results

# Ejecutar la función y mostrar los resultados
resultados = Punto2()
for key, value in resultados.items():
    print(f"{key}: {value}")
