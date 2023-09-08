import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt



#Variables


def p1_1():
    #Parametros
    A = 10
    f = 10 
    w = 2*np.pi*f
    fm = 0.001
    
    t = np.arange(-5,5+fm,fm)

    señal = A * np.sin(w*t)
    return t,señal,A,f,fm

def p1_2():
    #Parametros
    A = 10
    f = 10 
    w = 2*np.pi*f
    fm = 0.1
    
    t = np.arange(-5,5+fm,fm)

    señal = A * np.sin(w*t)
    return t,señal,A,f,fm

def p1_3():
     #Parametros
    A = 10
    f = 10 
    w = 2*np.pi*f
    fm = 0.001
    
    t = np.arange(-5,5+fm,fm)
    
    señal = A*signal.square(w*t)
    return t,señal,A,f,fm

def p1_4():
     #Parametros
    A = 10
    f = 10 
    w = 2*np.pi*f
    fm = 0.1
    
    
    t = np.arange(-5,5+fm,fm)       
    señal = A*signal.square(w*t)

    
    return t,señal,A,f,fm

def p1_5():    
     #Parametros
    A = 10
    f = 10 
    w = 2*np.pi*f
    fm = 0.001
    
    t = np.arange(-5,5+fm,fm)
    
    señal = A*signal.sawtooth(w*t, width=0.5)
    return t,señal,A,f,fm

def p1_6():    
     #Parametros
    A = 10
    f = 10 
    w = 2*np.pi*f
    fm = 0.1
    
    t = np.arange(-5,5+fm,fm)
    
    señal = A*signal.sawtooth(w*t, width=0.5)
    return t,señal,A,f,fm

def p1_7():    
     #Parametros
    A = 10
    f = 10 
    w = 2*np.pi*f
    fm = 0.001
    
    t = np.arange(-5,5+fm,fm)
    
    señal = A*signal.sawtooth(w*t)
    return t,señal,A,f,fm

def p1_8():    
     #Parametros
    A = 10
    f = 10 
    w = 2*np.pi*f
    fm = 0.1
    
    t = np.arange(-5,5+fm,fm)
    
    señal = A*signal.sawtooth(w*t)
    return t,señal,A,f,fm

def p1_9():    
     #Parametros
    A = 10
    f = 10 
    w = 2*np.pi*f
    fm = 0.001
    
    t = np.arange(-5,5+fm,fm)
    
    señal = -A*signal.sawtooth(w*t)
    return t,señal,A,f,fm

def p1_10():
    #Parametros
    A = 10
    f = 10 
    w = 2*np.pi*f
    fm = 0.1
    
    t = np.arange(-5,5+fm,fm)
    
    señal = -A*signal.sawtooth(w*t)
    return t,señal,A,f,fm

def p2():
    #Parametros
    fm = 0.1
    d = 3
    
    t = np.arange(-10,10,fm)
    
    señal1 = (t + d)**2
    señal2 = (t - d)**2
    y = t**2
    return t,señal1,señal2,fm,d,y

def p3_1():    
    # Parametros
    fm = 0.1
    d = -1
    
    t = np.arange(-10, 10 + fm, fm) 
    
    señal1 = (t - d)**2  
    señal2 = señal1[::-1]
    
    return t, señal1, señal2, fm, d

def p3_2():    
    # Parametros
    fm = 0.1
    d = -1
    
    t1 = np.arange(-10, 0 + fm, fm)
    t2 = np.arange(0, 10 + fm, fm)
    t = np.concatenate((t1, t2))
    
    trozo1 = (t1 - d) ** 2  
    trozo2 = np.zeros_like(t2)
    
    señal1 = np.concatenate((trozo1, trozo2))
    señal2 = señal1[::-1]
    
    return t, señal1, señal2, fm, d

def p4_1():
#Parametros
    fm = 0.1
    d = 0
    c = 1/3
    t = np.arange(-10,10,fm)
    tc = t*c
    
    señal1 = (t + d)**2
    señal2 = (tc + d)**2
    
    return t,señal1,tc,fm,d,c

def p4_2():
#Parametros
    fm = 0.1
    d = 0
    c = 3
    t = np.arange(-10,10,fm)
    tc = t*c
    
    señal1 = (t + d)**2
    señal2 = (tc + d)**2
    
    return t,señal1,tc,fm,d,c

def p4_3():    
    #Parametros
    fm = 0.1
    d = -1
    c = 3
    
    
    t1 = np.arange(-10, 0 + fm, fm)
    t2 = np.arange(0, 10 + fm, fm)
    t = np.concatenate((t1, t2))
    
    t1c = c*np.arange(-10,0+fm,fm)
    t2c = c*np.arange(0,10+fm,fm)
    tc = np.concatenate((t1c, t2c))
    
    trozo1 = np.zeros_like(t2) 
    trozo2 = (t2 + d) ** 2
    
    
    trozoa = np.zeros_like(t2) 
    trozob = (t2 + d) ** 2
     
    

    señal1 = np.concatenate((trozo1,trozo2))
    señal2 = np.concatenate((trozoa,trozob))
    
    return t,señal1,tc,fm,d,c




#########################################################################################################
#Graficas

#Puntos 1.1 a 1.4
def graf1(): 
     # Crear la figura y los subplots
    fig, axes = plt.subplots(nrows=2, ncols=2) # 5 filas, 2 columnas

    # Iterar a través de cada subplot
    for i, row in enumerate(axes):
        for j, ax in enumerate(row):
            
            # fila 0, col 0
            if i == 0 and j == 0:
                t,y,A,f,fm= p1_1()            
                ax.plot(t,y, linewidth=1.0, label="y(t)")
                ax.scatter(0, 0, color='red', label='Amplitud = {:.1f}\nFrecuencia = {:.1f}\nFrecuencia de Muestreo = {:.3f}\n'.format(A, f, fm), s=10)
                
                
                ax.set_title("Punto 1_1: Sinusoidal)")
                ax.set_xlabel(" t ", fontsize=12, fontstyle="italic")
                ax.set_ylabel(" y ", fontsize=12, fontstyle="italic")
                
                ax.set_xlim(-6, 6)
                ax.set_ylim(-15, 15)
                
                ax.axhline(0, color='black', linewidth=0.8)  # Línea horizontal en y = 0
                ax.axvline(0, color='black', linewidth=0.8)  # Línea vertical en x = 0

                ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)  # Agregar una cuadrícula

                
                ax.legend(fontsize=8 ,loc="upper right")

            if i == 0 and j == 1:
                t,y,A,f,fm= p1_2()            
                ax.plot(t,y, linewidth=1.0, label="y(t)")
                ax.scatter(0, 0, color='red', label='Amplitud = {:.1f}\nFrecuencia = {:.1f}\nFrecuencia de Muestreo = {:.3f}\n'.format(A, f, fm), s=10)
                
                
                ax.set_title("Punto 1_2: Sinusoidal")
                ax.set_xlabel(" t ", fontsize=12, fontstyle="italic")
                ax.set_ylabel(" y ", fontsize=12, fontstyle="italic")
                
                ax.set_xlim(-6, 6)
                ax.set_ylim(-15, 15)
                
                ax.axhline(0, color='black', linewidth=0.8)  # Línea horizontal en y = 0
                ax.axvline(0, color='black', linewidth=0.8)  # Línea vertical en x = 0

                ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)  # Agregar una cuadrícula

                
                ax.legend(fontsize=8 ,loc="upper right")

            if i == 1 and j == 0:
                t,y,A,f,fm= p1_3()            
                ax.plot(t,y, linewidth=1.0, label="y(t)")
                ax.scatter(0, 0, color='red', label='Amplitud = {:.1f}\nFrecuencia = {:.1f}\nFrecuencia de Muestreo = {:.3f}\n'.format(A, f, fm), s=10)
                
                
                ax.set_title("Punto 1_3: Cuadrada")
                ax.set_xlabel(" t ", fontsize=12, fontstyle="italic")
                ax.set_ylabel(" y ", fontsize=12, fontstyle="italic")
                
                ax.set_xlim(-6, 6)
                ax.set_ylim(-15, 15)
                
                ax.axhline(0, color='black', linewidth=0.8)  # Línea horizontal en y = 0
                ax.axvline(0, color='black', linewidth=0.8)  # Línea vertical en x = 0

                ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)  # Agregar una cuadrícula

                
                ax.legend(fontsize=8 ,loc="upper right")

            if i == 1 and j == 1:
                t,y,A,f,fm= p1_4()            
                ax.plot(t,y, linewidth = 1.0, label="y(t)")
                ax.scatter(0, 0, color='red', label='Amplitud = {:.1f}\nFrecuencia = {:.1f}\nFrecuencia de Muestreo = {:.3f}\n'.format(A, f, fm), s=10)
                
                
                ax.set_title("Punto 1_4: Cuadrada")
                ax.set_xlabel(" t ", fontsize=12, fontstyle="italic")
                ax.set_ylabel(" y ", fontsize=12, fontstyle="italic")
                
                ax.set_xlim(-6, 6)
                ax.set_ylim(-15, 15)
                
                ax.axhline(0, color='black', linewidth=0.8)  # Línea horizontal en y = 0
                ax.axvline(0, color='black', linewidth=0.8)  # Línea vertical en x = 0

                ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)  # Agregar una cuadrícula

                
                ax.legend(fontsize=8 ,loc="upper right")


    # Ajustar los subplots para evitar superposiciones
    plt.tight_layout()
    plt.show()

#Puntos 1.5 a 1.8   
def graf2():
     # Crear la figura y los subplots
    fig, axes = plt.subplots(nrows=2, ncols=2) # 5 filas, 2 columnas

    # Iterar a través de cada subplot
    for i, row in enumerate(axes):
        for j, ax in enumerate(row):
            
            # fila 0, col 0
            if i == 0 and j == 0:
                t,y,A,f,fm= p1_5()            
                ax.plot(t,y, linewidth=1.0, label="y(t)")
                ax.scatter(0, 0, color='red', label='Amplitud = {:.1f}\nFrecuencia = {:.1f}\nFrecuencia de Muestreo = {:.3f}\n'.format(A, f, fm), s=10)
                
                
                ax.set_title("Punto 1_5: Triangular")
                ax.set_xlabel(" t ", fontsize=12, fontstyle="italic")
                ax.set_ylabel(" y ", fontsize=12, fontstyle="italic")
                
                ax.set_xlim(-6, 6)
                ax.set_ylim(-15, 15)
                
                ax.axhline(0, color='black', linewidth=0.8)  # Línea horizontal en y = 0
                ax.axvline(0, color='black', linewidth=0.8)  # Línea vertical en x = 0

                ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)  # Agregar una cuadrícula

                
                ax.legend(fontsize=8 ,loc="upper right")

            if i == 0 and j == 1:
                t,y,A,f,fm= p1_6()            
                ax.plot(t,y, linewidth=1.0, label="y(t)")
                ax.scatter(0, 0, color='red', label='Amplitud = {:.1f}\nFrecuencia = {:.1f}\nFrecuencia de Muestreo = {:.3f}\n'.format(A, f, fm), s=10)
                
                
                ax.set_title("Punto 1_6: Triangular")
                ax.set_xlabel(" t ", fontsize=12, fontstyle="italic")
                ax.set_ylabel(" y ", fontsize=12, fontstyle="italic")
                
                ax.set_xlim(-6, 6)
                ax.set_ylim(-15, 15)
                
                ax.axhline(0, color='black', linewidth=0.8)  # Línea horizontal en y = 0
                ax.axvline(0, color='black', linewidth=0.8)  # Línea vertical en x = 0

                ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)  # Agregar una cuadrícula

                
                ax.legend(fontsize=8 ,loc="upper right")

            if i == 1 and j == 0:
                t,y,A,f,fm= p1_7()            
                ax.plot(t,y, linewidth=1.0, label="y(t)")
                ax.scatter(0, 0, color='red', label='Amplitud = {:.1f}\nFrecuencia = {:.1f}\nFrecuencia de Muestreo = {:.3f}\n'.format(A, f, fm), s=10)
                
                
                ax.set_title("Punto 1_7: Diente de Sierra")
                ax.set_xlabel(" t ", fontsize=12, fontstyle="italic")
                ax.set_ylabel(" y ", fontsize=12, fontstyle="italic")
                
                ax.set_xlim(-6, 6)
                ax.set_ylim(-15, 15)
                
                ax.axhline(0, color='black', linewidth=0.8)  # Línea horizontal en y = 0
                ax.axvline(0, color='black', linewidth=0.8)  # Línea vertical en x = 0

                ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)  # Agregar una cuadrícula

                
                ax.legend(fontsize=8 ,loc="upper right")

            if i == 1 and j == 1:
                t,y,A,f,fm= p1_8()            
                ax.plot(t,y, linewidth=1.0, label="y(t)")
                ax.scatter(0, 0, color='red', label='Amplitud = {:.1f}\nFrecuencia = {:.1f}\nFrecuencia de Muestreo = {:.3f}\n'.format(A, f, fm), s=10)
                
                
                ax.set_title("Punto 1_8: Diente de Sierra")
                ax.set_xlabel(" t ", fontsize=12, fontstyle="italic")
                ax.set_ylabel(" y ", fontsize=12, fontstyle="italic")
                
                ax.set_xlim(-6, 6)
                ax.set_ylim(-15, 15)
                
                ax.axhline(0, color='black', linewidth=0.8)  # Línea horizontal en y = 0
                ax.axvline(0, color='black', linewidth=0.8)  # Línea vertical en x = 0

                ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)  # Agregar una cuadrícula

                
                ax.legend(fontsize=8 ,loc="upper right")


    # Ajustar los subplots para evitar superposiciones
    plt.tight_layout()
    plt.show()
  
#Puntos 1.9 y 1.10      
def graf3():
     # Crear la figura y los subplots
    fig, axes = plt.subplots(nrows=2, ncols=2) # 5 filas, 2 columnas

    # Iterar a través de cada subplot
    for i, row in enumerate(axes):
        for j, ax in enumerate(row):
            
            # fila 0, col 0
            if i == 0 and j == 0:
                t,y,A,f,fm= p1_9()            
                ax.plot(t,y, linewidth=1.0, label="y(t)")
                ax.scatter(0, 0, color='red', label='Amplitud = {:.1f}\nFrecuencia = {:.1f}\nFrecuencia de Muestreo = {:.3f}\n'.format(A, f, fm), s=10)
                
                
                ax.set_title("Punto 1_9: Diente de Sierra Invertida")
                ax.set_xlabel(" t ", fontsize=12, fontstyle="italic")
                ax.set_ylabel(" y ", fontsize=12, fontstyle="italic")
                
                ax.set_xlim(-6, 6)
                ax.set_ylim(-15, 15)
                
                ax.axhline(0, color='black', linewidth=0.8)  # Línea horizontal en y = 0
                ax.axvline(0, color='black', linewidth=0.8)  # Línea vertical en x = 0

                ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)  # Agregar una cuadrícula

                
                ax.legend(fontsize=8 ,loc="upper right")

            if i == 0 and j == 1:
                t,y,A,f,fm= p1_10()            
                ax.plot(t,y, linewidth=1.0, label="y(t)")
                ax.scatter(0, 0, color='red', label='Amplitud = {:.1f}\nFrecuencia = {:.1f}\nFrecuencia de Muestreo = {:.3f}\n'.format(A, f, fm), s=10)
                
                
                ax.set_title("Punto 1_10: Diente de Sierra Invertida")
                ax.set_xlabel(" t ", fontsize=12, fontstyle="italic")
                ax.set_ylabel(" y ", fontsize=12, fontstyle="italic")
                
                ax.set_xlim(-6, 6)
                ax.set_ylim(-15, 15)
                
                ax.axhline(0, color='black', linewidth=0.8)  # Línea horizontal en y = 0
                ax.axvline(0, color='black', linewidth=0.8)  # Línea vertical en x = 0

                ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)  # Agregar una cuadrícula

                
                ax.legend(fontsize=8 ,loc="upper right")

            


    # Ajustar los subplots para evitar superposiciones
    plt.tight_layout()
    plt.show()

#Punto 2
def graf4():
     # Crear la figura y los subplots
    fig, axes = plt.subplots(nrows=2, ncols=2) # 5 filas, 2 columnas

    # Iterar a través de cada subplot
    for i, row in enumerate(axes):
        for j, ax in enumerate(row):
            
            # fila 0, col 0
            if i == 0 and j == 0:
                t,y1,y2,fm,d,y= p2()            
                ax.plot(t,y, linewidth=1.0, label="y(t)", color = "orange")
                ax.scatter(0, 0, color='red', label='Desfase = {:.1f}\nFrecuencia de Muestreo = {:.3f}'.format(d, fm), s=10)
                
                
                ax.set_title("Punto 2: Default")
                ax.set_xlabel(" t ", fontsize=12, fontstyle="italic")
                ax.set_ylabel(" y ", fontsize=12, fontstyle="italic")
                
                ax.set_xlim(-12, 12)
                ax.set_ylim(-25, 200)
                
                ax.axhline(0, color='black', linewidth=0.8)  # Línea horizontal en y = 0
                ax.axvline(0, color='black', linewidth=0.8)  # Línea vertical en x = 0

                ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)  # Agregar una cuadrícula

                
                ax.legend(fontsize=8 ,loc="upper right")

            if i == 0 and j == 1:
                t,y1,y2,fm,d,y = p2()            
                ax.plot(t,y1, linewidth=1.0, label="y(t)", color = "orange")
                ax.scatter(0, 0, color='red', label='Desfase = {:.1f}\nFrecuencia de Muestreo = {:.3f}'.format(d, fm), s=10)
                
                
                ax.set_title("Punto 2: Desfase hacia Izquierda")
                ax.set_xlabel(" t ", fontsize=12, fontstyle="italic")
                ax.set_ylabel(" y ", fontsize=12, fontstyle="italic")
                
                ax.set_xlim(-12, 12)
                ax.set_ylim(-25, 200)
                
                ax.axhline(0, color='black', linewidth=0.8)  # Línea horizontal en y = 0
                ax.axvline(0, color='black', linewidth=0.8)  # Línea vertical en x = 0

                ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)  # Agregar una cuadrícula

                
                ax.legend(fontsize=8 ,loc="upper right")
         
            if i == 1 and j == 0:
                t,y1,y2,fm,d,y = p2()            
                ax.plot(t,y, linewidth=1.0, label="y(t)", color = "orange")
                ax.scatter(0, 0, color='red', label='Desfase = {:.1f}\nFrecuencia de Muestreo = {:.3f}'.format(d, fm), s=10)
                
                
                ax.set_title("Punto 2: Default")
                ax.set_xlabel(" t ", fontsize=12, fontstyle="italic")
                ax.set_ylabel(" y ", fontsize=12, fontstyle="italic")
                
                ax.set_xlim(-12, 12)
                ax.set_ylim(-25, 200)
                
                ax.axhline(0, color='black', linewidth=0.8)  # Línea horizontal en y = 0
                ax.axvline(0, color='black', linewidth=0.8)  # Línea vertical en x = 0

                ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)  # Agregar una cuadrícula

                
                ax.legend(fontsize=8 ,loc="upper right")

            if i == 1 and j == 1:
                t,y1,y2,fm,d,y = p2()            
                ax.plot(t,y2, linewidth=1.0, label="y(t)", color = "orange")
                ax.scatter(0, 0, color='red', label='Desfase = {:.1f}\nFrecuencia de Muestreo = {:.3f}'.format(d, fm), s=10)
                
                
                ax.set_title("Punto 2: Desfase hacia Derecha")
                ax.set_xlabel(" t ", fontsize=12, fontstyle="italic")
                ax.set_ylabel(" y ", fontsize=12, fontstyle="italic")
                
                ax.set_xlim(-12, 12)
                ax.set_ylim(-25, 200)
                
                ax.axhline(0, color='black', linewidth=0.8)  # Línea horizontal en y = 0
                ax.axvline(0, color='black', linewidth=0.8)  # Línea vertical en x = 0

                ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)  # Agregar una cuadrícula

                
                ax.legend(fontsize=8 ,loc="upper right")


    # Ajustar los subplots para evitar superposiciones
    plt.tight_layout()
    plt.show()
    
#Punto 3
def graf5():
     # Crear la figura y los subplots
    fig, axes = plt.subplots(nrows=2, ncols=2) # 5 filas, 2 columnas

    # Iterar a través de cada subplot
    for i, row in enumerate(axes):
        for j, ax in enumerate(row):
            
            # fila 0, col 0
            if i == 0 and j == 0:
                t,y1,y2,fm,d = p3_1()            
                ax.plot(t,y1, linewidth=1.0, label="y(t)", color = "orange")
                ax.scatter(0, 0, color='red', label='Desfase = {:.1f}\nFrecuencia de Muestreo = {:.3f}'.format(d, fm), s=10)
                
                
                ax.set_title("Punto 3_1: Default")
                ax.set_xlabel(" t ", fontsize=12, fontstyle="italic")
                ax.set_ylabel(" y ", fontsize=12, fontstyle="italic")
                
                ax.set_xlim(-12, 12)
                ax.set_ylim(-20, 150)
                
                ax.axhline(0, color='black', linewidth=0.8)  # Línea horizontal en y = 0
                ax.axvline(0, color='black', linewidth=0.8)  # Línea vertical en x = 0

                ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)  # Agregar una cuadrícula

                
                ax.legend(fontsize=8 ,loc="upper right")

            if i == 0 and j == 1:
                t,y1,y2,fm,d = p3_1()            
                ax.plot(t,y2, linewidth=1.0, label="y(t)", color = "orange")
                ax.scatter(0, 0, color='red', label='Desfase = {:.1f}\nFrecuencia de Muestreo = {:.3f}'.format(d, fm), s=10)
                
                
                ax.set_title("Punto 3_1: Inversion")
                ax.set_xlabel(" t ", fontsize=12, fontstyle="italic")
                ax.set_ylabel(" y ", fontsize=12, fontstyle="italic")
                
                ax.set_xlim(-12, 12)
                ax.set_ylim(-20, 150)
                
                ax.axhline(0, color='black', linewidth=0.8)  # Línea horizontal en y = 0
                ax.axvline(0, color='black', linewidth=0.8)  # Línea vertical en x = 0

                ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)  # Agregar una cuadrícula

                
                ax.legend(fontsize=8 ,loc="upper right")

            if i == 1 and j == 0:
                t,y1,y2,fm,d = p3_2()            
                ax.plot(t,y1, linewidth=1.0, label="y(t)", color = "orange")
                ax.scatter(0, 0, color='red', label='Desfase = {:.1f}\nFrecuencia de Muestreo = {:.3f}'.format(d, fm), s=10)
                
                
                ax.set_title("Punto 3_2: Default")
                ax.set_xlabel(" t ", fontsize=12, fontstyle="italic")
                ax.set_ylabel(" y ", fontsize=12, fontstyle="italic")
                
                ax.set_xlim(-12, 12)
                ax.set_ylim(-20, 150)
                
                ax.axhline(0, color='black', linewidth=0.8)  # Línea horizontal en y = 0
                ax.axvline(0, color='black', linewidth=0.8)  # Línea vertical en x = 0

                ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)  # Agregar una cuadrícula

                
                ax.legend(fontsize=8 ,loc="upper right")

            if i == 1 and j == 1:
                t,y1,y2,fm,d = p3_2()            
                ax.plot(t,y2, linewidth=1.0, label="y(t)", color = "orange")
                ax.scatter(0, 0, color='red', label='Desfase = {:.1f}\nFrecuencia de Muestreo = {:.3f}'.format(d, fm), s=10)
                
                
                ax.set_title("Punto 3_2: Inversion")
                ax.set_xlabel(" t ", fontsize=12, fontstyle="italic")
                ax.set_ylabel(" y ", fontsize=12, fontstyle="italic")
                
                ax.set_xlim(-12, 12)
                ax.set_ylim(-20, 150)
                
                ax.axhline(0, color='black', linewidth=0.8)  # Línea horizontal en y = 0
                ax.axvline(0, color='black', linewidth=0.8)  # Línea vertical en x = 0

                ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)  # Agregar una cuadrícula

                
                ax.legend(fontsize=8 ,loc="upper right")


    # Ajustar los subplots para evitar superposiciones
    plt.tight_layout()
    plt.show()  
   
#Punto 4.1 y 4.2 
def graf6():
     # Crear la figura y los subplots
    fig, axes = plt.subplots(nrows=2, ncols=2) # 5 filas, 2 columnas

    # Iterar a través de cada subplot
    for i, row in enumerate(axes):
        for j, ax in enumerate(row):
            
            # fila 0, col 0
            if i == 0 and j == 0:
                t,y1,y2,fm,d,c = p4_1()            
                ax.plot(t,y1, linewidth=1.0, label="y(t)", color = "red")
                ax.scatter(0, 0, color='red', label='Desfase = {:.1f}\nFrecuencia de Muestreo = {:.3f}'.format(d, fm), s=10)
                
                
                ax.set_title("Punto 4_1 : Default")
                ax.set_xlabel(" t ", fontsize=12, fontstyle="italic")
                ax.set_ylabel(" y ", fontsize=12, fontstyle="italic")
                
                ax.set_xlim(-35, 35)
                ax.set_ylim(-25, 150)
                
                ax.axhline(0, color='black', linewidth=0.8)  # Línea horizontal en y = 0
                ax.axvline(0, color='black', linewidth=0.8)  # Línea vertical en x = 0

                ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)  # Agregar una cuadrícula

                
                ax.legend(fontsize=8 ,loc="upper right")

            if i == 0 and j == 1:
                t,y1,y2,fm,d,c = p4_1()            
                ax.plot(y2,y1, linewidth=1.0, label="y(t)",color = "red")
                ax.scatter(0, 0, color='red', label='Desfase = {:.1f}\nFrecuencia de Muestreo = {:.3f}\nFactor de Escala = {:.1f}'.format(d, fm,c), s=10)
                
                
                ax.set_title("Punto 4_1: Comprimida")
                ax.set_xlabel(" t ", fontsize=12, fontstyle="italic")
                ax.set_ylabel(" y ", fontsize=12, fontstyle="italic")
                
                ax.set_xlim(-35, 35)
                ax.set_ylim(-25, 150)
                
                ax.axhline(0, color='black', linewidth=0.8)  # Línea horizontal en y = 0
                ax.axvline(0, color='black', linewidth=0.8)  # Línea vertical en x = 0

                ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)  # Agregar una cuadrícula

                
                ax.legend(fontsize=8 ,loc="upper right")

            if i == 1 and j == 0:
                t,y1,y2,fm,d,c = p4_2()            
                ax.plot(t,y1, linewidth=1.0, label="y(t)",color = "red")
                ax.scatter(0, 0, color='red', label='Desfase = {:.1f}\nFrecuencia de Muestreo = {:.3f}'.format(d, fm), s=10)
                
                
                ax.set_title("Punto 4_2 : Default")
                ax.set_xlabel(" t ", fontsize=12, fontstyle="italic")
                ax.set_ylabel(" y ", fontsize=12, fontstyle="italic")
                
                ax.set_xlim(-35, 35)
                ax.set_ylim(-25, 150)
                
                ax.axhline(0, color='black', linewidth=0.8)  # Línea horizontal en y = 0
                ax.axvline(0, color='black', linewidth=0.8)  # Línea vertical en x = 0

                ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)  # Agregar una cuadrícula

                
                ax.legend(fontsize=8 ,loc="upper right")

            if i == 1 and j == 1:
                t,y1,y2,fm,d,c = p4_2()            
                ax.plot(y2,y1, linewidth=1.0, label="y(t)",color = "red")
                ax.scatter(0, 0, color='red', label='Desfase = {:.1f}\nFrecuencia de Muestreo = {:.3f}\nFactor de Escala = {:.1f}'.format(d, fm,c), s=10)
                
                
                ax.set_title("Punto 4_2: Expandida")
                ax.set_xlabel(" t ", fontsize=12, fontstyle="italic")
                ax.set_ylabel(" y ", fontsize=12, fontstyle="italic")
                
                ax.set_xlim(-35, 35)
                ax.set_ylim(-25, 150)
                
                ax.axhline(0, color='black', linewidth=0.8)  # Línea horizontal en y = 0
                ax.axvline(0, color='black', linewidth=0.8)  # Línea vertical en x = 0

                ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)  # Agregar una cuadrícula

                
                ax.legend(fontsize=8 ,loc="upper right")


    # Ajustar los subplots para evitar superposiciones
    plt.tight_layout()
    plt.show()  
 
#ahorita corrigo la 7  
#Punto 4.3 
def graf7():
     # Crear la figura y los subplots
    fig, axes = plt.subplots(nrows=2, ncols=2) # 5 filas, 2 columnas

    # Iterar a través de cada subplot
    for i, row in enumerate(axes):
        for j, ax in enumerate(row):
            
            # fila 0, col 0
            if i == 0 and j == 0:
                t,y1,y2,fm,d,c = p4_3()            
                ax.plot(t,y1, linewidth=1.0, label="y(t)",color = "red")
                ax.scatter(0, 0, color='red', label='Desfase = {:.1f}\nFrecuencia de Muestreo = {:.3f}'.format(d, fm), s=10)
                
                
                ax.set_title("Punto 4_3: Default")
                ax.set_xlabel(" t ", fontsize=12, fontstyle="italic")
                ax.set_ylabel(" y ", fontsize=12, fontstyle="italic")
                
                ax.set_xlim(-35, 35)
                ax.set_ylim(-25, 100)
                
                ax.axhline(0, color='black', linewidth=0.8)  # Línea horizontal en y = 0
                ax.axvline(0, color='black', linewidth=0.8)  # Línea vertical en x = 0

                ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)  # Agregar una cuadrícula

                
                ax.legend(fontsize=8 ,loc="upper right")

            if i == 0 and j == 1:
                t,y1,y2,fm,d,c = p4_3()            
                ax.plot(y2,y1, linewidth=1.0, label="y(t)",color = "red")
                ax.scatter(0, 0, color='red', label='Desfase = {:.1f}\nFrecuencia de Muestreo = {:.3f}\nFactor de Escala = {:.1f}'.format(d, fm,c), s=10)
                
                
                ax.set_title("Punto 4_3: Expandida")
                ax.set_xlabel(" t ", fontsize=12, fontstyle="italic")
                ax.set_ylabel(" y ", fontsize=12, fontstyle="italic")
                
                ax.set_xlim(-35, 35)
                ax.set_ylim(-25, 100)
                
                ax.axhline(0, color='black', linewidth=0.8)  # Línea horizontal en y = 0
                ax.axvline(0, color='black', linewidth=0.8)  # Línea vertical en x = 0

                ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)  # Agregar una cuadrícula

                
                ax.legend(fontsize=8 ,loc="upper right")

    # Ajustar los subplots para evitar superposiciones
    plt.tight_layout()
    plt.show()  
    
   
#################################################################

graf1()  

graf2()

graf3()

graf4()
  
graf5()

graf6() 

graf7()