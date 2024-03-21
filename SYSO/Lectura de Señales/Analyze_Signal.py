import pandas as pd
import numpy as np
import scipy.signal as sg
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit 
from scipy import stats


from Generator import Generator as gen



class AnalyzeSignal:
    def __init__(self, csv_title):
        self.csv_title = csv_title  # Corrected the variable name here to match with the rest of the code.
        self.df = None
        self.t = None
        self.signals = []

    def extract_csv(self):
        try:
            self.df = pd.read_csv(self.csv_title)
            print(f"Archivo {self.csv_title} cargado correctamente.")
            return self.df
        except FileNotFoundError:
            print(f"El archivo {self.csv_title} no se encontró.")
            return None
        except Exception as e:
            print(f"Se produjo un error al leer el archivo CSV: {str(e)}")
            return None

    def variables(self):
        if self.df is None:
            print("No se ha cargado ningún DataFrame.")
            return        
        self.t = self.df.iloc[:, 0].to_numpy()
        self.signals = [self.df[col].to_numpy() for col in self.df.columns[1:]]

        print("Hay", len(self.signals), "señales")
        
        print(f"Tipo de dato de t: {type(self.t)}")
        for i, signal in enumerate(self.signals):
            print(f"Tipo de dato de signals[{i}]: {type(signal)}")
            
    def simpleAnalysis(self, vectores):
        if isinstance(vectores, np.ndarray):
            vectores = [vectores]

        results = pd.DataFrame(columns=['Maximo', 'Minimo', 'Rango', 'FFT'])

        for i, vector in enumerate(vectores):
            if vector.size == 0:
                continue
            
            maximo = np.max(vector)
            minimo = np.min(vector)
            rango = maximo - minimo
            fft_result = np.fft.fft(vector)
            
            results.loc[i] = [maximo, minimo, rango, fft_result]
            
            

        return results

    # Corrección: Añadir 'self' como primer argumento en la definición del método
    def simplecharacterize(self, t, vectores):
        results = pd.DataFrame(columns=['Periodic', 'Linear', 'Polynomial', 'Normal'])
        for i, signal in enumerate(vectores):
            if signal.size == 0:
                continue
            autocorr = self.autocorrelation(signal)
            periodic = self.is_periodic(autocorr)
            linear = self.linear_regression(t, signal)
            polynomial = self.polynomial_regression(t, signal)
            normal = self.jarque_bera_test(signal)
            results.loc[i] = [periodic, linear, polynomial, normal]
        return results

    def periodicAnalysis(self, t, vectores):
        results = pd.DataFrame(columns=['Frecuencias', 'FFT', 'Ciclo de trabajo', 'RMS', 'Valor promedio'])

        for i, signal in enumerate(vectores):
            if signal.size == 0:
                continue

            autocorr = self.autocorrelation(signal)
            peaks, _ = sg.find_peaks(autocorr, height=0.1 * np.max(autocorr))
            fft_result = np.fft.fft(signal)
            frequencies = np.fft.fftfreq(len(signal), d=t[1]-t[0])
            
            if len(peaks) > 1:
                frequency = 1 / (t[peaks[1]] - t[peaks[0]])  # Frecuencia en Hz
                duty_cycle = np.mean(signal > 0)  # Ciclo de trabajo
            else:
                frequency = 0
                duty_cycle = 0

            rms = np.sqrt(np.mean(np.square(signal)))  # Valor RMS
            average_value = np.mean(signal)  # Valor promedio

            results.loc[i] = [frequencies, fft_result, duty_cycle, rms, average_value]

        return results

    def nLRegression(self, vInd, vDep, modelo):
        

        # Ajuste del modelo a los datos
        params, params_covariance = curve_fit(modelo, vInd, vDep)
        
        # Calcula el modelo con los parámetros optimizados
        fitted_model = modelo(vInd, *params)

        # Crear DataFrame para los resultados
        results_df = pd.DataFrame({'Parameter': params}, index=[f'Param {i+1}' for i in range(len(params))])

        # Crear la gráfica
        plt.figure(figsize=(10, 6))
        plt.plot(vInd, vDep, label='Datos', color='green')
        plt.plot(vInd, fitted_model, color='red', label='Modelo')
        plt.title('Regresion')
        plt.xlabel('Variable Independiente')
        plt.ylabel('Variable Dependiente')
        plt.legend()
        plt.show()

        return results_df
        
        

  
  
###############################################################      
    def autocorrelation(self,signal):
        """Compute the autocorrelation of the signal."""
        return np.correlate(signal, signal, mode='full')[len(signal)-1:]

    def is_periodic(self,autocorr):
        """Determine if a signal is periodic based on its autocorrelation."""
        return np.any(autocorr > (0.1 * autocorr[0]))

    def linear_regression(self,t, signal):
        """Perform linear regression and return the R-squared value."""
        slope, intercept, r_value, p_value, std_err = stats.linregress(t, signal)
        return r_value**2

    def polynomial_regression(self,t, signal, degree=2):
        """Perform polynomial regression and return the R-squared value."""
        coeffs = np.polyfit(t, signal, degree)
        p = np.poly1d(coeffs)
        # Calculate the r-squared value
        yhat = p(t)                         # or [p(z) for z in x]
        ybar = np.sum(signal)/len(signal)          # or sum(y)/len(y)
        ssreg = np.sum((yhat-ybar)**2)   # or sum([ (yihat - ybar)**2 for yihat in yhat])
        sstot = np.sum((signal - ybar)**2)    # or sum([ (yi - ybar)**2 for yi in y])
        return ssreg / sstot

    def jarque_bera_test(self,signal):
        """Perform Jarque-Bera test and return if the signal is normally distributed based on the test result."""
        _, p_value = stats.jarque_bera(signal)
        return p_value > 0.05  # Assuming alpha of 0.05 for normality
    
    
    
######################################################################################

analyzer = AnalyzeSignal('Generado.csv')


df_extracted = analyzer.extract_csv()
analyzer.variables()

# Análisis simple
simple_analysis_results = analyzer.simpleAnalysis(analyzer.signals)
print("Resultados del Análisis Simple:")
print(simple_analysis_results)

# Caracterización simple
simple_characterization_results = analyzer.simplecharacterize(analyzer.t, analyzer.signals)
print("Resultados de la Caracterización Simple:")
print(simple_characterization_results)


def exponential_model(x, a, b):
    return a * np.exp(b * x)

def polinomial_model(x , d, e , f, h):
    return  d*x**e + f*x + h

regression_results = analyzer.nLRegression(analyzer.t,analyzer.signals[0], polinomial_model)

print(regression_results)
