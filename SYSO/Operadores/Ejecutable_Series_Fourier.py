import numpy as np
import matplotlib.pyplot as plt
from Serie_Fourier import Serie_Fourier as sf
from Generator import Generator as gen

def codigo():
    
    print("Para usar este codigo es necesario definir l,N,fs")
    l = 7
    N = 5000 # numero de sumas
    fs = 10000
    
    #crea el objeto de la clase generadora
    f = gen(-l,l,fs)
    
    #genera la variable independiente con el metodo de la clase generadora
    t = f.t()
    
    
    #genera funciones 
    f1 = f.sq(5,0.7)
    f2 = f.triang(4,0.5)
    f3 = f.new('1.5 * exp(1.2 * t)')
    f4 = f.new('0.5*t**2')
    
    #Las funciones a trozos requeiren 3 atributos, el primero es la funcion, y luego esta el intervalo de los trozos para definir la entrada
    
    trozos1 = np.array([['(1/3)*t**2', -l, 1],
                      ['exp(t)', 1, 4],
                      ['15*sin(t)', 4, l]])    
    f5 = f.new_piece(trozos1) #aca llama a la funcion y le pasa la matriz que indica los trozos
    
    taller2_1 = np.array([['Heaviside(t-10)',-l,-4],
                         ['Heaviside(t+10)',-4,-3],
                         ['Heaviside(t-10)',-3, 0],
                         ['Heaviside(t+10)', 0, 1],
                         ['Heaviside(t-10)', 1, 4],
                         ['Heaviside(t+10)', 4, 5],
                         ['Heaviside(t-10)', 5, l]])
    f6 = f.new_piece(taller2_1)
    
    
    taller2_2 = np.array([['Heaviside(t-10)',-l,-4],
                         ['t + 3',-4,-2],
                         ['Heaviside(t-10)',-2, -1],
                         ['t',-1, 1],
                         ['Heaviside(t-10)', 1, 2],
                         ['t - 3', 2, 4],               
                         ['Heaviside(t-10)', 4, l]])
    
    f7 = f.new_piece(taller2_2)
    
    
    """
    
    #Fourier funcion f1
    sff1 = sf(t,l,N,f1)
    sff1.graf()
    
    #Fourier funcion f2
    sff2 = sf(t,l,N,f2)
    sff2.graf()
    
    #Fourier funcion f3
    sff3 = sf(t,l,N,f3)
    sff3.graf()
    
    #Fourier funcion f4
    sff4 = sf(t,l,N,f4)
    sff4.graf()
    
    #Fourier funcion f5
    sff5 = sf(t,l,N,f5)
    sff5.graf()
    """

    
    #Fourier funcion f6
    sff6 = sf(t,l,N,f6)
    sff6.graf()
    
    #Fourier funcion f7
    sff7 = sf(t,l,N,f7)
    sff7.graf()
    
    
 ##################################################################################################################################################################################   
if __name__ == "__main__":
    codigo()



    
    
