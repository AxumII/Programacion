import pandas as pd
import matplotlib.pyplot as plt

# Ruta absoluta de los archivos
grupo1_path = r'C:\GitHub\Programacion\Python\Analisis Estatica\grupo1.csv'
grupo2_path = r'C:\GitHub\Programacion\Python\Analisis Estatica\grupo2.csv'
grupo3_path = r'C:\GitHub\Programacion\Python\Analisis Estatica\grupo3.csv'

# Leer los archivos CSV usando rutas absolutas
grupo1 = pd.read_csv(grupo1_path)
grupo2 = pd.read_csv(grupo2_path)
grupo3 = pd.read_csv(grupo3_path)

print("Archivos CSV leídos correctamente")

# Modificar el análisis con líneas adicionales
def basic_analysis_modified(df):
    # Calcular media, desviación estándar y varianza
    media = df.mean()
    desvest = df.std()
    varianza = df.var()
    
    # Mostrar resultados
    print("Media:\n", media)
    print("Desviación Estándar:\n", desvest)
    print("Varianza:\n", varianza)
    
    # Crear histogramas con línea en 15
    for column in df.columns:
        plt.figure()
        plt.hist(df[column], bins=15, alpha=0.7, label=column)
        plt.axvline(media[column], color='r', linestyle='dashed', linewidth=1, label='Media')
        plt.axvline(media[column] + desvest[column], color='g', linestyle='dashed', linewidth=1, label='+1 Sigma')
        plt.axvline(media[column] - desvest[column], color='g', linestyle='dashed', linewidth=1, label='-1 Sigma')
        plt.axvline(15, color='blue', linestyle='-', linewidth=2, label='Línea en 15')
        plt.title(f'Histograma con media y sigma - {column}')
        plt.legend()
        plt.show()

def filtered_analysis_modified(df):
    # Filtrar filas donde P4 es distinto de 0
    df_filtered = df[df['P4'] != 0]
    
    # Calcular media, desviación estándar y varianza para los datos filtrados
    media = df_filtered.mean()
    desvest = df_filtered.std()
    varianza = df_filtered.var()
    
    # Mostrar resultados
    print("Media (Filtrado):\n", media)
    print("Desviación Estándar (Filtrado):\n", desvest)
    print("Varianza (Filtrado):\n", varianza)
    
    # Crear histogramas con línea en 15 y línea en 3 para columna 'F' / 20
    for column in df_filtered.columns:
        plt.figure()
        plt.hist(df_filtered[column], bins=20, alpha=0.7, label=column)
        plt.axvline(media[column], color='r', linestyle='dashed', linewidth=1, label='Media')
        plt.axvline(media[column] + desvest[column], color='g', linestyle='dashed', linewidth=1, label='+1 Sigma')
        plt.axvline(media[column] - desvest[column], color='g', linestyle='dashed', linewidth=1, label='-1 Sigma')
        plt.axvline(15, color='blue', linestyle='-', linewidth=2, label='Línea en 15')
        if column == 'F':
            plt.axvline(3, color='orange', linestyle='--', linewidth=2, label='Línea en 3')
        plt.title(f'Histograma con media y sigma - {column} (Filtrado)')
        plt.legend()
        plt.show()

# Llamar a las funciones de análisis modificadas
print("Análisis Básico Modificado del Grupo 1:")
basic_analysis_modified(grupo1)

print("Análisis Filtrado Modificado del Grupo 1:")
filtered_analysis_modified(grupo1)
