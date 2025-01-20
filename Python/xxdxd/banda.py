import sympy as sp

def ban():
    # Definimos los símbolos
    N, theta = sp.symbols('N theta')
    
    # Constantes
    m = 0.5  # masa (kg)
    v = 1    # velocidad (m/s)
    r = 0.5  # radio (m)
    u = 0.4  # coeficiente de fricción
    g = 9.81 # gravedad (m/s^2)
    
    # Fuerzas y aceleración
    w = m * g  # peso
    an = (v**2) / r  # aceleración centrípeta

    # Ecuaciones
    ecN = sp.Eq(w * sp.sin(theta) - u * N, 0)
    ecT = sp.Eq(w * sp.cos(theta) - N, m * an)
    
    # Resolviendo para N y theta
    N_sol = sp.solve(ecT, N)[0]
    theta_sol = sp.solve(ecN.subs(N, N_sol), theta)
    
    # Convertimos el resultado de theta a grados
    theta_deg = [sp.deg(t.evalf()) for t in theta_sol]
    
    return N_sol, theta_sol, theta_deg

# Ejecutamos la función
N_result, theta_result, theta_degrees = ban()
print(N_result, theta_result, theta_degrees )
