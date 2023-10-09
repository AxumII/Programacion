import pandas as pd
import numpy as np
from Integral_Fourier import Integral_Fourier as intf
import scipy.signal as sg

class ProcessSignal:
    
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
        if self.signal is None:
            print("No se han extraído variables de la señal.")
            return

        max_value = self.signal.max()
        min_value = self.signal.min()
        vpp = max_value - min_value

        iff = intf(self.t, self.signal, threshold=0.1)
        frecuencias, ft, integral = iff.result()
        frecP, armP = iff.mresult()

        def autocorrelation(signal):
            N = len(signal)
            autocorr = np.correlate(signal, signal, mode='full')  # Calcula la autocorrelación cruzada
            autocorr = autocorr / np.max(autocorr)  # Normaliza la autocorrelación
            return autocorr[N-1:]  # Conserva solo la mitad derecha de la autocorrelación

        autocorr = autocorrelation(self.signal)
        print(autocorr)
        peaks, _ = sg.find_peaks(autocorr, height=0.5)  # Ajusta el valor de "height" según tu caso
        is_periodic = len(peaks) > 1  # Se considera periódica si hay más de un pico en la autocorrelación

        
        
        

        # Crear un nuevo DataFrame con los resultados
        result_df = pd.DataFrame({
            'Máximo': [max_value],
            'Mínimo': [min_value],
            'Rango (Vpp)': [vpp],
            'Frecuencias Principales': [frecP],
            'Autocorrelacion': [autocorr.tolist()],  # Convierte el array de autocorrelación a una lista
            'Es Periódica': [is_periodic]
        })
        
        if is_periodic:
            # Calcular la frecuencia, ciclo de trabajo, RMS y valor promedio cuando la señal es periódica
            frequency = 1 / (self.t[peaks[1]] - self.t[peaks[0]])  # Frecuencia en Hz
            duty_cycle = (self.t[peaks[1]] - self.t[peaks[0]]) / (self.t[peaks[-1]] - self.t[peaks[0]])  # Ciclo de trabajo
            rms = np.sqrt(np.mean(np.square(self.signal)))  # Valor RMS
            average_value = np.mean(self.signal)  # Valor promedio
            
            # Crear un DataFrame adicional con los resultados cuando la señal es periódica
            periodic_result_df = pd.DataFrame({
                'Frecuencia (Hz)': [frequency],
                'Ciclo de Trabajo': [duty_cycle],
                'RMS': [rms],
                'Valor Promedio': [average_value]
            })
            
            print(result_df)
            print(periodic_result_df)
            return result_df, periodic_result_df

        print(result_df)
        return result_df

if __name__ == "__main__":
    processor = ProcessSignal("Generado.csv")
    processor.extract_csv()
    processor.variables()
    result_df = processor.analysis()
    
    # Imprimir el DataFrame con los resultados
    
