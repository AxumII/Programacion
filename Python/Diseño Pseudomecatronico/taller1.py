import numpy as np
import matplotlib.pyplot as plt

class Calculate:
    def __init__(self, w_motor, n_aspas, d, h, rel_pol, F_arr_aspas):
        self.w_motor = w_motor
        self.n_aspas = n_aspas
        self.rel_pol = rel_pol
        self.F_arr_aspas = F_arr_aspas   # N/m^2   
        self.d = d
        self.h = h  
        self.g = 9.81
        
        # Parámetros dependientes geométricos según la tabla
        self.dp = 0.3 * self.d         # m
        self.r_in = 0.25 * self.d      # m 
        self.r_out = 0.45 * self.d     # m
        self.h_aspa = 0.05 + 0.04 * self.h # m
        
    def torque_eje_aspas(self):
        # CORRECCIÓN DIMENSIONAL: Multiplicar por h_aspa
        # Integral de d(Torque) = (F_arr * h_aspa * r dr) resulta en h_aspa * (r^2 / 2)
        t_aspa = (self.F_arr_aspas * self.h_aspa / 2) * (self.r_out**2 - self.r_in**2)
        return t_aspa * self.n_aspas
    
    def potencias(self):
        w_out = self.w_motor * self.rel_pol  
        pot_eje = self.torque_eje_aspas() * w_out
        return pot_eje
    
    def axis(self, Sy=250e6, FS=2.0):
        """
        Calcula el radio mínimo (m) de un eje macizo sometido a torsión pura.
        Sy: Límite de fluencia del material en Pascales (ej. 250 MPa para acero dulce)
        FS: Factor de seguridad deseado
        """
        torque = self.torque_eje_aspas() # Torque aplicado en N.m
        
        # 1. Límite de fluencia al cortante según Von Mises
        Sys = 0.577 * Sy 
        
        # 2. Esfuerzo cortante permisible
        Tau_perm = Sys / FS
        
        # 3. Cálculo del radio mínimo (r)
        # De la fórmula Tau = (Torque * r) / J, sabiendo que J = (pi * r^4) / 2 para un eje macizo
        # Se deduce: Tau = (2 * Torque) / (pi * r^3)  =>  r = [ (2 * Torque) / (pi * Tau) ]^(1/3)
        r = ((2 * torque) / (np.pi * Tau_perm))**(1/3)
        
        # 4. Cálculo del Momento Polar de Inercia (J) resultante en m^4
        J = (np.pi * r**4) / 2
        
        # 5. Comprobación del esfuerzo cortante máximo T (Tau) resultante en Pa
        T = (torque * r) / J 
        
        return r
    
    def chavetas(self):
        return
        
    
    def reacciones(self, masa_eje):
        """
        Calcula las reacciones 3D en los rodamientos.
        Se asume la polea alineada con el eje X positivo.
        Eje Z positivo hacia arriba.
        masa_eje = masa del eje (por diseñar) + masa de las aspas.
        """
        torque = self.torque_eje_aspas()
        radio_polea = self.dp / 2
        
        # 1. Fuerza radial de la correa en el Eje X
        F2 = torque / (3 * radio_polea)
        F1 = 4 * F2        
        F_polea_x = F1 + F2  
        
        # 2. Equilibrio en el plano XZ (Radial en X)
        # Sumatoria de momentos en rodamiento superior = 0
        # (F_polea_x * 0.15h) - (R_inferior_x * 0.30h) = 0
        R_inferior_x = F_polea_x * (0.15 / 0.30)
        
        # Sumatoria de fuerzas en X = 0
        # F_polea_x + R_inferior_x + R_superior_x = 0
        R_superior_x = -(F_polea_x + R_inferior_x)
        
        # 3. Equilibrio en el plano YZ (Radial en Y)
        # Asumiendo aspas simétricas ideales y fluido homogéneo, no hay fuerza radial neta
        R_inferior_y = 0.0
        R_superior_y = 0.0
        
        # 4. Equilibrio en el Eje Z (Axial)
        # El rodamiento inferior soporta todo el peso por restricción de diseño
        peso_total = masa_eje * self.g
        
        R_inferior_z = peso_total # Reacciona empujando hacia arriba (positivo)
        R_superior_z = 0.0        # Libre de carga axial
        
        # 5. Vectores resultantes (X, Y, Z)
        R_superior = np.array([R_superior_x, R_superior_y, R_superior_z])
        R_inferior = np.array([R_inferior_x, R_inferior_y, R_inferior_z])
        
        return {
            "Torque_Eje_Nm": torque,
            "Vector_Reaccion_Sup_N": R_superior,
            "Vector_Reaccion_Inf_N": R_inferior,
            "Carga_Dinamica_Equivalente_Inf_N": np.linalg.norm(R_inferior),
            "Carga_Dinamica_Equivalente_Sup_N": np.linalg.norm(R_superior)
        }
        
    def graf(self, masa_eje):
        """
        Genera los diagramas de Fuerza Cortante y Momento Flector
        reciclando los resultados del método reacciones().
        """
        # 1. Llamar al método de reacciones para reciclar datos
        resultados = self.reacciones(masa_eje)
        
        # Extraer las componentes horizontales (Eje X) de los vectores
        R_sup_x = resultados["Vector_Reaccion_Sup_N"][0]
        R_inf_x = resultados["Vector_Reaccion_Inf_N"][0]
        
        # Por equilibrio estático (F_polea + R_sup_x + R_inf_x = 0)
        F_polea = -(R_sup_x + R_inf_x)
        
        # 2. Definir cotas Z[cite: 1]
        z_polea = 0.0
        z_rod_sup = 0.15 * self.h
        z_rod_inf = z_rod_sup + (0.30 * self.h)
        z_fin = self.h + z_rod_inf  # Extremo inferior del eje
        
        # 3. Arreglos para diagramas
        z_array = np.array([
            z_polea, 
            z_rod_sup, z_rod_sup, 
            z_rod_inf, z_rod_inf, 
            z_fin
        ])
        
        # Diagrama de Fuerza Cortante V(z) utilizando los valores reciclados
        V_z = np.array([
            F_polea,               
            F_polea,               
            F_polea + R_sup_x,     
            F_polea + R_sup_x,     
            0,                     # Se anula con R_inf_x
            0                      
        ])
        
        # Diagrama de Momento Flector M(z)
        M_max = F_polea * z_rod_sup
        M_z = np.array([
            0,                     
            M_max, M_max,          
            0, 0,                  
            0                      
        ])
        
        # 4. Configuración de gráficas con Matplotlib
        fig, axs = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
        fig.suptitle('Diagramas de Esfuerzos Internos del Eje (Z)', fontsize=14, fontweight='bold')
        
        # Gráfica de Fuerza Cortante
        axs[0].plot(z_array, V_z, color='teal', linewidth=2)
        axs[0].fill_between(z_array, V_z, alpha=0.2, color='teal')
        axs[0].axhline(0, color='black', linewidth=1)
        axs[0].axvline(z_rod_sup, color='gray', linestyle='--', alpha=0.5, label='Rod. Superior')
        axs[0].axvline(z_rod_inf, color='gray', linestyle='-.', alpha=0.5, label='Rod. Inferior')
        axs[0].set_title('Diagrama de Fuerza Cortante $V(z)$')
        axs[0].set_ylabel('Fuerza Cortante [N]')
        axs[0].legend()
        axs[0].grid(True, linestyle=':', alpha=0.7)
        
        # Gráfica de Momento Flector
        axs[1].plot(z_array, M_z, color='darkred', linewidth=2)
        axs[1].fill_between(z_array, M_z, alpha=0.2, color='red')
        axs[1].axhline(0, color='black', linewidth=1)
        axs[1].axvline(z_rod_sup, color='gray', linestyle='--', alpha=0.5)
        axs[1].axvline(z_rod_inf, color='gray', linestyle='-.', alpha=0.5)
        axs[1].set_title('Diagrama de Momento Flector $M(z)$')
        axs[1].set_xlabel('Distancia desde la polea Z [m]')
        axs[1].set_ylabel('Momento Flector [N·m]')
        axs[1].grid(True, linestyle=':', alpha=0.7)
        
        plt.tight_layout()
        plt.show()
        
        
    def calculate_S_N(self):
        """
        Genera los diagramas S-N para casos de Torsión (Von Mises) y Axial iterando
        sobre diferentes valores de resistencia última (S_ut) de posibles aceros.
        """
        # Resistencias a la tensión (S_ut) de prueba en MPa (ej. AISI 1020, 1040, Inox)
        Lista_S_ut_Inox = [400, 600, 800] 
        
        # Diámetro en mm para la fórmula empírica (asumiendo conversión de self.d)
        d_mm = self.d * 1000.0 
        
        # Factores constantes asumidos para un entorno controlado
        C_temp = 1.0    # Temperatura ambiente[cite: 3]
        C_conf = 0.753  # Confiabilidad del 99.9%[cite: 3]
        
        # Factor de tamaño (fórmula para flexión/torsión no rotatoria)[cite: 3]
        # Nota: Teóricamente válida hasta 250mm, se extrapola matemáticamente para ejes mayores.
        C_tamano = 1.189 * (d_mm)**(-0.097) #[cite: 3]
        
        # Vector de ciclos de vida (escala logarítmica de 10^3 a 10^6)
        N_cycles = np.logspace(3, 6, 100) 
        
        fig, axs = plt.subplots(1, 2, figsize=(14, 6), sharey=True)
        fig.suptitle('Curvas de Fatiga S-N para el Eje', fontsize=14, fontweight='bold')
        
        for S_ut in Lista_S_ut_Inox:
            # Factor de superficie (Asumiendo acabado Rolado en Caliente para aceros como estimación conservadora)
            # A = 57.7, b = -0.718 para valores en MPa[cite: 3]
            C_sup = 57.7 * (S_ut)**(-0.718) #[cite: 3]
            if C_sup > 1.0: C_sup = 1.0     #[cite: 3]
            
            # Límite de resistencia a la fatiga ideal sin corregir (aceros < 1400 MPa)[cite: 3]
            Se_ = 0.5 * S_ut #[cite: 3]
            
            # ==========================================
            # 1. Caso Torsión del eje (usando Von Mises)
            # ==========================================
            C_carga_torsion = 1.0 # Factor es 1.0 al usar Von Mises[cite: 3]
            Se_torsion = C_carga_torsion * C_tamano * C_sup * C_temp * C_conf * Se_ #[cite: 3]
            Sm_torsion = 0.90 * S_ut # Resistencia a 10^3 ciclos[cite: 3]
            
            # Cálculo de la pendiente (b) y coeficiente (a) para la recta S-N[cite: 3]
            b_torsion = -(1/3) * np.log10(Sm_torsion / Se_torsion) #[cite: 3]
            a_torsion = 10**(np.log10(Sm_torsion) - 3 * b_torsion) #[cite: 3]
            
            # Generación de la curva
            S_N_torsion = a_torsion * (N_cycles)**b_torsion #[cite: 3]
            axs[0].plot(N_cycles, S_N_torsion, linewidth=2, label=f'$S_{{ut}}$ = {S_ut} MPa')
            
            # ==========================================
            # 2. Caso Axial del eje
            # ==========================================
            C_carga_axial = 0.70 # Factor de penalización por carga axial[cite: 3]
            Se_axial = C_carga_axial * C_tamano * C_sup * C_temp * C_conf * Se_ #[cite: 3]
            Sm_axial = 0.75 * S_ut # Mayor degradación inicial en cargas axiales[cite: 3]
            
            b_axial = -(1/3) * np.log10(Sm_axial / Se_axial) #[cite: 3]
            a_axial = 10**(np.log10(Sm_axial) - 3 * b_axial) #[cite: 3]
            
            S_N_axial = a_axial * (N_cycles)**b_axial #[cite: 3]
            axs[1].plot(N_cycles, S_N_axial, linestyle='--', linewidth=2, label=f'$S_{{ut}}$ = {S_ut} MPa')
            
        # Formateo visual de Matplotlib
        titulos = ['Cortante / Torsión (Eq. Von Mises)', 'Carga Axial Pura']
        for i, ax in enumerate(axs):
            ax.set_title(titulos[i])
            ax.set_xlabel('Número de ciclos ($N$)')
            if i == 0:
                ax.set_ylabel('Resistencia a la fatiga $S(N)$ [MPa]')
            ax.set_xscale('log')
            ax.set_yscale('log')
            ax.grid(True, which="both", ls=":", alpha=0.7)
            ax.legend()
            
        plt.tight_layout()
        plt.show()
        
        
# ==========================================
# EJECUCIÓN CON LOS PARÁMETROS DEL USUARIO
# ==========================================
if __name__ == "__main__":
    # Conversión de unidades milimétricas a metros para congruencia
    d_m = 490 / 1000.0
    h_m = 890 / 1000.0
    
    # Instanciamos la clase
    # (El parámetro de rpm w_motor debe pasar a rad/s si se usa para potencia, 
    # pero aquí lo dejamos como lo requiere la clase original).
    # La relación de poleas 4:1 indica que el eje gira 4 veces más lento (o más rápido). 
    # Asumiendo reducción: rel_pol = 0.25 (1/4). Si es multiplicación, usar 4.0.
    # Aquí asumimos reducción por ser un agitador:
    calc = Calculate(w_motor=200, n_aspas=8, d=d_m, h=h_m, rel_pol=0.25, F_arr_aspas=40000)
    
    # Asumimos una masa de eje preliminar de 25 kg para el cálculo de reacciones axiales
    masa_asumida = 25.0
    
    print("==================================================")
    print("   RESULTADOS DEL ANÁLISIS MECÁNICO DEL EJE       ")
    print("==================================================")
    
    # 1. Torque y Potencia
    torque = calc.torque_eje_aspas()
    potencia = calc.potencias()
    print(f"Torque total en el eje: {torque:.2f} N·m")
    # Nota: para la potencia mecánica en Watts, w_motor debería estar en rad/s. 
    # Si ingresaste 200 rpm, la salida actual es (Torque * 200 * 0.25), lo cual requiere conversión
    # w_rad_s = (200 * 0.25) * (2 * np.pi / 60)
    w_rad_s = (calc.w_motor * calc.rel_pol) * (2 * np.pi / 60)
    potencia_watts = torque * w_rad_s
    print(f"Velocidad de salida del eje: {calc.w_motor * calc.rel_pol} RPM ({w_rad_s:.2f} rad/s)")
    print(f"Potencia mecánica requerida: {potencia_watts:.2f} Watts")
    
    # 2. Reacciones
    print("\n---------------- REACCIONES EN RODAMIENTOS ----------------")
    reacciones_data = calc.reacciones(masa_eje=masa_asumida)
    
    print(f"Vector Rodamiento Superior (X, Y, Z):")
    print(f"  Fx = {reacciones_data['Vector_Reaccion_Sup_N'][0]:.2f} N")
    print(f"  Fy = {reacciones_data['Vector_Reaccion_Sup_N'][1]:.2f} N")
    print(f"  Fz = {reacciones_data['Vector_Reaccion_Sup_N'][2]:.2f} N")
    print(f"  -> Carga Equivalente Superior = {reacciones_data['Carga_Dinamica_Equivalente_Sup_N']:,.2f} N")
    
    print(f"\nVector Rodamiento Inferior (X, Y, Z):")
    print(f"  Fx = {reacciones_data['Vector_Reaccion_Inf_N'][0]:.2f} N")
    print(f"  Fy = {reacciones_data['Vector_Reaccion_Inf_N'][1]:.2f} N")
    print(f"  Fz = {reacciones_data['Vector_Reaccion_Inf_N'][2]:.2f} N")
    print(f"  -> Carga Equivalente Inferior = {reacciones_data['Carga_Dinamica_Equivalente_Inf_N']:,.2f} N")
    
    print("==================================================")
    
    # 3. Generar gráficas
    calc.graf(masa_eje=masa_asumida)
