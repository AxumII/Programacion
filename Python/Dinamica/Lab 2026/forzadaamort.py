import os
import pandas as pd
import numpy as np
import scipy.signal as sg
import matplotlib.pyplot as plt

from libreamort import AnalisisLibreAmortiguado

class AnalisisForzadaAmortiguado:
    def __init__(
        self,
        d=0.119,   
        I=1.0,     
        L=0.845,   
        l1=0.375,    # Distancia al motor (excitador)
        l2=0.664,    # Distancia al amortiguador
        Mh=0.05616,
        r=0.045,
        k=1.5,       
        config=None,
    ):
        if config is None:
            config = {
                "abierto": {
                    2.4: {"folder": "Archivos", "file": "forzado amortiguado abierto 2.4.csv"},
                    2.8: {"folder": "Archivos", "file": "forzado amortiguado abierto 2.8.csv"},
                    3.2: {"folder": "Archivos", "file": "forzado amortiguado abierto 3.2.csv"},
                },
                "cerrado": {
                    2.4: {"folder": "Archivos", "file": "forzado amortiguado cerrado 2.4.csv"},
                    2.8: {"folder": "Archivos", "file": "forzado amortiguado cerrado 2.8.csv"},
                    3.2: {"folder": "Archivos", "file": "forzado amortiguado cerrado 3.2.csv"},
                },
            }

        self.d = d
        self.I = I
        self.L = L
        self.l1 = l1
        self.l2 = l2
        self.Mh = Mh
        self.r = r
        # Convierte kN/m a N/m para mantener consistencia de unidades
        self.k = k * 1000.0  

        self.config = config

        self.w_n = self.extract_w_n()
        self.zeta = self.extract_zeta()
        self.C = self.extract_C()

    def _parse_keys(self, res):
        """Asigna de forma segura las llaves provenientes de AnalisisLibreAmortiguado"""
        parsed = {}
        for caso, vals in res.items():
            k = str(caso).lower()
            if "abiert" in k:
                parsed["abierto"] = vals
            elif "cerrad" in k:
                parsed["cerrado"] = vals
        return parsed

    def extract_w_n(self):
        analisis = AnalisisLibreAmortiguado()
        res = self._parse_keys(analisis.result())
        wn = {}
        for key, vals in res.items():
            # Extrae la frecuencia natural wn (o wd como respaldo)
            wn[key] = vals.get("wn", vals.get("w_n", vals.get("wd", 0.0)))
        return wn    

    def extract_zeta(self):
        analisis = AnalisisLibreAmortiguado()
        res = self._parse_keys(analisis.result())
        zetas = {}
        for key, vals in res.items():
            zetas[key] = vals.get("zeta", 0.0)
        return zetas
    
    def extract_C(self):
        analisis = AnalisisLibreAmortiguado()
        res = self._parse_keys(analisis.result())
        C = {}
        for key, vals in res.items():
            C[key] = vals.get("C", 0.0)
        return C
        
    def p2p(self, theta, frac=0.1):
        n0 = int(len(theta) * frac)
        th = theta[n0:]
        if len(th) == 0:
            return 0.0
        return (np.max(th) - np.min(th)) / 2
    
    def read(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        datos = {}

        for estado, freqs in self.config.items():
            for freq, info in freqs.items():
                folder = info["folder"]
                file = info["file"]
                ruta = os.path.join(base_dir, folder, file)

                if not os.path.exists(ruta):
                    raise FileNotFoundError(f"No se encontró el archivo:\n{ruta}")

                df = pd.read_csv(ruta, sep=";", decimal=",", skiprows=[1])

                for col in ["Tiempo", "Canal A", "Canal B"]:
                    df[col] = pd.to_numeric(df[col], errors="coerce")

                df = df.dropna(subset=["Tiempo", "Canal A", "Canal B"])

                tiempo = df["Tiempo"].to_numpy()
                canal_a = df["Canal A"].to_numpy() # Asumiendo Canal A = Proximidad
                canal_b = df["Canal B"].to_numpy() # Asumiendo Canal B = LVDT

                datos[(estado, freq)] = (tiempo, canal_a, canal_b)

        return datos
    
    def fix(self):
        datos = self.read()
        resultados = {}

        for (estado, freq), (t, _, y) in datos.items():
            t = t - t[0]
            delta = y / 350.0
            theta = delta / self.d
            resultados[(estado, freq)] = (t, theta)

        return resultados

    def phi_exp(self, t, x, y):
        # 1. Centrar la señal LVDT
        y_c = y - np.mean(y)
        
        # 2. Encontrar cruces por cero de y (LVDT) con pendiente negativa
        zero_crossings = (y_c[:-1] >= 0) & (y_c[1:] < 0)
        t_zc = t[:-1][zero_crossings]
        
        # 3. Encontrar flancos de bajada de x (Sensor de proximidad)
        thresh = (np.max(x) + np.min(x)) / 2
        edges = (x[:-1] >= thresh) & (x[1:] < thresh)
        t_edges = t[:-1][edges]
        
        if len(t_zc) == 0 or len(t_edges) < 2:
            return 0.0, 0.0, 0.0 
            
        # 4. Periodo T promedio basado en el sensor
        T = np.mean(np.diff(t_edges))
        
        # 5. Calcular delta_t para cada flanco de bajada
        delta_ts = []
        for t_e in t_edges:
            # Buscar el cruce por cero previo más cercano
            valid_zc = t_zc[t_zc <= t_e]
            if len(valid_zc) > 0:
                dt = t_e - valid_zc[-1]
                # Asegurar que dt sea representativo (< T)
                if dt < T:
                    delta_ts.append(dt)
        
        if not delta_ts:
            return 0.0, 0.0, 0.0
            
        delta_t_mean = np.mean(delta_ts)
        
        # 6. Aplicar la fórmula (19)
        phi = -(delta_t_mean / T) * 2.0 * np.pi - (np.pi / 2.0)
        
        # Normalizar el ángulo a [-pi, pi]
        phi = np.arctan2(np.sin(phi), np.cos(phi))
        
        return phi, T, delta_t_mean

    def result(self):
        resultados = {}
        datos_ang = self.fix()
        datos_raw = self.read()

        for (estado, f_forzada), (t, theta) in datos_ang.items():
            w_f = 2.0 * np.pi * f_forzada
            P_m = self.Mh * self.r * w_f**2
            
            w_n = self.w_n[estado]
            r = w_f / w_n
            zeta = self.zeta[estado]
            
            theta_st = (P_m * self.l1) / (self.k * (self.L ** 2))
            
            theta_m_teorico = theta_st / (np.sqrt((1 - r**2)**2 + (2 * zeta * r)**2))
            theta_m_exp = self.p2p(theta)
            
            FA = theta_m_exp / theta_st

            phi_teorico = np.arctan2(2.0 * zeta * r, 1.0 - r**2)
            
            t_raw, x_raw, y_raw = datos_raw[(estado, f_forzada)]
            phi_exp_val, T_exp, delta_t = self.phi_exp(t_raw, x_raw, y_raw)
            
            resultados[(estado, f_forzada)] = {
                "estado": estado,
                "f": f_forzada,
                "w_f": w_f,
                "P_m": P_m,
                "theta_st": theta_st,
                "theta_m_teorico": theta_m_teorico,
                "theta_m_exp": theta_m_exp,
                "FA": FA,
                "r": r,
                "phi_teorico": phi_teorico,
                "phi_exp": phi_exp_val,
                "T_exp": T_exp,
                "delta_t": delta_t,
            }

        return resultados
    
    def tabulate(self):
        resultados = self.result()
        filas = []
        for (estado, f_motor), vals in resultados.items():
            filas.append(
                {
                    "Caso": estado.capitalize(),
                    "f [Hz]": f_motor,
                    "Pm [N]": round(vals["P_m"], 4),
                    "theta_m_exp [°]": round(np.degrees(vals["theta_m_exp"]), 4),
                    "theta_m_teo [°]": round(np.degrees(vals["theta_m_teorico"]), 4),
                    "FA": round(vals["FA"], 4),
                    "r = w_f/w_n": round(vals["r"], 4),
                    "phi_teo [°]": round(np.degrees(vals["phi_teorico"]), 4),
                    "phi_exp [°]": round(np.degrees(vals["phi_exp"]), 4),
                }
            )

        df = pd.DataFrame(filas).sort_values(["Caso", "f [Hz]"])
        return df
    
    def export(self, base="Forzada Amortiguada", out_dir=None):
        df = self.tabulate()
        csv_name = base + "_resonancia_resultados.csv"
        
        if out_dir:
            ruta_csv = os.path.join(out_dir, csv_name)
            os.makedirs(out_dir, exist_ok=True)
        else:
            ruta_csv = csv_name
            
        df.to_csv(ruta_csv, index=False, sep=";")
        print(f"Tabla de configuraciones exportada en: {ruta_csv}")
    
    def plot_senales(self, tiempo_zoom=2.0, out_dir=None):
        """
        Grafica las señales individuales y superpuestas de cada experimento y opcionalmente las exporta.
        tiempo_zoom: Segundos iniciales a mostrar para no saturar la vista con demasiados ciclos.
        out_dir: Directorio donde se guardarán las gráficas generadas.
        """
        datos_raw = self.read()

        for (estado, f_forzada), (t, x, y) in datos_raw.items():
            # Acomodar el tiempo para que empiece en 0
            t = t - t[0]
            
            # Centrar la señal del LVDT para una mejor visualización
            y_c = y - np.mean(y)
            
            # Normalizar las señales al rango [-1, 1] para el gráfico superpuesto
            x_norm = 2.0 * (x - np.min(x)) / (np.max(x) - np.min(x)) - 1.0
            y_norm = 2.0 * (y_c - np.min(y_c)) / (np.max(y_c) - np.min(y_c)) - 1.0

            # Crear figura con 3 subgráficos (filas)
            fig, axs = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
            fig.suptitle(f"Configuración {estado.capitalize()} | Frecuencia: {f_forzada} Hz", fontsize=14, fontweight='bold')

            # 1. Señal del Sensor de Proximidad (Canal A)
            axs[0].plot(t, x, color='tab:red', label='Sensor Proximidad (Canal A)')
            axs[0].set_ylabel('Voltaje [V]')
            axs[0].legend(loc='upper right')
            axs[0].grid(True, linestyle='--', alpha=0.6)

            # 2. Señal del LVDT (Canal B)
            axs[1].plot(t, y_c, color='tab:blue', label='LVDT Centrado (Canal B)')
            axs[1].set_ylabel('Voltaje [V]')
            axs[1].legend(loc='upper right')
            axs[1].grid(True, linestyle='--', alpha=0.6)

            # 3. Señales Superpuestas Normalizadas
            axs[2].plot(t, x_norm, color='tab:red', alpha=0.8, label='Proximidad (Norm.)')
            axs[2].plot(t, y_norm, color='tab:blue', alpha=0.8, label='LVDT (Norm.)')
            
            # Línea horizontal en 0 para ver claramente los cruces
            axs[2].axhline(0, color='black', linewidth=1, linestyle='-')
            
            axs[2].set_xlabel('Tiempo [s]')
            axs[2].set_ylabel('Amplitud Normal.')
            axs[2].legend(loc='upper right')
            axs[2].grid(True, linestyle='--', alpha=0.6)
            
            # Hacer "zoom" al inicio de la señal para ver el detalle de los flancos y cruces
            axs[2].set_xlim([0, tiempo_zoom])

            plt.tight_layout()
            
            # Exportar gráfica si se especificó el directorio de salida
            if out_dir:
                img_name = f"FA_Senal_{estado}_{f_forzada}Hz.png"
                ruta_img = os.path.join(out_dir, img_name)
                plt.savefig(ruta_img, dpi=300, bbox_inches='tight')
                print(f"Gráfica guardada en: {ruta_img}")

            plt.show()

if __name__ == "__main__":
    try:
        OUTPUT_DIR = r"C:\GitHub\Programacion\Python\Dinamica\Lab 2026\Resultados"
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        print("Iniciando extracción de datos forzados amortiguados...\n")
        analisis = AnalisisForzadaAmortiguado()
        df = analisis.tabulate()

        print("\n===== TABLA DE CONFIGURACIONES Y RESULTADOS =====\n")
        print(df.to_string(index=False))

        # Exportar CSV
        analisis.export(out_dir=OUTPUT_DIR)
        
        print("\nGenerando y exportando gráficas de señales. Cierra cada ventana para ver la siguiente...")
        # Llama a plot_senales pasándole el directorio de salida
        analisis.plot_senales(tiempo_zoom=1.5, out_dir=OUTPUT_DIR)
        
    except Exception as e:
        import traceback
        print(f"Ocurrió un error en la ejecución:\n")
        traceback.print_exc()