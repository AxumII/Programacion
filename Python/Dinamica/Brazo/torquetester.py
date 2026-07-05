import numpy as np
import matplotlib.pyplot as plt

def analizar_torque_motor():
    # ==========================================
    # 1. PARÁMETROS DE ENTRADA (¡Modifícalos aquí!)
    # ==========================================
    torque_motor_kgcm = 21   # Torque nominal de tu motor en kg·cm
    aceleracion_angular = 2  # Aceleración deseada en rad/s^2
    
    # Define las masas adicionales en la barra. 
    # Formato: (masa_en_kg, distancia_al_eje_en_metros)
    pesos = [
        (0.0, 0.10),
        (0.0, 0.15),
        (0.0, 0.20),
        (0.0, 0.25),
        (0.0, 0.30),
        (0.0, 0.35),
        #(210/1000, 0.40) # Peso: 128 g a 40 cm del eje
    ]
    
    gravedad = 9.81  # m/s^2
    
    # --- PARÁMETROS DE LA BARRA DE MDF ---
    largo_m = 0.448
    ancho_m = 0.0055
    alto_m = 0.0315
    densidad_mdf = 700  # Densidad promedio del MDF en kg/m^3
    eje_m = 0.018       # Distancia del eje a un extremo (brazo corto en m)
    
    # ==========================================
    # 2. CONVERSIONES Y CÁLCULOS
    # ==========================================
    # Conversión: 1 kg·cm = 0.0980665 N·m
    torque_motor_nm = torque_motor_kgcm * 0.0980665
    
    # --- CÁLCULOS FÍSICOS DE LA PROPIA BARRA ---
    volumen_barra = largo_m * ancho_m * alto_m
    masa_total_barra = volumen_barra * densidad_mdf
    
    largo_brazo_1 = eje_m               # Brazo corto (0.018 m)
    largo_brazo_2 = largo_m - eje_m     # Brazo largo (0.430 m)
    
    masa_brazo_1 = masa_total_barra * (largo_brazo_1 / largo_m)
    masa_brazo_2 = masa_total_barra * (largo_brazo_2 / largo_m)
    
    # Torque estático de la barra 
    # (El centro de gravedad de cada brazo está a la mitad de su longitud)
    # El brazo largo suma al torque a vencer, el corto resta porque actúa como contrapeso.
    torque_estatico_barra = (masa_brazo_2 * gravedad * (largo_brazo_2 / 2)) - (masa_brazo_1 * gravedad * (largo_brazo_1 / 2))
    
    # Inercia de la barra (rotación en el eje) = 1/3 * masa * Largo^2 para cada brazo
    inercia_barra = (1/3 * masa_brazo_1 * largo_brazo_1**2) + (1/3 * masa_brazo_2 * largo_brazo_2**2)
    
    # --- CÁLCULOS TOTALES (BARRA + PESOS) ---
    torque_estatico_nm = torque_estatico_barra
    inercia_total = inercia_barra
    
    for masa, radio in pesos:
        torque_estatico_nm += masa * gravedad * radio
        inercia_total += masa * (radio ** 2)
        
    # T_dinamico = Inercia * Aceleracion Angular
    torque_dinamico_nm = inercia_total * aceleracion_angular
    
    # Torque Total Requerido
    torque_total_nm = torque_estatico_nm + torque_dinamico_nm
    
    # Porcentaje de uso y Factor de Seguridad (FS)
    if torque_motor_nm > 0:
        porcentaje_uso = (torque_total_nm / torque_motor_nm) * 100
    else:
        porcentaje_uso = float('inf')
        
    fs = torque_motor_nm / torque_total_nm if torque_total_nm > 0 else 0
    
    # ==========================================
    # 3. REPORTE EN CONSOLA
    # ==========================================
    print("=" * 40)
    print(" ANÁLISIS DE CARGA DEL MOTOR CON BARRA MDF")
    print("=" * 40)
    print(f"Capacidad del Motor : {torque_motor_kgcm} kg·cm ({torque_motor_nm:.2f} N·m)")
    print(f"Masa total de barra : {masa_total_barra*1000:.1f} gramos")
    print(f"Torque Estático     : {torque_estatico_nm:.2f} N·m (Barra + Pesos)")
    print(f"Momento de Inercia  : {inercia_total:.4f} kg·m^2")
    print(f"Torque Dinámico     : {torque_dinamico_nm:.2f} N·m (a {aceleracion_angular} rad/s^2)")
    print("-" * 40)
    print(f"TORQUE TOTAL        : {torque_total_nm:.2f} N·m")
    print(f"Porcentaje de Uso   : {porcentaje_uso:.1f}%")
    print(f"Factor de Seg. (FS) : {fs:.2f}")
    
    print("\n--- DIAGNÓSTICO ---")
    if fs < 1.0:
        print("❌ PELIGRO: El motor se estancará. El torque requerido supera la capacidad.")
    elif fs < 1.5:
        print("⚠️ ADVERTENCIA: El motor funcionará, pero el Factor de Seguridad es bajo. Propenso a sobrecalentamiento.")
    else:
        print("✅ SEGURO: El motor tiene capacidad suficiente para esta carga dinámica.")

    # ==========================================
    # 4. GRÁFICA: Torque vs Aceleración Angular
    # ==========================================
    rango_aceleraciones = np.linspace(0, 20, 100)
    torques_simulados = torque_estatico_nm + (inercia_total * rango_aceleraciones)
    
    plt.figure(figsize=(9, 6))
    
    plt.plot(rango_aceleraciones, torques_simulados, label='Torque Total Requerido', color='blue', linewidth=2)
    plt.axhline(y=torque_motor_nm, color='red', linestyle='--', linewidth=2, 
                label=f'Límite del Motor ({torque_motor_nm:.1f} N·m)')
    
    plt.plot(aceleracion_angular, torque_total_nm, 'ko', markersize=8, 
             label=f'Tu Operación ({aceleracion_angular} rad/s²)')
    
    plt.fill_between(rango_aceleraciones, torques_simulados, torque_motor_nm, 
                     where=(torques_simulados > torque_motor_nm), color='red', alpha=0.2, label='Zona de Falla')
    plt.fill_between(rango_aceleraciones, torques_simulados, torque_motor_nm, 
                     where=(torques_simulados <= torque_motor_nm), color='green', alpha=0.1, label='Zona Segura')
    
    plt.title('Estudio Dinámico (Barra MDF 448mm): Torque vs Aceleración', fontsize=14, fontweight='bold')
    plt.xlabel('Aceleración Angular (rad/s²)', fontsize=12)
    plt.ylabel('Torque Requerido (N·m)', fontsize=12)
    plt.legend(loc='upper left')
    plt.grid(True, linestyle=':', alpha=0.7)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    analizar_torque_motor()