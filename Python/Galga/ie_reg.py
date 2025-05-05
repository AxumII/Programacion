import statsmodels.api as sm
import statsmodels.stats.diagnostic as smdg
import scipy.stats as st
import numpy as np
import pandas as pd
from pb import N_fit as N_fit


class Estimador:
    def __init__(self,data, alpha = 0.05, n , m):
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

        # Tests por grupos
        stat_levene, p_levene = st.levene(*res_chunks)
        stat_fligner, p_fligner = st.fligner(*res_chunks)
        stat_bartlett, p_bartlett = st.bartlett(*res_chunks)

        # Variables explicativas
        X = sm.add_constant(self.data["X"])

        # Test de White
        white_lm_stat, white_lm_pvalue, white_f_stat, white_f_pvalue = smdg.het_white(res, X)

        # Test de Breusch-Pagan
        bp_lm_stat, bp_lm_pvalue, bp_f_stat, bp_f_pvalue = smdg.het_breuschpagan(res, X)

        # Construcción del DataFrame
        df = pd.DataFrame({
            "Test": [
                "Levene", "Fligner", "Bartlett",
                "White (LM)", "White (F)",
                "Breusch-Pagan (LM)", "Breusch-Pagan (F)"
            ],
            "Estadístico": [
                stat_levene, stat_fligner, stat_bartlett,
                white_lm_stat, white_f_stat,
                bp_lm_stat, bp_f_stat
            ],
            "p-valor": [
                p_levene, p_fligner, p_bartlett,
                white_lm_pvalue, white_f_pvalue,
                bp_lm_pvalue, bp_f_pvalue
            ],
            "¿Homocedástico?": [
                "Sí" if p > self.alpha else "No" for p in [
                    p_levene, p_fligner, p_bartlett,
                    white_lm_pvalue, white_f_pvalue,
                    bp_lm_pvalue, bp_f_pvalue
                ]
            ]
        })

        return df
    
    def test_norm_errores(self):
        res = self.OLS().resid
        normal = N_fit(data=res)
        return normal.results_table()

    def WLS(self):
        X = sm.add_constant(self.data["X"])
        y = self.data["Y"]

        res = self.OLS().resid
        res_chunks = np.array_split(res, self.m)
        # Calcula las varianzas por grupo
        varianzas_por_grupo = data.groupby("X")["residuos"].apply(lambda g: np.var(g, ddof=1))
        # Expandir varianzas para que cada fila tenga la suya correspondiente
        varianzas = data["X"].map(varianzas_por_grupo)
        # Evitar división por cero si la varianza es 0
        varianzas[varianzas == 0] = 1e-8

        pesos = 1 / varianzas
        model = sm.WLS(y, X, weights=pesos).fit()
        return model