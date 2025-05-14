import scipy.stats as st
import numpy as np


class Estimator:
    def __init__(self, muestra, alpha):
        self.muestra = muestra
        self.alpha = alpha
        self.n = muestra.shape[0]  # Tamaño de la muestra

    def est_norm(self):  # Estimadores de distribución normal
        X_m = np.mean(self.muestra)               # Media muestral
        Sn2_m = np.var(self.muestra, ddof=1)      # Varianza muestral (ddof=1)
        #Usa el estimador sesgado, dado a que es el MLE, mas no usa el insesgado ya que se asume 
        #que se usaran muestras grandes
        return X_m, Sn2_m

    def ic_norm(self):
        X_m, Sn2_m = self.est_norm()

        # IC para la media 
        margen = st.t.ppf(1 - self.alpha / 2, self.n - 1) * np.sqrt(Sn2_m / self.n)
        X_m_min = X_m - margen
        X_m_max = X_m + margen

        # IC para la varianza 
        chi_l = st.chi2.ppf(self.alpha / 2, df=self.n - 1)  
        chi_u = st.chi2.ppf(1 - self.alpha / 2, df=self.n - 1)  

        var_min = ((self.n - 1) * Sn2_m) / chi_u  
        var_max = ((self.n - 1) * Sn2_m) / chi_l  

        return {
            "media": (X_m_min, X_m_max),
            "varianza": (var_min, var_max)
        }