import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Datos base
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

# Aplicar Mirror en X (x -> -x)
mirror_x = [(n, [-p1[0], p1[1]], ([-pv[0], pv[1]] if pv else None), [-p2[0], p2[1]]) for n, p1, pv, p2 in raw_data]

# Crear Tabla
df = pd.DataFrame([{"ID": m[0], "P1": m[1], "Via": m[2], "P2": m[3]} for m in mirror_x])
print(df.to_string())

# Función de dibujo MoveC
def plot_movec(p1, pv, p2, ax):
    x, y = zip(p1, pv, p2)
    D = 2 * (x[0]*(y[1]-y[2]) + x[1]*(y[2]-y[0]) + x[2]*(y[0]-y[1]))
    ux = ((x[0]**2+y[0]**2)*(y[1]-y[2]) + (x[1]**2+y[1]**2)*(y[2]-y[0]) + (x[2]**2+y[2]**2)*(y[0]-y[1])) / D
    uy = ((x[0]**2+y[0]**2)*(x[2]-x[1]) + (x[1]**2+y[1]**2)*(x[0]-x[2]) + (x[2]**2+y[2]**2)*(x[1]-x[0])) / D
    radius = np.sqrt((x[0]-ux)**2 + (y[0]-uy)**2)
    a1, av, a2 = np.arctan2(np.array(y)-uy, np.array(x)-ux)
    diff = (av-a1+np.pi)%(2*np.pi)-np.pi + (a2-av+np.pi)%(2*np.pi)-np.pi
    angles = a1 + np.linspace(0, diff, 50)
    ax.plot(ux + radius*np.cos(angles), uy + radius*np.sin(angles), 'b-')

# Graficar
fig, ax = plt.subplots(figsize=(8, 8))
for n, p1, pv, p2 in mirror_x:
    if pv: plot_movec(p1, pv, p2, ax)
    else: ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 'r--')

ax.set_aspect('equal')
ax.grid(True)
plt.title("Espejo en Eje X (X = -X)")
plt.show()