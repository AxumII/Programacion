import numpy as np
import matplotlib.pyplot as plt

def dh_transform(theta, d, a, alpha):
    """
    Calcula la matriz de transformación homogénea usando parámetros DH estándar.
    """
    th = np.radians(theta)
    al = np.radians(alpha)
    
    ct = np.cos(th)
    st = np.sin(th)
    ca = np.cos(al)
    sa = np.sin(al)
    
    T = np.array([
        [ct, -st*ca,  st*sa, a*ct],
        [st,  ct*ca, -ct*sa, a*st],
        [0,   sa,     ca,    d   ],
        [0,   0,      0,     1   ]
    ])
    return T

def graficar_robot_3d_corregido(q1, q2, q3, q4):
    # --- CORRECCIÓN DE LA TABLA DH ---
    # Para que el eslabón sea vertical y gire axialmente sobre su base, 
    # la altura 153 DEBE ir en el parámetro 'd' (eje Z), no en 'a' (eje X).
    
    # OFFSET: Sumamos 90 grados al hombro para que, cuando ingreses q=[0,0,0,0], 
    # el robot apunte completamente hacia el cielo en lugar de hacia el horizonte.
    q_offset = [0, 90, 0, 0] 
    
    # Parámetros DH Aplicados:  (theta,           d,   a, alpha)
    T01 = dh_transform(q1 + q_offset[0], 153,   0,    90) # Base a Hombro (Corregido)
    T12 = dh_transform(q2 + q_offset[1],   0, 106,     0) # Hombro a Codo
    T23 = dh_transform(q3 + q_offset[2],   0, 106,     0) # Codo a Muñeca
    T34 = dh_transform(q4 + q_offset[3],   0,  96,     0) # Muñeca a TCP
    
    # Acumulación de transformaciones (Cinemática Directa)
    T_base = np.eye(4) # Base en (0,0,0)
    T1 = T_base @ T01  # Base -> Hombro
    T2 = T1 @ T12      # Hombro -> Codo
    T3 = T2 @ T23      # Codo -> Muñeca
    T4 = T3 @ T34      # Muñeca -> TCP 
    
    # Extraer posiciones (x, y, z)
    p_base = T_base[0:3, 3]
    p_hombro = T1[0:3, 3]
    p_codo = T2[0:3, 3]
    p_muneca = T3[0:3, 3]
    p_tcp = T4[0:3, 3]
    
    # Agrupar coordenadas para dibujar
    X = [p_base[0], p_hombro[0], p_codo[0], p_muneca[0], p_tcp[0]]
    Y = [p_base[1], p_hombro[1], p_codo[1], p_muneca[1], p_tcp[1]]
    Z = [p_base[2], p_hombro[2], p_codo[2], p_muneca[2], p_tcp[2]]
    
    # --- VISUALIZACIÓN 3D ---
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Dibujar eslabones
    ax.plot(X, Y, Z, '-o', linewidth=5, markersize=10, color='dodgerblue', markerfacecolor='red')
    
    # Etiquetas
    nombres = ['Art1 Base', 'Art2 (Hombro)', 'Art3 (Codo)', 'Art4 (Muñeca)', 'TCP']
    for i in range(len(X)):
        ax.text(X[i], Y[i], Z[i] + 15, nombres[i], fontsize=10, fontweight='bold')
    
    # Configuración de proporciones correctas
    ax.set_box_aspect([1, 1, 1]) 
    rango = 300 
    ax.set_xlim([-rango, rango])
    ax.set_ylim([-rango, rango])
    ax.set_zlim([0, 500]) # Z más alto para que quepa todo el brazo extendido
    
    ax.set_xlabel('X (mm)')
    ax.set_ylabel('Y (mm)')
    ax.set_zlabel('Z (mm)')
    ax.set_title(f"Posición del Robot\nÁngulos: q=[{q1}°, {q2}°, {q3}°, {q4}°]", pad=20)
    
    print("-" * 50)
    print(f"Ángulos (q1, q2, q3, q4) = [{q1}°, {q2}°, {q3}°, {q4}°]")
    print(f"POSICIÓN EXACTA TCP:")
    print(f"X: {p_tcp[0]:.2f} mm")
    print(f"Y: {p_tcp[1]:.2f} mm")
    print(f"Z: {p_tcp[2]:.2f} mm")
    print("-" * 50)
    
    plt.show()

if __name__ == "__main__":
    # Prueba modificando estos ángulos. 
    # Ahora la base se mantendrá perfectamente vertical en 0,0,0
    q = [90, 45, 45, -45] 
    
    graficar_robot_3d_corregido(q[0], q[1], q[2], q[3])