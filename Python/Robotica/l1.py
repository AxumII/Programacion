import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class Conversor:
    def __init__(self, raw_data):
        self.raw_data = raw_data
        # Convertimos todo a un DataFrame de NumPy internamente para velocidad
        self.df = pd.DataFrame(raw_data, columns=["ID", "P1", "Via", "P2"])
        self.current_df = self.df.copy()

    def transform(self, tipo, **kwargs):
        # Extraemos solo las columnas de puntos para operar en bloque
        for col in ["P1", "Via", "P2"]:
            # Filtramos los None (para las líneas rectas)
            mask = self.current_df[col].notnull()
            if not mask.any(): continue
            
            # Convertimos la columna en una matriz de NumPy (N x 2)
            pts = np.array(self.current_df.loc[mask, col].tolist())
            
            if tipo == 'm_x': pts[:, 0] = -pts[:, 0]
            elif tipo == 'm_y': pts[:, 1] = -pts[:, 1]
            elif tipo == 't':
                pts += [kwargs.get('dx', 0), kwargs.get('dy', 0)]
            elif tipo == 's':
                f = kwargs.get('f', 1.0)
                cx, cy = kwargs.get('origin', (0, 0))
                pts = np.array([cx, cy]) + (pts - [cx, cy]) * f
            elif tipo == 'r':
                angle = np.radians(kwargs.get('angle', 0))
                cx, cy = kwargs.get('origin', (0, 0))
                c, s = np.cos(angle), np.sin(angle)
                R = np.array([[c, -s], [s, c]])
                pts = (pts - [cx, cy]) @ R.T + [cx, cy]

            # Re-insertamos los puntos transformados en el DataFrame
            self.current_df.loc[mask, col] = list(pts)
        
        return self

    def extract_points(self):
        res = self.current_df.copy()
        # Usamos una forma más robusta de detectar el trazo para DataFrames
        res["Trazo"] = ["Arco (MoveC)" if isinstance(v, (list, np.ndarray)) else "Línea (MoveL)" for v in res["Via"]]
        return res

    def plot(self, title="Trayectoria"):
        fig, ax = plt.subplots(figsize=(8, 8))
        for row in self.current_df.itertuples():
            # Cambio aquí: Verificamos si NO es un float (los None en Pandas se vuelven NaN/float)
            # O simplemente comprobamos si es distinto de None de forma segura
            if isinstance(row.Via, (list, np.ndarray)):
                self._plot_movec(row.P1, row.Via, row.P2, ax)
            else:
                p1, p2 = row.P1, row.P2
                ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 'r--')
        
        ax.set_aspect('equal')
        ax.grid(True)
        plt.title(title)
        plt.show()

    def _plot_movec(self, p1, pv, p2, ax):
        # (La lógica matemática del arco sigue igual, es necesaria para la curva)
        x, y = zip(p1, pv, p2)
        D = 2 * (x[0]*(y[1]-y[2]) + x[1]*(y[2]-y[0]) + x[2]*(y[0]-y[1]))
        if np.isclose(D, 0):
            ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 'b-')
            return
        ux = ((x[0]**2+y[0]**2)*(y[1]-y[2]) + (x[1]**2+y[1]**2)*(y[2]-y[0]) + (x[2]**2+y[2]**2)*(y[0]-y[1])) / D
        uy = ((x[0]**2+y[0]**2)*(x[2]-x[1]) + (x[1]**2+y[1]**2)*(x[0]-x[2]) + (x[2]**2+y[2]**2)*(x[1]-x[0])) / D
        radius = np.sqrt((x[0]-ux)**2 + (y[0]-uy)**2)
        a1, av, a2 = np.arctan2(np.array(y)-uy, np.array(x)-ux)
        diff = (av-a1+np.pi)%(2*np.pi)-np.pi + (a2-av+np.pi)%(2*np.pi)-np.pi
        angles = a1 + np.linspace(0, diff, 30) # Reducido a 30 puntos para ganar velocidad
        ax.plot(ux + radius*np.cos(angles), uy + radius*np.sin(angles), 'b-')

    def reset(self):
        self.current_df = self.df.copy()
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
"""mi_trayectoria.plot("Original")
df_o = mi_trayectoria.extract_points() 
print(df_o.to_string())"""


mi_trayectoria.transform(tipo='m_x')
#mi_trayectoria.transform(tipo='r', angle=90, origin=(0,0))
mi_trayectoria.transform(tipo='t', dx=280, dy=0)
mi_trayectoria.transform(tipo='s', f=0.5, origin=(0,0))

mi_trayectoria.plot("transf")
df_t = mi_trayectoria.extract_points()
print(df_t.to_string())


"""mi_trayectoria.reset() # Volvemos a los puntos iniciales
mi_trayectoria.plot("Original")
df_o = mi_trayectoria.extract_points()
print(df_o.to_string())"""


