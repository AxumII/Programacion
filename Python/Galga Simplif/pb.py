import pandas as pd
import numpy as np
import scipy.stats as st

class NFit:
    def __init__(self, data, alpha=0.05):
        self.data = data
        self.alpha = alpha
        self.nombres_tests = [
            "Shapiro-Wilk",
            "D’Agostino-Pearson",
            "Jarque-Bera",
            "Cramér-von Mises",
            "Anderson-Darling",
            "Kolmogorov-Smirnov"
        ]
        self.resultados_array = []
        self.pvalores_array = []
        self.all_tests()

    def normality_shapiro_test(self, data):
        stat, p = st.shapiro(data)
        return ("No" if p < self.alpha else "Si", p)

    def normality_normaltest(self, data):
        stat, p = st.normaltest(data)
        return ("No" if p < self.alpha else "Si", p)

    def normality_jarque_bera_test(self, data):
        stat, p = st.jarque_bera(data)
        return ("No" if p < self.alpha else "Si", p)

    def normality_cramer_test(self, data):
        data_std = (data - np.mean(data)) / np.std(data, ddof=1)
        res = st.cramervonmises(data_std, 'norm')

        return ("No" if res.pvalue < self.alpha else "Si", res.pvalue)

    def normality_anderson_test(self, data):
        res = st.anderson(data, dist='norm')
        index_5 = np.where(res.significance_level == 5)[0][0]
        critical = res.critical_values[index_5]
        p = np.nan  # Anderson no da p-valor
        resultado = "No" if res.statistic > critical else "Si"
        return (resultado, p)

    def normality_kolmogorov_test(self, data):
        data_std = (data - np.mean(data)) / np.std(data, ddof=1)
        stat, p = st.kstest(data_std, 'norm')
        return ("No" if p < self.alpha else "Si", p)

    def all_tests(self):
        tests = [
            self.normality_shapiro_test,
            self.normality_normaltest,
            self.normality_jarque_bera_test,
            self.normality_cramer_test,
            self.normality_anderson_test,
            self.normality_kolmogorov_test
        ]
        resultados, pvalores = zip(*[test(self.data) for test in tests])
        self.resultados_array = np.array(resultados)
        self.pvalores_array = np.array(pvalores)

    def table_results(self):
        return pd.DataFrame({
            "Test": self.nombres_tests,
            "¿Normal?": self.resultados_array
        })

    def table_pvalues(self):
        return pd.DataFrame({
            "Test": self.nombres_tests,
            "p-valor": self.pvalores_array
        })
