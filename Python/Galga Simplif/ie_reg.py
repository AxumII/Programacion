import statsmodels.api as sm
import statsmodels.stats.diagnostic as smdg
import scipy.stats as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pandas.plotting import table
from pb import NFit as N_fit



class Estimador:
    def __init__(self, data,n, m , alpha = 0.05):
        self.data = data
        self.alpha = alpha
        self.n = n #numero de elementos por muestra
        self.m = m #numero de muestras

    def OLS(self):
        X = sm.add_constant(self.data["X"])
        y = self.data["Y"]
        model = sm.OLS(y, X).fit()
        return model

    def test_homsk(self):
        res = self.OLS().resid
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
        normal = N_fit(data=res)
        return normal.table_results()

    def WLS(self):
        X = sm.add_constant(self.data["X"], has_constant='add')
        y = self.data["Y"]

        # Obtener residuos del modelo OLS
        residuos = self.OLS().resid

        # Copia del DataFrame con residuos
        df = self.data.copy()
        df["residuos"] = residuos

        # Varianzas por grupo de X
        varianzas_por_grupo = df.groupby("X")["residuos"].var(ddof=1)
        varianzas = df["X"].map(varianzas_por_grupo)

        # Reemplazar valores inválidos o extremos
        varianzas = varianzas.replace([0, np.nan, np.inf, -np.inf], 1e-6)
        varianzas = np.clip(varianzas, 1e-6, 1e6)

        # Pesos inversos
        pesos = 1 / varianzas

        # Modelo WLS ajustado
        model = sm.WLS(y, X, weights=pesos).fit()
        return model


    def plot_comparacion_OLS_WLS(self):
        model_ols = self.OLS()
        model_wls = self.WLS()

        # Cálculo de residuos
        df_pval, df_resultados = self.test_homsk()

        # Subplot 1: Comparación de regresiones
        fig, axs = plt.subplots(1, 3, figsize=(18, 6), gridspec_kw={'width_ratios': [1.2, 1.2, 1]})

        # Gráfico de datos y regresiones
        axs[0].scatter(self.data["X"], self.data["Y"], label="Datos", color="steelblue", alpha=0.6)
        axs[0].plot(self.data["X"], model_ols.fittedvalues, label="OLS", color="orange", linewidth=2)
        axs[0].plot(self.data["X"], model_wls.fittedvalues, label="WLS", color="green", linestyle="--", linewidth=2)
        axs[0].set_title("Regresión: OLS vs WLS")
        axs[0].set_xlabel("Voltage")
        axs[0].set_ylabel("Model Output")
        axs[0].legend()
        axs[0].grid(True)

        # Gráfico de residuos
        axs[1].scatter(model_ols.fittedvalues, model_ols.resid, label="OLS", color="crimson", alpha=0.6)
        axs[1].scatter(model_wls.fittedvalues, model_wls.resid, label="WLS", color="darkgreen", alpha=0.6)
        axs[1].axhline(0, linestyle="--", color="black")
        axs[1].set_title("Residuos: OLS vs WLS")
        axs[1].set_xlabel("Valores Ajustados")
        axs[1].set_ylabel("Residuos")
        axs[1].legend()
        axs[1].grid(True)

        # Tabla de homocedasticidad
        axs[2].axis('off')
        axs[2].set_title("Homocedasticidad", fontsize=12)
        tabla = table(axs[2], df_resultados, loc='center')
        tabla.auto_set_font_size(False)
        tabla.set_fontsize(9)
        tabla.scale(1.2, 1.2)

        plt.tight_layout()
        plt.show()
