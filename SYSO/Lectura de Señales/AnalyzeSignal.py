import pandas as pd
import numpy as np
import scipy.signal as sg
import matplotlib.pyplot as plt

from scipy.optimize import curve_fit as fitnl


from Generator import Generator as gen
from Integral_Fourier import Integral_Fourier as intf





class AnalyzeSignal:
    
    def __init__(self, csvtitle):
        self.csvtitle = csvtitle
        self.df = None
        self.signal = None
        self.t = None
    
    def extract_csv(self):
        try:
            # Lee el archivo CSV y lo convierte en un DataFrame
            df = pd.read_csv(self.csvtitle)
            self.df = df
            return df
        except FileNotFoundError:
            print(f"El archivo {self.csvtitle} no se encontró.")
            return None
        except Exception as e:
            print(f"Se produjo un error al leer el archivo CSV: {str(e)}")
            return None



    def variables(self):
        if self.df is None:
            print("No se ha cargado ningún DataFrame.")
            return
        # Obtener la primera columna del DataFrame
        self.signal = self.df.iloc[:, 1]
        self.t = self.df.iloc[:, 0]


    def analysis(self):
        ###################################################################################################################
        #FUNCIONES UTILES PARA REALIZAR ANALISIS
        
        ########################################################################################################################
        #AUTOCORRELACION PARA PERIODICAS
        def autocorrelation(signal):
            N = len(signal)
            autocorr = np.correlate(signal, signal, mode='full')  # Calcula la autocorrelación cruzada
            autocorr = autocorr / np.max(autocorr)  # Normaliza la autocorrelación
            return autocorr[N-1:]  # Conserva solo la mitad derecha de la autocorrelación
        
        
        #REGRESION EN GENERAL
        def regresion(x_data, y_data, funcion):
            
            params, covariance = fitnl(funcion, x_data, y_data)
            a, b = params
            
            residuals = y_data - funcion(x_data, a, b)
            ss_res = np.sum(residuals**2)
            ss_tot = np.sum((y_data - np.mean(y_data))**2)
            r_2 = 1 - (ss_res / ss_tot)
            
            return params, r_2

        def graf(x, y, funcion=None):
            fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 8))

            ax1.plot(x, y, color='green')
            ax1.set_title('Señal 1')
            ax1.set_xlabel('Tiempo')
            ax1.set_ylabel('Amplitud')
            ax1.grid(True)

            if funcion is not None:
                
                
                ax2.plot(x, funcion, color='red')
                ax2.set_title('Fteorica')
                ax2.set_xlabel('Tiempo')
                ax2.set_ylabel('Amplitud')
                ax2.grid(True)

                ax3.plot(x, y, color='green')
                ax3.plot(x, funcion, color='red')
                ax3.set_title('Ambas')
                ax3.set_xlabel('Tiempo')
                ax3.set_ylabel('Amplitud')
                ax3.grid(True)
            else:
                pass

            plt.tight_layout()
            plt.show()
                    
        def expon(x, a, b):
            return a * np.exp(b * x)

        #####################################################################################################################
        
        #CODIGO DE ANALISIS
        #####################################################################################################################
        if self.signal is None:
            print("No se han extraído variables de la señal.")
            return

        #Extremos
        max_value = self.signal.max()
        min_value = self.signal.min()
        vpp = max_value - min_value

        #Fourier (usa el propio)
        iff = intf(self.t, self.signal, threshold=0.1)
        frecuencias, ft, integral = iff.result()
        frecP, armP = iff.mresult()
        
        #Autocorrelacion para periodica
        autocorr = autocorrelation(self.signal)        
        peaks, _ = sg.find_peaks(autocorr, height=0.8)  # Ajusta el valor de "height" según tu caso
        is_periodic = len(peaks) > 1  # Se considera periódica si hay más de un pico en la autocorrelación
        
        #Exponencial Propuesta
        
        rc = -0.0046389
        rc_inv = rc ** -1        
        exponencial = expon(self.t,-1*rc_inv,rc_inv)
        
        
        reg_exp = regresion(self.t,self.signal,expon) #Regresion Exponencial, pasa la funcion como parametro, no los datos
        
        is_exponential = reg_exp[1] > 0.8
        
        
        # Dataframe de resultados
        result_df = pd.DataFrame({
            'Máximo': [max_value],
            'Mínimo': [min_value],
            'Rango (Vpp)': [vpp],
            'Frecuencias Principales': [frecP],            
            'Es Periódica': [is_periodic],
            'Es Exponencial' : [is_exponential]
        })
        
        #print(exponencial)
        
        graf(self.t,self.signal, exponencial)
        
        
        
        ##################################################################################################################################################
        ##################################################################################################################################################
        
        #CASO PERIODICO
        
        if is_periodic:
            # Calcular la frecuencia, ciclo de trabajo, RMS y valor promedio cuando la señal es periódica
            frequency = 1 / (self.t[peaks[1]] - self.t[peaks[0]])  # Frecuencia en Hz
            duty_cycle = (self.t[peaks[1]] - self.t[peaks[0]]) / (self.t[peaks[-1]] - self.t[peaks[0]])  # Ciclo de trabajo
            rms = np.sqrt(np.mean(np.square(self.signal)))  # Valor RMS
            average_value = np.mean(self.signal)  # Valor promedio
            
            
            
            # Crear un DataFrame adicional con los resultados cuando la señal es periódica
            periodic_df = pd.DataFrame({
                'Frecuencia (Hz)': [frequency],
                'Ciclo de Trabajo': [duty_cycle],
                'RMS': [rms],
                'Valor Promedio': [average_value]
            })
            
            print(result_df)
            print(periodic_df)
            return result_df, periodic_df


        #CASO EXPONENCIAL
        if is_exponential:
            a,b = reg_exp[0]
            r_2 = reg_exp[1]
            
   
            exp_df = pd.DataFrame({
                'a': [a],
                'b': [b],
                'r_2': [r_2]
            })
            
            
            print(result_df)
            print(exp_df)
            return result_df, exp_df


        
        ###############################################################################################
        #Final
        print(result_df)
        return result_df


if __name__ == "__main__":
    processor = AnalyzeSignal("Prueba2.csv")
    processor.extract_csv()
    processor.variables()
    result_df = processor.analysis()
    
    # Imprimir el DataFrame con los resultados
    
