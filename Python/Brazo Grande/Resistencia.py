import math

# --- 1. Parámetros de Entrada (todo en mm y N) ---
b = 20.0             # Base del perfil
h = 40.0             # Altura del perfil
n = 8                # Número de contornos
m_porcentaje = 40.0  # Relleno
P = 80           # Carga deducida (100 N)
L_list = [200.0, 300.0]

D_brida = 18.0       # Diámetro del círculo de agujeros M4
N_tornillos = 6
d_tornillo = 4.0
e_brida = 10.0       # Espesor de la brida

# --- 2. Propiedades del PETG ---
E_petg = 2100.0      # Módulo de Young (MPa)
Sy_petg = 45.0       # Límite elástico a tracción/flexión (MPa)
Tau_petg = 27.0      # Resistencia al corte (MPa)
rho_petg = 1.27 / 1000 # Densidad del PETG en g/mm^3
e_w = 0.42           # Ancho de línea de extrusión 

# --- 3. Propiedades de la Sección ---
t = n * e_w
m = m_porcentaje / 100.0

# Área efectiva (para masa y cortante)
A_total = b * h
A_nucleo = max(b - 2*t, 0) * max(h - 2*t, 0)
A_eff = (A_total - A_nucleo) + (m * A_nucleo)

# Inercia efectiva
I_total = (b * h**3) / 12.0
I_nucleo_y = (max(b - 2*t, 0) * max(h - 2*t, 0)**3) / 12.0
I_eff = (I_total - I_nucleo_y) + (m * I_nucleo_y)

print(f"==================================================")
print(f" PROPIEDADES DE LA SECCIÓN TRANSVERSAL")
print(f"==================================================")
print(f"Inercia Efectiva (I_eff) : {I_eff:.2f} mm^4")
print(f"Área Efectiva (A_eff)    : {A_eff:.2f} mm^2")
print(f"Masa lineal estimada     : {A_eff * rho_petg:.2f} g/mm\n")

# --- 4. Análisis por Distancia ---
for L in L_list:
    # Momentos y Fuerzas
    M_Nmm = P * L
    M_Nm = M_Nmm / 1000.0
    
    # 1. Deflexión y Ángulo en la punta
    deflexion_max = (P * L**3) / (3 * E_petg * I_eff)
    theta_rad = (P * L**2) / (2 * E_petg * I_eff)
    theta_deg = math.degrees(theta_rad)
    
    # 2. Esfuerzos en el Perfil (Flexión y Cortante)
    # Esfuerzo máximo en las fibras exteriores (c = h/2)
    sigma_flector = (M_Nmm * (h / 2.0)) / I_eff
    FS_flexion = Sy_petg / sigma_flector
    
    # Esfuerzo cortante promedio en el perfil
    tau_promedio = P / A_eff
    
    # 3. Esfuerzos en la Brida / Tornillos
    R_brida = D_brida / 2.0
    F_t = (2.0 * M_Nmm) / (N_tornillos * R_brida) 
    
    # Desgarro (Pull-out)
    A_desgarro = math.pi * d_tornillo * e_brida
    tau_arranque = F_t / A_desgarro
    FS_arranque = Tau_petg / tau_arranque
    
    # Aplastamiento (Bearing) por el peso transversal
    V_s = P / N_tornillos
    A_aplastamiento = d_tornillo * e_brida
    sigma_aplastamiento = V_s / A_aplastamiento
    
    # Estimación de masa para el eslabón completo
    masa_total = A_eff * L * rho_petg
    
    print(f"--- RESULTADOS PARA CARGA DE {P}N A L = {L} mm ---")
    print(f"[Cinemática y Dinámica]")
    print(f"  Torque en articulación : {M_Nm:.2f} N·m")
    print(f"  Deformación en punta   : {deflexion_max:.3f} mm")
    print(f"  Desviación angular     : {theta_deg:.2f}° ({theta_rad:.4f} rad)")
    print(f"  Masa del eslabón (aprox): {masa_total:.1f} g")
    
    print(f"\n[Esfuerzos en el Eslabón (PETG)]")
    print(f"  Esfuerzo Flector Máx.  : {sigma_flector:.2f} MPa")
    print(f"  Factor Seg. Flexión    : {FS_flexion:.1f}x (Evita rotura del brazo)")
    print(f"  Cortante transversal   : {tau_promedio:.3f} MPa")
    
    print(f"\n[Esfuerzos en la Brida / Tornillos]")
    print(f"  Fuerza de tracción máx.: {F_t:.2f} N (Agujero superior)")
    print(f"  Esfuerzo de desgarro   : {tau_arranque:.2f} MPa")
    print(f"  Factor Seg. Desgarro   : {FS_arranque:.1f}x (Evita que el tornillo arranque el plástico)")
    print(f"  Esfuerzo aplastamiento : {sigma_aplastamiento:.2f} MPa")
    print(f"--------------------------------------------------\n")