# Código corregido:
# - Interpreta f_min y f_max en kHz (como indicaste en el ejemplo).
# - La gráfica usa Frecuencia (kHz) en X y Vin (V) en Y.
# - Devuelve la pendiente en kHz/V y Vin en f_max.
# - El parámetro Vin en la firma anterior era innecesario para esta curva, se eliminó.

import numpy as np
import matplotlib.pyplot as plt

def lm(Rt=6.8e3, Ct=0.01e-6, RL=100e3, Rs=12e3,
       f_min_khz=0.0, f_max_khz=12.0, points=300, show=True):
    """
    Grafica Vin (V) vs Frecuencia (kHz) para LM231/LM331.

    Parámetros:
        Rt, Ct, RL, Rs : componentes (Ohm, F, Ohm, Ohm)
        f_min_khz      : frecuencia mínima (kHz)
        f_max_khz      : frecuencia máxima (kHz)
        points         : número de puntos
        show           : muestra la figura si True
    Retorna:
        (pendiente_kHz_por_V, Vin_en_f_max_V)
    """
    # Ganancia (Hz/V) del modelo lineal de la hoja de datos
    K_hz_per_V = (Rs / RL) / (2.09 * Rt * Ct)  # Hz/V
    K_khz_per_V = K_hz_per_V / 1e3             # kHz/V

    # Vector de frecuencias (kHz) y cálculo de Vin
    f_khz = np.linspace(float(f_min_khz), float(f_max_khz), int(points))
    Vin = f_khz / K_khz_per_V  # (kHz) / (kHz/V) = V

    if show:
        plt.figure(figsize=(7,5))
        plt.plot(f_khz, Vin)
        plt.xlabel('Frecuencia (kHz)')
        plt.ylabel('Voltaje de entrada Vin (V)')
        plt.title(
            f'LM231/LM331 — Vin vs Frecuencia\n'
            f'Rt={Rt:.0f} Ω, Ct={Ct:g} F, RL={RL:.0f} Ω, Rs={Rs:.0f} Ω'
        )
        plt.grid(True, ls=':')
        plt.tight_layout()
        plt.show()

    return K_khz_per_V, float(Vin[-1])


# ====== EJEMPLO (personaliza aquí) ======
M = 1e6; k = 1e3; m = 1e-3; u = 1e-6; n = 1e-9; p = 1e-12

Rt = 6.8*k
Ct = 0.01*u
RL = 100*k
Rs = 17*k
fmin_khz = 1.0      # kHz
fmax_khz = 1.05      # kHz
points = 500
show = True

pendiente_khz_V, Vin_fs = lm(Rt, Ct, RL, Rs, fmin_khz, fmax_khz, points, show)
print("Pendiente (kHz/V):", pendiente_khz_V)
print("Vin en f_max (V):", Vin_fs)
