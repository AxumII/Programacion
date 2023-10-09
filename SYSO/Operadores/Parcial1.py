import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as sg


from Convolucion import Convolucion as cv
from Generator import Generator as gen
from Integral_Fourier import Integral_Fourier as intf

def autocorrelation(signal):
            N = len(signal)
            autocorr = np.correlate(signal, signal, mode='full')  # Calcula la autocorrelación cruzada
            autocorr = autocorr / np.max(autocorr)  # Normaliza la autocorrelación
            return autocorr[N-1:]  # Conserva solo la mitad derecha de la autocorrelación



def codigo():
    
    l = 6
    fs = 500    
    fsn = l*2
    
    #crea el objeto de la clase generadora
    f = gen(-l,l,fs)    
    #genera la variable independiente con el metodo de la clase generadora
    t = f.t()
    
    fn = gen(-l,l,fsn) 
    
    n = f.n()
    
   
    
    
    #PRIMER  y SEGUNDO PUNTO
    
           
    #Las funciones a trozos requeiren 3 atributos, el primero es la funcion, y luego esta el intervalo de los trozos para definir la entrada
    trozos1 = np.array([['Heaviside(t-10)',-l,-0],                         
                         ['t',0, 2],                         
                         ['Heaviside(t)', 2, 3],
                         ['Heaviside(t-10)', 3, l]])
    f1 = f.new_piece(trozos1) #aca llama a la funcion y le pasa la matriz que indica los trozos
    
    trozos2 = np.array([['Heaviside(t-10)',-l,-2],                              
                         ['Heaviside(t+2)', -2, -1],
                         ['Heaviside(t-10)', -1, l]])  
     
    f2 = f.new_piece(trozos2) #aca llama a la funcion y le pasa la matriz que indica los trozos
    
    
    
    a = 1
    b = 5+1
    trozos3 = np.array([['Heaviside(t+10)',-l,a],                         
                         ['t',a, b],                       
                         ['Heaviside(t+10)', b, l]])
    
    f3 = fn.new_piece(trozos3) #aca llama a la funcion y le pasa la matriz que indica los trozos
    
    a = -4
    b = -1  +1
      
    trozos4 = np.array([['Heaviside(t+10)',-l,a],                         
                         ['t',a, b],                       
                         ['Heaviside(t+10)', b, l]])
    
    
    f4 = fn.new_piece(trozos4) #aca llama a la funcion y le pasa la matriz que indica los trozos
    
    
    #TERCER PUNTO
    
    
    
    trozos5 = np.array([['Heaviside(t-10)',-l,-4],
                         ['Heaviside(t+10)',-4,-3],
                         ['Heaviside(t-10)',-3, 0],
                         ['Heaviside(t+10)', 0, 1],
                         ['Heaviside(t-10)', 1, 4],
                         ['Heaviside(t-10)', 4, 5],
                         ['Heaviside(t+10)', 5, l]])
    
    f5 = f.new_piece(trozos5) #aca llama a la funcion y le pasa la matriz que indica los trozos
    
    
    
    
    
    
    
    
    
    
    
########################################################################################################################################################################    
    
########################################################################################################################################################################   
    
########################################################################################################################################################################   
    
########################################################################################################################################################################
    """c1 = cv(t,f1,f2)
    c1.graf()
    
    c2 = cv(n,f3,f4)
    c2.graf()
    """
    
    iff1 = intf(t,f5, threshold=0.2)
    iff1.graf()

    

    autocorr = autocorrelation(f5)    
    peaks, _ = sg.find_peaks(autocorr, height=0.3)  # Ajusta el valor de "height" según tu caso
    
    print(peaks)
    
    is_periodic = len(peaks) > 1  # Se considera periódica si hay más de un pico en la autocorrelación
    frequency = 1 / (t[peaks[1]] - t[peaks[0]])  # Frecuencia en Hz
    
    
    print(is_periodic, frequency)
    
    
    
    
    
    
codigo()