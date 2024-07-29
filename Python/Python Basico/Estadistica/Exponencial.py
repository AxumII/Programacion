import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

class Generador:
    def genExp(self,parametro1,size):
        expV = (stats.expon.rvs( scale = parametro1 ,size = size, random_state = 169))
        return expV
        
    def genMuestras(self,pob,m,n):
        vectorMuestras = np.empty((m,n))
        for x in range(m):            
            muestra = np.random.choice(pob, size = n, replace = False)  
            vectorMuestras[x] = muestra

        return vectorMuestras
    
    
    
    
    
    
    
    
############################################################################################################################   
generator = Generador()
poblacion = generator.genExp(50,10000) #(parametro lambda, tamaño)
#nota: normalmente conocemos la pdf de la expon como {\displaystyle \lambda e^{-\lambda x}}
#sin embargo hay otra forma de parametrizar usando parametros de escala y localizacion
#B = par loc = 1/lambda
#B = media

print(poblacion.mean())
print("lambda")
print(1/(poblacion.mean()))
vMuestras = generator.genMuestras(poblacion,3,5) #(poblacionAMuestrear, m cantidad de muestras, n tamaño de muestras)


plotPob = plt.hist(poblacion, bins = 30) #bin indica cuantas barras van a crearse
plotPob = plt.title("Distribucion de poblacion")
plotPob = plt.xlabel("Valores")
plotPob = plt.ylabel("Frecuencia de cada valor")

plotPob = plt.show()