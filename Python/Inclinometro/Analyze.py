import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import math

class Analysis:
    def __init__(self, resolution: float) -> None:
        self.resolution = resolution
        self.data = None
        self.temp_mean = None
        self.time_mean = None
        self.uncertainties = {}

    def load_data(self, file_path: str = "datosMPU6050.csv") -> None:
        self.data = pd.read_csv(file_path)
        self.time_mean = self.data.iloc[:, 0].mean()
        self.temp_mean = self.data.iloc[:, -1].mean()

    def normality_shapiro_test(self, data):
        statistic, p_value = stats.shapiro(data)
        alpha = 0.05
        return "No" if p_value < alpha else "Si"
        
    def normality_normaltest(self, data):
        statistic, p_value = stats.normaltest(data)
        alpha = 0.05
        return "No" if p_value < alpha else "Si"

    def normality_jarque_bera_test(self, data):
        statistic, p_value = stats.jarque_bera(data)
        alpha = 0.05
        return "No" if p_value < alpha else "Si"

    def normality_cramer_test(self, data):
        res = stats.cramervonmises(data, 'norm')
        alpha = 0.05
        return "No" if res.pvalue < alpha else "Si"
        
    def calculate_statistics(self) -> pd.DataFrame:
        columns = self.data.columns[1:-1]
        stats_dict = {
            "Estadísticos": ["Media Muestral", "Desviación Estándar", "Varianza Muestral", "Shapiro-Wilk", "Normaltest", "Jarque-Bera", "Cramer-Von Mises"]
        }
        
        for col in columns:
            stats_dict[col] = [
                self.data[col].mean(),
                self.data[col].std(),
                self.data[col].var(),
                self.normality_shapiro_test(self.data[col]),
                self.normality_normaltest(self.data[col]),
                self.normality_jarque_bera_test(self.data[col]),
                self.normality_cramer_test(self.data[col])
            ]
        
        return pd.DataFrame(stats_dict)
    
    def calculate_uncertainties(self) -> pd.DataFrame:
        columns = self.data.columns[1:-1]
        incertidumbre_dict = {
            "Incertidumbres": ["Incertidumbre Tipo A", "Incertidumbre por Resolución", "Incertidumbre por Temperatura", "Incertidumbre por Calibración", "Incertidumbre Combinada ", "Factor de Cobertura", "Incertidumbre Expandida (Tipo B)", "Grados de Libertad"]
        }

        for col in columns:
            n = len(self.data[col])
            std_dev = self.data[col].std()
            mean = self.data[col].mean()
            
            # Incertidumbre tipo A
            incertidumbre_type_A = std_dev / np.sqrt(n)*0
            
            # Incertidumbre por resolución
            incertidumbre_resolution = self.resolution / np.sqrt(12)
            
            # Incertidumbre por temperatura
            incertidumbre_temp = self.temp_mean * 0.0002
            
            # Incertidumbre por calibración
            incertidumbre_calibration = abs(mean * 0.03)
            
            # Incertidumbre combinada
            incertidumbre_combinada = np.sqrt(
                incertidumbre_type_A**2 + 
                incertidumbre_resolution**2 + 
                incertidumbre_temp**2 + 
                incertidumbre_calibration**2
            )
            
            # Cálculo de grados de libertad efectivos usando la aproximación de Welch-Satterthwaite
            degrees_of_freedom = (incertidumbre_combinada**4) / (
                (incertidumbre_type_A**4 / (n - 1)) + 
                (incertidumbre_resolution**4 / float('inf')) + 
                (incertidumbre_temp**4 / float('inf')) + 
                (incertidumbre_calibration**4 / float('inf'))
            )
            
            # Factor de cobertura (usando k=2 para distribución normal)
            factor_k = 2 if (self.normality_shapiro_test(self.data[col]) == "Si" or
                             self.normality_cramer_test(self.data[col]) == "Si" or
                             self.normality_jarque_bera_test(self.data[col]) == "Si" or
                             self.normality_normaltest(self.data[col]) == "Si") else stats.t.ppf(0.975, degrees_of_freedom)
            
            # Incertidumbre expandida
            incertidumbre_expandida = factor_k * incertidumbre_combinada

            self.uncertainties[col] = incertidumbre_expandida
            
            incertidumbre_dict[col] = [
                incertidumbre_type_A,
                incertidumbre_resolution,
                incertidumbre_temp,
                incertidumbre_calibration,
                incertidumbre_combinada,
                factor_k,
                incertidumbre_expandida,
                degrees_of_freedom
            ]
        
        return pd.DataFrame(incertidumbre_dict)
    
    def plot_data(self) -> None:
        columns = self.data.columns[1:-1]
        num_plots = len(columns)
        fig, axs = plt.subplots((num_plots + 1) // 2, 2, figsize=(12, num_plots * 2))
        axs = axs.flatten()
        
        for i, col in enumerate(columns):
            axs[i].plot(self.data.iloc[:, 0], self.data[col], label=col)
            axs[i].set_xlabel("Tiempo")
            axs[i].set_ylabel(col)
            axs[i].set_title(f"Datos de {col}")
            axs[i].legend()
        
        for i in range(num_plots, len(axs)):
            fig.delaxes(axs[i])
        
        plt.tight_layout()
        plt.show()

    def plot_histograms(self) -> None:
        columns = self.data.columns[1:-1]
        num_plots = len(columns)
        fig, axs = plt.subplots((num_plots + 1) // 2, 2, figsize=(12, num_plots * 2))
        axs = axs.flatten()
        
        for i, col in enumerate(columns):
            bins = np.histogram_bin_edges(self.data[col], bins='auto')
            axs[i].hist(self.data[col], bins=bins, alpha=0.7, color='b', edgecolor='black', density=True)
            
            # Añadir la distribución normal
            mean = self.data[col].mean()
            std_dev = self.data[col].std()
            x = np.linspace(self.data[col].min(), self.data[col].max(), 100)
            p = stats.norm.pdf(x, mean, std_dev)
            axs[i].plot(x, p, 'k', linewidth=2)
            
            # Añadir líneas de incertidumbre expandida
            incertidumbre_expandida = self.uncertainties[col]
            axs[i].axvline(mean + incertidumbre_expandida, color='r', linestyle='dashed', linewidth=1)
            axs[i].axvline(mean - incertidumbre_expandida, color='r', linestyle='dashed', linewidth=1)
            
            title = f"Histograma de {col}\nMedia = {mean:.2f}, Desviación Estándar = {std_dev:.2f}"
            axs[i].set_title(title)
            axs[i].set_xlabel(col)
            axs[i].set_ylabel("Frecuencia")
        
        for i in range(num_plots, len(axs)):
            fig.delaxes(axs[i])
        
        plt.tight_layout()
        plt.show()

    def print_means(self) -> None:
        print(f"Promedio del tiempo: {self.time_mean}")
        print(f"Promedio de la temperatura: {self.temp_mean}")

# Uso del código
"""
g = 9.80665
nbits = 2e16
analysis = Analysis(resolution=(2*g/nbits))
analysis.load_data("datosMPU6050.csv")
estadisticos_basicos = analysis.calculate_statistics()
incertidumbres = analysis.calculate_uncertainties()
analysis.print_means()
print(estadisticos_basicos)
print(incertidumbres)
analysis.plot_data()
analysis.plot_histograms()
"""