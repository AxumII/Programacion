import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd
############################################################################################################################
#Funciones para la regresion

def exponential_func(x, a, b):
    return a * np.exp(b * x)

def fit_exponential(x, y):
    params, covariance = curve_fit(exponential_func, x, y)
    return params

def calculate_fitted_values(x, params):
    a, b = params
    return np.exp(b * x) * a
#################################################################################################################################
#Recta de carga
def Recta(vymax):   
    # Definir los puntos (0, 0.05) y (25, 0)
    x_points = np.array([0, 25])
    y_points = np.array([vymax, 0])

    # Crear un conjunto de valores de x en el intervalo de 0 a 1
    xCarga = np.linspace(0, 1, 100)

    # Calcular los valores correspondientes de y en la recta utilizando interpolación lineal
    yCarga = np.interp(xCarga, x_points, y_points)
    
    return(xCarga,yCarga)
###############################################################################################################################
# Graficar los datos originales y las curvas ajustadas

def graf(x1, y1, x2, y2, ajr,xC,yC,xP,yP):
    
    #borrar
    xid = (np.ones(100))*0.7
    yid = np.linspace(0, 0.05, 100)
    
    
    
    
    
    # Gráfica 1: Real
    plt.figure(figsize=(18, 9))
    
    
    plt.subplot(2, 3, 1)
    plt.plot(x2, y2, label='Valores Reales', color="purple")
    plt.title('Valores Reales del Diodo')
    plt.xlabel('Voltaje Diodo (V)')
    plt.ylabel('Corriente Diodo (A)')
    plt.xlim(0, 0.9)
    plt.ylim(0, 0.06)
    plt.legend()

    # Gráfica 2: Ajuste Exponencial
    plt.subplot(2, 3, 2)
    plt.plot(x2, ajr, label='Curva Caracteristica', color = "orange")
    """
    plt.plot(xid, yid, label = " Modelo en 0.7V ", color = "green")
    plt.plot(xid*0.01, yid, label = " Modelo Ideal ", color = "red")
    """
    
    plt.title('Curva Caracteristica Calculada del Diodo')
    plt.xlabel('Voltaje Diodo (V)')
    plt.ylabel('Corriente Diodo (A)')
    plt.xlim(0, 0.9)
    plt.ylim(0, 0.06)
    plt.legend()

    # Gráfica 3: Comparación de las dos líneas anteriores
    plt.subplot(2, 3, 3)
    plt.plot(x2, y2, label='Valores Reales', color = "purple")
    plt.plot(x2, ajr, label='Curva Caracteristica', color = "orange", linestyle = "dashdot")
    plt.title('Real vs Curva Caracteristica')
    plt.xlabel('Voltaje Diodo (V)')
    plt.ylabel('Corriente Diodo (A)')
    plt.xlim(0, 0.9)
    plt.ylim(0, 0.06)
    plt.legend()

    # Gráfica 4: Ajuste exponencial y Linea de Carga
    plt.subplot(2, 3, 4)
    plt.plot(x2, ajr, label='Curva Caracteristica', color = "orange")
    plt.plot(xC, yC, label='Recta de Carga', color = "red")
    plt.title('Curva Caracteristica y Recta de Carga')
    plt.xlabel('Voltaje Diodo (V)')
    plt.ylabel('Corriente Diodo (A)')
    plt.ylim(0, 0.06)
    
    plt.plot(xP, yP, marker="o", markersize=4, color="black", label=f'Punto de Trabajo ({xP}, {yP})')
    
    plt.legend()

    # Gráfica 5: Simulacion vs Real
    plt.subplot(2, 3, 5)
    plt.plot(x1, y1, label='Valores de Simulacion', color = "green")
    plt.plot(x2, y2, label='Valores Reales', color = "purple",linestyle = "dashed")
    plt.title('Simulacion vs Real')
    plt.xlabel('Voltaje Diodo (V)')
    plt.ylabel('Corriente Diodo (A)')
    plt.xlim(0, 0.9)
    plt.ylim(0, 0.06)
    plt.legend()

    # Gráfica 6: Simulacion Vs Ajuste
    plt.subplot(2, 3, 6)
    plt.plot(x1, y1, label='Valores de Simulacion', color = "green")
    plt.plot(x2, ajr, label='Curva Caracteristica', color = "orange", linestyle = "dashdot")
    plt.title('Simulacion vs Curva Caracteristica')
    plt.xlabel('Voltaje Diodo (V)')
    plt.ylabel('Corriente Diodo (A)')
    plt.xlim(0, 0.9)
    plt.ylim(0, 0.06)
    plt.legend()

    plt.tight_layout()
    plt.show()

#############################################################################################################################
# Datos
sim4001VD = np.array([
    0, 0.446, 0.556, 0.593, 0.615, 0.631, 0.643, 0.653, 0.661, 0.668, 0.674, 0.68, 0.685, 0.69, 0.694, 0.698, 0.702, 0.705, 0.708, 0.711, 0.714, 0.719, 0.724, 0.729, 0.733, 0.737, 0.74, 0.743, 0.747, 0.75, 0.752, 0.755, 0.758, 0.76, 0.762, 0.765
    ])

sim4001AD = np.array([
    0, 0.000106, 0.00088, 0.0018, 0.0027, 0.0037, 0.0047, 0.0056, 0.0066, 0.0076, 0.0085, 0.0096, 0.01, 0.011, 0.012, 0.013, 0.0145, 0.015, 0.016, 0.017, 0.018, 0.02, 0.022, 0.024, 0.026, 0.028, 0.03, 0.032, 0.034, 0.036, 0.038, 0.04, 0.042, 0.044, 0.046, 0.049
    ])

real4001VD = np.array([
    0,0.4,0.55,0.6,0.65,0.66,0.67,0.68,0.69,0.7,0.71,0.71,0.72,0.72,0.73,0.73,0.74,0.74,0.74,0.75,0.75,0.75,0.75,0.76,0.76,0.76,0.76
])

real4001AD = np.array( [
    0,0.0001,0.0009,0.0028,0.0048,0.0069,0.0085,0.01,0.012,0.015,0.017,0.019,0.02,0.022,0.024,0.027,0.028,0.03,0.031,0.034,0.036,0.037,0.04,0.042,0.044,0.046,0.049
])

sim4148VD = np.array([
    0,0.469,0.598,0.636,0.658,0.674,0.687,0.697,0.705,0.713,0.719,0.725,0.731,0.736,0.741,0.745,0.749,0.753,0.757,0.76,0.764,0.77,0.776,0.781,0.787,0.791,0.796,0.8,0.805,0.809,0.813,0.816,0.82,0.824,0.827,0.83
])

sim4148AD = np.array([
    0,0.0006,0.0008,0.001,0.0026,0.0035,0.0046,0.0056,0.0065,0.0075,0.0085,0.0095,0.01,0.011,0.012,0.013,0.014,0.015,0.016,0.017,0.018,0.02,0.022,0.024,0.026,0.028,0.03,0.032,0.034,0.036,0.038,0.04,0.042,0.044,0.046,0.048
])

real4148VD = np.array([
    0,0.45,0.6,0.67,0.69,0.7,0.72,0.73,0.74,0.75,0.76,0.76,0.77,0.78,0.78,0.79,0.79,0.79,0.8,0.8,0.81,0.81,0.82,0.82,0.82,0.82,0.83
])

real4148AD = np.array([
    0,0.0005,0.0008,0.0027,0.005,0.0066,0.0087,0.01,0.012,0.015,0.017,0.019,0.02,0.02,0.025,0.026,0.027,0.03,0.032,0.033,0.036,0.037,0.04,0.042,0.044,0.046,0.048
])

sim4001VDCautin = np.array([
    0,0.33,0.404,0.462,0.492,0.513,0.528,0.541,0.552,0.562,0.571,0.578,0.585,0.592,0.598,0.604,0.609,0.614,0.619,0.624,0.628,0.632,0.636,0.641,0.644,0.648,0.652
])

sim4001ADCautin = np.array([
    0,0.00034,0.0012,0.0031,0.005,0.007,0.009,0.011,0.013,0.015,0.017,0.019,0.021,0.023,0.025,0.027,0.029,0.031,0.033,0.035,0.0367,0.039,0.041,0.043,0.045,0.047,0.049
])

real4001VDCautin =  np.array([
    0,0.33,0.4,0.42,0.45,0.47,0.5,0.5,0.51,0.52,0.53,0.54,0.54,0.54,0.55,0.55,0.56,0.56,0.57,0.57,0.58,0.58,0.58,0.59,0.6,0.6,0.6,0.61,0.62,0.63,0.64,0.64,0.640,0.64,0.65,0.65
])

real4001ADCautin = np.array([
    0,0.0004,0.0014,0.0021,0.003,0.004,0.005,0.006,0.0066,0.007,0.009,0.0096,0.01,0.011,0.012,0.014,0.015,0.016,0.017,0.018,0.019,0.02,0.022,0.024,0.027,0.029,0.03,0.033,0.035,0.037,0.039,0.04,0.041,0.044,0.048,0.049
])

#############################################################################################################################

# Ajuste exponencial para real4001VD y real4001AD
paramsR4001 = fit_exponential(real4001VD, real4001AD)
calRA4001 = calculate_fitted_values(real4001VD, paramsR4001)

# Ajuste exponencial para real4148VD y real4148AD
paramsR4148 = fit_exponential(real4148VD, real4148AD)
calRA4148 = calculate_fitted_values(real4148VD, paramsR4148)

# Ajuste exponencial para real4001VDCAUTIN y real4001ADCAUTIN
paramsR4001Cautin = fit_exponential(real4001VDCautin, real4001ADCautin)
calRA4001Cautin = calculate_fitted_values(real4001VDCautin, paramsR4001Cautin)

#Tabla de datos de parametros Real
parameters_data = {
    'Sample': ['1n4001', '1n4148', '1n4148 + cautin'],
    'a': [paramsR4001[0], paramsR4148[0], paramsR4001Cautin[0]],
    'b': [paramsR4001[1], paramsR4148[1], paramsR4001Cautin[1]]
}

# Create a Pandas DataFrame
parameters_df = pd.DataFrame(parameters_data)

print(parameters_df)

"""

# Define the Excel file path
excel_file_path = 'exponential_parameters.xlsx'

# Export the DataFrame to Excel
parameters_df.to_excel(excel_file_path, index=False)

"""

###############################################################################################################################

# Ajuste exponencial para simulados
paramsS4001 = fit_exponential(sim4001VD, sim4001AD)
calSA4001 = calculate_fitted_values(sim4001VD, paramsS4001)

# Ajuste exponencial para simulados
paramsS4148 = fit_exponential(sim4148VD, sim4148AD)
calSA4148 = calculate_fitted_values(sim4148VD, paramsS4148)

#Tabla de datos de parametros Real
parameters_dataSim = {
    'Diodos Simulados': ['1n4001', '1n4148'],
    'a': [paramsS4001[0], paramsS4148[0]],
    'b': [paramsS4001[1], paramsS4148[1]]
}

# Create a Pandas DataFrame
parameters_dfSim = pd.DataFrame(parameters_dataSim)

print(parameters_dfSim)


"""
# Define the Excel file path
excel_file_path = 'exponential_parametersSimulado.xlsx'

# Export the DataFrame to Excel
parameters_dfSim.to_excel(excel_file_path, index=False)

"""


##############################################################################################################################

#Calculos Is, n y T REALES

K = 1.38e-23
q = 1.6e-19
Tamb = 293.15

def nDesc(b,T):
    return (q/(b*T*K))
    
def TDesc(b,n):
    return (q/(b*n*K))


tablaCalculos = {
    'Diodos': ['1n4001', '1n4148', '1n4148 + cautin'],
    'Is': [paramsR4001[0], paramsR4148[0], paramsR4001Cautin[0]],
    'b': [paramsR4001[1], paramsR4148[1], paramsR4001Cautin[1]],
    'n' : [ nDesc(paramsR4001[1],Tamb), nDesc(paramsR4148[1],Tamb) , nDesc(paramsR4148[1],Tamb) ],
    'T en °K' : [ Tamb, Tamb, TDesc(paramsR4001Cautin[1],nDesc(paramsR4148[1],Tamb))],
    'T en °C' : [Tamb-273.15, Tamb-273.15, TDesc(paramsR4001Cautin[1],nDesc(paramsR4148[1],Tamb))-273.15]
}

dfCalculos = pd.DataFrame(tablaCalculos)

print(dfCalculos)
"""
# Define the Excel file path
excel_file_path2 = 'calculosIsTn.xlsx'

# Export the DataFrame to Excel
dfCalculos.to_excel(excel_file_path2, index=False)
"""
###########################################################################################################################
########################################################################################################################

#Calculos Is, n y T Simulados

K = 1.38e-23
q = 1.6e-19
Tamb = 293.15

def nDesc(b,T):
    return (q/(b*T*K))
    
def TDesc(b,n):
    return (q/(b*n*K))


tablaCalculosSim = {
    'Diodos Simulados': ['1n4001', '1n4148'],
    'Is': [paramsS4001[0], paramsS4148[0]],
    'b': [paramsS4001[1], paramsS4148[1]],
    'n' : [ nDesc(paramsS4001[1],Tamb), nDesc(paramsS4148[1],Tamb) ],
    'T en °K' : [ Tamb, Tamb],
    'T en °C' : [Tamb-273.15, Tamb-273.15]
}

dfCalculosSim = pd.DataFrame(tablaCalculosSim)

print(dfCalculosSim)
"""
# Define the Excel file path
excel_file_path2 = 'calculosIsTnSimulados.xlsx'

# Export the DataFrame to Excel
dfCalculosSim.to_excel(excel_file_path2, index=False)
"""
#####################################################################################################################################

EAIs4001 =round( 2.52394716489728e-08 - 1.67952572224708e-08 , 9)
EAIs4148 =round( 1.57699431681667e-07 - 1.35365176667382e-07, 9)
EAb4001 = round(18.93187752286 - 19.448444909307, 3)
EAb4148 = round(15.2573712034044 - 15.4256908838734, 3)
EAn4001 = round(2.089090776049 - 2.03360273228681, 3)
EAn4148 = round(2.59221658692235 - 2.5639312367943, 3)

ERIs4001  = round(EAIs4001 / 1.67952572224708e-08, 3)
ERIs4148  = round(EAIs4148 / 1.35365176667382e-07, 3)
ERb4001   = round(EAb4001  / 19.448444909307, 3)
ERb4148   = round(EAb4148  / 15.4256908838734, 3)
ERn4001   = round(EAn4001  / 2.03360273228681, 3)
ERn4148   = round(EAn4148  / 2.5639312367943, 3)



TablaErrores = {
    'Diodos' : ['1n4001', '1n4148'],
    'Is Error Absoluto' : [EAIs4001 , EAIs4148],
    'Is Error Relativo' : [ERIs4001 , ERIs4148 ],
    'b Error Absoluto'  : [EAb4001  , EAb4148 ],
    'b Error Relativo'  : [ERb4001  , ERb4148],
    'n Error Absoluto'  : [EAn4001  , EAn4148 ],
    'n Error Relativo'  : [ERn4001  , ERn4148]
}

dfErrores = pd.DataFrame(TablaErrores)

print(dfErrores)

"""
# Define the Excel file path
excel_file_path3 = 'Errores.xlsx'

# Export the DataFrame to Excel
dfErrores.to_excel(excel_file_path3, index=False)
"""
##############################################################################################################################
#Calcula las rectas de carga
r4001 = Recta(calculate_fitted_values(real4001VD[-1], paramsR4001))
r4148 = Recta(calculate_fitted_values(real4148VD[-1], paramsR4148))
rCautin = Recta(calculate_fitted_values(real4001VDCautin[-1], paramsR4001Cautin))

###############################################################################################################################

graf(sim4001VD, sim4001AD, real4001VD, real4001AD  ,calRA4001 ,r4001[0],r4001[1],0.755,0.0433)
graf(sim4148VD, sim4148AD, real4148VD, real4148AD  ,calRA4148 ,r4148[0],r4148[1],0.825,0.0482)
graf(sim4001VDCautin, sim4001ADCautin, real4001VDCautin, real4001ADCautin  ,calRA4001Cautin ,rCautin[0],rCautin[1],0.647,0.0472)

####################################################################################################
