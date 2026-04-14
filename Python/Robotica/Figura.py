import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class Conversor:
    def __init__(self, raw_data):
        # Guardamos la data original y creamos una copia para el estado actual
        self.raw_data = raw_data
        self.current_data = raw_data.copy()
        
    def extract_points(self):
        """
        Devuelve un DataFrame con el estado actual de los puntos 
        y determina el tipo de trazo (Línea o Arco).
        """
        data = []
        for n, p1, pv, p2 in self.current_data:
            # Si hay un punto 'Via' (pv), es un arco. Si no, es una línea recta.
            tipo_trazo = "Arco (MoveC)" if pv is not None else "Línea (MoveL)"
            data.append({
                "ID": n, 
                "P1": [round(x, 2) for x in p1], 
                "Via": [round(x, 2) for x in pv] if pv else None, 
                "P2": [round(x, 2) for x in p2], 
                "Trazo": tipo_trazo
            })
        return pd.DataFrame(data)
        
    def transform(self, tipo, **kwargs):
        """
        Aplica una transformación geométrica a todos los puntos actuales.
        :param tipo: 'mirror_x', 'mirror_y', 'rotate' o 'translate'
        :param kwargs: 
            - 'angle' y 'origin' requeridos para 'rotate'
            - 'dx' y 'dy' requeridos para 'translate' (desplazamiento en X e Y)
        """
        new_data = []
        for n, p1, pv, p2 in self.current_data:
            np1 = self._apply_math(p1, tipo, **kwargs)
            npv = self._apply_math(pv, tipo, **kwargs) if pv else None
            np2 = self._apply_math(p2, tipo, **kwargs)
            new_data.append((n, np1, npv, np2))
            
        self.current_data = new_data
        return self

    def _apply_math(self, point, tipo, **kwargs):
        """Método interno para calcular la matemática punto por punto."""
        if point is None:
            return None
        
        x, y = point
        if tipo == 'mirror_x':
            return [-x, y]
        elif tipo == 'mirror_y':
            return [x, -y]
        elif tipo == 'rotate':
            angle = kwargs.get('angle', 0)
            cx, cy = kwargs.get('origin', (0, 0))
            rad = np.radians(angle)
            nx = cx + (x - cx) * np.cos(rad) - (y - cy) * np.sin(rad)
            ny = cy + (x - cx) * np.sin(rad) + (y - cy) * np.cos(rad)
            return [nx, ny]
        elif tipo == 'translate':
            dx = kwargs.get('dx', 0)
            dy = kwargs.get('dy', 0)
            return [x + dx, y + dy]
        
        return point
    def _apply_math(self, point, tipo, **kwargs):
        """Método interno para calcular la matemática punto por punto."""
        if point is None:
            return None
        
        x, y = point
        if tipo == 'mirror_x':
            return [-x, y]
        elif tipo == 'mirror_y':
            return [x, -y]
        elif tipo == 'rotate':
            angle = kwargs.get('angle', 0)
            cx, cy = kwargs.get('origin', (0, 0))
            rad = np.radians(angle)
            # Fórmulas de rotación 2D
            nx = cx + (x - cx) * np.cos(rad) - (y - cy) * np.sin(rad)
            ny = cy + (x - cx) * np.sin(rad) + (y - cy) * np.cos(rad)
            return [nx, ny]
        
        return point

    def _plot_movec(self, p1, pv, p2, ax):
        """Método interno con la matemática para graficar arcos (MoveC)."""
        x, y = zip(p1, pv, p2)
        D = 2 * (x[0]*(y[1]-y[2]) + x[1]*(y[2]-y[0]) + x[2]*(y[0]-y[1]))
        
        # Evitar división por cero si los puntos son colineales
        if np.isclose(D, 0):
            ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 'b-')
            return

        ux = ((x[0]**2+y[0]**2)*(y[1]-y[2]) + (x[1]**2+y[1]**2)*(y[2]-y[0]) + (x[2]**2+y[2]**2)*(y[0]-y[1])) / D
        uy = ((x[0]**2+y[0]**2)*(x[2]-x[1]) + (x[1]**2+y[1]**2)*(x[0]-x[2]) + (x[2]**2+y[2]**2)*(x[1]-x[0])) / D
        radius = np.sqrt((x[0]-ux)**2 + (y[0]-uy)**2)
        a1, av, a2 = np.arctan2(np.array(y)-uy, np.array(x)-ux)
        diff = (av-a1+np.pi)%(2*np.pi)-np.pi + (a2-av+np.pi)%(2*np.pi)-np.pi
        angles = a1 + np.linspace(0, diff, 50)
        ax.plot(ux + radius*np.cos(angles), uy + radius*np.sin(angles), 'b-')

    def plot(self, title="Trayectoria Actual"):
        """Dibuja el estado actual de los datos cargados en la clase."""
        fig, ax = plt.subplots(figsize=(8, 8))
        
        for n, p1, pv, p2 in self.current_data:
            if pv:
                self._plot_movec(p1, pv, p2, ax)
            else:
                ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 'r--')

        ax.set_aspect('equal')
        ax.grid(True)
        plt.title(title)
        plt.show()
        
    def reset(self):
        """Devuelve los puntos a su estado original crudo."""
        self.current_data = self.raw_data.copy()
        return self
    
    
    ###########################################
    # 1. Tu data original
raw_data = [
    ("c1", [5, 52], [24, 22], [60, 20]),
    ("c2", [60, 20], [160, 72], [250, 144.5]),
    ("c3", [250, 144.5], [255, 151], [250, 158.5]),
    ("c4", [250, 158.5], [144, 222], [23, 230]),
    ("c5", [23, 230], [12, 222], [5, 212]),
    ("r1", [5, 212], None, [5, 52]),
    ("c1_int1", [60, 20], [65, 30], [60, 40]),
    ("c2_int1", [60, 40], [100, 100], [158, 148]),
    ("c3_int1", [158, 148], [200, 156], [250, 144.5]),
    ("c1_int2", [23, 230], [32, 152], [23, 73]),
    ("c2_int2", [23, 73], [12, 65], [5, 52])
]

# 2. Instancias tu objeto
mi_trayectoria = Conversor(raw_data)

# 3. Puedes plotear el estado original
mi_trayectoria.plot("Original")

# 4. Haces la transformación (Mirror X) y ploteas el resultado
mi_trayectoria.transform(tipo='mirror_x')
mi_trayectoria.plot("Espejo en Eje X (X = -X)")

# 5. Obtienes tu DataFrame (ahora con los datos transformados en X)
df_transformado = mi_trayectoria.extract_points()
print(df_transformado.to_string())

# Extra: Si quisieras rotar 90 grados desde el centro (0,0)
mi_trayectoria.reset() # Volvemos a los puntos iniciales
mi_trayectoria.transform(tipo='rotate', angle=90, origin=(0,0))
mi_trayectoria.plot("Rotación de 90 Grados")

mi_trayectoria.reset() # Partimos de los puntos originales

# Movemos todo el dibujo 50 unidades a la derecha (X) y 100 hacia arriba (Y)
mi_trayectoria.transform(tipo='translate', dx=50, dy=100)

# Ploteamos para ver el resultado
mi_trayectoria.plot("Traslación: dx=50, dy=100")

# Extra: Recuerda que puedes encadenar transformaciones
# Por ejemplo: Mover, luego hacer espejo, y luego plotear
mi_trayectoria.reset()
mi_trayectoria.transform(tipo='translate', dx=-20, dy=-20).transform(tipo='mirror_x').plot("Trasladado y Espejado")