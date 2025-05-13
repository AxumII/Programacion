import pandas as pd
import numpy as np
import scipy.stats as st

class N_fit:
    def __init__(self, data, alpha = 0.05):
        self.data = data
        self.alpha = alpha
        self.nombres_tests = [
            "Shapiro-Wilk",
            "D’Agostino-Pearson",
            "Jarque-Bera",
            "Cramér-von Mises",
            "Anderson-Darling",
            "Kolmogorov-Smirnov",
            "Lilliefors"
        ]
        self.resultados_array = []
        self.pvalores_array = []
        self.all_tests()
#NO Parametricas
    def normality_shapiro_test(self, data):
        statistic, p_value = st.shapiro(data)        
        return "No" if p_value < self.alpha else "Si"
        
    def normality_normaltest(self, data):
        statistic, p_value = st.normaltest(data)
        return "No" if p_value < self.alpha else "Si"

    def normality_jarque_bera_test(self, data):
        statistic, p_value = st.jarque_bera(data)
        return "No" if p_value < self.alpha else "Si"

    def normality_cramer_test(self, data):
        res = st.cramervonmises(data, 'norm')
        return "No" if res.pvalue < self.alpha else "Si"
#Parametricas
   
    def normality_anderson_test(self, data):
        res = st.anderson(data, dist='norm')
        alpha = 5  # 5% nivel de significancia
        index_5 = np.where(res.significance_level == alpha)[0][0]
        critical_value = res.critical_values[index_5]
        return "No" if res.statistic > critical_value else "Si"

    def normality_kolmogorov_test(self, data):
        data_standardized = (data - np.mean(data)) / np.std(data, ddof=1)
        statistic, p_value = st.kstest(data_standardized, 'norm')
        return "No" if p_value < self.alpha else "Si"
    
    def normality_lilliefors_test(self, data):
        statistic, p_value = st.lilliefors(data)
        return ("No" if p_value < self.alpha else "Si", p_value)
    
    #poner tambien las del libro, los test de comparacion

    def all_tests(self):
        
        tests = [
        self.normality_shapiro_test,
        self.normality_normaltest,
        self.normality_jarque_bera_test,
        self.normality_cramer_test,
        self.normality_anderson_test,
        self.normality_kolmogorov_test,
        self.normality_lilliefors_test
        ]

        self.resultados_array, self.pvalores_array = zip(*[test(self.data) for test in tests])
        self.resultados_array = np.array(self.resultados_array)
        self.pvalores_array = np.array(self.pvalores_array)

        conteo_si = np.sum(self.resultados_array == "Si")
        conteo_no = len(self.resultados_array) - conteo_si

        return self.resultados_array, conteo_si, conteo_no

    def results_table(self):
        if not self.resultados_array or not self.pvalores_array.any():
            self.all_tests()

        df = pd.DataFrame({
            "Test": self.nombres_tests,
            "¿Normal?": self.resultados_array,
            "p-valor": self.pvalores_array
        })
        return df
