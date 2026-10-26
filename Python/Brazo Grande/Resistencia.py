import math
import numpy as np
import matplotlib.pyplot as plt

# --- 1. Parámetros de Entrada (todo en mm y N) ---
b = 20.0             # Base del perfil
h = 40.0             # Altura del perfil
n = 8                # Número de contornos
m_porcentaje = 40.0  # Relleno
P = 80               # Carga deducida (N)
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

# --- Preparación de Gráficas ---
plt.style.use('seaborn-v0_8-darkgrid')
fig, axs = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle('Análisis Estructural de Eslabón (PETG)', fontsize=16, fontweight='bold')

fs_flexion_list = []
fs_arranque_list = []

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
    sigma_flector = (M_Nmm * (h / 2.0)) / I_eff
    FS_flexion = Sy_petg / sigma_flector
    tau_promedio = P / A_eff
    
    # 3. Esfuerzos en la Brida / Tornillos
    R_brida = D_brida / 2.0
    F_t = (2.0 * M_Nmm) / (N_tornillos * R_brida) 
    
    A_desgarro = math.pi * d_tornillo * e_brida
    tau_arranque = F_t / A_desgarro
    FS_arranque = Tau_petg / tau_arranque
    
    V_s = P / N_tornillos
    A_aplastamiento = d_tornillo * e_brida
    sigma_aplastamiento = V_s / A_aplastamiento
    
    masa_total = A_eff * L * rho_petg
    
    # Guardar FS para la gráfica de barras
    fs_flexion_list.append(FS_flexion)
    fs_arranque_list.append(FS_arranque)
    
    # --- Datos para Gráficas ---
    x_vals = np.linspace(0, L, 100)
    
    # Ecuación de deflexión para viga empotrada: y(x) = (P*x^2 * (3L - x)) / (6*E*I)
    y_vals = (P * x_vals**2 * (3*L - x_vals)) / (6 * E_petg * I_eff)
    axs[0].plot(x_vals, -y_vals, linewidth=2, label=f'Carga en L={L}mm')
    
    # Ecuación de momento flector: M(x) = P*(L - x)
    M_vals = P * (L - x_vals) / 1000.0 # Convertido a N.m
    axs[1].plot(x_vals, M_vals, linewidth=2, label=f'Carga en L={L}mm')
    
    # --- Consola ---
    print(f"--- RESULTADOS PARA CARGA DE {P}N A L = {L} mm ---")
    print(f"[Cinemática y Dinámica]")
    print(f"  Torque en articulación : {M_Nm:.2f} N·m")
    print(f"  Deformación en punta   : {deflexion_max:.3f} mm")
    print(f"  Desviación angular     : {theta_deg:.2f}° ({theta_rad:.4f} rad)")
    print(f"  Masa del eslabón       : {masa_total:.1f} g")
    print(f"\n[Esfuerzos en el Eslabón (PETG)]")
    print(f"  Esfuerzo Flector Máx.  : {sigma_flector:.2f} MPa")
    print(f"  Factor Seg. Flexión    : {FS_flexion:.1f}x")
    print(f"\n[Esfuerzos en la Brida / Tornillos]")
    print(f"  Esfuerzo de desgarro   : {tau_arranque:.2f} MPa")
    print(f"  Factor Seg. Desgarro   : {FS_arranque:.1f}x")
    print(f"--------------------------------------------------\n")

# --- Configuración de Subplot 1: Deflexión ---
axs[0].set_title('Perfil de Deformación')
axs[0].set_xlabel('Distancia desde la brida (mm)')
axs[0].set_ylabel('Deflexión (mm)')
axs[0].axhline(0, color='black', linewidth=1)
axs[0].legend()

# --- Configuración de Subplot 2: Momento Flector ---
axs[1].set_title('Diagrama de Momento Flector')
axs[1].set_xlabel('Distancia desde la brida (mm)')
axs[1].set_ylabel('Momento Flector (N·m)')
axs[1].axhline(0, color='black', linewidth=1)
axs[1].legend()

# --- Configuración de Subplot 3: Factores de Seguridad ---
bar_width = 0.35
index = np.arange(len(L_list))

axs[2].bar(index, fs_flexion_list, bar_width, label='Flexión Eslabón', color='#2ca02c')
axs[2].bar(index + bar_width, fs_arranque_list, bar_width, label='Desgarro Brida', color='#d62728')

axs[2].set_title('Factores de Seguridad (FS)')
axs[2].set_xlabel('Longitud del Eslabón')
axs[2].set_ylabel('Factor de Seguridad (x veces)')
axs[2].set_xticks(index + bar_width / 2)
axs[2].set_xticklabels([f'{L} mm' for L in L_list])
axs[2].axhline(1, color='red', linestyle='--', linewidth=1.5, label='Límite de Fallo (FS=1)')
axs[2].legend()

plt.tight_layout()
plt.show()