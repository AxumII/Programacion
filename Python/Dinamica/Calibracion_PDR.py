import numpy as np

def calibracion(data1, data2):
    mean_d1 = data1.mean()
    mean_d2 = data2.mean()    
    std_d1 = data1.std()
    std_d2 = data2.std()
    
    return [mean_d1, mean_d2], [std_d1, std_d2]

# Datos extraídos de la imagen
data1 = np.array([6.5, 6.2, 6.3, 6.3, 6.1, 6.1, 6.1, 6.3, 6.3, 6.1, 
                  6.1, 6.2, 6.4, 6.2, 6.1, 6.1, 6.1, 6.2, 6.2, 6.1])

data2 = np.array([6.25, 6.3, 6.2, 6.25, 6.3, 6.3, 6.3, 6.3, 6.25, 6.3,
                  6.25, 6.3, 6.3, 6.3, 6.25, 6.25, 6.4, 6.25, 6.25, 6.3])

# Llamar a la función y guardar los resultados
promedios, desviaciones = calibracion(data1, data2)

# Mostrar resultados
print("Promedio (Temu, Manual):", promedios)
print("3 * Std (Temu, Manual):", [3 * std for std in desviaciones])
