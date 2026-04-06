import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Leer el archivo CSV
file_name = 'datos1.csv'
df = pd.read_csv(file_name)

# 2. Extraer datos y convertir a radianes para los cálculos
t = df['t'].values
theta_deg = df['angulo'].values
theta_rad = np.radians(theta_deg)

# 3. Calcular Velocidad Angular (omega) y Aceleración Angular (alpha)
# Usamos np.gradient para obtener las derivadas numéricas
omega = np.gradient(theta_rad, t)
alpha = np.gradient(omega, t)

# Añadir resultados al dataframe
df['omega_rad_s'] = omega
df['alpha_rad_s2'] = alpha

# 4. Cálculo del Sobrepico (Overshoot)
theta_initial = theta_deg[0]
# Promedio de los últimos 10 puntos para definir el estado estable final
theta_final = np.mean(theta_deg[-10:]) 
# El valor de pico (el más alejado del valor final en la dirección del movimiento)
theta_peak = np.min(theta_deg) 

# Magnitud del cambio total (Escalón)
delta_total = abs(theta_final - theta_initial)
# Magnitud del exceso respecto al valor final
sobrepaso = abs(theta_peak - theta_final)

porcentaje_overshoot = (sobrepaso / delta_total) * 100

# 5. Crear las Gráficas
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 15), sharex=True)

# Gráfica de Posición Angular con línea de estado estable
ax1.plot(t, theta_deg, color='blue', label='Posición Angular')
ax1.axhline(y=theta_final, color='red', linestyle='--', label=f'Estado Estable: {theta_final:.2f}°')
ax1.set_ylabel('Ángulo (grados)')
ax1.set_title('Análisis del Movimiento Angular')
ax1.grid(True, alpha=0.3)
ax1.legend()

# Gráfica de Velocidad Angular
ax2.plot(t, omega, color='orange', label=r'Velocidad Angular ($\omega$)')
ax2.set_ylabel('rad/s')
ax2.grid(True, alpha=0.3)
ax2.legend()

# Gráfica de Aceleración Angular
ax3.plot(t, alpha, color='red', label=r'Aceleración Angular ($\alpha$)')
ax3.set_ylabel('rad/s²')
ax3.set_xlabel('Tiempo (s)')
ax3.grid(True, alpha=0.3)
ax3.legend()

plt.tight_layout()
plt.show()

# 6. Mostrar Resultados en Consola
print(f"--- Análisis de Oscilación ---")
print(f"Valor Inicial: {theta_initial:.2f}°")
print(f"Valor Final (Estable): {theta_final:.2f}°")
print(f"Valor Pico: {theta_peak:.2f}°")
print(f"Porcentaje de Sobrepico (Overshoot): {porcentaje_overshoot:.2f}%")

print("\n--- Tabla de Datos (Primeras filas) ---")
print(df.head(10))

# Guardar los resultados calculados en un nuevo archivo
df.to_csv('datos1_resultados.csv', index=False)