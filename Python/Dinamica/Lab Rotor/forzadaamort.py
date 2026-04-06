import os
import pandas as pd
import numpy as np
import scipy.signal as sg
import matplotlib.pyplot as plt

from libreamort import AnalisisLibreAmortiguado


class AnalisisForzadaAmortiguado:
    def __init__(
        self,
        d=0.119,   # m  distancia sensor–eje
        I=1.0,     # kg·m^2
        L=0.845,   # m
        Mh=0.05616,
        r=0.045,
        k=3,       # [N·mm/rad] → se convierte a N·m/rad
        config=None,
    ):
        """
        Clase para analizar la oscilación forzada con amortiguamiento.
        """

        # Config por defecto: 3 abiertos + 3 cerrados
        if config is None:
            config = {
                "abierto": {
                    2.5: {
                        "folder": "Archivos",
                        "file": "Forzada con amortiguamiento - abierto 2.5Hz_unido.csv",
                    },
                    2.8: {
                        "folder": "Archivos",
                        "file": "Forzada con amortiguamiento - abierto 2.8Hz_unido.csv",
                    },
                    3.1: {
                        "folder": "Archivos",
                        "file": "Forzada con amortiguamiento - abierto 3.1Hz_unido.csv",
                    },
                },
                "cerrado": {
                    2.5: {
                        "folder": "Archivos",
                        "file": "Forzada con amortiguamiento - cerrado 2.5Hz_unido.csv",
                    },
                    2.8: {
                        "folder": "Archivos",
                        "file": "Forzada con amortiguamiento - cerrado 2.8Hz_unido.csv",
                    },
                    3.1: {
                        "folder": "Archivos",
                        "file": "Forzada con amortiguamiento - cerrado 3.1Hz_unido.csv",
                    },
                },
            }

        # Constantes del sistema
        self.d = d
        self.I = I
        self.L = L
        self.Mh = Mh
        self.r = r
        self.k = k / 1e-3 #k está en KN·m/rad → convertir a N·m/rad

        self.config = config

        # wn tomada del caso libre amortiguado
        self.w_n = self.extract_w_n()
        
        #zeta tomada del caso libre amortiguado
        self.zeta = self.extract_zeta()
        self.C = self.extract_C()


    # ----------------------------------------------------------
    def extract_w_n(self):
        analisis = AnalisisLibreAmortiguado()
        res = analisis.result()   # dict: 'Abierta' -> {...}, 'Cerrada' -> {...}

        # Mapeo de nombres entre las dos clases
        name_map = {
            "Abierta": "abierto",
            "Cerrada": "cerrado",
        }

        wn = {}
        for caso, vals in res.items():
            key = name_map.get(caso, caso.lower())
            wn[key] = vals["wd"]   # usar la frecuencia amortiguada del libre como "wn"

        return wn    

    def extract_zeta(self):
        """
        Obtiene zeta para los casos libre amortiguado (Abierta, Cerrada)
        y los mapea a las llaves usadas aquí ('abierto', 'cerrado').
        """
        analisis = AnalisisLibreAmortiguado()
        res = analisis.result()   # dict: 'Abierta' -> {...}, 'Cerrada' -> {...}

        # Mapeo de nombres entre las dos clases
        name_map = {
            "Abierta": "abierto",
            "Cerrada": "cerrado",
        }

        zetas = {}
        for caso, vals in res.items():
            key = name_map.get(caso, caso.lower())
            zetas[key] = vals["zeta"]

        return zetas
    
    def extract_C(self):
        """
        Obtiene zeta para los casos libre amortiguado (Abierta, Cerrada)
        y los mapea a las llaves usadas aquí ('abierto', 'cerrado').
        """
        analisis = AnalisisLibreAmortiguado()
        res = analisis.result()   # dict: 'Abierta' -> {...}, 'Cerrada' -> {...}

        # Mapeo de nombres entre las dos clases
        name_map = {
            "Abierta": "abierto",
            "Cerrada": "cerrado",
        }

        C = {}
        for caso, vals in res.items():
            key = name_map.get(caso, caso.lower())
            C[key] = vals["C"]

        return C
        
    # ----------------------------------------------------------
    def p2p(self, theta, frac=0.1):
        """
        Calcula la amplitud pico a pico / 2 usando solo el 10% final.
        """
        n0 = int(len(theta) * frac)
        th = theta[n0:]
        return (np.max(th) - np.min(th)) / 2
    
    # ----------------------------------------------------------
    def read(self):
        """
        Devuelve:

        {
            ("abierto", 2.5): (t, canal_a, canal_b),
            ("abierto", 2.8): (t, canal_a, canal_b),
            ("abierto", 3.1): (t, canal_a, canal_b),
            ("cerrado", 2.5): (t, canal_a, canal_b),
            ("cerrado", 2.8): (t, canal_a, canal_b),
            ("cerrado", 3.1): (t, canal_a, canal_b),
        }
        """

        base_dir = os.path.dirname(os.path.abspath(__file__))
        datos = {}

        for estado, freqs in self.config.items():
            for freq, info in freqs.items():

                folder = info["folder"]
                file = info["file"]
                ruta = os.path.join(base_dir, folder, file)

                if not os.path.exists(ruta):
                    raise FileNotFoundError(
                        f"No se encontró el archivo:\n{ruta}\n"
                        "Verifica la carpeta Archivos y los nombres."
                    )

                df = pd.read_csv(
                    ruta,
                    sep=";",
                    decimal=",",
                )

                for col in ["Tiempo", "Canal A", "Canal B"]:
                    df[col] = pd.to_numeric(df[col], errors="coerce")

                df = df.dropna(subset=["Tiempo", "Canal A", "Canal B"])

                tiempo = df["Tiempo"].to_numpy()
                canal_a = df["Canal A"].to_numpy()
                canal_b = df["Canal B"].to_numpy()

                datos[(estado, freq)] = (tiempo, canal_a, canal_b)

        return datos
    
    # ----------------------------------------------------------
    def fix(self):
        """
        Convierte voltajes → ángulos (rad).

        Devuelve:
        {
            ("abierto", 2.5): (t, theta),
            ...
            ("cerrado", 3.1): (t, theta)
        }
        """

        datos = self.read()
        resultados = {}

        for (estado, freq), (t, _, y) in datos.items():

            # strain = (y[mV] / 1000 ) / 350
            delta = (y / 1000.0) / 350.0
            theta = delta / self.d

            resultados[(estado, freq)] = (t, theta)

        return resultados
    
    def phi_exp(self, t, x, y):
        """
        Desfase experimental entre:
        - x: sensor de proximidad (excitación)
        - y: LVDT (respuesta)

        Convención: phi > 0 => la respuesta y(t) SE ATRASA respecto a x(t).
        """

        # Tomar solo régimen estacionario (segunda mitad)
        n0 = len(t) // 2
        t_ss = t[n0:]
        x_ss = x[n0:]
        y_ss = y[n0:]

        # --- Cruces por cero ascendentes de y (respuesta) ---
        idx_zc = np.where((y_ss[:-1] <= 0.0) & (y_ss[1:] > 0.0))[0]
        if len(idx_zc) < 2:
            raise RuntimeError("No se encontraron suficientes cruces por cero en y.")
        t_zc = t_ss[idx_zc]

        # --- Flancos de subida en x (excitación) ---
        umbral = (np.max(x_ss) + np.min(x_ss)) / 2.0
        idx_edges = np.where((x_ss[:-1] <= umbral) & (x_ss[1:] > umbral))[0]
        if len(idx_edges) < 2:
            raise RuntimeError("No se encontraron suficientes flancos de subida en x.")
        t_edges = t_ss[idx_edges]

        # Periodo de la excitación
        T = np.mean(np.diff(t_edges))

        # --- Para cada flanco de subida en x, buscar el siguiente cruce por cero ascendente de y ---
        deltas = []
        for te in t_edges:
            posteriores = t_zc[t_zc >= te]
            if len(posteriores) == 0:
                continue
            tz = posteriores[0]
            deltas.append(tz - te)   # respuesta - excitación

        if len(deltas) == 0:
            raise RuntimeError("No se pudo emparejar flancos de x con cruces de y.")

        delta_t = np.mean(deltas)

        # Fase: phi = ((Δt / T) *2π  )-( π / 2)
        phi = (-(delta_t / T)*(2.0 * np.pi))  - (np.pi/2)

        # Envolver a (-π, π]
        phi = np.arctan2(np.sin(phi), np.cos(phi))

        return phi, T, delta_t

 
  
    def result(self):
        resultados = {}
        datos_ang = self.fix()
        datos_raw = self.read()

        for (estado, f_forzada), (t, theta) in datos_ang.items():
            
            # Frecuencia forzada
            w_f = 2.0 * np.pi * f_forzada

            # Carga dinámica
            P_m = self.Mh * self.r * w_f**2
            
            k = self.k  # rigidez en N·m/rad
            
            # Relación de frecuencia
            w_n = self.w_n[estado]
            r = w_f / w_n
            
            # Amplitud teórica (modelo)            
            zeta = self.zeta[estado]
            theta_m_teorico = (P_m / self.k) / (np.sqrt((1 - r**2)**2 + (2 * zeta * r)**2))

            # Amplitud experimental (pico a pico/2)
            theta_m_exp = self.p2p(theta)
            
            # Factor de amplificación
            FA = theta_m_exp / (P_m / k)

            # Relación de frecuencia
            r = w_f / w_n
            
            #desfase Teorico
            # Coeficiente de amortiguamiento crítico
            tan_phi = (2.0 * zeta * r) / (1.0 - r**2)
            tan_phi = (2.0 * zeta * r) / (1.0 - r**2)
            phi_teorico = np.arctan(tan_phi)
            
            
            #desfase experimental
            # Desfase experimental (usar datos crudos x,y)
            t_raw, x_raw, y_raw = datos_raw[(estado, f_forzada)]
            phi_exp, T_exp, delta_t = self.phi_exp(t_raw, x_raw, y_raw)
            

            resultados[(estado, f_forzada)] = {
                "estado": estado,
                "f": f_forzada,
                "w_f": w_f,
                "P_m": P_m,
                "theta_m_teorico": theta_m_teorico,
                "theta_m_exp": theta_m_exp,
                "FA": FA,
                "r": r,
                "phi_teorico": phi_teorico,
                "phi_exp": phi_exp,
                "T_exp": T_exp,
                "delta_t": delta_t,
            }

        return resultados
    
    def tabulate(self):
        """
        Devuelve un DataFrame con una fila por (estado, velocidad del motor).
        Columnas:
        - estado
        - f_motor (Hz) = rev/s del motor
        - w_f (rad/s)
        - P_m (N·m)
        - theta_m_teorico (rad)
        - theta_m_exp (rad)
        - FA
        - r = w_f/w_n
        - phi_teorico (rad)
        - phi_exp (rad)
        """
        resultados = self.result()

        filas = []
        for (estado, f_motor), vals in resultados.items():
            filas.append(
                {
                    "estado": estado,
                    "f_motor (Hz)": f_motor,                # Hz = rev/s
                    "w_f (rad/s)": vals["w_f"],
                    "P_m (N·m)": vals["P_m"],
                    "theta_m_teorico (rad)": vals["theta_m_teorico"],
                    "theta_m_exp (rad)": vals["theta_m_exp"],
                    "FA": vals["FA"],
                    "r = w_f/w_n": vals["r"],
                    "phi_teorico (rad)": vals["phi_teorico"],
                    "phi_exp (rad)": vals["phi_exp"],
                }
            )

        df = pd.DataFrame(filas).sort_values(["estado", "f_motor (Hz)"])
        return df
    

    
    def graf_resonance(self, n_points=500,  base="Forzada Amortiguada", save=False):
        """
        Grafica la curva de resonancia FA vs ωf/ωn para:
        - Caso abierto (ζ tomado de AnalisisLibreAmortiguado)
        - Caso cerrado (ζ idem)
        y superpone los puntos experimentales de FA obtenidos en self.result().
        """

        # ------------------------------
        # 1) Curvas teóricas
        # ------------------------------
        r_grid = np.linspace(0.4, 1.2, n_points)

        # Ya las tienes precalculadas en el __init__:
        # self.zeta = {"abierto": ζ_abierto, "cerrado": ζ_cerrado}
        # self.C    = {"abierto": C_abierto, "cerrado": C_cerrado}
        zetas = self.zeta
        Cs = self.C

        def FA_teorico(r, zeta):
            return 1.0 / np.sqrt((1.0 - r**2)**2 + (2.0 * zeta * r)**2)

        FA_abierto = FA_teorico(r_grid, zetas["abierto"])
        FA_cerrado = FA_teorico(r_grid, zetas["cerrado"])


        # ------------------------------
        # 2) Puntos experimentales
        # ------------------------------
        resultados = self.result()  # ya calcula FA y r para cada (estado, f)
        r_exp = []
        FA_exp = []

        for (estado, f_forzada), vals in resultados.items():
            r_exp.append(vals["r"])
            FA_exp.append(vals["FA"])

        r_exp = np.array(r_exp)
        FA_exp = np.array(FA_exp)

        # ------------------------------
        # 3) Gráfico
        # ------------------------------
        plt.figure()

        plt.plot(
            r_grid,
            FA_abierto,
            label=f"Abierta  (c = {Cs['abierto']:.2f} Ns/m)",
        )
        plt.plot(
            r_grid,
            FA_cerrado,
            label=f"Cerrada (c = {Cs['cerrado']:.2f} Ns/m)",
        )

        # Puntos experimentales en rojo
        plt.scatter(r_exp, FA_exp, color="red", zorder=5, label="Datos experimentales")

        # Línea vertical en la resonancia teórica (r = 1)
        plt.axvline(1.0, color="gray", linestyle="--")

        plt.xlabel(r"$\omega_f / \omega_n$")
        plt.ylabel("FA")
        plt.title("FA – amortiguador abierto vs cerrado")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()

        # Guardar si se pide
        if save:
            filename = base + "_resonancia_grafica.png"
            plt.savefig(filename, dpi=300, bbox_inches="tight")
            print(f"Gráfica exportada como: {filename}")
            plt.close()
        else:
            plt.show()
    
    def export(self, base="Forzada Amortiguada"):
        """
        Exporta:
        - la tabla procesada de vibración forzada (CSV)
        - la gráfica de FA vs r (PNG) usando graf_resonance()

        base : prefijo para los nombres de archivo exportados
        """

        # ===== EXPORTAR TABLA =====
        df = self.tabulate()
        csv_name = base + "_resonancia_resultados.csv"
        df.to_csv(csv_name, index=False, sep=";")
        print(f"Tabla exportada como: {csv_name}")

        # ===== EXPORTAR GRÁFICA =====
        self.graf_resonance(save=True, base=base)

    

analisis = AnalisisForzadaAmortiguado()

    
df = analisis.tabulate()

# Imprimir resultados en la terminal
print("\n===== TABLA DE RESULTADOS =====\n")
print(df.to_string(index=False))

analisis.graf_resonance()
analisis.export()