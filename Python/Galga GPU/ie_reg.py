import statsmodels.api as sm
import statsmodels.stats.diagnostic as smdg
import scipy.stats as st
import numpy as np
import pandas as pd
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
        return normal.results_table()

    def WLS(self):
        X = sm.add_constant(self.data["X"])
        y = self.data["Y"]

        # Obtener residuos del modelo OLS
        residuos = self.OLS().resid

        # Crear una copia del DataFrame con los residuos añadidos
        df = self.data.copy()
        df["residuos"] = residuos

        # Calcular la varianza de los residuos por grupo de X
        varianzas_por_grupo = df.groupby("X")["residuos"].var(ddof=1)

        # Mapear cada fila de X con su varianza correspondiente
        varianzas = df["X"].map(varianzas_por_grupo)

        # Evitar división por cero si alguna varianza es 0
        varianzas = varianzas.replace(0, 1e-8)

        # Calcular pesos inversos
        pesos = 1 / varianzas

        # Ajustar modelo WLS
        model = sm.WLS(y, X, weights=pesos).fit()
        return model
