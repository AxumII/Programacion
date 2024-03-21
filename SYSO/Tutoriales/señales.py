import numpy as np
import sympy as sp
import scipy.signal as signal
import matplotlib.pyplot as plt

def createSignal():
    fs = 1000  # Frecuencia de muestreo
    t = np.linspace(0, 1, fs, endpoint=False)  # Vector de tiempo

    # Señal cuadrada
    square_wave = signal.square(2 * np.pi * 5 * t)

    # Señal sinusoidal
    sin_wave = np.sin(2 * np.pi * 10 * t)

    # Señal triangular
    triangular_wave = signal.sawtooth(2 * np.pi * 5 * t, width=0.5)

    # Señal diente de sierra
    sawtooth_wave = signal.sawtooth(2 * np.pi * 5 * t)

    # Graficar las señales
    fig = plt.figure(figsize=(10, 6))

    graf1 = fig.add_subplot(4, 1, 1)
    graf1.plot(t, square_wave)
    graf1.set_title('Señal Cuadrada')

    graf2= fig.add_subplot(4, 1, 2)
    graf2.plot(t, sin_wave)
    graf2.set_title('Señal Sinusoidal')

    graf3= fig.add_subplot(4, 1, 3)
    graf3.plot(t, triangular_wave)
    graf3.set_title('Señal Triangular')

    graf4= fig.add_subplot(4, 1, 4)
    graf4.plot(t, sawtooth_wave)
    graf4.set_title('Señal Diente de Sierra')

    plt.tight_layout()
    plt.show()
        
def desfasar():
    print("desfasar")
    fs = 1000  # Frecuencia de muestreo
    w = 10
    t = np.linspace(0, 1, fs, endpoint=False)  # Vector de tiempo
    standart = np.sin(2 * np.pi * w * t)
    desfase = np.pi/3
    modified = np.sin(2 * np.pi * w * t + desfase)  
    
    
    # Convertir el vector de tiempo a radianes
    t_rad = 2 * np.pi * w * t
    
    fig = plt.figure(figsize=(10, 6))
    graf2 = fig.add_subplot(1, 1, 1)
    graf2.plot(t_rad, standart)
    graf2.plot(t_rad, modified)
    graf2.set_title('Señal Sinusoidal')
    graf2.set_xlabel('Radianes')
    
    plt.show()
    
def invertir():
    print("invertir")
    fs = 1000  # Frecuencia de muestreo
    w = 10
    t = np.linspace(0, 1, fs, endpoint=False)  # Vector de tiempo
    standart = np.sin(2 * np.pi * w * t)
    desfase = np.pi/3
    modified =  standart[::-1]

    # Convertir el vector de tiempo a radianes
    t_rad = 2 * np.pi * w * t
    
    fig = plt.figure(figsize=(10, 6))
    graf2 = fig.add_subplot(1, 1, 1)
    graf2.plot(t_rad, standart)
    graf2.plot(t_rad, modified)
    graf2.set_title('Señal Sinusoidal')
    graf2.set_xlabel('Radianes')
    
    plt.show()
    
def escalar():
    print("escalar")
    fs = 1000  # Frecuencia de muestreo
    w = 10
    t = np.linspace(0, 1, fs, endpoint=False)  # Vector de tiempo
    standart = np.sin(2 * np.pi * w * t)
    escala = 3
    modified = escala * np.sin(2 * np.pi * w * t )  
    
    
    # Convertir el vector de tiempo a radianes
    t_rad = 2 * np.pi * w * t
    
    fig = plt.figure(figsize=(10, 6))
    graf2 = fig.add_subplot(1, 1, 1)
    graf2.plot(t_rad, standart)
    graf2.plot(t_rad, modified)
    graf2.set_title('Señal Sinusoidal')
    graf2.set_xlabel('Radianes')
    
    plt.show()
    
def opb():
    print("op basicas")
        
###################################################################################################################################################################################
#createSignal()
#desfasar()
#invertir()
#escalar()