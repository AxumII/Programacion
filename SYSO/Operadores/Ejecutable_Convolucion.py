import numpy as np
import matplotlib.pyplot as plt
from Convolucion import Convolucion as cv
from Generator import Generator as gen

def codigo():
    
    l = 8
    fs = 500    
    
    
    #crea el objeto de la clase generadora
    f = gen(-l,l,fs)    
    #genera la variable independiente con el metodo de la clase generadora
    t = f.t()
    
    
    #genera funciones 
    f1 = f.sq(5,3)
    f2 = f.triang(4,4)
    f3 = f.new('1.5 * exp(1.2 * t)')
    f6 = f.sen(3, 2)
    
    
    #Las funciones a trozos requeiren 3 atributos, el primero es la funcion, y luego esta el intervalo de los trozos para definir la entrada
    trozos1 = np.array([['(1/3)*t**2', -l, 1],
                      ['exp(t)', 1, 4],
                      ['15*sin(t)', 4, l]])    
    f4 = f.new_piece(trozos1) #aca llama a la funcion y le pasa la matriz que indica los trozos
    
    trozos2 = np.array([['2*(t+6)* (t+5.1) *(t+7.5)', -l, -5.1],
                      ['-15 *( (t + 5.1) * (t + 3.72))', -5.1,-3.72 ],
                      ['(1/60)*(t**4 - 3*(t**3) - 30*(t**2) -5*t + 50 )', -3.72, l]])   
     
    f5 = f.new_piece(trozos2) #aca llama a la funcion y le pasa la matriz que indica los trozos
    
    
    #######################################################################################
    
    c1 = cv(t,f6,f1)
    c1.graf()
    
    
codigo()