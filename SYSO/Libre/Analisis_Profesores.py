import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt



class DataAnalysis:
    def __init__(self, data):
        self.data = data
        self.mean = np.mean(data)
        self.std_dev = np.std(data)
        self.kurtosis = stats.kurtosis(data)
        self.skewness = stats.skew(data)
        self.maximum = np.max(data)
        self.minimum = np.min(data)
        self.count_above_3 = sum(np.sum(np.array(sublist) >= 3) for sublist in data)
        self.count_below_3 = sum(np.sum(np.array(sublist) < 3) for sublist in data)


    #Es una pearson para ver si es normal o no
    def normality_shapiro_test(self):
        statistic, p_value = stats.shapiro(data)
        alpha = 0.05
        if p_value < alpha:
            return "No"
        else:
            return "Si"

    #Es unna kolmogorov para ver si tiene una chi cuadrado xd
    def kolmogorov_test(self):
        # Realiza la prueba de Kolmogorov-Smirnov para verificar si los datos siguen una distribución 
        mean = np.mean(self.data)
        std_dev = np.std(self.data)
        kstest_result = stats.kstest(self.data, 'norm', args=(mean, std_dev))
        # Define un nivel de significancia (alpha)
        alpha = 0.05
        # Compara el valor p con el nivel de significancia
        if kstest_result.pvalue < alpha:
            return "No"
        else:
            return "Si"


    def normality_anderson_darling_test(self):
        result = stats.anderson(self.data)
        if result.statistic < result.critical_values[2]:
            return "Si"
        else:
            return "No"

    def normality_normaltest(self):
        statistic, p_value = stats.normaltest(self.data)
        alpha = 0.05
        if p_value < alpha:
            return "No"
        else:
            return "Si"


    def anderson_gumbel_l_test(self):
        result = stats.anderson(self.data, dist='gumbel_l')
        if result.statistic < result.critical_values[2]:
            return "Si"
        else:
            return "No"
        
    def normality_jarque_bera_test(self):
        statistic, p_value = stats.jarque_bera(self.data)
        alpha = 0.05
        if p_value < alpha:
            return "No"
        else:
            return "Si"

    def normality_cramer_test(self):
        # Realiza el test de Cramer-Von Mises
        res = stats.cramervonmises(self.data, 'norm')
        res.statistic, res.pvalue
        # Comprueba si el valor p es menor que un umbral de significancia (por ejemplo, 0.05)
        alpha = 0.05
        if res.pvalue < alpha:
            return 'No'
        else:
            return 'Si'



# Crear instancias de la clase DataAnalysis para cada conjunto de datos

Normal = np.random.normal(loc=3, scale=2, size= 50)

chi_cuadrado1 = np.random.chisquare(df=5, size=50)

chi_cuadrado2 =  2 - chi_cuadrado1

G4_P1_FOOO_RamiroCardona = ([3.9, 1.9, 2.5, 1.4, 1.0, 1.8, 4.0, 3.0, 1.4, 2.4, 1.0, 1.3, 1.5, 2.5, 4.0, 2.0, 4.4, 2.0, 3.3, 1.5, 3.5, 1.9, 1.9, 1.0, 4.0, 1.7, 2.0, 3.9, 1.3, 2.0])

G2_P1_FOOO_RamiroCardona = ([3.5, 3.4, 3.5, 1.5, 1.5, 3.8, 2.8, 2.9, 3.8, 1.0, 2.9, 1.9, 1.5, 2.3, 3.4, 3.9, 4.4, 4.4, 2.4, 4.0, 0.5, 4.2, 1.5, 3.8, 1.4, 0.4, 1.5, 4.5, 2.0, 3.5, 3.9, 2.5])

Fin_Estatica_Cristian = ([2.7, 2.3, 3.5, 3, 3.8, 2.9, 4.1, 2.8, 2.5, 3.1, 3.3, 3.2, 3, 3.4, 2.8, 0.9, 2, 3.4, 2.9, 2.5, 3.8, 2.4, 1.9, 2.5, 2.8, 1.1, 2.8, 2.1, 3.2, 3.6, 3.7, 2.3, 2, 2.2, 3.2, 1.7, 3.1])

Fin_Estatica_Guerrero = ([3.6, 2, 4.4, 2.6, 2.1, 1.9, 2.2, 1.9, 2.2, 1.9, 4.2, 2.5, 3.7, 5, 2.5, 3.6, 2.2, 1.6, 1.8, 2.6, 4.4, 4, 1.2, 1.1, 4.3, 4.6, 1.9, 2.9, 4.6, 2.6, 1, 1.6, 2, 1.9, 2.4, 3.6, 2.5, 2, 2.1, 1.4])

Fin_Inferencia_Mario = ([5, 4.108620079, 2.852238791, 3.011549451, 3.889204945, 4.089777473, 3.879524725, 4.614024725, 3.203760989, 5.104215385, 0.977483356, 3.556813077, 3.775691868, 3.691793956, 3.897614725, 4.43892967, 3.146499467, 4.232412088, 3.283925824, 1.36498967, 3.569031758, 4.657865714, 3.488841429, 4.232003736, 3.365426044, 4.827502747, 2.592456044, 4.409232308, 4.090950549, 3.779035714, 3.884664835, 4.369633516, 4.159593956, 4.615541209, 3.456564066, 3.58053022, 4.223043956, 5, 3.616801238, 3.63139011, 3.415797363, 3.67085044, 4.622195055, 2.454244025, 3.533766484, 4.443901099, 1.250785714, 3.348458132, 0.915780166, 3.142706044, 4.532239011, 3.980708681, 4.264373516])

Fin_PYE_Mario = ([4.8, 5.0, 4.3, 4.7, 5.0, 1.4, 4.4, 4.3, 1.3, 4.4, 4.7, 4.5, 3.5, 4.7, 4.8, 3.7, 3.7, 4.5, 2.0, 4.5, 4.6, 1.5, 4.6, 4.3, 4.7, 4.6, 5.0, 4.6, 3.9, 4.3, 3.2, 4.6, 4.3, 4.8, 3.7, 4.5, 4.8, 4.6, 4.2, 4.7, 4.5, 4.4, 4.6, 5.0, 3.7, 4.3, 5.0, 0.6, 1.2, 4.3, 4.8, 4.8, 5.0, 3.7, 4.1, 4.8, 3.8, 4.7])
    
Fin_EDO_Ivan = ([4.90, 4.01, 5, 3.55, 2.95, 4.08, 4.05, 4.63, 3.05, 4.00, 4.25, 1.50, 3.18, 3.77, 3.10, 4.80, 3.34, 3.28, 3.70, 4.83, 3.48, 4.10, 3.10, 3.96, 4.53, 4.13, 4.30, 4.33, 2.96, 3.23, 3.70, 4.20, 2.60, 4.43, 5, 4.35, 4.68, 4.05, 3.68, 3.65, 3.70, 3.88, 4.65, 5, 4.70, 3.00, 4.50, 4.38, 4.40, 4.48, 3.88, 3.83, 4.05, 5.20, 3.40, 0.51, 5.00, 3.20, 4.40, 4.31, 4.05, 3.38, 3.50, 4.15, 3.66, 4.90, 2.99, 4.70, 3.22, 4.75, 3.30, 3.76, 0.92, 3.48, 3.00, 3.60, 3.19, 4.53, 3.98])

Fin_PQ_Angela = ([4.52, 4.23, 4.60, 4.71, 3.01, 3.16, 3.94, 4.37, 4.53, 3.42, 4.14, 4.50, 4.58, 4.76, 4.55, 4.84, 4.80, 2.79, 4.11, 4.14, 4.47, 4.78, 4.74, 4.45, 3.00, 4.80])

Fin_Algebra_Julian = ([3.2, 0.3, 3.0, 3.1, 0.5, 4.4, 4.3, 0.4, 3.4, 0.9, 4.2, 0.3, 0.6, 4.3, 4.2, 3.6, 3.3, 3.6, 3.5, 3.3, 0.4, 4.2, 3.1, 2.6, 2.8, 4.0, 3.9, 1.8, 2.8, 3.9, 3.3, 4.7, 2.1, 3.2, 4.3, 3.5, 0.8, 3.0, 4.6, 3.7, 1.9, 4.3, 3.7, 3.3, 4.7, 2.8, 4.1, 3.8, 4.2, 1.5, 0.3, 3.4, 0.5, 4.0])

G7_Fin_FDM_Sanchez = ([4.6, 3.0, 3.1, 3.1, 3.4, 3.1, 2.5, 2.6, 3.4, 3.7, 3.1, 4.4, 3.6, 3.6, 3.2, 4.5, 3.8, 3.9, 4.5, 0.8, 3.9, 3.2, 4.3, 2.4, 3.6, 3.2, 3.8, 3.3, 2.9, 3.2, 3.4, 4.4, 3.6, 3.6, 4.3, 4.0, 3.9, 3.4])

G6_Fin_FDM_Sanchez = ([3.4, 2.4, 2.5, 3.5, 3.1, 3.8, 2.9, 4.0, 4.4, 3.6, 2.0, 3.6, 4.9, 3.3, 4.1, 3.2, 4.0, 2.0, 3.6, 2.7, 3.1, 4.3, 4.4, 2.9, 3.2, 3.8, 3.9, 4.2, 3.7, 2.2, 4.3, 3.2, 3.4, 3.6, 3.9, 4.0, 1.8, 3.8])

Fin_InglesIV_Jennly = ([3.5, 3.6, 3.5, 3.5, 3.5, 3.2, 2.6, 3.7, 3.3, 3.8, 2.6, 3.8, 2.6, 3.7, 3.7, 3.7, 4.0, 3.3, 0.0, 3.9, 3.9, 3.2, 3.6, 3.7, 4.0, 3.6])

#Toca hacer el convertidor que extraiga los nombres de la variable y los añada en orden, un for y me da pereza lo demas

data_names = [
    "Normal",
    "chi_cuadrado1",
    "chi_cuadrado2",
    "G4_P1_FOOO_RamiroCardona",
    "G2_P1_FOOO_RamiroCardona",
    "Fin_Estatica_Cristian",
    "Fin_Estatica_Guerrero",
    "Fin_Inferencia_Mario",
    "Fin_PYE_Mario",
    "Fin_EDO_Ivan",
    "Fin_PQ_Angela",
    "Fin_Algebra_Julian",
    "G7_Fin_FDM_Sanchez",
    "G6_Fin_FDM_Sanchez",
    "Fin_InglesIV_Jennly"
]




data_arrays = [
    Normal,
    chi_cuadrado1,
    chi_cuadrado2,
    G4_P1_FOOO_RamiroCardona,
    G2_P1_FOOO_RamiroCardona,
    Fin_Estatica_Cristian,
    Fin_Estatica_Guerrero,
    Fin_Inferencia_Mario,
    Fin_PYE_Mario,
    Fin_EDO_Ivan,
    Fin_PQ_Angela,
    Fin_Algebra_Julian,
    G7_Fin_FDM_Sanchez,
    G6_Fin_FDM_Sanchez,
    Fin_InglesIV_Jennly
]



results_list = []
for data, name in zip(data_arrays, data_names):
    analysis = DataAnalysis(data)
    result = {
        'Nombre': name,  # Add the name of the array as 'Nombre'
        'Media': analysis.mean,
        'Desviación Estándar': analysis.std_dev,
        'Curtosis': analysis.kurtosis,
        'Asimetría': analysis.skewness,
        'Máximo': analysis.maximum,
        'Mínimo': analysis.minimum,
        'Valores >= 3': analysis.count_above_3,
        'Valores < 3': analysis.count_below_3,
        'Prueba N (Shapiro)': analysis.normality_shapiro_test(),
        'Prueba N (Anderson)': analysis.normality_anderson_darling_test(),
        'Prueba N (Normaltest)': analysis.normality_normaltest(),
        'Prueba N (Kolmogorov)': analysis.kolmogorov_test(),        
        'Prueba N (Jarque-Bera)': analysis.normality_jarque_bera_test(),
        'Prueba N (Cramer)': analysis.normality_cramer_test(),
        'Prueba (Anderson Gumbel)': analysis.anderson_gumbel_l_test(),
    }
    results_list.append(result)

# Crear un DataFrame de pandas con los resultados para cada conjunto de datos
results = pd.DataFrame(results_list)



print(results)


# Especifica la ruta y el nombre del archivo Excel
nombre_archivo_excel = 'Analisis notas.xlsx'

# Exporta el DataFrame a Excel
results.to_excel(nombre_archivo_excel, index=False)  # index=False para no incluir el índice en el archivo

print(f'Se ha exportado el DataFrame a {nombre_archivo_excel}')

for data, name in zip(data_arrays, data_names):
    bins = int(len(data) / 2.5)

    plt.figure(figsize=(8, 6))
    plt.hist(data, bins, color='blue', alpha=0.7, density=True)
    
    # Línea de la media
    plt.axvline(np.mean(data), color='red', linestyle='dashed', linewidth=2, label='Media')
    
    # Líneas de desviación estándar
    std_dev = np.std(data)
    plt.axvline(np.mean(data) + std_dev, color='green', linestyle='dashed', linewidth=2, label='Desviación Estándar')
    plt.axvline(np.mean(data) - std_dev, color='green', linestyle='dashed', linewidth=2)

    # Línea en 3
    plt.axvline(3, color='purple', linestyle='dashed', linewidth=2, label='Valor 3')

    plt.title(f'Histogram of {name}')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.legend()
    plt.grid(True)
    plt.show()