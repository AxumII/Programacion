import numpy as np
from Kin import Kinematic
from limits_pincher import Limits

class Tracer:
    def __init__(self, robot_kinematic: Kinematic, limits_analyzer: Limits):
        """
        Clase principal para trazar movimientos, validación de colisiones y 
        generación de trayectorias (interpolación).
        """
        self.robot = robot_kinematic
        self.limits = limits_analyzer
        self.intervalos_cacheados = {}

    def mapear_obstaculos(self, obstaculos):
        """Pre-calcula los rangos prohibidos de los obstáculos una sola vez y los imprime."""
        print("Mapeando obstáculos en el C-Space...")
        for obs in obstaculos:
            nombre = obs.get('name', 'Obstáculo')
            intervalos = self.limits.analyze_obstacle(obs, step=10.0)
            self.intervalos_cacheados[nombre] = intervalos
            
            # NUEVO: Imprimir los límites calculados en la consola
            print(f" -> {nombre}:")
            if intervalos:
                for art, rangos in intervalos.items():
                    print(f"      {art}: [{rangos[0]:.1f}°, {rangos[1]:.1f}°] prohibidos")
            else:
                print("      (Sin colisión en el espacio de trabajo / No alcanzable)")
                
        print("Mapeo completo.\n")

    def _esta_colisionando(self, q_sol):
        """Evalúa si una configuración específica entra en algún volumen prohibido."""
        for nombre, intervalos in self.intervalos_cacheados.items():
            if not intervalos: continue
            
            en_colision = True
            for i, art in enumerate(['θ1', 'θ2', 'θ3', 'θ4']):
                if art in intervalos:
                    vmin, vmax = intervalos[art]
                    if not (vmin <= q_sol[i] <= vmax):
                        en_colision = False
                        break
            
            if en_colision:
                return True, nombre
        return False, None

    def trace_forward(self, q1, q2, q3, q4=None, use_tcp_norm = False):
        """Pasa de Ángulos -> Posición Cartesiana y Orientación (RPY)"""
        x, y, z, roll, pitch, yaw = self.robot.get_pose(q1, q2, q3, q4, use_tcp_norm = False)
        return {
            'Coordenadas': (x, y, z),
            'Rotacion_RPY': (roll, pitch, yaw)
        }

    def trace_inverse(self, x, y, z, phi, obstaculos=None):
        """Pasa de Posición Cartesiana -> Posibles Ángulos (Codo Arriba/Abajo y Colisiones)"""
        exito, soluciones = self.robot.InvKin(x, y, z, phi_val=phi)
        
        if not exito:
            return {"Estado": "Error", "Mensaje": "Coordenadas fuera del alcance geométrico del robot."}

        resultados = []
        etiquetas = ["Codo Arriba", "Codo Abajo"]

        for idx, sol in enumerate(soluciones):
            etiqueta = etiquetas[idx] if idx < len(etiquetas) else f"Solución {idx+1}"
            
            # Validar colisiones usando la caché de obstáculos
            colision, obstaculo_nombre = self._esta_colisionando(sol)
            estado_seguridad = "ALCANZABLE (Seguro)" if not colision else f"¡COLISIÓN! ({obstaculo_nombre})"
            
            resultados.append({
                'Tipo': etiqueta,
                'Configuracion': sol,
                'Estado': estado_seguridad,
                'Colision': colision
            })
            
        return {"Estado": "Éxito", "Soluciones": resultados}

    def interpolar_trayectoria(self, q_start, q_end, steps, method='lineal', validar_colisiones=False):
        """
        Genera una trayectoria angular suave entre q_start y q_end.
        Opciones de 'method': 'lineal', 'cuadratica', 'cubica', 'cuartica', 'quintica', 'sinusoidal'
        """
        q_start = np.array(q_start)
        q_end = np.array(q_end)
        trayectoria = []
        reporte_colisiones = []

        # Vector de tiempo normalizado de 0 a 1
        t_norm = np.linspace(0, 1, steps)

        for t in t_norm:
            # Calcular factor de escala 's' según la matemática seleccionada
            if method == 'lineal':
                s = t
            elif method == 'cuadratica':
                s = 2 * (t**2) if t < 0.5 else 1 - ((-2 * t + 2)**2) / 2
            elif method == 'cubica':
                s = 3*(t**2) - 2*(t**3)
            elif method == 'cuartica':
                s = 8 * (t**4) if t < 0.5 else 1 - ((-2 * t + 2)**4) / 2
            elif method == 'quintica':
                s = 10*(t**3) - 15*(t**4) + 6*(t**5)
            elif method == 'sinusoidal':
                s = 0.5 - 0.5 * np.cos(np.pi * t)
            else:
                s = t # Lineal por defecto

            # Aplicar la escala al delta de posiciones
            q_actual = q_start + s * (q_end - q_start)
            trayectoria.append(q_actual.tolist())

            # Validar cada punto de la trayectoria generada
            if validar_colisiones:
                colision, obs_nombre = self._esta_colisionando(q_actual)
                if colision:
                    reporte_colisiones.append(f"Colisión en paso con {obs_nombre}")
                else:
                    reporte_colisiones.append("Seguro")

        return trayectoria, reporte_colisiones

    def interpolar_trayectoria_cartesiana(self, pose_start, pose_end, steps, method='lineal'):
        """
        Genera una trayectoria a partir de poses Cartesianas: 
        pose_start/end en formato (x, y, z, phi). Retorna la interpolación en ángulos.
        """
        # Calcular inversa para el punto inicial
        inv_start = self.trace_inverse(*pose_start)
        if inv_start['Estado'] != "Éxito": return None, ["Punto de inicio inalcanzable"]
        
        # Calcular inversa para el punto final
        inv_end = self.trace_inverse(*pose_end)
        if inv_end['Estado'] != "Éxito": return None, ["Punto final inalcanzable"]

        # Se toma la primera configuración segura disponible
        q_start = next((sol['Configuracion'] for sol in inv_start['Soluciones'] if not sol['Colision']), None)
        q_end = next((sol['Configuracion'] for sol in inv_end['Soluciones'] if not sol['Colision']), None)

        if not q_start or not q_end:
            return None, ["Colisión en los puntos extremos elegidos"]

        # Interpolar en el espacio articular
        return self.interpolar_trayectoria(q_start, q_end, steps, method=method, validar_colisiones=True)

    def graficar_trayectoria(self, theta1=0.0, theta2=0.0, theta3=0.0, theta4=0.0, obstacles=None):
        """Delega la llamada de graficación a la clase cinemática subyacente con sus parámetros."""
        self.robot.plot(theta1, theta2, theta3, theta4=theta4, obstacles=obstacles)

# ===============================================
# EJECUCIÓN DE PRUEBA DESDE TRACER
# ===============================================
if __name__ == "__main__":
    # 1. Instanciamos clases de otros archivos 
    mi_robot = Kinematic(
        l1=46, l2=106, l3=106, w1=0, w2=0, w3=0, lTool=96, wTool=0, thetaTool=0, phi=None, 
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
        
        # Cilindro: Atrás del robot
        {'type': 'cylinder', 'center': [260, 0, 0], 'radius': 25, 'height': 150, 'name': 'Columna Camara'}
    ]
    mi_tracer.mapear_obstaculos(obstaculos)

    # 3. Prueba de Cinemática Directa (Forward),
    print("--- 1. FORWARD KINEMATICS ---")
    fwd = mi_tracer.trace_forward(0, 0, 0, 1,use_tcp_norm = False)
    print(f"Posición Cartesiana : {[round(v, 2) for v in fwd['Coordenadas']]}")
    print(f"Orientación RPY     : {[round(v, 2) for v in fwd['Rotacion_RPY']]}\n")

    # 4. Prueba de Cinemática Inversa (Inverse) con Detección de Codo
    print("--- 2. INVERSE KINEMATICS ---")
    x, y, z, phi = 200, 0, 50, -45
    inv = mi_tracer.trace_inverse(x, y, z, phi)
    if inv['Estado'] == "Éxito":
        for sol in inv['Soluciones']:
            angulos = [f"{a:.1f}°" for a in sol['Configuracion']]
            print(f"> {sol['Tipo']}: [{', '.join(angulos)}] -> {sol['Estado']}")
    print("\n")

    # 5. Prueba de Interpolación (Quintica)
    print("--- 3. INTERPOLACIÓN DE TRAYECTORIA ---")
    q_inicial = [0.0, 0.0, 0.0, 0.0]
    q_final = [0, 45, 0, 0.0]
    
    # Probemos con interpolación quíntica (5th order)
    trayectoria, colisiones = mi_tracer.interpolar_trayectoria(
        q_start=q_inicial, 
        q_end=q_final, 
        steps=5,              # Solo 5 pasos para verlo fácil en consola
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