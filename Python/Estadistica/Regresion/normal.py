import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st

class NormalModel:
    #Modelo Normal Gamma Inversa
    def __init__(self, data, hiperparams, nsim=10000):
        self.data = np.array(data).flatten()
        
        self.u_hp = hiperparams[0] 
        self.sigma2_hp = hiperparams[1] 
        self.alpha_hp = hiperparams[2] 
        self.beta_hp = hiperparams[3]
        self.kappa_hp =  hiperparams[4]
        self.nsim = nsim 
        
        if self.alpha_hp <= 0 or self.beta_hp <= 0:
            raise ValueError("Los hiperparámetros de la Gamma deben ser positivos.")
        
        # Estadísticas básicas
        self.mean = np.mean(self.data) #(Estadístico suficiente 1)
        self.var = np.var(self.data) #(Estadístico suficiente 2)
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
        sigma2 = np.linspace(0.1, self.beta_hp * 3, 200)
        u = np.linspace(self.u_hp - 2, self.u_hp + 2, 200)
        """P= (u,sigma2) = P(u|sigma2)*P(sigma2)
        """
        #P(sigma2)
        p_sigma = st.invgamma.pdf(x = sigma2, self.alpha_hp, self.beta_hp)
        #P(u|sigma2)
        p_u_sigma = st.norm.pdf(x = u, loc = self.u_hp, scale = self.sigma2_hp / self.kappa_hp)
        
        y = p_u_sigma*p_sigma
        self.graf_plot(x, [y], [f"Prior Gamma(α={self.alpha_hp}, β={self.beta_hp})"], ['orange'], "Distribución Prior")
   
    def muestral(self):
        """Calcula la Verosimilitud conjunta L(mu, sigma2)""" 
        m_mean = self.mean
        s2 = self.var
        x = np.linspace(0, * 3, 500)
        likelihood = (s2**(-self.n/2)) * np.exp(-m_mean / (2 * m_mean))
        y_like = likelihood / np.trapezoid(likelihood, x) if self.n > 0 else np.ones_like(x)
        self.graf_plot(x, [y_like], ["Verosimilitud (Normal)"], ['green'], "Evidencia de los Datos")

    def posteriori(self, show=False):
        # 1. Parámetros del posterior
        self.kappa_ps = self.kappa_hp + self.n
        self.u_ps = (self.kappa_hp/self.kappa_ps)*self.u_hp + (self.n/self.kappa_ps)*self.mean
        self.sigma_ps = 1
        
        # 2. Monte Carlo
        np.random.seed(1111)
        # scipy usa scale = 1/beta
        #P(sigma2)
        p_sigma = st.invgamma.pdf(x = self.sigma2_ps, self.alpha_hp, self.beta_hp)
        #P(u|sigma2)
        p_u_sigma = st.norm.pdf(x = u, loc = self.u_hp, scale = self.sigma2_hp / self.kappa_hp)
        
        y = p_u_sigma*p_sigma
        
        
        self.media_ps_sim = np.mean(samples_ps)
        self.var_ps_sim = np.var(samples_ps)
        