import numpy as np
import pandas as pd

from Generator import Generator as gen

def generar():
    fs = 500    
    max = 5
    
    f = gen(0, 5, fs)
    t = f.t()
    
    #f1 = f.new('1.5 * t ** 2')
    f1 = f.sen(5,700)
    #f1 = f.new('1.5 * exp(2.5*t)')
    
    # Crear un DataFrame con pandas
    df = pd.DataFrame({'t': t, 'f1': f1})
    
    # Guardar el DataFrame en un archivo CSV
    df.to_csv('Generado.csv', index=False)


# Llamar a la función para generar y guardar los datos
generar()
