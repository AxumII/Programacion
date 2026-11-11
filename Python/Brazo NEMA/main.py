import numpy as np

from kinematic import Kinematic
from kinetic import Kinetic
from resistance import Resistance

def analizar_robot(nombre, robot_def, q_actuales, alpha_target, m_load, m_tool, L_critica):
    print(f"\n" + "="*75)
    print(f"=== {nombre} ===")
    print("="*75)

    kinematic_model = Kinematic(joints=robot_def)
    kinetic_model = Kinetic(
        joints=robot_def, 
        alpha_target=alpha_target, 
        m_load=m_load,              
        m_tool=m_tool               
    )

    datos_cinematicos = kinematic_model.calculate_kinematic(q_actuales)
    datos_cineticos = kinetic_model.calculate_kinetic(datos_cinematicos)

    print("\n[RESULTADOS CINEMÁTICOS Y CINÉTICOS]")
    print(f"Posición TCP Final (X,Y,Z): {np.round(datos_cinematicos['p_tcp'], 4)} m")
    
    # Se filtran los eslabones virtuales (is_dummy) para no imprimirlos como motores
    for i in range(len(robot_def)):
        if robot_def[i].get('is_dummy', False):
            continue
            
        t_tot = datos_cineticos['t_total'][i]
        t_max = robot_def[i]['torque_max']
        fuerzas = np.round(datos_cineticos['reaction_forces'][i], 2)
        print(f"  Articulación {i+1} | Torque Requerido: {t_tot:.2f} / {t_max:.2f} Nm | Fuerzas Reacción: {fuerzas} N")
        
        if abs(t_tot) > t_max:
            print(f"    -> [!] ADVERTENCIA: Motor excede capacidad en Articulación {i+1}")

    # Análisis Estructural (Se evalúa la Articulación 2 - Hombro)
    joint_critica = 1 
    longitudes_vigas = [0]*len(robot_def)
    longitudes_vigas[joint_critica] = L_critica # La viga conectada al hombro mide L

    resistance_model = Resistance(datos_cinematicos, datos_cineticos, longitudes_vigas)

    casos_estudio = [
        {"mat": "PLA",      "b": 0.040, "h": 0.040, "w": 0.005,  "r": 0.0},
        {"mat": "PETG",     "b": 0.040, "h": 0.040, "w": 0.005,  "r": 0.0},
        {"mat": "Aluminio", "b": 0.030, "h": 0.030, "w": 0.002,  "r": 0.0},
        {"mat": "Acero",    "b": 0.030, "h": 0.030, "w": 0.0015, "r": 0.0}
    ]

    for caso in casos_estudio:
        prof_data = resistance_model.calculate_profile(
            material=caso["mat"], b=caso["b"], h=caso["h"], 
            r=caso["r"], w=caso["w"], L=L_critica
        )
        res_viga = resistance_model.calculate_arm_beam(joint_critica, prof_data)
        res_viga["elemento"] = f"Viga Hombro ({caso['mat']})"

    resistance_model.calculate_flange(joint_critica)

    print("\n[REPORTE ESTRUCTURAL DE LA ARTICULACIÓN CRÍTICA (HOMBRO Y VIGA PRINCIPAL)]")
    resultados_fs = resistance_model.calculate_FS()
    for elemento, datos in resultados_fs.items():
        if "Brida" in elemento:
            print(f"\n  -- {elemento} --")
            print(f"     Estado: {datos['Estado_Estructural']} | Factor de Seguridad: {datos['Factor_Seguridad']}")
        else:
            print(f"\n  -- {elemento} --")
            print(f"     Estado: {datos['Estado_Estructural']} | FS: {datos['Factor_Seguridad']}")
            print(f"     Deflexión en punta: {datos['Deflexion_Punta_mm']} mm | Peso propio: {datos['Peso_kg']} kg")


def main():
    L = 0.250  # Longitud base en metros (Hombro a Codo)
    
    torque_hombro = 31.2 * 0.35   # 10.92 Nm
    torque_restante = 15.2 * 0.35 # 5.32 Nm
    
    # Parámetros del motor paso a paso (stepper) estandarizados
    m_stepper = 0.520    # 520g en kg
    i_stepper = 6.8e-6   # Inercia típica de rotor de 50mm (~68 g*cm^2 a kg*m^2)

    # =========================================================
    # CONFIGURACIÓN 1: 4 GRADOS DE LIBERTAD (4-DOF)
    # =========================================================
    robot_4dof = [
        # J1: Base Z
        {'axis': 'z', 'offset': [0.0, 0.0, 0.132], 'com_link': [0, 0, 0.06],
         'm_link': 0.7, 'm_motor': m_stepper, 'I_rotor': i_stepper, 'torque_max': torque_restante},
        
        # J2: Hombro Y (Inicio de la longitud L)
        {'axis': 'y', 'offset': [0.0, 0.0, 0.0], 'com_link': [L/2, 0, 0],
         'm_link': 0.7, 'm_motor': m_stepper, 'I_rotor': i_stepper, 'torque_max': torque_hombro},
        
        # J3: Codo Y (A distancia L del hombro)
        {'axis': 'y', 'offset': [L, 0.0, 0.0], 'com_link': [(0.8*L)/2, 0, 0],
         'm_link': 0.5, 'm_motor': m_stepper, 'I_rotor': i_stepper, 'torque_max': torque_restante},
        
        # J4: Muñeca Pitch Y (A distancia 0.8L del codo)
        {'axis': 'y', 'offset': [0.8*L, 0.0, 0.0], 'com_link': [0.090/2, 0, 0],
         'm_link': 0.3, 'm_motor': m_stepper, 'I_rotor': i_stepper, 'torque_max': torque_restante},
         
        # J5: NODO VIRTUAL TCP - Añade los 90mm mecánicos de la muñeca para el cálculo de palanca
        {'axis': 'x', 'offset': [0.090, 0.0, 0.0], 'com_link': [0, 0, 0],
         'm_link': 0.0, 'm_motor': 0.0, 'I_rotor': 0.0, 'torque_max': np.inf, 'is_dummy': True}
    ]

    # Se añade un '0.0' al final para llenar el ángulo y aceleración del nodo virtual
    q_4dof = [0.0, np.pi/4, -np.pi/4, np.pi/6, 0.0]
    alpha_4dof = [1.0, 1.0, 1.0, 1.0, 0.0]

    # =========================================================
    # CONFIGURACIÓN 2: 5 GRADOS DE LIBERTAD (5-DOF)
    # =========================================================
    robot_5dof = [
        # J1: Base Z
        {'axis': 'z', 'offset': [0.0, 0.0, 0.132], 'com_link': [0, 0, 0.06],
         'm_link': 1.0, 'm_motor': m_stepper, 'I_rotor': i_stepper, 'torque_max': torque_restante},
        
        # J2: Hombro Y
        {'axis': 'y', 'offset': [0.0, 0.0, 0.0], 'com_link': [L/2, 0, 0],
         'm_link': 1.5, 'm_motor': m_stepper, 'I_rotor': i_stepper, 'torque_max': torque_hombro},
        
        # J3: Codo Y 
        {'axis': 'y', 'offset': [L, 0.0, 0.0], 'com_link': [(0.8*L)/2, 0, 0],
         'm_link': 1.2, 'm_motor': m_stepper, 'I_rotor': i_stepper, 'torque_max': torque_restante},
        
        # J4: Muñeca Pitch Y
        {'axis': 'y', 'offset': [0.8*L, 0.0, 0.0], 'com_link': [0, 0, 0], 
         'm_link': 0.2, 'm_motor': m_stepper, 'I_rotor': i_stepper, 'torque_max': torque_restante},
         
        # J5: Muñeca Roll X (Acoplado físicamente a J4 sin sumar desplazamiento)
        {'axis': 'x', 'offset': [0.0, 0.0, 0.0], 'com_link': [0.180/2, 0, 0],
         'm_link': 0.4, 'm_motor': m_stepper, 'I_rotor': i_stepper, 'torque_max': torque_restante},
         
        # J6: NODO VIRTUAL TCP - Añade los 180mm mecánicos del efector tras la rotación Roll
        {'axis': 'x', 'offset': [0.180, 0.0, 0.0], 'com_link': [0, 0, 0],
         'm_link': 0.0, 'm_motor': 0.0, 'I_rotor': 0.0, 'torque_max': np.inf, 'is_dummy': True}
    ]

    # Matrices de 6 elementos (5 motores reales + 1 nodo virtual)
    q_5dof = [0.0, np.pi/4, -np.pi/4, np.pi/6, 0.0, 0.0]
    alpha_5dof = [1.0, 1.0, 1.0, 1.0, 1.0, 0.0]

    # =========================================================
    # EJECUCIÓN
    # =========================================================
    masa_herramienta = 0.2
    masa_carga = 0.3       

    analizar_robot("ROBOT 4 GDL", robot_4dof, q_4dof, alpha_4dof, masa_carga, masa_herramienta, L)
    analizar_robot("ROBOT 5 GDL", robot_5dof, q_5dof, alpha_5dof, masa_carga, masa_herramienta, L)


if __name__ == "__main__":
    main()