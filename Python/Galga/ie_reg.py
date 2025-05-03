import statsmodels.api as sm
import scipy.stats as st
import numpy as np
import pandas as pd

class Estimador:
    def __init__(self,data, df_m, alpha = 0.05):
        self.data = data
        self.df_m = df_m
        self.alpha = alpha
        self.n = df_m.shape[0]  #numero de elementos por muestra
        self.m = df_m.shape[1] #numero de muestras

    def test_homsk(self):
        muestras = [self.df_m[col] for col in self.df_m.columns]
        nombres_grupos = self.df_m.columns.tolist()
        varianzas = [grupo.var(ddof=1) for grupo in muestras]

        # Aplicar pruebas
        stat_levene, p_levene = st.levene(*muestras, center='median')  # Brown-Forsythe
        stat_fligner, p_fligner = st.fligner(*muestras)

        # Evaluar decisiones
        decision_levene = "Homocedásticas" if p_levene > self.alpha else "Heterocedásticas"
        decision_fligner = "Homocedásticas" if p_fligner > self.alpha else "Heterocedásticas"

        # Tabla de varianzas por grupo
        df_resultado = pd.DataFrame({
            "Grupo": nombres_grupos,
            "Varianza": varianzas
        })

       # Tabla resumen con mayor precisión
        resumen = pd.DataFrame([
            {
                "Método": "Brown-Forsythe",
                "p-value": f"{p_levene:.12f}",
                "Estadístico": round(stat_levene, 4),
                "Decisión": decision_levene
            },
            {
                "Método": "Fligner-Killeen",
                "p-value": f"{p_fligner:.12f}",
                "Estadístico": round(stat_fligner, 4),
                "Decisión": decision_fligner
            }
        ])

        return resumen
        

    def est_reg(self):
        pass

    def ic_reg(self):
        pass