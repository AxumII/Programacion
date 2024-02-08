import serial
import matplotlib.pyplot as plt
import pandas as pd

class ReadSignal():
    def __init__(self, usbPort, baudrate, fm, collection_time, title=None):
        self.usbPort = usbPort
        self.baudrate = baudrate
        self.fm = fm
        self.pm = 1 / fm
        self.data_frame = pd.DataFrame()  # Inicializamos el DataFrame sin columnas
        self.countTime = 0
        self.collection_time = collection_time
        self.title = title

    def connect(self):
        return serial.Serial(self.usbPort, baudrate=self.baudrate)

    def collectData(self):
        ser = self.connect()
        
        while True:
            try:
                data = ser.readline().decode('utf-8').strip()
                values = [float(val) for val in data.split()]
                
                # Creamos un diccionario para la nueva fila
                new_row = {'Tiempo': self.countTime * self.pm}
                # Añadimos los valores de cada señal al diccionario
                for i, value in enumerate(values):
                    new_row[f'Senal {i+1}'] = value
                
                # Usamos pd.concat para añadir la nueva fila al DataFrame
                self.data_frame = pd.concat([self.data_frame, pd.DataFrame([new_row])], ignore_index=True)
                
                self.countTime += 1
                
                if self.countTime * self.pm >= self.collection_time:
                    break
                
            except ValueError as e:
                print(f"Error al convertir los datos: {e}")
            except KeyboardInterrupt:
                print("Lectura del puerto serial detenida.")
                ser.close()
                break

        ser.close()

        print(self.data_frame)

        if self.title is not None:
            self.plot_and_save_data()

    def plot_and_save_data(self):
        # Guardar los datos en un archivo CSV
        self.data_frame.to_csv(self.title + '.csv', index=False)

        plt.figure(figsize=(10, 6))
        # Plotear cada una de las señales
        for i in range(1, len(self.data_frame.columns)):
            plt.plot(self.data_frame['Tiempo'], self.data_frame[f'Senal {i}'], label=f"Senal {i}")

        plt.xlabel("Tiempo (s)", fontsize=12, fontstyle="italic")
        plt.ylabel("Valor", fontsize=12, fontstyle="italic")
        plt.title(self.title if self.title else "Plot de Señales")
        plt.legend()

        data_plot_filename = self.title + '.png'
        plt.savefig(data_plot_filename)
        plt.show()





# Ejemplo de uso
lector = ReadSignal('COM8', 115200, fm=50, collection_time=2, title='Lectura')
lector.collectData()
