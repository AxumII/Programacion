import pandas as pd
import matplotlib.pyplot as plt
import io

# 1. Cargar los datos
# Asegúrate de guardar el CSV limpio que te pasé en un archivo llamado 'datos_robot.csv'
# Si quieres usar un string directo, puedes usar io.StringIO(tu_string_csv)
df = pd.read_csv(r'C:\GitHub\Programacion\Python\Dinamica\Brazo\DatosMotores.csv')

# Convertir el tiempo de milisegundos a segundos para facilitar la lectura
df['Tiempo(s)'] = df['Tiempo(ms)'] / 1000.0

# 2. Configurar la figura y los subplots (2 filas, 1 columna)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

# --- Gráfica 1: Comportamiento General ---
ax1.plot(df['Tiempo(s)'], df['Q1(deg)'], label='Q1 (Base)', color='blue')
ax1.plot(df['Tiempo(s)'], df['Q2(deg)'], label='Q2 (Hombro)', color='orange')
ax1.plot(df['Tiempo(s)'], df['Q3(deg)'], label='Q3 (Codo)', color='green')
ax1.plot(df['Tiempo(s)'], df['Q4(deg)'], label='Q4 (Muñeca)', color='red')

ax1.set_title('Respuesta General del Sistema (Trayectoria hacia Home)')
ax1.set_xlabel('Tiempo (s)')
ax1.set_ylabel('Posición Angular (°)')
ax1.grid(True, linestyle='--', alpha=0.7)
ax1.legend()

# --- Gráfica 2: Zoom al Sobreimpulso (Estado Estacionario) ---
# Filtrar los datos para ver solo los últimos segundos del movimiento
# El movimiento parece estabilizarse después de los 5.0 segundos
df_zoom = df[df['Tiempo(s)'] > 5.0]

ax2.plot(df_zoom['Tiempo(s)'], df_zoom['Q1(deg)'], label='Q1', color='blue')
ax2.plot(df_zoom['Tiempo(s)'], df_zoom['Q2(deg)'], label='Q2', color='orange')
ax2.plot(df_zoom['Tiempo(s)'], df_zoom['Q3(deg)'], label='Q3', color='green')
ax2.plot(df_zoom['Tiempo(s)'], df_zoom['Q4(deg)'], label='Q4', color='red')

# Añadir líneas de referencia para el Setpoint (Home = 90, -90, 90, -90)
ax2.axhline(y=90, color='gray', linestyle=':', label='Setpoint (90°)')
ax2.axhline(y=-90, color='black', linestyle=':', label='Setpoint (-90°)')

ax2.set_title('Análisis de Sobreimpulso (Zoom: t > 5s)')
ax2.set_xlabel('Tiempo (s)')
ax2.set_ylabel('Posición Angular (°)')
ax2.grid(True, linestyle='--', alpha=0.7)
ax2.legend(loc='center right')

# Ajustar el diseño y mostrar
plt.tight_layout()
plt.show()