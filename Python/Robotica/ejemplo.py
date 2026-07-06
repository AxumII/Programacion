import numpy as np
from Kin import Kinematic
from limits_pincher import Limits
from tracer import Tracer

def ejemplo():
    # 1. Instanciamos clases de otros archivos 
    mi_robot = Kinematic(
        l1=153, l2=106, l3=106, w1=0, w2=0, w3=0, lTool=96, wTool=0, thetaTool=0, phi=None, 
        offset_t2=90.0, dir_t2=-1.0,  
        offset_t3=0.0, dir_t3=1.0  
    )
    mi_limite = Limits(mi_robot)
    mi_tracer = Tracer(mi_robot, mi_limite)

    # 2. Definimos y mapeamos obstaculos
    obstaculos = [
        # Caja 1: A la izquierda, inclinada 45 grados en Yaw
        {'type': 'box', 'center': [200, 100, 40], 'dims': [30, 80, 80], 'rpy': [0, 0, 45], 'name': 'Caja 1 Azul (Inclinada a 45)'},
        
        # Caja 2: A la derecha, inclinada 45 grados en Yaw
        {'type': 'box', 'center': [200, -100, 40], 'dims': [30, 80, 80], 'rpy': [0, 0, -45], 'name': 'Caja 2 Verde (Inclinada a -45)'},
        
        # Caja 3: A la izquierda recta
        {'type': 'box', 'center': [30, 110, 30], 'dims': [30, 80, 60], 'rpy': [0, 0, 90], 'name': 'Caja 3 Amarilla '},
        
        # Caja 4: A La derecha recta
        {'type': 'box', 'center': [30, -110, 30], 'dims': [30, 80, 60], 'rpy': [0, 0, 90], 'name': 'Caja 4 Roja '},
        
        
        # Piso
        {'type': 'box', 'center': [0, 0, -152.5], 'dims': [600, 600, 300], 'rpy': [0, 0, 0], 'name': 'Piso '},
        
        
        # Cilindro: Atrás del robot
        {'type': 'cylinder', 'center': [260, 0, 0], 'radius': 25, 'height': 140, 'name': 'Columna Camara'}
    ]
    mi_tracer.mapear_obstaculos(obstaculos)

    # 3. Prueba de Cinemática Directa (Forward),
    print("--- 1. FORWARD KINEMATICS ---")
    fwd = mi_tracer.trace_forward(24.9,26.4,20.8,-19.6)
    print(f"Posición Cartesiana : {[round(v, 2) for v in fwd['Coordenadas']]}")
    print(f"Orientación RPY     : {[round(v, 2) for v in fwd['Rotacion_RPY']]}\n")

    # 4. Prueba de Cinemática Inversa (Inverse) con Detección de Codo
    print("--- 2. INVERSE KINEMATICS ---")
    x, y, z, theta4 = 200, 0, 100, 0
    inv = mi_tracer.trace_inverse(x, y, z, theta4 = theta4)
    if inv['Estado'] == "Éxito":
        for sol in inv['Soluciones']:
            angulos = [f"{a:.1f}°" for a in sol['Configuracion']]
            print(f"> {sol['Tipo']}: [{', '.join(angulos)}] -> {sol['Estado']}")
    print("\n")

    # 5. Prueba de Interpolación (Quintica)
    print("--- 3. INTERPOLACIÓN DE TRAYECTORIA ---")
    q_inicial = [0.0, 0.0, 0.0, 0.0]
    q_final = [24.9,26.4,20.8,-19.6]
    
    # Probemos con interpolación quíntica (5th order)
    trayectoria, colisiones = mi_tracer.interpolar_trayectoria(
        q_start=q_inicial, 
        q_end=q_final, 
        steps=5,              
        method='quintica', 
        validar_colisiones=True
    )
    
    for i, q in enumerate(trayectoria):
        print(f"Paso {i+1} | Ángulos: {[round(a, 1) for a in q]} | Estado: {colisiones[i]}")
        
    # 6. Llamados de Graficación    
    # Extraemos la última posición de la trayectoria si existe, sino usamos ceros
    q_actual = trayectoria[-1] if 'trayectoria' in locals() and trayectoria else [0.0, 0.0, 0.0, 0.0]
    
    mi_tracer.graficar_trayectoria(
        theta1=q_actual[0], 
        theta2=q_actual[1], 
        theta3=q_actual[2], 
        theta4=q_actual[3], 
        obstacles=obstaculos
    )
ejemplo()