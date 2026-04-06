import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st

class BernoulliModel:
    def __init__(self, data, hiperparams, nsim=10000):
        self.data = np.array(data).flatten()
        self.a_hp = hiperparams[0]
        self.b_hp = hiperparams[1]
        self.nsim = nsim 
        
        if self.a_hp <= 0 or self.b_hp <= 0:
            raise ValueError("Los hiperparámetros deben ser positivos.")
        
        # Estadísticas básicas de la muestra
        self.s = np.sum(self.data) 
        self.n = len(self.data)
        
        # Inicialización de atributos del posterior
        self.a_ps = None
        self.b_ps = None
        self.media_ps_an = 0
        self.var_ps_an = 0
        self.ic_inf, self.ic_sup = 0, 0
        self.p = 0

    def graf_plot(self, x, y_list, labels, colors, title):
        plt.figure(figsize=(10, 5))
        for y, label, color in zip(y_list, labels, colors):
            plt.plot(x, y, label=label, color=color, lw=2.5)
            plt.fill_between(x, 0, y, color=color, alpha=0.1)
        plt.title(title)
        plt.xlabel(r"$\theta$")
        plt.ylabel("Densidad")
        plt.legend()
        plt.grid(alpha=0.2)
        plt.show()

    def priori(self):
        x = np.linspace(0, 1, 500)
        y = st.beta.pdf(x, self.a_hp, self.b_hp)
        self.graf_plot(x, [y], [f"Prior Beta({self.a_hp}, {self.b_hp})"], ['orange'], "Distribución Prior")

    def muestral(self):
        x = np.linspace(0, 1, 500)
        likelihood = (x**self.s) * ((1 - x)**(self.n - self.s))
        y_like = likelihood / np.trapezoid(likelihood, x) if self.n > 0 else np.ones_like(x)
        self.graf_plot(x, [y_like], ["Verosimilitud (Muestra)"], ['green'], "Evidencia de los Datos")

    def posteriori(self, show=False):
        # 1. Parámetros del posterior (Actualización Bayesiana)
        self.a_ps = self.a_hp + self.s
        self.b_ps = self.b_hp + (self.n - self.s)
        
        # 2. Estimación analítica 
        self.media_ps_an = self.a_ps / (self.a_ps + self.b_ps)
        self.var_ps_an = (self.a_ps * self.b_ps) / ((self.a_ps + self.b_ps)**2 * (self.a_ps + self.b_ps + 1))
        
        # 3. Monte Carlo
        np.random.seed(1111)
        samples_ps = st.beta.rvs(a=self.a_ps, b=self.b_ps, size=self.nsim)
        self.media_ps_sim = np.mean(samples_ps)
        self.var_ps_sim = np.var(samples_ps)
        
        # 4. Intervalos y Probabilidad Predictiva
        self.ic_inf, self.ic_sup = st.beta.ppf([0.025, 0.975], self.a_ps, self.b_ps)
        self.p = self.media_ps_an 
        
        # 5. Comparación visual (Solo si show=True)
        if show:
            x = np.linspace(0, 1, 500)
            y_prior = st.beta.pdf(x, self.a_hp, self.b_hp)
            y_post = st.beta.pdf(x, self.a_ps, self.b_ps)
            
            like = (x**self.s) * ((1 - x)**(self.n - self.s))
            y_like = like / np.trapezoid(like, x)
            
            self.graf_plot(x, [y_prior, y_like, y_post], 
                           ['Prior', 'Verosimilitud (Muestra)', 'Posterior'], 
                           ['orange', 'green', 'blue'], 
                           "Actualización del Modelo")
            print(f"Media Posterior: {self.media_ps_an:.4f} | IC 95%: [{self.ic_inf:.4f}, {self.ic_sup:.4f}]")

    def predictiva(self, show=False):
        # Aseguramos que existan parámetros
        if self.a_ps is None:
            self.posteriori(show=False)
            
        if show:
            plt.figure(figsize=(6, 4))
            plt.bar(['0', '1'], [1 - self.p, self.p], color=['salmon', 'skyblue'])
            plt.title(f"Distribución Predictiva: P(Éxito) = {self.p:.4f}")
            plt.ylabel("Probabilidad")
            plt.show()

    def tab(self):
        """Ejecuta los cálculos y genera el resumen tabular"""
        # Ejecución automática de los cálculos en modo silencioso
        self.posteriori(show=False)
        self.predictiva(show=False)

        std_ps = np.sqrt(self.var_ps_an)
        ic_str = f"[{self.ic_inf:.4f}, {self.ic_sup:.4f}]"

        resumen = {
            "--- Prior (Beta) ---": "",
            "Alpha Prior (a)": self.a_hp,
            "Beta Prior (b)": self.b_hp,
            "--- Muestra (Data) ---": "",
            "Éxitos (s)": self.s,
            "Total Ensayos (n)": self.n,
            "Proporción (s/n)": round(self.s/self.n, 4) if self.n > 0 else 0,
            "--- Posterior (Calculado) ---": "",
            "Alpha Post (a_ps)": self.a_ps,
            "Beta Post (b_ps)": self.b_ps,
            "Media Posterior": round(self.media_ps_an, 4),
            "Desv. Estándar": round(std_ps, 4),
            "IC 95%": ic_str,
            "--- Predictiva ---": "",
            "P(Y=1 | Datos)": round(self.p, 4),
            "P(Y=0 | Datos)": round(1 - self.p, 4)
        }

        print(f"\n{'RESUMEN TÉCNICO DEL MODELO':^50}")
        print(f"{'CONCEPTO':<35} | {'VALOR':<15}")
        print("-" * 55)
        for k, v in resumen.items():
            print(f"{k:<35} | {str(v):<15}")

# --- Ejecución ---
datos_moneda = [1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1]
prior_hiper = [10, 3]

modelo = BernoulliModel(data=datos_moneda, hiperparams=prior_hiper, nsim=20000)

print("--- Iniciando Análisis Bayesiano ---")
# Puedes llamar a tab() directamente y él se encarga de lo demás
modelo.tab()

# Si quieres ver las gráficas específicamente, llamas a los métodos con show=True
# modelo.posteriori(show=True)
# modelo.predictiva(show=True)