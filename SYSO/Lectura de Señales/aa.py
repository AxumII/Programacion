import csv
import math

# Parámetros de la señal sinusoidal
amplitud = 1.0   # Amplitud de la señal
frecuencia = 1.0 # Frecuencia de la señal (en Hz)
muestras = 100   # Número de muestras

# Crear una lista de valores de tiempo
tiempo = [i / frecuencia / muestras for i in range(muestras*10)]

# Calcular los valores de la señal sinusoidal
valores = [amplitud * math.sin(2 * math.pi * frecuencia * t) for t in tiempo]

# Nombre del archivo CSV de salida
nombre_archivo = "senal_periodica.csv"

# Escribir los valores en el archivo CSV
with open(nombre_archivo, mode='w', newline='') as archivo_csv:
    escritor_csv = csv.writer(archivo_csv, delimiter=',')
    escritor_csv.writerow(["Tiempo", "Valor"])  # Escribir encabezados
    for t, valor in zip(tiempo, valores):
        escritor_csv.writerow([t, valor])

print(f"Se ha creado el archivo '{nombre_archivo}' con los valores de la señal.")
print(valores)
