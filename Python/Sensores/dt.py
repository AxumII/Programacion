import numpy as np
import statsmodels.api as sm
import scipy.stats as st
import matplotlib.pyplot as plt
import statsmodels.stats.diagnostic as smdg
import pandas as pd

class Dt:
    def __init__(self, v_values, f_values, alpha=0.05, m=5):
        self.v_values = np.asarray(v_values)
        self.f_values = np.asarray(f_values)
        self.alpha = alpha
        self.m = m

        # Crear DataFrame base
        self.data = pd.DataFrame({
            "X": self.f_values,
            "Y": self.v_values
        })


    def static_ch(self):

        # Modelos de regresión OLS
        model_ols = self.OLS()

        v_min = np.min(self.v_values)
        v_max = np.max(self.v_values)
        f_min = np.min(self.f_values)
        f_max = np.max(self.f_values)

        FSO = v_max # Full Scale Output (mV)
        out_range =  v_max - v_min
        in_range = f_max - f_min
        sens =  out_range/ in_range  # Sensibilidad (mV/Hz)

        # --- No linealidad ---
        residuos = model_ols.resid
        max_abs_dev_mV = np.max(np.abs(residuos))
        nonlin_pct = (max_abs_dev_mV / FSO) * 100 if FSO != 0 else np.nan

        # Guardamos como atributos
        self.FSO = FSO
        self.sens = sens
        self.out_range = out_range
        self.in_range = in_range
        self.nonlin_mV = max_abs_dev_mV
        self.nonlin_pct = nonlin_pct

        # También devolvemos como DataFrame, para usar en tabla de resultados
        df_static = pd.DataFrame({
            "Indicador": [
                "B0 (OLS) [mV]",
                "B1 (OLS) [mV/Hz]",
                "Error estándar (promedio) [mV]",
                "R²",
                "FSO [mV]",
                "Sensibilidad [mV/Hz]",
                "OutRange [mV]",
                "InRange [Hz]",
                "No-linealidad [%FSO]",
                "No-linealidad [mV]"
            ],
            "Valor": [
                float(model_ols.params[0]),
                float(model_ols.params[1]),
                float(model_ols.bse.mean()),
                float(model_ols.rsquared),
                float(FSO),
                float(sens),
                float(out_range),
                float(in_range),
                float(nonlin_pct),
                float(max_abs_dev_mV)
            ]
        }).set_index("Indicador").round(6)

        return df_static

    def OLS(self):
        X = sm.add_constant(self.f_values)
        model = sm.OLS(self.v_values, X).fit()
        return model

    def test_homsk(self):
        model = self.OLS()
        res = model.resid
        res_chunks = np.array_split(res, self.m)

        # Pruebas de homocedasticidad
        stat_levene, p_levene = st.levene(*res_chunks)
        stat_fligner, p_fligner = st.fligner(*res_chunks)
        stat_bartlett, p_bartlett = st.bartlett(*res_chunks)

        X = sm.add_constant(self.data["X"])
        white_lm_stat, white_lm_pvalue, white_f_stat, white_f_pvalue = smdg.het_white(res, X)
        bp_lm_stat, bp_lm_pvalue, bp_f_stat, bp_f_pvalue = smdg.het_breuschpagan(res, X)

        test_names = [
            "Levene", "Fligner", "Bartlett",
            "White (LM)", "White (F)",
            "Breusch-Pagan (LM)", "Breusch-Pagan (F)"
        ]

        p_values = [
            p_levene, p_fligner, p_bartlett,
            white_lm_pvalue, white_f_pvalue,
            bp_lm_pvalue, bp_f_pvalue
        ]

        decisions = [
            "Sí" if p > self.alpha else "No"
            for p in p_values
        ]

        df_pvalores = pd.DataFrame({
            "Test": test_names,
            "p-valor": p_values
        }).set_index("Test")

        df_veredictos = pd.DataFrame({
            "Test": test_names,
            "¿Homocedástico?": decisions
        }).set_index("Test")

        return df_pvalores, df_veredictos

    def test_norm_errores(self):
        res = self.OLS().resid
        shapiro_stat, shapiro_p = st.shapiro(res)
        jb_stat, jb_p, skew, kurt = sm.stats.stattools.jarque_bera(res)

        df = pd.DataFrame({
            "Test": ["Shapiro-Wilk", "Jarque-Bera"],
            "Estadístico": [shapiro_stat, jb_stat],
            "p-valor": [shapiro_p, jb_p],
            "¿Normal?": ["Sí" if p > self.alpha else "No" for p in [shapiro_p, jb_p]]
        }).set_index("Test")

        return df


    def WLS(self):
        """
        Ajusta un modelo WLS agrupando los datos de X en self.m grupos
        con cantidad uniforme de datos por grupo.
        """
        X = sm.add_constant(self.data["X"])
        y = self.data["Y"]

        # Modelo OLS inicial
        ols_model = self.OLS()
        residuos = ols_model.resid

        # Crear copia con residuos
        df = self.data.copy()
        df["residuos"] = residuos

        # Agrupar X en self.m intervalos de igual cantidad de datos (cuantiles)
        df["grupo"] = pd.qcut(df["X"], q=self.m, duplicates="drop")

        # Calcular varianza de los residuos en cada grupo
        varianzas_por_grupo = df.groupby("grupo")["residuos"].var(ddof=1)

        # Asignar la varianza correspondiente a cada observación (convertida a float)
        df["varianza"] = df["grupo"].map(varianzas_por_grupo).astype(float)

        # Si todas las varianzas son NaN, usar la varianza global de los residuos
        if df["varianza"].isna().all():
            df["varianza"] = np.var(residuos, ddof=1)

        # Reemplazar valores inválidos con el promedio numérico
        var_mean = np.nanmean(df["varianza"])
        df["varianza"] = df["varianza"].replace([0, np.nan, np.inf, -np.inf], var_mean)
        df["varianza"] = np.clip(df["varianza"], 1e-6, 1e6)

        # Pesos inversos
        pesos = 1.0 / df["varianza"]

        # Modelo WLS ajustado
        model_wls = sm.WLS(y, X, weights=pesos).fit()
        return model_wls


    def comparar_estadisticos(self, model_ols, model_wls):
        """Tabla comparativa limpia entre OLS y WLS"""
        estadisticos = [
            "Constante (β₀)",
            "X (β₁)",
            "Error estándar (promedio)",
            "t (promedio)",
            "p (promedio)",
            "R²",
            "R² ajustado",
            "σ² (varianza residual)"
        ]

        ols_vals = [
            model_ols.params[0],
            model_ols.params[1],
            model_ols.bse.mean(),
            model_ols.tvalues.mean(),
            model_ols.pvalues.mean(),
            model_ols.rsquared,
            model_ols.rsquared_adj,
            model_ols.scale
        ]

        wls_vals = [
            model_wls.params[0],
            model_wls.params[1],
            model_wls.bse.mean(),
            model_wls.tvalues.mean(),
            model_wls.pvalues.mean(),
            model_wls.rsquared,
            model_wls.rsquared_adj,
            model_wls.scale
        ]

        df_comparacion = pd.DataFrame({
            "Estadístico": estadisticos,
            "OLS": ols_vals,
            "WLS": wls_vals
        }).set_index("Estadístico")

        return df_comparacion.round(6)

    def plot_comparacion_OLS_WLS(self):
        model_ols = self.OLS()
        model_wls = self.WLS()

        # Obtener tablas de tests y comparaciones
        df_pval, df_resultados = self.test_homsk()
        df_comp = self.comparar_estadisticos(model_ols, model_wls)
        df_homsk = df_pval.copy()
        df_homsk["¿Homocedástico?"] = df_resultados["¿Homocedástico?"]

        # 📊 Calcular estáticos y no linealidad
        df_static = self.static_ch()

        # Crear figura 3x2 (dejamos una fila extra para la 5ta tabla)
        fig, axs = plt.subplots(3, 2, figsize=(14, 14))
        axs = axs.flatten()

        # 1️⃣ Datos + regresión
        axs[0].scatter(self.data["X"], self.data["Y"], label="Datos experimentales", color="steelblue", alpha=0.7)
        axs[0].plot(self.data["X"], model_ols.fittedvalues, label="OLS", color="orange", linewidth=2)
        axs[0].plot(self.data["X"], model_wls.fittedvalues, label="WLS", color="green", linestyle="--", linewidth=2)
        axs[0].set_title("Regresión: Voltaje [mV] vs Frecuencia [Hz]", fontsize=12)
        axs[0].set_xlabel("Frecuencia [Hz]", fontsize=10)
        axs[0].set_ylabel("Voltaje [mV]", fontsize=10)
        axs[0].legend()
        axs[0].grid(True, linestyle="--", alpha=0.6)

        # ➕ Mostrar ecuación OLS
        b0, b1 = model_ols.params
        eq_text = f"V = {b0:.3f} + {b1:.3f}·f"
        axs[0].text(0.05, 0.95, eq_text, transform=axs[0].transAxes,
                    fontsize=11, color="black", verticalalignment='top',
                    bbox=dict(facecolor='white', alpha=0.7, edgecolor='black'))

        # 2️⃣ Residuos
        axs[1].scatter(model_ols.fittedvalues, model_ols.resid, label="OLS", color="crimson", alpha=0.7)
        axs[1].scatter(model_wls.fittedvalues, model_wls.resid, label="WLS", color="darkgreen", alpha=0.7)
        axs[1].axhline(0, linestyle="--", color="black", linewidth=1)
        axs[1].set_title("Residuos: OLS vs WLS", fontsize=12)
        axs[1].set_xlabel("Voltaje ajustado [mV]", fontsize=10)
        axs[1].set_ylabel("Residuos [mV]", fontsize=10)
        axs[1].legend()
        axs[1].grid(True, linestyle="--", alpha=0.6)

        # 3️⃣ Tabla comparativa OLS vs WLS
        axs[2].axis("off")
        axs[2].set_title("Comparación de parámetros: OLS vs WLS", fontsize=12)
        tabla_comp = axs[2].table(cellText=df_comp.values,
                                rowLabels=df_comp.index,
                                colLabels=df_comp.columns,
                                loc="center")
        tabla_comp.auto_set_font_size(False)
        tabla_comp.set_fontsize(9)
        tabla_comp.scale(1.3, 1.3)

        # 4️⃣ Tabla de homocedasticidad
        axs[3].axis("off")
        axs[3].set_title("Tests de Homocedasticidad", fontsize=12)
        tabla_homsk = axs[3].table(cellText=df_homsk.values,
                                rowLabels=df_homsk.index,
                                colLabels=df_homsk.columns,
                                loc="center")
        tabla_homsk.auto_set_font_size(False)
        tabla_homsk.set_fontsize(9)
        tabla_homsk.scale(1.3, 1.3)

        # 5️⃣ Tabla de resultados estáticos (FSO, sensibilidad, no linealidad, etc.)
        axs[4].axis("off")
        axs[4].set_title("Resultados Estáticos del Sensor", fontsize=12)
        tabla_static = axs[4].table(cellText=df_static.values,
                                    rowLabels=df_static.index,
                                    colLabels=df_static.columns,
                                    loc="center")
        tabla_static.auto_set_font_size(False)
        tabla_static.set_fontsize(9)
        tabla_static.scale(1.3, 1.3)

        # Ocultamos el sexto subplot (no lo usamos)
        axs[5].axis("off")

        plt.tight_layout()
        plt.show()

#######################################
# Datos de prueba heterocedásticos
n = 100
np.random.seed(0)
X = np.linspace(0, 200, n)
Y = 20 + 7 * X + np.random.normal(0, 100+ 0.01*X, n)

dt = Dt(v_values=Y, f_values=X)
dt.plot_comparacion_OLS_WLS()
