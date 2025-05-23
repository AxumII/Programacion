import pandas as pd
import numpy as np

import os
from pb import NFit as Nf
from ie_one_s import Estimator as Est
from ie_reg import Estimador as EstReg

from unc_gauge_gpu import UncGauge
from unc_dist_gpu import UncDistance as UncD

from montecarlo_sens_unc import Monteca

from model_gauge_gpu import Model

from derivation import Derivation
import matplotlib.pyplot as plt
from pandas.plotting import table


class Executable:
    def __init__(self, file_names, datasheet_values, datasheet_values_d,instrument_values):
        self.file_names = file_names
        self.dataframes = {}
        self.load_status = {}
        self.df_resultados_pb = None
        self.df_pvalores_pb = None
        self.df_ic_estimadores = None
        self.df_homsk_pvalores = None
        self.df_homsk_resultados = None
        self.df_normalidad_errores = None
        self.datasheet_values = datasheet_values
        self.datasheet_values_d = datasheet_values_d
        self.instrument_values = instrument_values
        self.unc_df = None
        self.unc_df_deriv = None
        self.montecarlo_array = None 
        self.montecarlo_df = None
        self.df_sobol = None
        self.df_unc_sobol = None
        self.u_exp_sobol  = None
        self.df_unc_deriv = None
        self.u_exp_deriv = None
        self.df_comparation = None

    def loader(self):
        for name in self.file_names:
            filename = f"{name}.csv"
            try:
                df = pd.read_csv(filename)
                self.dataframes[f"data_{name}"] = df
                self.load_status[name] = "CARGADO"
            except Exception as e:
                self.dataframes[f"data_{name}"] = None
                self.load_status[name] = f"ERROR: {str(e)}"

    def statistical_analysis_single_samples(self):
        resultados_dict = {}
        pvalores_dict = {}
        index_tests = None
        ic_rows = []

        for key, df in self.dataframes.items():
            if df is None:
                continue

            colname = df.columns[0]
            data_array = df[colname].to_numpy()

            result_n_t = Nf(data_array)
            df_resultados = result_n_t.table_results()
            df_pvalores = result_n_t.table_pvalues()

            if index_tests is None:
                index_tests = df_resultados["Test"].values

            resultados_dict[key] = df_resultados["¿Normal?"].values
            pvalores_dict[key] = df_pvalores["p-valor"].values

            I_e = Est(muestra=data_array, alpha=0.05)
            X_barra, Sn2 = I_e.est_norm()
            ic = I_e.ic_norm()

            ic_rows.append({
                "Variable": key,
                "X̄ (Media)": X_barra,
                "Sn² (Varianza)": Sn2,
                "IC Media Min": ic["media"][0],
                "IC Media Max": ic["media"][1],
                "IC Varianza Min": ic["varianza"][0],
                "IC Varianza Max": ic["varianza"][1]
            })

        self.df_resultados_pb = pd.DataFrame(resultados_dict, index=index_tests)
        self.df_pvalores_pb = pd.DataFrame(pvalores_dict, index=index_tests)
        self.df_ic_estimadores = pd.DataFrame(ic_rows)
        conteo_si = self.df_resultados_pb.apply(lambda col: (col == "Si").sum())
        self.df_resultados_pb.loc["Total 'Si'"] = conteo_si
        print("\n=== Variables disponibles para incertidumbre ===")
        print(self.df_ic_estimadores["Variable"].tolist())

    def adjust_input_unc_gauge(self):
        inputs_tipo_a_b = {}
        inputs_tipo_b = {}
        inputs_tipo_a_b_dist = {}
        inputs_tipo_b_dist = {}
        num_values = {}
        inputs_distance = ["hg","b","h","L", "x"]
        datasheet_dict = self.datasheet_values.set_index("Variable").to_dict("index")
        datasheet_d_dict = self.datasheet_values_d.set_index("Variable").to_dict("index")
        instrument_dict = self.instrument_values.set_index("Variable").to_dict("index")
        desvest_dict = self.df_ic_estimadores.set_index("Variable")["Sn² (Varianza)"].apply(np.sqrt).to_dict()
        mean_dict = self.df_ic_estimadores.set_index("Variable")["X̄ (Media)"].to_dict()
        map_var_to_name = {
            "voltage_measurement": "Vlect",
            "voltage_input": "Vi",
            "mass": "m",
            "phi": "phi",
            "T": "T",
            "theta": "theta"
        }

        map_var_sub = {
            "high_grid": "hg",
            "base_cell": "b",
            "high_cell": "h",
            "L_force": "L",
            "L_def": "x"
        }

        map_var_to_instr = {
            "Vlect": "ADC",
            "Vi": "Voltimeter",
            "m": "Scales",
            "phi": "Angle Sensor",
            "T": "Thermometer"
        }
        # tipo A+B principal (excluye submodelo)
        for raw_name, std in desvest_dict.items():
            raw_clean = raw_name.replace("data_", "")
            if raw_clean in map_var_sub:
                continue
            name = map_var_to_name.get(raw_clean, raw_clean)
            mean = mean_dict[raw_name]
            num_values[name] = mean

            instr_name = map_var_to_instr.get(name, None)
            resol = instrument_dict.get(instr_name, {}).get("Resolution", None)
            calib = instrument_dict.get(instr_name, {}).get("Calibration", None)

            inputs_tipo_a_b[name] = (None, name, resol, calib, std)

        
        # tipo B general
        for var, props in datasheet_dict.items():
            nominal = props["Nominal Value"]
            tol = props["+-%"]
            num_values[var] = nominal
            inputs_tipo_b[var] = (var, None, (nominal * tol) / np.sqrt(3))

      

        # tipo B submodelo
        for var, props in datasheet_d_dict.items():
            nominal = props["Nominal Value"]
            tol = props["+-%"]
            num_values[var] = nominal
            inputs_tipo_b_dist[var] = (var, None, nominal * tol)

    

        # tipo A submodelo
        for raw_name, std in desvest_dict.items():
            raw_clean = raw_name.replace("data_", "")
            if raw_clean in ["T", "theta"]:
                name = map_var_to_name.get(raw_clean, raw_clean)
                mean = mean_dict[raw_name]
                inputs_tipo_a_b_dist[name] = (None, name, None, None, std)
                num_values[name] = mean

 

        # calcular submodelo por cada distancia
        for var in inputs_distance:
            val = num_values[var]
            instr_name = "Vernier"
            resol = instrument_dict.get(instr_name, {}).get("Resolution", None)
            calib = instrument_dict.get(instr_name, {}).get("Calibration", None)
            inputs_tipo_a_b_dist_local = {
                "d_mean": (None, "d_mean", resol, calib, None),
                "T": inputs_tipo_a_b_dist["T"],
                "theta": inputs_tipo_a_b_dist["theta"]
            }
            num_values_local = {**num_values, "d_mean": val}

            unc_sub = UncD(
                num_values=num_values_local,
                inputs_tipo_a_b_dist=inputs_tipo_a_b_dist_local,
                inputs_tipo_b_dist=inputs_tipo_b_dist,
                sensitivity_dict=None
            )
            unc_sub.calculate()
            u_exp = unc_sub.unc_expanded(k=3)
            inputs_tipo_b[var] = (var, None, float(u_exp))
            inputs_tipo_a_b[var] = (None, var, None, None, float(u_exp))

        return inputs_tipo_a_b, inputs_tipo_b, inputs_tipo_a_b_dist,inputs_tipo_b_dist, inputs_distance, num_values

    def uncertainly_gauge_default(self, sensitivity_dict = None):
        
        inputs_tipo_a_b, inputs_tipo_b, inputs_tipo_a_b_dist,inputs_tipo_b_dist, inputs_distance, num_values = self.adjust_input_unc_gauge()
        
        self.unc = UncGauge(
        num_values=num_values,
        inputs_tipo_a_b=inputs_tipo_a_b,
        inputs_tipo_b=inputs_tipo_b,
        inputs_tipo_a_b_dist=inputs_tipo_a_b_dist,
        inputs_tipo_b_dist=inputs_tipo_b_dist,
        inputs_distance=inputs_distance,
        sensitivity_dict= sensitivity_dict
        )
        self.unc.calculate()
        self.unc.unc_expanded()
        return self.unc.df_gen , self.unc.u_exp
        
    def montecarlo_gauge_model(self, n_iter=100):
        distribuciones = self.distribution_generator()
        print("\n🎲 Ejecutando simulación Monte Carlo...")
        mc = Mcg(n=n_iter, distribuciones=distribuciones)
        mc.generar_muestras()
        self.montecarlo_array = mc.simulation()
        self.montecarlo_df = mc.resumen_estadistico()
        mc.graficar_resultados()

    def sobol(self, n_iter = 2**4):
        distribuciones = self.distribution_generator()
        sobol = Sb(n=n_iter, distribuciones = distribuciones)
        sobol.calculate()
        Y = sobol.run_model()
        resultados = sobol.analyze(Y)
        sobol.plot_sobol_indices()

        nombres = sobol.problem["names"]
        s1 = resultados["S1"]
        st = resultados["ST"]

        # Crear DataFrame
        df_sobol = pd.DataFrame({
            "Variable": nombres,
            "S1 (Primer Orden)": s1,
            "ST (Total)": st
        })

        self.df_sobol =  df_sobol
        
    def distribution_generator(self):
        if self.df_ic_estimadores is None:
            raise ValueError("Primero ejecuta `statistical_analysis_single_samples()` para obtener medias.")
        if not hasattr(self, 'unc') or self.unc is None or not hasattr(self.unc, 'df_gen'):
            raise ValueError("Primero ejecuta `uncertainly_gauge_default()` para generar la tabla de incertidumbre.")

        df_unc = self.unc.df_gen
        distribuciones = {}

        # === solo usar las variables que están en el modelo ===
        vars_modelo = {
            "Vlect", "K", "R1", "R2", "R3", "RG", "RL", "Vi", "GF", "v", "phi",
            "hg", "m", "g", "L", "x", "E", "b", "h", "lg"
        }

        # === 1. Combinar incertidumbres por variable ===
        incertidumbres_combinadas = {}
        for _, row in df_unc.iterrows():
            name = row["Name"]
            u = row["Uncertainty"]
            if pd.isna(u):
                continue
            var = name.split(" of ")[-1].strip()
            if var not in vars_modelo:
                continue
            incertidumbres_combinadas.setdefault(var, []).append(u)

        # === 2. Construir normales solo para variables válidas ===
        for var, lista_u in incertidumbres_combinadas.items():
            std_total = np.sqrt(sum(u**2 for u in lista_u))
            if var in self.df_ic_estimadores["Variable"].values:
                media = self.df_ic_estimadores.set_index("Variable").at[var, "X̄ (Media)"]
            else:
                media = 0.0
            distribuciones[var] = {
                "tipo": "normal",
                "params": {
                    "media": media,
                    "desv": std_total
                }
            }

        # === 3. Uniformes desde datasheet (general, NO submodelo) ===
        if self.datasheet_values is not None:
            for _, row in self.datasheet_values.iterrows():
                var = row["Variable"]
                if var not in vars_modelo:
                    continue
                nominal = row["Nominal Value"]
                tol = row["+-%"]
                min_val = nominal * (1 - tol)
                max_val = nominal * (1 + tol)
                distribuciones[var] = {
                    "tipo": "uniform",
                    "params": {"min": min_val, "max": max_val}
                }

        return distribuciones

    def uncertainly_with_sens(self):
        #Sobol
        sensitivity_dict_sobol = dict(zip(self.df_sobol["Variable"], self.df_sobol["S1 (Primer Orden)"]))
        sensitivity_dict_sobol.update({
            "delta_0": 1.0,
            "delta_paral":0,
            "delta_F": 0,
            "delta_desg":0,
            "delta_h": 0
        })
        self.df_unc_sobol, self.u_exp_sobol = self.uncertainly_gauge_default(sensitivity_dict = sensitivity_dict_sobol)
        
        
        #Derivacion
        __, __ , __ , __ , __ , num_values =self.adjust_input_unc_gauge()

        deriv = Derivation(model_class=Model, input_values=num_values)
        # Derivar y evaluar
        deriv.build_symbolic_model()
        self.sensitivity_dict_deriv = deriv.evaluate_derivatives()
        self.df_unc_deriv, self.u_exp_deriv = self.uncertainly_gauge_default(sensitivity_dict = self.sensitivity_dict_deriv)
        

    def comparar_sensibilidades(self, plot=True):
        if self.df_sobol is None or self.sensitivity_dict_deriv is None:
            raise ValueError("Faltan datos de sensibilidad. Asegúrate de haber ejecutado 'uncertainly_with_sens()' primero.")

        # Crear DataFrame con ambas sensibilidades
        df_comparacion = pd.DataFrame()
        df_comparacion["Variable"] = self.df_sobol["Variable"]
        df_comparacion["Sobol_S1"] = self.df_sobol["S1 (Primer Orden)"]
        df_comparacion["Derivada"] = df_comparacion["Variable"].map(self.sensitivity_dict_deriv)

        if plot:
            # Gráfico de barras agrupadas: Sobol vs Derivada
            x = np.arange(len(df_comparacion["Variable"]))  # posiciones para el eje X
            width = 0.35

            plt.figure(figsize=(14, 6))
            plt.bar(x - width/2, df_comparacion["Sobol_S1"], width, label='Sobol S1', color='steelblue')
            plt.bar(x + width/2, df_comparacion["Derivada"], width, label='Derivada', color='darkorange')

            plt.xticks(x, df_comparacion["Variable"], rotation=45, ha='right')
            plt.ylabel("Sensibilidad")
            plt.title("Comparación de Coeficientes de Sensibilidad")
            plt.legend()
            plt.grid(axis="y", linestyle="--", alpha=0.7)
            plt.tight_layout()
            plt.show()

            self.df_comparacion = df_comparacion
  
    def regression_analysis_def_v(self):
        # Cargar archivo CSV
        try:
            df_voltage = pd.read_csv("voltage_complete.csv")
        except FileNotFoundError:
            print("❌ Error: No se encontró el archivo 'voltage_complete.csv'.")
            return
        except Exception as e:
            print(f"❌ Error al leer el archivo: {e}")
            return
        if df_voltage.shape[1] == 0:
            print("❌ El archivo está vacío o no tiene columnas válidas.")
            return

        colname = df_voltage.columns[0]
        voltajes = df_voltage[colname].to_numpy()

        # Obtener valores base del modelo
        _, _, _, _, _, num_values = self.adjust_input_unc_gauge()

        # Evaluar modelo para cada voltaje
        model_outputs = []
        for v in voltajes:
            try:
                model = Model(
                    Vlect=v,
                    K=num_values["K"],
                    R1=num_values["R1"],
                    R2=num_values["R2"],
                    R3=num_values["R3"],
                    RG=num_values["RG"],
                    RL=num_values["RL"],
                    Vi=num_values["Vi"],
                    GF=num_values["GF"],
                    v=num_values["v"],
                    phi=num_values["phi"],
                    hg=num_values["hg"],
                    m=num_values["m"],
                    g=num_values["g"],
                    L=num_values["L"],
                    x=num_values["x"],
                    E=num_values["E"],
                    b=num_values["b"],
                    h=num_values["h"],
                    lg=num_values["lg"]
                )
                output = model.calculate()
                model_outputs.append(float(output))
            except Exception as e:
                print(f"⚠️ Error al evaluar el modelo con Vlect={v}: {e}")
                model_outputs.append(np.nan)

        df_reg = pd.DataFrame({
            "X": voltajes,
            "Y": model_outputs
        })

        self.df_voltage_regression = df_reg

                # Ajustar regresión
        est = EstReg(data=df_reg, n=len(df_reg), m=5)
        model = est.OLS()
        self.df_summary_ols = model.summary2().tables[1]  
        self.df_norm_errores = est.test_norm_errores()
        self.df_pvalores_homsk, self.df_resultados_homsk = est.test_homsk()

        # Mostrar comparación gráfica OLS vs WLS + tabla homocedasticidad
        est.plot_comparacion_OLS_WLS()

        print("✅ Regresión completada. Datos disponibles en:")
        print("- self.df_voltage_regression")
        print("- self.df_summary_ols")
        print("- self.df_pvalores_homsk")
        print("- self.df_resultados_homsk")
        print("- self.df_norm_errores")

    def regression_analysis_m_v(self):


        # Cargar archivo CSV
        try:
            df_voltage = pd.read_csv("voltage_complete.csv")
        except FileNotFoundError:
            print("❌ Error: No se encontró el archivo 'voltage_complete.csv'.")
            return
        except Exception as e:
            print(f"❌ Error al leer el archivo: {e}")
            return
        if df_voltage.shape[1] == 0:
            print("❌ El archivo está vacío o no tiene columnas válidas.")
            return

        colname = df_voltage.columns[0]
        voltajes = df_voltage[colname].to_numpy()

        # Obtener valores base del modelo
        _, _, _, _, _, num_values = self.adjust_input_unc_gauge()

        # Evaluar modelo para cada voltaje
        model_outputs = []
        for v in voltajes:
            try:
                model = MassModel(
                    Vlect=v,
                    K=num_values["K"],
                    R1=num_values["R1"],
                    R2=num_values["R2"],
                    R3=num_values["R3"],
                    RG=num_values["RG"],
                    RL=num_values["RL"],
                    Vi=num_values["Vi"],
                    GF=num_values["GF"],
                    v=num_values["v"],
                    phi=num_values["phi"],
                    hg=num_values["hg"],
                    g=num_values["g"],
                    L=num_values["L"],
                    x=num_values["x"],
                    E=num_values["E"],
                    b=num_values["b"],
                    h=num_values["h"],
                    lg=num_values["lg"]
                )
                result = model.calculate()
                if isinstance(result, list) and len(result) > 0:
                    model_outputs.append(float(result[0]))  # toma la solución válida
                else:
                    model_outputs.append(np.nan)
            except Exception as e:
                print(f"⚠️ Error al evaluar el modelo con Vlect={v}: {e}")
                model_outputs.append(np.nan)

        df_reg = pd.DataFrame({
            "X": voltajes,
            "Y": model_outputs
        }).dropna()

        self.df_mass_regression = df_reg

        # Ajustar regresión
        est = EstReg(data=df_reg, n=len(df_reg), m=5)
        model = est.OLS()
        self.df_summary_ols_m_v = model.summary2().tables[1]
        self.df_norm_errores_m_v = est.test_norm_errores()
        self.df_pvalores_homsk_m_v, self.df_resultados_homsk_m_v = est.test_homsk()

        # Mostrar gráfica comparativa y tabla de homocedasticidad
        est.plot_comparacion_OLS_WLS()

        print("✅ Regresión masa vs voltaje completada.")
        print("- self.df_mass_regression")
        print("- self.df_summary_ols_m_v")
        print("- self.df_pvalores_homsk_m_v")
        print("- self.df_resultados_homsk_m_v")
        print("- self.df_norm_errores_m_v")



    def df_process(self):
        dfs_a_mostrar = [
            ("Resultados Pruebas de Bondad", self.df_resultados_pb),
            ("P-valores", self.df_pvalores_pb),
            ("Estimadores", self.df_ic_estimadores),
            ("Incertidumbre General", self.unc.df_gen if hasattr(self, "unc") else None),
            ("Resumen Monte Carlo", self.montecarlo_df),
            ("Sensibilidad Sobol", self.df_sobol),
            ("Incertidumbre con Sobol", self.df_unc_sobol),
            ("Incertidumbre con Derivadas", self.df_unc_deriv),
            ("Comparación de Sensibilidades", self.df_comparacion),
        ]

        for titulo, df in dfs_a_mostrar:
            if df is None:
                continue
            fig, ax = plt.subplots(figsize=(min(20, max(8, len(df.columns) * 2)), min(12, max(6, len(df) * 0.5))))
            ax.axis('off')
            tabla = ax.table(cellText=df.values, colLabels=df.columns, rowLabels=df.index if df.index.name or df.index.any() else None, loc='center')
            tabla.auto_set_font_size(False)
            tabla.set_fontsize(8)
            tabla.scale(1.2, 1.2)
            plt.title(titulo, fontsize=14, fontweight='bold')
            plt.tight_layout()
            plt.show()



if __name__ == "__main__":
    archivos = [
        "voltage_measurement", "voltage input", "mass", "phi",
        "L_force", "base_cell", "high_cell", "L_def",
        "high_grid", "T", "theta", "voltage_input"
    ]

    datasheet_values = pd.DataFrame({
        "Variable": ["R1", "R2", "R3", "RG", "RL", "GF", "v", "g", "E", "K", "lg"],
        "Nominal Value": [120, 120, 120, 120, 0.1, 2.1, 0.33, 9.7805, 6.9e10, 200, 1],
        "+-%": [0.01, 0.01, 0.01, 0.1, 0.01, 0.2, 0.1, 0.0001, 0.01, 0.02, 0.03]
    })

    instrument_values = pd.DataFrame({
        "Variable": ["ADC", "Voltimeter", "Scales", "Angle Sensor", "Thermometer", "Vernier"],
        "Resolution": [5/2**10, None, 0.01, np.pi/180, None, 0.02*10**-3],
        "Calibration": [None, 0.01, 0.01, None, 0.5, None]
    })

    datasheet_values_d = pd.DataFrame({
        "Variable": ["L", "hg", "x", "b", "h"],
        "Nominal Value": [1.2, 0.2, 0.8, 0.01, 0.005],
        "+-%": [0.03, 0.02, 0.04, 0.05, 0.07]
    })

    exe = Executable(archivos, datasheet_values,datasheet_values_d ,instrument_values)
    exe.loader()
    exe.statistical_analysis_single_samples()
    """
    exe.uncertainly_gauge_default()
    exe.montecarlo_gauge_model(n_iter = 100)
    exe.sobol(n_iter = 2**2)
    exe.uncertainly_with_sens()    
    exe.comparar_sensibilidades()"""

    #exe.regression_analysis_def_v()
    exe.regression_analysis_m_v()
    exe.df_process()
    