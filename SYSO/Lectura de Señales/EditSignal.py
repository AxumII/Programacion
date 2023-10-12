import serial
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class ReadSignal():
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
        
        print("iniciales")
        print(self.signal)
        #print(self.t)    

    def clip(self, umbral_clip, eliminar_mayores=True, eliminar_menores=True):
        if self.signal is None or self.t is None:
            raise ValueError("No se han cargado los datos de señal y tiempo.")

        indices_a_eliminar = []

        if eliminar_mayores:
            indices_a_eliminar.extend(np.where(self.signal > umbral_clip)[0])

        if eliminar_menores:
            indices_a_eliminar.extend(np.where(self.signal < umbral_clip)[0])

        indices_a_eliminar = np.unique(indices_a_eliminar).astype(int)

        print(indices_a_eliminar)

        self.signal = np.delete(self.signal, indices_a_eliminar)
        self.t = np.delete(self.t, indices_a_eliminar)

        self.t -= self.t[0]

        

        """
        print("Recorte")
        print(self.signal)
        print(self.t)"""

    def offset(self, offset_value):
        
        if self.signal is None:
            print("La señal no está definida.")
            return

        
        self.signal += offset_value
            
        
        """
        print("Desfase")
        print(self.signal)
        print(self.t)"""
    
    def graf(self):
        if self.signal is None or self.t is None:
            print("La señal o el tiempo no están definidos.")
            return
        print(len(self.signal))

        plt.plot(self.t, self.signal)
        plt.xlabel("Tiempo")
        plt.ylabel("Señal")
        plt.title("Señal Procesada")
        plt.show()
        
    def save(self, output_csv_filename):
        if self.signal is None or self.t is None:
            print("No hay datos para guardar.")
            return

        # Create a DataFrame from the signal and time data
        data_to_save = pd.DataFrame({'Time': self.t, 'Signal': self.signal})

        try:
            # Save the data to a CSV file
            data_to_save.to_csv(output_csv_filename, index=False)
            print(f"Data saved to {output_csv_filename}")
            
        except Exception as e:
            print(f"Error while saving data: {str(e)}")
        
####################################################################################        
        

# Ejemplo de uso:
if __name__ == "__main__":
    
    name = "Prueba2.csv"
    # Crear una instancia de la clase ReadSignal
    reader = ReadSignal('a.csv')

    # Extraer datos del archivo CSV
    df = reader.extract_csv()

    if df is not None:
        
        reader.variables()

        #Recordar que esta en mV, osea 1000 a 5000
        reader.clip(4400,eliminar_mayores=True, eliminar_menores=False)  # Puedes especificar límites aquí

        
        #reader.offset(offset_value=-108)  # Puedes especificar el valor del desfase aquí

        
        reader.graf()
        
        reader.save("Prueba2_1.csv")
