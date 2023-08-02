import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

class Generador: 
    
    def genPoisson(self,parametro1,size):
        poisV = stats.poisson.rvs(mu = parametro1, size = size, random_state = 169)
        
        print("poblacion")
        print(poisV)
        
        return poisV
        
    def genMuestras(self,pob,m,n):
        vectorMuestras = np.empty((m,n))
        for x in range(m):
            
            muestra = np.random.choice(pob, size = n, replace = False)  
            vectorMuestras[x] = muestra
            
        print("Muestras")
        print(vectorMuestras)
        
        return vectorMuestras    
    
    def sumatorioK(self,vector,k):
        n = vector.shape[0]
        suma = np.sum(vector**k)
        
        return suma
      
    def primMom(self,vectorMuestras):
        n = vectorMuestras.shape[0]
        vectorSumas = np.empty((n))
                
        for x in range(n):
            muestra = vectorMuestras[x]
            m = muestra.shape[0]             
            vectorSumas[x] = (np.sum(muestra))/m              
        print("Primeros Momentos")             
        print(vectorSumas)
        return vectorSumas
    
    def segMom(self,vectorMuestras):
        n = vectorMuestras.shape[0]
        vectorSumas = np.empty((n)) 
        
        for x in range(n):
            muestra = vectorMuestras[x]
            m = muestra.shape[0]
            
            res = self.sumatorioK(muestra,2) #calcula el sumatorio de x²    
            est = (-1 + ((1 + (4*(res)))**(1/2)))/2
                              
            vectorSumas[x] = est
            
        print("Segundos Momentos")             
        print(vectorSumas)
        
        return vectorSumas
            
            
            
            
            

#################################################################################################################################
   
generator = Generador()
poblacion = generator.genPoisson(1,10000) #(parametro lambda, tamaño)
vMuestras = generator.genMuestras(poblacion,5,10) #(poblacionAMuestrear, m cantidad de muestras, n tamaño de muestras)
estimador1 = generator.primMom(vMuestras)#genera un vector de medias muestrales
estimador2 = generator.segMom(vMuestras)#genera un vector de segundos momentos, por ahora segundos momentos muestrales


plotPob = plt.hist(poblacion, bins = 30) #bin indica cuantas barras van a crearse
plotPob = plt.title("Distribucion de poblacion")
plotPob = plt.xlabel("Valores")
plotPob = plt.ylabel("Frecuencia de cada valor")



plotPob = plt.show()

print(estimador1.mean())
print(estimador2.mean())
