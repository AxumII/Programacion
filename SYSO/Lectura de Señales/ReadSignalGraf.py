import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import pandas as pd

class ReadSignalGraf():
    def __init__(self, usbPort, baudrate, fm, title=None):
        self.usbPort = usbPort
        self.baudrate = baudrate
        self.fm = fm
        self.pm = 1 / fm
        self.data_frame = pd.DataFrame({'Tiempo (s)': [], 'Datos Seriales': []})
        self.countTime = 0        
        self.title = title

    def connect(self):
        return serial.Serial(self.usbPort, baudrate=self.baudrate)

    def realTimeGraf(self):
        ser = self.connect()
        fig, ax = plt.subplots()
        line, = ax.plot([], [])
        ax.set_ylim(-6000, 6000)
        ax.set_xlabel("Tiempo (s)", fontsize=12, fontstyle="italic")
        ax.set_ylabel("Voltaje (mV)", fontsize=12, fontstyle="italic")

        def update(frame):
            try:
                data = ser.readline().decode('utf-8').strip()
                y_value = float(data)
                
                self.data_frame.loc[self.countTime] = [self.countTime * self.pm, y_value]
                line.set_data(self.data_frame['Tiempo (s)'], self.data_frame['Datos Seriales'])
                
                ax.set_xlim(0, max(10, self.countTime * self.pm + 2))
                self.countTime += 1
            except ValueError:
                pass
            except KeyboardInterrupt:
                print("Lectura del puerto serial detenida.")
                ser.close()

        #plt.grid(True)

        ani = FuncAnimation(fig, update, frames=None, repeat=False, blit=False, interval=int(self.pm * 1000))  # Corregido el intervalo en milisegundos

        # El color y la etiqueta (label) deben configurarse en el objeto 'line' en lugar de 'FuncAnimation'
        line.set_color('red')
        #line.set_label('Voltaje')

        plt.legend(fontsize=10, loc="upper right")
        plt.show()
        ser.close()
        
        print(self.data_frame)
        
        if self.title is not None:
            self.plot_and_save_data()
        
    def plot_and_save_data(self):
        # Guardar los datos en un archivo CSV
        self.data_frame.to_csv(self.title + '.csv', index=False)
        
        plt.figure(figsize=(10, 6))
        plt.plot(self.data_frame['Tiempo (s)'], self.data_frame['Datos Seriales'],color = 'red',  label="Voltaje")
        plt.xlabel("Tiempo (s)", fontsize=12, fontstyle="italic")
        plt.ylabel("Voltaje (mV)", fontsize=12, fontstyle="italic")
        plt.title("Plot Final")
        
        data_plot_filename = self.title + '.png'
        plt.savefig(data_plot_filename)
        plt.show()
        

lector = ReadSignalGraf('COM7', 9600, 20, 'Prueba')  # Replace 'data_filename' with your desired file name
lector.realTimeGraf()
