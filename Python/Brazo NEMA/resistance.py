import numpy as np

class Resistance:
    def __init__(self, kinematic_data, kinetic_data, joint_lengths):
        """
        Inicializa el cálculo de resistencia alimentado por los modelos previos.
        :param joint_lengths: Lista con la longitud de cada eslabón en metros (L).
        """
        self.kinematic = kinematic_data
        self.kinetic = kinetic_data
        self.lengths = joint_lengths
        self.fs_results = []
        
        # Propiedades base de los materiales (Unidades: Pa, kg/m^3)
        self.materials = {
            "PLA": {"yield": 40e6, "E": 3.5e9, "rho": 1250, "is_3d": True, "infill": 0.20},
            "PETG": {"yield": 50e6, "E": 2.0e9, "rho": 1270, "is_3d": True, "infill": 0.25, "desc": "Perfil filamento 4D-Lab Colombia"},
            "Aluminio": {"yield": 276e6, "E": 69e9, "rho": 2700, "is_3d": False},
            "Acero": {"yield": 250e6, "E": 200e9, "rho": 7850, "is_3d": False}
        }

    def calculate_profile(self, material, b, h, r, w, L):
        """
        Calcula las inercias, áreas y el peso final de un perfil rectangular de ancho 'b', 
        alto 'h' y espesor de pared 'w'. El radio 'r' se simplifica para la inercia.
        """
        mat = self.materials.get(material)
        if not mat:
            raise ValueError(f"Material {material} no registrado.")
        
        # Dimensiones internas para el área hueca/reticular
        b_in = max(0, b - 2*w)
        h_in = max(0, h - 2*w)
        
        A_out = b * h
        A_in = b_in * h_in
        
        Ixx_out = (b * h**3) / 12
        Ixx_in = (b_in * h_in**3) / 12
        
        Iyy_out = (h * b**3) / 12
        Iyy_in = (h_in * b_in**3) / 12

        if mat["is_3d"]:
            # Impresión 3D: Paredes exteriores 100% sólidas + núcleo con densidad del infill
            A_eff = (A_out - A_in) + (A_in * mat["infill"])
            Ixx = (Ixx_out - Ixx_in) + (Ixx_in * mat["infill"])
            Iyy = (Iyy_out - Iyy_in) + (Iyy_in * mat["infill"])
        else:
            # Metales: Perfiles completamente huecos en el centro
            A_eff = A_out - A_in
            Ixx = Ixx_out - Ixx_in
            Iyy = Iyy_out - Iyy_in

        # Módulos de sección transversal y torsional (aproximación Bredt para tubo rectangular)
        W_x = Ixx / (h/2) if h > 0 else 0
        A_enclosed = (b - w) * (h - w)
        W_torsion = 2 * w * A_enclosed
        
        # Cálculo del peso final del perfil 
        peso_final = A_eff * mat["rho"] * L
        
        return {
            "material": material,
            "A_eff": A_eff,
            "Ixx": Ixx,
            "W_x": W_x,
            "W_torsion": W_torsion,
            "peso_kg": peso_final,
            "yield": mat["yield"],
            "E": mat["E"]
        }
    
    def calculate_arm_beam(self, joint_idx, profile_data):
        """
        Analiza cuánto se deflecta la viga y si el perfil aguanta los torques dinámicos y estáticos.
        """
        # Extrae las reacciones 3D calculadas en la cinética
        F = self.kinetic['reaction_forces'][joint_idx]
        M = self.kinetic['reaction_moments'][joint_idx]
        L = self.lengths[joint_idx]
        
        F_transversal = max(1e-9, np.linalg.norm([F[0], F[1]]))
        M_flector = max(1e-9, np.linalg.norm([M[0], M[1]]))
        T_torsion = abs(M[2])
        
        # Esfuerzo de Von Mises combinando flexión y torsión
        sigma_bend = M_flector / profile_data["W_x"]
        tau_torsion = T_torsion / profile_data["W_torsion"]
        sigma_vm = np.sqrt(sigma_bend**2 + 3 * tau_torsion**2)
        
        # Deflexión en la punta de la viga (Modelo de voladizo)
        deflexion = (F_transversal * (L**3)) / (3 * profile_data["E"] * profile_data["Ixx"]) + \
                    (M_flector * (L**2)) / (2 * profile_data["E"] * profile_data["Ixx"])
        
        fs = profile_data["yield"] / sigma_vm
        rompe = fs < 1.0
        
        resultado = {
            "elemento": f"Viga {joint_idx + 1}",
            "material": profile_data["material"],
            "sigma_max_MPa": sigma_vm / 1e6,
            "deflexion_mm": deflexion * 1000,
            "peso_kg": profile_data["peso_kg"],
            "FS": fs,
            "estado": "ROMPE" if rompe else "AGUANTA"
        }
        self.fs_results.append(resultado)
        return resultado
    
    def calculate_flange(self, joint_idx):
        """
        Evalúa si la brida del codo aguanta el peso y torque usando 6 tornillos M4 en un PCD de 18mm.
        """
        n_bolts = 6
        d_pcd = 0.018 
        r_pcd = d_pcd / 2
        A_bolt = np.pi * (0.004 / 2)**2 
        yield_bolt_8_8 = 640e6 # Límite elástico típico de un tornillo de acero M4
        
        F = self.kinetic['reaction_forces'][joint_idx]
        M = self.kinetic['reaction_moments'][joint_idx]
        
        M_flector = np.linalg.norm([M[0], M[1]])
        T_torsion = abs(M[2])
        F_axial = abs(F[2])
        F_cortante = np.linalg.norm([F[0], F[1]])
        
        # Tracción por flexión y carga axial en el perno superior más crítico
        inercia_polar_tornillos = sum([r_pcd**2 for _ in range(n_bolts)]) / 2
        F_traccion_perno = (M_flector * r_pcd / inercia_polar_tornillos) + (F_axial / n_bolts)
        sigma_perno = F_traccion_perno / A_bolt
        
        # Corte por torsión y carga transversal
        F_corte_perno = (F_cortante / n_bolts) + (T_torsion / (n_bolts * r_pcd))
        tau_perno = F_corte_perno / A_bolt
        
        # Esfuerzo equivalente y seguridad de la brida
        sigma_vm_perno = np.sqrt(sigma_perno**2 + 3 * tau_perno**2)
        fs = yield_bolt_8_8 / sigma_vm_perno
        
        resultado = {
            "elemento": f"Brida {joint_idx + 1}",
            "sigma_tornillo_MPa": sigma_vm_perno / 1e6,
            "FS": fs,
            "estado": "FALLA PESO/TORQUE" if fs < 1.0 else "AGUANTA"
        }
        self.fs_results.append(resultado)
        return resultado
    
    def calculate_FS(self):
        """
        Retorna la recopilación de todos los factores de seguridad del sistema.
        """
        resumen = {}
        for r in self.fs_results:
            resumen[r["elemento"]] = {
                "Factor_Seguridad": round(r["FS"], 2),
                "Estado_Estructural": r["estado"]
            }
            if "deflexion_mm" in r:
                resumen[r["elemento"]]["Deflexion_Punta_mm"] = round(r["deflexion_mm"], 3)
                resumen[r["elemento"]]["Peso_kg"] = round(r["peso_kg"], 3)
                
        return resumen