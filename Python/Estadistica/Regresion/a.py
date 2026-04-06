import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st

class NormalModel:
    def __init__(self, data, hiperparams, nsim=10000):
        self.data = np.array(data).flatten()
        
        self.alpha_hp = hiperparams[0] 
        self.beta_hp = hiperparams[1] 
        self.nsim = nsim 
        
        if self.alpha_hp <= 0 or self.beta_hp <= 0:
            raise ValueError("Los hiperparámetros de la Gamma deben ser positivos.")
        
        # Estadísticas básicas
        self.s = np.sum(self.data) # Suma de los conteos (Estadístico suficiente)
        self.s2 = np.sum((self.data)**2)
        self.n = len(self.data)    # Tamaño de la muestra
        
        # Inicialización de atributos del posterior
        self.alpha_ps = None
        self.beta_ps = None
        self.media_ps_an = 0
        self.var_ps_an = 0
        self.ic_inf, self.ic_sup = 0, 0

    def graf_plot(self, x, y_list, labels, colors, title):
        plt.figure(figsize=(10, 5))
        for y, label, color in zip(y_list, labels, colors):
            plt.plot(x, y, label=label, color=color, lw=2.5)
            plt.fill_between(x, 0, y, color=color, alpha=0.1)
        plt.title(title)
        plt.xlabel(r"$\lambda$ (Tasa de ocurrencia)")
        plt.ylabel("Densidad")
        plt.legend()
        plt.grid(alpha=0.2)
        plt.show()

    def priori(self):
        # Definimos un rango de x basado en la media del prior
        mu_prior = self.alpha_hp / self.beta_hp
        x = np.linspace(0, mu_prior * 3, 500)
        y = st.gamma.pdf(x, self.alpha_hp, scale=1/self.beta_hp)
        self.graf_plot(x, [y], [f"Prior Gamma(α={self.alpha_hp}, β={self.beta_hp})"], ['orange'], "Distribución Prior")

    def muestral(self):
        # La verosimilitud Poisson es proporcional a: exp(-n*lambda) * lambda^(suma x)
        mu_mle = self.s / self.n
        x = np.linspace(0, mu_mle * 3, 500)
        likelihood = np.exp(-self.n * x) * (x**self.s)
        y_like = likelihood / np.trapezoid(likelihood, x) if self.n > 0 else np.ones_like(x)
        self.graf_plot(x, [y_like], ["Verosimilitud (Poisson)"], ['green'], "Evidencia de los Datos")

    def posteriori(self, show=False):
        # 1. Parámetros del posterior 
        self.alpha_ps = self.alpha_hp + self.s
        self.beta_ps = self.beta_hp + self.n
        
        # 2. Estimación analítica
        self.media_ps_an = self.alpha_ps / self.beta_ps
        self.var_ps_an = self.alpha_ps / (self.beta_ps**2)
        
        # 3. Monte Carlo
        np.random.seed(1111)
        # scipy usa scale = 1/beta
        samples_ps = st.gamma.rvs(self.alpha_ps, scale=1/self.beta_ps, size=self.nsim)
        self.media_ps_sim = np.mean(samples_ps)
        self.var_ps_sim = np.var(samples_ps)
        
        # 4. Intervalos de Credibilidad
        self.ic_inf, self.ic_sup = st.gamma.ppf([0.025, 0.975], self.alpha_ps, scale=1/self.beta_ps)
        
        if show:
            # Rango de visualización dinámico
            x_max = max(self.media_ps_an * 2, self.alpha_hp/self.beta_hp * 2)
            x = np.linspace(0, x_max, 500)
            
            y_prior = st.gamma.pdf(x, self.alpha_hp, scale=1/self.beta_hp)
            y_post = st.gamma.pdf(x, self.alpha_ps, scale=1/self.beta_ps)
            
            like = np.exp(-self.n * x) * (x**self.s)
            y_like = like / np.trapezoid(like, x)
            
            self.graf_plot(x, [y_prior, y_like, y_post], 
                           ['Prior', 'Verosimilitud', 'Posterior'], 
                           ['orange', 'green', 'blue'], 
                           "Actualización Poisson-Gamma")
            print(f"Media Posterior: {self.media_ps_an:.4f} | IC 95%: [{self.ic_inf:.4f}, {self.ic_sup:.4f}]")

    def predictiva(self, show=False):
        """
        En el modelo Poisson-Gamma, la predictiva es una Binomial Negativa
        pero se suele reportar la media, que es igual a la media del posterior.
        """
        if self.alpha_ps is None: self.posteriori(show=False)
        
        media_pred = self.alpha_ps / self.beta_ps
        
        if show:
            # Graficamos la probabilidad de observar k eventos en el futuro
            k = np.arange(0, st.poisson.ppf(0.99, media_pred))
            # La predictiva exacta es una Gamma-Poisson (Binomial Negativa)
            # p = beta / (beta + 1)
            p_nbinom = self.beta_ps / (self.beta_ps + 1)
            prob_k = st.nbinom.pmf(k, self.alpha_ps, p_nbinom)
            
            plt.figure(figsize=(8, 4))
            plt.stem(k, prob_k, basefmt=" ")
            plt.title(f"Distribución Predictiva Posterior (P. Próximo Conteos)")
            plt.xlabel("Número de eventos (k)")
            plt.ylabel("Probabilidad")
            plt.show()
        
        return media_pred

    def tab(self):
        self.posteriori(show=False)
        std_ps = np.sqrt(self.var_ps_an)
        ic_str = f"[{self.ic_inf:.4f}, {self.ic_sup:.4f}]"

        resumen = {
            "--- Prior (Gamma) ---": "",
            "Shape (alpha)": self.alpha_hp,
            "Rate (beta)": self.beta_hp,
            "Media Prior": round(self.alpha_hp / self.beta_hp, 4),
            "--- Muestra (Poisson) ---": "",
            "Suma conteos (s)": self.s,
            "Muestra (n)": self.n,
            "Media Muestral (x_bar)": round(self.s / self.n, 4),
            "--- Posterior ---": "",
            "Alpha Post": self.alpha_ps,
            "Beta Post": self.beta_ps,
            "Media Posterior": round(self.media_ps_an, 4),
            "Desv. Estándar": round(std_ps, 4),
            "IC 95%": ic_str,
            "--- Predictiva ---": "",
            "E[X_futuro]": round(self.media_ps_an, 4)
        }

        print(f"\n{'RESUMEN TÉCNICO POISSON-GAMMA':^50}")
        print(f"{'CONCEPTO':<35} | {'VALOR':<15}")
        print("-" * 55)
        for k, v in resumen.items():
            print(f"{k:<35} | {str(v):<15}")

# --- Ejemplo de ejecución ---
# Supongamos que contamos clientes que entran a una tienda por hora
# Datos: 5 horas observadas con los siguientes clientes:
clientes_por_hora = [10, 12, 8, 14, 11] 

# Prior: Creemos que la tasa es de 5 clientes por hora (alpha=5, beta=1)
hiper_creencia = [5, 1]

modelo_p = PoissonModel(data=clientes_por_hora, hiperparams=hiper_creencia)
modelo_p.tab()
modelo_p.posteriori(show=True)
modelo_p.predictiva(show=True)