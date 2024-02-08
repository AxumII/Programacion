import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class ReadSignal:
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
            
    #al usar clip para mayores siempre va de la forma [None, Valor]
    #al usar clip para menores siempre va de la forma [Valor, None]
    #otros = un vector (, vector). si es n vectores ( ,  [vectro1, vetor2])
    def clip(self, vector, limits, del_parameter, otros=None):
        if del_parameter == 'mayor':
            # Encuentra índices de valores mayores que el límite superior.
            indices = np.where(vector > limits[1])[0]
        elif del_parameter == 'menor':
            # Encuentra índices de valores menores que el límite inferior.
            indices = np.where(vector < limits[0])[0]
        elif del_parameter == 'interno':
            # Encuentra índices de valores dentro del intervalo.
            indices = np.where((vector >= limits[0]) & (vector <= limits[1]))[0]
        elif del_parameter == 'externo':
            # Encuentra índices de valores fuera del intervalo.
            indices = np.where((vector < limits[0]) | (vector > limits[1]))[0]
        else:
            print("del_parameter no válido.")
            return

        # Elimina los elementos de `vector` en los índices encontrados.
        vector = np.delete(vector, indices)
        self.t = np.delete(self.t, indices)

        # Si `otros` es un ndarray o una matriz y no es None, elimina los elementos correspondientes.
        if otros is not None and isinstance(otros, (np.ndarray, list)):
            # Verifica si otros es una lista de arrays o un único array.
            if isinstance(otros, list) and all(isinstance(el, np.ndarray) for el in otros):
                for i, other_signal in enumerate(otros):
                    otros[i] = np.delete(other_signal, indices)
            elif isinstance(otros, np.ndarray):
                otros = np.delete(otros, indices)
            else:
                print("El parámetro otros debe ser un ndarray o una lista de ndarrays.")
    
        return vector, otros

    def adjust_time(self):
       
        intervals = np.diff(self.t)        
        min_interval = np.min(intervals)
        
        
        if not np.allclose(intervals, min_interval):
            
            self.t = np.arange(0, min_interval * len(self.t), min_interval)
            
        else:
            print("Cada intervalo esta a la misma distancia")

  
    def offset(self,vector, offset):
        if vector is None or offset is None:
            print("La señal no está definida.")
            return
        
        vector += offset
        
        return vector

    

    def save_to_csv(self):
        # Primero, guardamos las señales coincidentes en longitud con self.t
        matched_signals = [signal for signal in self.signals if len(signal) == len(self.t)]
        matched_signals_indices = [i for i, signal in enumerate(self.signals) if len(signal) == len(self.t)]

        if matched_signals:
            data_matched = np.column_stack((self.t, *matched_signals))
            column_names_matched = ['Tiempo'] + [f'Señal_{i+1}' for i in matched_signals_indices]
            df_matched = pd.DataFrame(data_matched, columns=column_names_matched)
            matched_csv_title = f"{self.csv_title.replace('.csv', '')}_Edit.csv"
            df_matched.to_csv(matched_csv_title, index=False)
            print(f"Archivo {matched_csv_title} guardado correctamente con señales coincidentes.")
            
            
            print(df_matched)

        
   




if __name__ == "__main__":
    
    np.random.seed(0)  # Establece la semilla para reproducibilidad
    num_rows = 100  # Número de filas
    num_signals = 3  # Número de señales (columnas)

    # Crear un array de tiempo
    t = np.linspace(0, 10, num_rows)

    # Crear arrays de señales con valores aleatorios
    signals = np.random.random((num_rows, num_signals)) * 100  # Valores entre 0 y 100

    # Crear un DataFrame con estos datos
    data = np.column_stack((t, signals))  # Añadir el tiempo como primera columna
    column_names = ['Tiempo'] + [f'Señal_{i+1}' for i in range(num_signals)]
    df = pd.DataFrame(data, columns=column_names)

    # Guardar el DataFrame en un archivo CSV para utilizarlo con ReadSignal
    df.to_csv('Prueba.csv', index=False)
    
    
    
    
    reader = ReadSignal('Prueba.csv')
    df = reader.extract_csv()        
    reader.variables()
    
    
    
    # Selecciona una señal para probar el método clip
    vector_de_prueba = df['Señal_1'].to_numpy()
    vector2 = df['Señal_2'].to_numpy()
    vector3 = df['Señal_3'].to_numpy()

    print("vector in",vector_de_prueba)
    """
    vector_modificado, otros_modificados = reader.clip(vector_de_prueba, [10, 15], 'externo', otros= [vector2,vector3])
    
    reader.signals[1],reader.signals[2]  = otros_modificados"""
    
    vector_modificado, otros_modificados = reader.clip(vector_de_prueba, [10, 15], 'externo', otros= vector2)
    
    reader.signals[1]  = otros_modificados
    
    reader.signals[0] = vector_modificado
    
    
    
    # Ahora vector_modificado contiene la señal con valores mayores que 80 eliminados
    print("vector fin",vector_modificado)
    
    print("vector in",vector_de_prueba)
    
    print("vectores modifcidados", otros_modificados)
    
    print("\n")
    
    print("tiempo con edit", reader.t )
    
    reader.adjust_time()
    
    print("tiempo con edit", reader.t )
    
    reader.save_to_csv()
    