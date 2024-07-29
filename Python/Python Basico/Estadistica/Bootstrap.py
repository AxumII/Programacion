import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import pandas as pd


class Generador:
    def genNorm(self,parametro1,parametro2,size):
        normV = stats.norm.rvs(loc = parametro1, scale = parametro2, size = size, random_state = 13169)   
        #u es el parametro de localizacion, desvest es el parametro de escala, aca trabaja es con desvest como paraemtro y no var  

        return normV
        
    def genMuestras(self,pob,m,n):
        vectorMuestras = np.empty((m,n))
        for x in range(m):
            
            muestra = np.random.choice(pob, size = n, replace = False)  
            vectorMuestras[x] = muestra
            
        return vectorMuestras
    
    def sumatorioK(self,vector,k):
        n = vector.shape[0]
        suma = np.sum(vector**k)
        
        return suma
    
    def medMuestral(self,vectorMuestras):
        m = vectorMuestras.shape[0]
        vectorSumas = np.empty((m))
                
        for x in range(m):
            muestra = vectorMuestras[x]
            n = muestra.shape[0]             
            vectorSumas[x] = (np.sum(muestra))/n              
                
        return vectorSumas
    
    def desvestMuestral(self,vectorMuestras): # Estimador 1
        m = vectorMuestras.shape[0]
        vMedM = self.medMuestral(vectorMuestras)
        vectorVar = np.empty((m))
        
        for x in range(m):
            muestra = vectorMuestras[x]
            n = muestra.shape[0]
            sumBin = np.sum((muestra - vMedM[x])**2)
            vectorVar[x] = sumBin/(n-1)
            vectorVar[x] = (vectorVar[x])**(1/2)
            
        return vectorVar
           
    def sumAbsMuestral(self,vectorMuestras, c):
        m = vectorMuestras.shape[0]
        vMedM = self.medMuestral(vectorMuestras)
        vectorSA = np.empty((m))
        
        for x in range(m):
            muestra = vectorMuestras[x]
            n = muestra.shape[0]             
            vectorSA[x] = (c/n)*(np.sum(np.absolute(muestra)))          
                
        return vectorSA
        
    def percentil(self,vectorMuestras,percent):
        
        Percentil = np.percentile(vectorMuestras,percent)       

        return Percentil
       
    def plots(self, vector, bins, size, est):
        mediaM = vector.mean()
        desvestM = vector.std()

        bins = 30

        hist, binEdges = np.histogram(vector, bins=bins)
        distHist = stats.rv_histogram((hist, binEdges))
        ejeX = np.linspace(min(vector), max(vector), bins)

        # Crea una distribución normal suavizada
        pdfSmooth = stats.norm.pdf(ejeX, mediaM, desvestM)

        plt.hist(vector, bins=bins, density=True, label="Histograma", color = "orange",edgecolor='black')

        # Línea vertical en la media

        plt.axvline(x=mediaM, color='g', linestyle='--', label="μ = " + str(round(mediaM, 2)))
        plt.axvline(x=mediaM + desvestM, color='r', linestyle='--', label="σ = " + str(round(desvestM, 2)))
        plt.axvline(x=mediaM - desvestM, color='r', linestyle='--')

        plt.plot(ejeX, pdfSmooth, label="PDF N(μ,σ²)", linewidth=1, color = 'purple')  # Utiliza la PDF suavizada

        plt.title("Distribución de 1000 muestras de tamaño " + str(size) + " del estimador " + str(est))
        plt.xlabel("Valores")
        plt.ylabel("Frecuencia relativa")

        plt.legend()
        # Guardar la imagen como PNG
        name = 'Hist' + str(size) + str(est)
        plt.savefig(name+'.png')

        #plt.show()

        plt.clf()  
###########################################################################################################################################      
###########################################################################################################################################     
###########################################################################################################################################     
       
def  evEst(pob,m,n):
    
    vMuestras = generator.genMuestras(pob,m,n) #(poblacionAMuestrear, m cantidad de muestras, n tamaño de muestras)
    
    Percent5Pob = generator.percentil(pob,5)
    Percent95Pob = generator.percentil(pob,95)


    vMediaMuestral = generator.medMuestral(vMuestras)

    vEstimador1 = generator.desvestMuestral(vMuestras)
    Percent5E1 = generator.percentil(vEstimador1,5)
    Percent95E1 = generator.percentil(vEstimador1,95)

    vEstimador2 = generator.sumAbsMuestral(vMuestras,1.2533)
    Percent5E2 = generator.percentil(vEstimador2,5)
    Percent95E2 = generator.percentil(vEstimador2,95)
    
    generator.plots(vEstimador1,30, n, "Sn");
    generator.plots(vEstimador2,30, n, "Dn");
            
    res = np.array([vEstimador1.mean(),Percent5E1,Percent95E1,vEstimador2.mean(),Percent5E2,Percent95E2])
    
    return res
    
     
    
   
   
    
 #############################################################################################################################   

###########################################################################################################################################
###########################################################################################################################################
###########################################################################################################################################
def Ejecutar():
    generator = Generador()
    seed = stats.randint.rvs(50, 10000)
    mu = 0
    sigma = 1
    print(seed)

    poblacion = generator.genNorm(mu,(sigma),100000) #(parametro loc o mu, parametro esc o desvest, tamaño)
    #se genero con una media de 0 y una varianza de 400, pero no es real, la real es de la poblacion
    mediaReal = np.mean(poblacion)
    varianzaReal = np.var(poblacion)
    desvestReal = np.std(poblacion)
    print("ok primera parte")

    
        ##################################################################################################################################

    
    bins = 200
    hist, binEdges = np.histogram(poblacion, bins=bins)
    distHist = stats.rv_histogram((hist, binEdges))
    ejeX = np.linspace(min(poblacion), max(poblacion), bins)
    # Crea una distribución normal suavizada
    pdfSmooth = stats.norm.pdf(ejeX, mu, sigma)
    plt.hist(poblacion, bins=bins, density=True, label="Histograma", color = '#00DE00' )
    # Línea vertical en la media
    plt.axvline(x=mediaReal, color='#FF7400', linestyle='--', label="μ = " + str(round(mediaReal, 2)))
    plt.axvline(x=mediaReal + desvestReal, color='#FF00CE', linestyle='--', label="σ = " + str(round(desvestReal, 2)))
    plt.axvline(x=mediaReal - desvestReal, color='#FF00CE', linestyle='--')
    plt.plot(ejeX, pdfSmooth, label="PDF Normal", linewidth=1, color = '#5723E9')  # Utiliza la PDF suavizada
    plt.title("Distribución de población")
    plt.xlabel("Valores")
    plt.ylabel("Frecuencia relativa")
    plt.legend()
    # Guardar la imagen como PNG
    plt.savefig('HistPob1.png')
    plt.clf()
    #plt.show()
    print("ok graficar")
    ###############################################################################################################################

    
    v10 = evEst(poblacion,1000,10)
    v50 = evEst(poblacion,1000,50)
    v100 = evEst(poblacion,1000,100)
    v200 = evEst(poblacion,1000,200)
    v1000 = evEst(poblacion,1000,1000)
    v10000 = evEst(poblacion,1000,10000)
    # Concatenar los arrays a lo largo del eje de las columnas
    data = np.row_stack((v10,v50,v100,v200,v1000,v10000))
    # Crear el DataFrame de pandas
    filas = [10 , 50, 100, 200, 1000, 10000]
    columnas = ['Promedio Estimaciones Sn', 'Percentil 5% Sn', 'Percentil 95% Sn','Promedio Estimaciones Dn', 'Percentil 5% Dn', 'Percentil 95% Dn']
    df = pd.DataFrame(data, columns= columnas, index = filas  )
    # Imprimir el DataFrame
    print(df)
    df = df.round(6)
    #exportar a csv
    df.to_csv('Tabla.csv', index=False)
    print("fin")




######################################################################################################

    
    
generator = Generador()
Ejecutar()




"""
#TODO ESTE RELLENO FUE SOLO PARA IR PROBANDO QUE TUVIERAN COHERENCIA LOS DATOS
Percent5Pob = generator.percentil(poblacion,5)
Percent95Pob = generator.percentil(poblacion,95)

vMuestras = generator.genMuestras(poblacion,50,20) #(poblacionAMuestrear, m cantidad de muestras, n tamaño de muestras)
vMediaMuestral = generator.medMuestral(vMuestras)

vEstimador1 = generator.varMuestral(vMuestras)
Percent5E1 = generator.percentil(vEstimador1,5)
Percent95E1 = generator.percentil(vEstimador1,95)

vEstimador2 = generator.sumAbsMuestral(vMuestras,25)
Percent5E2 = generator.percentil(vEstimador2,5)
Percent95E2 = generator.percentil(vEstimador2,95)

print("poblacion")
print(poblacion)
print("muestras")
print(vMuestras)
print("media")
print(poblacion.mean())
print("varianza")
print(poblacion.var())
print("percentil 5")
print(Percent5Pob)
print("percentil 95")
print(Percent95Pob)

print("medias muestrales")
print(vMediaMuestral)
print("promedio de la media muestral")
print(vMediaMuestral.mean())
print("varianza de la media muestral")
print(vMediaMuestral.var())

print("Estimador 1: varianzas muestrales")
print(vEstimador1)
print("promedio de la varianza muestral")
print(vEstimador1.mean())
print("varianza de la varianza muestral")
print(vEstimador1.var())

print("Estimador 2: suma abs de la muestra ")
print(vEstimador2)
print("promedio del estimador 2")
print(vEstimador2.mean())
print("varianza del estimador 2")
print(vEstimador2.var())

print("percentil 5% de estimador 1")
print(Percent5E1)
print("percentil 95% de estimador 1")
print(Percent95E1)

print("percentil 5% de estimador 2")
print(Percent5E2)
print("percentil 95% de estimador 2")
print(Percent95E2)"""