import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class AnalisisAmortiguado:
    def __init__(self, base_dir=None):
        """
        Analiza los dos casos de 'Libre - con amortiguamiento':
        - abierto_unido.csv
        - cerrado_unido.csv
        """

        if base_dir is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
        self.base_dir = base_dir

        # ======= DATOS DEL ROTOR (EDITAR ESTO) ======================
        # Momento de inercia Id [kg·m^2] y longitud efectiva L [m]
        # para cada configuración (valores de tu guía de laboratorio)
        self.casos = [
            {
                "nombre": "Abierta",
                "archivo": r"Archivos/Libre - con amortiguamiento - abierto_unido.csv",
                "Id": 0.0,   # TODO: poner Id_abierta [kg·m^2]
                "L":  0.0,   # TODO: poner L_abierta [m]
            },
            {
                "nombre": "Cerrada",
                "archivo": r"Archivos/Libre - con amortiguamiento - cerrado_unido.csv",
                "Id": 0.0,   # TODO: poner Id_cerrada [kg·m^2]
                "L":  0.0,   # TODO: poner L_cerrada [m]
            },
        ]
        # ============================================================

    # ---------- Lectura de CSV ----------

    def _leer_csv(self, relative_path):
        """
        Lee un CSV con 'Tiempo' y 'Canal B' (mV).
        Devuelve:
            t  : tiempo [s]
            dV : señal LVDT en voltios [V]
        """
        ruta = os.path.join(self.base_dir, relative_path)

        if not os.path.exists(ruta):
            raise FileNotFoundError(f"No se encontró el archivo:\n  {ruta}")

        df = pd.read_csv(ruta, sep=";", decimal=",")

        # Convertimos a numérico y quitamos filas con texto (unidades, etc.)
        for col in ["Tiempo", "Canal B"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        df = df.dropna(subset=["Tiempo", "Canal B"])

        t = df["Tiempo"].to_numpy()
        d_mV = df["Canal B"].to_numpy()

        # En los *_unido.csv el tiempo ya viene en segundos (0–6 aprox).
        # Si algún día te salen en ms (>10), puedes activar:
        # if t.max() > 10:
        #     t = t * 1e-3

        d_V = d_mV / 1000.0  # mV → V

        return t, d_V

    # ---------- Detección de picos ----------

    def _encontrar_picos(self, t, d):
        """
        Encuentra índices de picos positivos en la señal centrada.
        """
        d_c = d - np.mean(d)

        idx = np.where((d_c[1:-1] > d_c[:-2]) & (d_c[1:-1] > d_c[2:]))[0] + 1
        idx = idx[d_c[idx] > 0]  # solo picos positivos

        if len(idx) < 2:
            raise ValueError("Se encontraron muy pocos picos en la señal.")

        return idx

    # ---------- Análisis de un caso ----------

    def analizar_caso(self, caso):
        """
        Aplica el procedimiento del informe a un archivo:
        1) d0, dn, n
        2) ζ por decremento logarítmico
        3) Td como promedio entre picos sucesivos
        4) ωd = 2π/Td
        5) ωn = ωd / sqrt(1-ζ²)
        6) Cc = 2 Id ωn / L² ; C = ζ Cc
        """
        nombre = caso["nombre"]
        archivo = caso["archivo"]
        Id = caso["Id"]
        L = caso["L"]

        # t en s, d en V
        t, d = self._leer_csv(archivo)
        idx_peaks = self._encontrar_picos(t, d)

        # --- 1) d0 y dn separados n ciclos ---
        i0 = idx_peaks[0]
        iN = idx_peaks[-1]

        d0 = d[i0]
        dn = d[iN]

        # número de ciclos completos entre d0 y dn
        n = len(idx_peaks) - 1

        # --- 2) ζ mediante decremento logarítmico (ecuaciones 6–7) ---
        # δ = (1/n) ln(d0/dn)
        delta = (1.0 / n) * np.log(d0 / dn)

        # ζ = δ / sqrt( (2π)² + δ² )
        zeta = delta / np.sqrt((2.0 * np.pi) ** 2 + delta ** 2)

        # --- 3) Td como promedio entre picos sucesivos ---
        periodos = np.diff(t[idx_peaks])   # diferencias entre tiempos de picos
        Td = periodos.mean()

        # --- 4) ωd = 2π / Td ---
        w_d = 2.0 * np.pi / Td

        # --- 5) ωn a partir de ωd = ωn sqrt(1-ζ²) ---
        w_n = w_d / np.sqrt(1.0 - zeta ** 2)

        # --- 6) Cc y C ---
        if Id > 0 and L > 0:
            Cc = 2.0 * Id * w_n / (L ** 2)   # Cc = 2 Id ωn / L²
            C = zeta * Cc                    # C = ζ Cc
        else:
            Cc = np.nan
            C = np.nan

        resultados = {
            "Caso": nombre,
            "d0 [V]": d0,
            "dn [V]": dn,
            "Td [s]": Td,
            "ωd [rad/s]": w_d,
            "ζ": zeta,
            "ωn [rad/s]": w_n,
            "Cc [Ns/m]": Cc,
            "C [Ns/m]": C,
            "t": t,
            "d": d,
            "idx_peaks": idx_peaks,
        }

        return resultados

    # ---------- Tabla tipo Cuadro IX ----------

    def tabla_resultados(self):
        filas = []
        resultados_detallados = []

        for caso in self.casos:
            res = self.analizar_caso(caso)
            resultados_detallados.append(res)
            filas.append([
                res["Caso"],
                res["d0 [V]"],
                res["dn [V]"],
                res["Td [s]"],
                res["ωd [rad/s]"],
                res["ζ"],
                res["C [Ns/m]"],
            ])

        tabla = pd.DataFrame(
            filas,
            columns=["Caso", "d0 [V]", "dn [V]", "Td [s]", "ωd [rad/s]", "ζ", "C [Ns/m]"],
        )

        return tabla, resultados_detallados

    # ---------- Gráfica de cada caso (picos ≥ 5% d0) ----------

    def graficar_caso(self, res, porcentaje=0.05):
        """
        Grafica la señal amortiguada mostrando SOLO los picos cuya
        amplitud es mayor o igual a 'porcentaje' de d0 (por defecto 5%).
        """
        t = res["t"]
        d = res["d"]
        idx_peaks = res["idx_peaks"]
        nombre = res["Caso"]

        # Primer pico d0
        i0 = idx_peaks[0]
        d0 = d[i0]
        umbral = porcentaje * d0

        # Filtrar picos por umbral
        idx_filtrados = [i for i in idx_peaks if d[i] >= umbral]
        idx_filtrados = np.array(idx_filtrados, dtype=int)

        plt.figure(figsize=(9, 4))

        # Señal completa
        plt.plot(t, d, label="Señal LVDT (V)")

        # Picos por encima del 5% de d0
        if len(idx_filtrados) > 0:
            plt.plot(
                t[idx_filtrados],
                d[idx_filtrados],
                "ro",
                label=f"Picos ≥ {porcentaje*100:.0f}% d₀"
            )

        # Marcar d0 y dn (primer y último pico usados en el análisis)
        iN = idx_peaks[-1]
        plt.plot(t[i0], d[i0], "go", markersize=10, label="d₀")
        plt.plot(t[iN], d[iN], "mo", markersize=10, label="dₙ")

        plt.xlabel("Tiempo (s)")
        plt.ylabel("d (V)")
        plt.title(
            f"Respuesta amortiguada - {nombre}\n"
            f"(picos mostrados solo hasta ≥ {porcentaje*100:.0f}% d₀)"
        )
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()


# ============================
# EJECUCIÓN
# ============================
if __name__ == "__main__":
    analizador = AnalisisAmortiguado()

    tabla, resultados = analizador.tabla_resultados()
    print(tabla)           # Tu Cuadro IX

    # Gráficas de Abierta y Cerrada (con picos ≥ 5% d0)
    for res in resultados:
        analizador.graficar_caso(res)
