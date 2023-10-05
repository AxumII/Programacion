import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd

    
def exponential_func(x, a, b):
    return a * np.exp(b * x)

def fit_exponential(x, y):
    params, covariance = curve_fit(exponential_func, x, y)
    return params

def calculate_fitted_values(x, params):
    a, b = params
    return np.exp(b * x) * a
    
def graf(x,y1,y2):
    
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))
    
    # Primer gráfico
    ax1.plot(x, y1, label = "Valores de Simulacion", color = "green")
    ax1.set_title('Simulacion del Diodo')
    ax1.set_xlabel("Voltaje Diodo (V)", fontsize=12, fontstyle="italic")
    ax1.set_ylabel("Corriente en Diodo (mA)", fontsize=12, fontstyle="italic")
    ax1.legend()
    ax1.grid(True)

    # Segundo Grafico
    ax2.plot(x, y2, label = "Valores de Regresion", color = "orange")
    ax2.set_title('Curva Caracteristica')
    ax2.set_xlabel("Voltaje Diodo (V)", fontsize=12, fontstyle="italic")
    ax2.set_ylabel("Corriente en Diodo (mA)", fontsize=12, fontstyle="italic")
    ax2.legend()
    ax2.grid(True)

    # Tercer Grafico
    ax3.plot(x, y1, label='Simulacion', color = "green", linewidth = "2")
    ax3.plot(x, y2, label='Curva Caracteristica', color = "orange", linestyle = "dashdot")
    ax3.set_title('Simulacion vs Calculo curva')
    ax3.set_xlabel("Voltaje Diodo (V)", fontsize=12, fontstyle="italic")
    ax3.set_ylabel("Corriente en Diodo (mA)", fontsize=12, fontstyle="italic")
    ax3.grid(True)
    ax3.legend()  # Agregar leyenda para diferenciar las curvas

    plt.tight_layout()
    plt.show()

    
#############################################################################   

# Definición de los datos
sim4001VD25 = np.array([
    0, 0.446, 0.556, 0.615, 0.643, 0.661, 0.674, 0.685, 0.694, 0.702, 0.708, 0.714, 0.719, 0.724,
    0.729, 0.733, 0.737, 0.74, 0.743, 0.747, 0.75, 0.752, 0.755, 0.758, 0.76, 0.762, 0.765
])

sim4001AD25 = np.array([
    0, 0.000106, 0.00088, 0.0027, 0.0047, 0.0066, 0.0085, 0.01, 0.012, 0.0145, 0.016, 0.018,
    0.02, 0.022, 0.024, 0.026, 0.028, 0.03, 0.032, 0.034, 0.036, 0.038, 0.04, 0.042, 0.044,
    0.046, 0.049
])/1000

sim4148VD25 = np.array([
    0, 0.469, 0.598, 0.658, 0.687, 0.705, 0.719, 0.731, 0.741, 0.749, 0.757, 0.764, 0.77, 0.776,
    0.781, 0.787, 0.791, 0.796, 0.8, 0.805, 0.809, 0.813, 0.816, 0.82, 0.824, 0.827, 0.83
])

sim4148AD25 = np.array([
    0, 0.0006, 0.0008, 0.0026, 0.0046, 0.0065, 0.0085, 0.01, 0.012, 0.014, 0.016, 0.018,
    0.02, 0.022, 0.024, 0.026, 0.028, 0.03, 0.032, 0.034, 0.036, 0.038, 0.04, 0.042, 0.044,
    0.046, 0.048
])/1000

sim4001VD25Hot = np.array([
    0,
    0.343,
    0.406,
    0.451,
    0.475,
    0.49,
    0.502,
    0.512,
    0.52,
    0.527,
    0.533,
    0.538,
    0.543,
    0.547,
    0.551,
    0.555,
    0.558,
    0.562,
    0.565,
    0.567,
    0.571,
    0.573,
    0.576,
    0.578,
    0.580,
    0.582,
    0.584
])

sim4001AD25Hot = np.array([
    0,
    0.00031364,
    0.001187,
    0.003096,
    0.005049,
    0.007018,
    0.008994,
    0.010976,
    0.01296,
    0.014946,
    0.016934,
    0.018923,
    0.020914,
    0.022905,
    0.024897,
    0.026889,
    0.028882,
    0.030876,
    0.03287,
    0.034864,
    0.036859,
    0.038853,
    0.040849,
    0.042844,
    0.044839,
    0.046835,
    0.048831
])/1000

sim4148VD25Hot = np.array([
    0,
    0.33,
    0.404,
    0.462,
    0.492,
    0.513,
    0.528,
    0.541,
    0.552,
    0.562,
    0.571,
    0.578,
    0.585,
    0.592,
    0.598,
    0.604,
    0.609,
    0.614,
    0.619,
    0.624,
    0.628,
    0.632,
    0.636,
    0.641,
    0.644,
    0.648,
    0.652
])

sim4148AD25Hot = np.array([
    0,
    0.0003397,
    0.0011902,
    0.0030755,
    0.0050152,
    0.0069739,
    0.0089421,
    0.010916,
    0.012894,
    0.014875,
    0.016858,
    0.018842,
    0.020828,
    0.022815,
    0.024803,
    0.026792,
    0.028781,
    0.030771,
    0.032761,
    0.034752,
    0.036743,
    0.038734,
    0.040726,
    0.042718,
    0.04471,
    0.046703,
    0.048696
])/1000

sim4001VD25Cold = np.array([
    0,    
    0.848,
    0.884,
    0.896,
    0.903,
    0.909,
    0.913,
    0.916,
    0.919,
    0.922,
    0.924,
    0.926,
    0.928,
    0.929,
    0.931,
    0.932,
    0.934,
    0.935,
    0.936,
    0.937,
    0.938,
    0.939,
    0.94,
    0.941,
    0.942,
    0.943
])

sim4001AD25Cold = np.array([
    0,
    0.0003,
    0.0022,
    0.0042,
    0.0061,
    0.0081,
    0.010,
    0.012,
    0.014,
    0.016,
    0.018,
    0.020,
    0.022,
    0.024,
    0.026,
    0.028,
    0.030,
    0.032,
    0.034,
    0.036,
    0.038,
    0.040,
    0.042,
    0.044,
    0.046,
    0.048])/1000

sim4148VD25Cold = np.array([
    0,   
    0.841,
    0.888,
    0.903,
    0.913,
    0.921,
    0.927,
    0.932,
    0.937,
    0.941,
    0.945,
    0.949,
    0.952,
    0.955,
    0.958,
    0.961,
    0.964,
    0.966,
    0.969,
    0.971,
    0.974,
    0.976,
    0.978,
    0.98,
    0.983,
    0.985
])

sim4148AD25Cold = np.array([
    0,    
    0.00031,
    0.0022,
    0.0041,
    0.0061,
    0.0081,
    0.010,
    0.012,
    0.014,
    0.016,
    0.018,
    0.020,
    0.022,
    0.024,
    0.026,
    0.028,
    0.030,
    0.032,
    0.034,
    0.036,
    0.038,
    0.040,
    0.042,
    0.044,
    0.046,
    0.048])/1000



####################################################

# Ajuste exponencial para sim4001VD25 y sim4001AD25
params4001 = fit_exponential(sim4001VD25, sim4001AD25)
calA4001 = calculate_fitted_values(sim4001VD25, params4001)

# Ajuste exponencial para sim4148VD25 y sim4148AD25
params4148 = fit_exponential(sim4148VD25, sim4148AD25)
calA4148 = calculate_fitted_values(sim4148VD25, params4148)



# Ajuste exponencial para sim4001VD25 y sim4001AD25  CALIENTE
params4001Hot = fit_exponential(sim4001VD25Hot, sim4001AD25Hot)
calA4001Hot = calculate_fitted_values(sim4001VD25Hot, params4001Hot)

# Ajuste exponencial para sim4148VD25 y sim4148AD25 CALIENTE
params4148Hot = fit_exponential(sim4148VD25Hot, sim4148AD25Hot)
calA4148Hot = calculate_fitted_values(sim4148VD25Hot, params4148Hot)



# Ajuste exponencial para sim4001VD25 y sim4001AD25    FRIO
#params4001Cold = fit_exponential(sim4001VD25Cold, sim4001AD25Cold)
#calA4001Cold = calculate_fitted_values(sim4001VD25Cold, params4001Cold)

# Ajuste exponencial para sim4148VD25 y sim4148AD25  FRIO
params4148Cold = fit_exponential(sim4148VD25Cold, sim4148AD25Cold)
calA4148Cold = calculate_fitted_values(sim4148VD25Cold, params4148Cold)

###############################################################################################################################
#Tabla de datos de parametros
parameters_data = {
    'Diodos': ['1n4001', '1n4148', '1n4001 120°C', '1n4148 120°C', '1n4148 -120°C' ],
    'a': [params4001[0], params4148[0], params4001Hot[0] , params4148Hot[0] , params4148Cold[0]],
    'b': [params4001[1], params4148[1], params4001Hot[1] , params4148Hot[1] , params4148Cold[1] ]
} 

# Create a Pandas DataFrame
parameters_df = pd.DataFrame(parameters_data)

print(parameters_df)



# Define the Excel file path
excel_file_path = 'exponential_parameters25VSim.xlsx'

# Export the DataFrame to Excel
parameters_df.to_excel(excel_file_path, index=False)


##############################################################################################################################

##############################################################################################################################

#Calculos Is, n y T

K = 1.38e-23
q = 1.6e-19
Tamb = 293.15
THot = Tamb + 100
TCold = Tamb -140

def nDesc(b,T):
    return (q/(b*T*K))
    
def TDesc(b,n):
    return (q/(b*n*K))


tablaCalculos = {
    'Diodos': ['1n4001', '1n4148', '1n4001 120°C', '1n4148 120°C', '1n4148 -120°C' ],
    'Is':  [params4001[0], params4148[0], params4001Hot[0] , params4148Hot[0] , params4148Cold[0]],
    'b': [params4001[1], params4148[1], params4001Hot[1] , params4148Hot[1] , params4148Cold[1] ],
    'n' : [ nDesc(params4001[1],Tamb), nDesc(params4148[1],Tamb) , nDesc(params4001Hot[1],THot), nDesc(params4148Hot[1],THot), nDesc(params4148Cold[1],TCold) ],
    'T en °K' : [ Tamb, Tamb, THot, THot, TCold],
    'T en °C' : [Tamb-273.15, Tamb-273.15,  THot-273.15, THot-273.15, TCold -273.15]
}

dfCalculos = pd.DataFrame(tablaCalculos)

print(dfCalculos)

# Define the Excel file path
excel_file_path2 = 'calculosIs_n_25Sim.xlsx'

# Export the DataFrame to Excel
dfCalculos.to_excel(excel_file_path2, index=False)

##############################################################################################################################

##################################################################################

# Graficar los datos originales y las curvas ajustadas

graf(sim4001VD25, sim4001AD25, calA4001)
graf(sim4148VD25, sim4148AD25, calA4148)

graf(sim4001VD25Hot, sim4001AD25Hot, calA4001Hot)
graf(sim4148VD25Hot, sim4148AD25Hot, calA4148Hot)

graf(sim4001VD25Cold, sim4001AD25Cold, sim4001VD25Cold)
#graf(sim4001VD25Cold, sim4001AD25Cold, calA4001Cold)
graf(sim4148VD25Cold, sim4148AD25Cold, calA4148Cold)




