import serial
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class ReadSignal():
    def __init__(self, usbPort, baudrate, fm, collection_time, title=None):
        self.usbPort = usbPort
        self.baudrate = baudrate
        self.fm = fm
        self.pm = 1 / fm
        self.data_frame = pd.DataFrame({'Tiempo (s)': [], 'Datos Seriales': []})
        self.countTime = 0
        self.collection_time = collection_time  # Set the collection time in seconds
        self.title = title

    def connect(self):
        return serial.Serial(self.usbPort, baudrate=self.baudrate)

    def collectData(self):
        ser = self.connect()
        # Get the current time as the start time

        
        while True:  # Collect data until the time limit is reached
            try:
                data = ser.readline().decode('utf-8').strip()
                y_value = float(data)

                self.data_frame.loc[self.countTime] = [self.countTime * self.pm, y_value]
                self.countTime += 1
                
                #print(self.countTime*self.pm,self.collection_time)
                
                if(self.countTime * self.pm ) == self.collection_time:
                    break
                
                
                
            except ValueError:
                pass
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
        plt.plot(self.data_frame['Tiempo (s)'], self.data_frame['Datos Seriales'], color='red', label="Voltaje")
        plt.xlabel("Tiempo (s)", fontsize=12, fontstyle="italic")
        plt.ylabel("Voltaje (mV)", fontsize=12, fontstyle="italic")
        plt.title("Plot Final")

        data_plot_filename = self.title + '.png'
        plt.savefig(data_plot_filename)
        plt.show()

lector = ReadSignal('COM7', 115200, fm = 860, collection_time= 3, title='a.csv')  
lector.collectData()
