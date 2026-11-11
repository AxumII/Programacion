import numpy as np

# Se asume que los archivos están en la misma carpeta y se llaman kinematic.py y kinetic.py
from kinematic import Kinematic
from kinetic import Kinetic

def main():
    # 1. Definir los parámetros físicos y geométricos del robot
    # Cada articulación incluye datos para la cinemática (eje, offset, com) 
    # y para la cinética (masas y torque máximo del motor)
    L_ejemplo = 0.250
    robot_def = [
        {
            'axis': 'z', 
            'offset': [0.00475, 0.0, 0.132], 
            'com_link': [0, 0, 0.150 / 2],
            'm_link': 1.5,       # Masa del eslabón en kg
            'm_motor': 0.8,      # Masa del motor en kg
            'I_rotor': 0.01,     # Inercia propia del rotor
            'torque_max': 25.0   # Torque máximo del motor en Nm
        },
        {
            'axis': 'y', 
            'offset': [L_ejemplo, -0.027, 0.0], 
            'com_link': [L_ejemplo / 2, 0, 0],
            'm_link': 1.2,
            'm_motor': 0.6,
            'I_rotor': 0.005,
            'torque_max': 15.0
        }
    ]

    # 2. Instanciar los modelos
    kinematic_model = Kinematic(joints=robot_def)
    
    kinetic_model = Kinetic(
        joints=robot_def, 
        alpha_target=[2.0, 3.5], # Aceleración angular objetivo rad/s^2 por motor
        m_load=0.5,              # Carga de 500g
        m_tool=0.2               # Herramienta de 200g
    )

    # 3. Definir el estado actual del robot (ángulos en radianes)
    q_actuales = [0.0, np.pi/4] # Articulación 1 en 0°, Articulación 2 en 45°

    # 4. Calcular la cinemática
    # Retorna: positions, rot_axes, com_positions, p_tcp, T_matrices
    datos_cinematicos = kinematic_model.calculate_kinematic(q_actuales)

    # 5. Calcular la cinética alimentando los resultados espaciales anteriores
    # Retorna: reaction_forces, reaction_moments, t_static, t_dynamic_target, t_total, inertia_array, alpha_max_permitida
    datos_cineticos = kinetic_model.calculate_kinetic(datos_cinematicos)

    # 6. Imprimir los resultados
    print("=== RESULTADOS CINEMÁTICOS ===")
    print(f"Posición del TCP (X, Y, Z): {np.round(datos_cinematicos['p_tcp'], 4)} m")
    
    print("\n=== RESULTADOS CINÉTICOS (TORQUES DEL MOTOR) ===")
    for i in range(len(robot_def)):
        print(f"Articulación {i+1}:")
        print(f"  Torque Estático (sostener peso): {datos_cineticos['t_static'][i]:.3f} Nm")
        print(f"  Torque Dinámico (acelerar):      {datos_cineticos['t_dynamic_target'][i]:.3f} Nm")
        print(f"  Torque Total Requerido:          {datos_cineticos['t_total'][i]:.3f} Nm")
        print(f"  Aceleración Máx Permitida:       {datos_cineticos['alpha_max_permitida'][i]:.3f} rad/s²")

    print("\n=== REACCIONES MECÁNICAS EN LOS EJES (ESTRUCTURA Y RODAMIENTOS) ===")
    for i in range(len(robot_def)):
        fuerzas = np.round(datos_cineticos['reaction_forces'][i], 3)
        momentos = np.round(datos_cineticos['reaction_moments'][i], 3)
        print(f"Articulación {i+1}:")
        print(f"  Fuerzas soportadas [Fx, Fy, Fz]:  {fuerzas} N")
        print(f"  Momentos soportados [Mx, My, Mz]: {momentos} Nm")

if __name__ == "__main__":
    main()