import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm
import scipy.stats as stats


class Generador:
    def genNorm(self, parametro1, parametro2, size, seed):
        return norm.rvs(loc=parametro1, scale=parametro2, size=size, random_state=seed)
    def genMuestras(self, pob, m, n):
        if m * n > len(pob):
            m = len(pob) // n
        return np.random.choice(pob, size=(m, n), replace=False)

    def medMuestral(self, vectorMuestras):
        return np.mean(vectorMuestras, axis=1)

    def desvestMuestral(self, vectorMuestras):
        vMedM = self.medMuestral(vectorMuestras)
        sumBin = np.sum((vectorMuestras - vMedM[:, np.newaxis]) ** 2, axis=1)
        vectorVar = sumBin / (vectorMuestras.shape[1] - 1)
        return np.sqrt(vectorVar)

    def sumAbsMuestral(self, vectorMuestras, c):
        n = vectorMuestras.shape[1]
        return (c / n) * np.sum(np.abs(vectorMuestras), axis=1)

    def percentil(self, vectorMuestras, percent):
        return np.percentile(vectorMuestras, percent, axis=0)

    def plots(self, vector, bins, size, est):
        mediaM = vector.mean()
        desvestM = vector.std()

        bins = 30

        hist, binEdges = np.histogram(vector, bins=bins)
        distHist = stats.rv_histogram((hist, binEdges))
        ejeX = np.linspace(min(vector), max(vector), bins)

        # Crea una distribución normal suavizada
        pdfSmooth = stats.norm.pdf(ejeX, mediaM, desvestM)

        plt.hist(vector, bins=bins, density=True, label="Histograma", color="orange", edgecolor='black')

        # Línea vertical en la media
        plt.axvline(x=mediaM, color='g', linestyle='--', label="μ = " + str(round(mediaM, 2)))
        plt.axvline(x=mediaM + desvestM, color='r', linestyle='--', label="σ = " + str(round(desvestM, 2)))
        plt.axvline(x=mediaM - desvestM, color='r', linestyle='--')

        plt.plot(ejeX, pdfSmooth, label="PDF N(μ,σ²)", linewidth=1, color='purple')  # Utiliza la PDF suavizada

        plt.title("Distribución de 1000 muestras de tamaño " + str(size) + " del estimador " + str(est))
        plt.xlabel("Valores")
        plt.ylabel("Frecuencia relativa")

        plt.legend()
        # Guardar la imagen como PNG
        name = 'Hist' + str(size) + str(est)
        plt.savefig(name + '.png')

        plt.clf()


def evEst(generator, pob, m, n):
    vMuestras = generator.genMuestras(pob, m, n)
    Percent5Pob = generator.percentil(pob, 5)
    Percent95Pob = generator.percentil(pob, 95)
    vMediaMuestral = generator.medMuestral(vMuestras)
    vEstimador1 = generator.desvestMuestral(vMuestras)
    Percent5E1 = generator.percentil(vEstimador1, 5)
    Percent95E1 = generator.percentil(vEstimador1, 95)
    vEstimador2 = generator.sumAbsMuestral(vMuestras, 1.2533)
    Percent5E2 = generator.percentil(vEstimador2, 5)
    Percent95E2 = generator.percentil(vEstimador2, 95)

    generator.plots(vEstimador1, 30, n, "Sn")
    generator.plots(vEstimador2, 30, n, "Dn")

    res = np.array([
        vEstimador1.mean(), Percent5E1, Percent95E1,
        vEstimador2.mean(), Percent5E2, Percent95E2
    ])
    return res


def evEstNoPlots(generator, pob, m, n):
    vMuestras = generator.genMuestras(pob, m, n)
    Percent5Pob = generator.percentil(pob, 5)
    Percent95Pob = generator.percentil(pob, 95)
    vMediaMuestral = generator.medMuestral(vMuestras)
    vEstimador1 = generator.desvestMuestral(vMuestras)
    Percent5E1 = generator.percentil(vEstimador1, 5)
    Percent95E1 = generator.percentil(vEstimador1, 95)
    vEstimador2 = generator.sumAbsMuestral(vMuestras, 1.2533)
    Percent5E2 = generator.percentil(vEstimador2, 5)
    Percent95E2 = generator.percentil(vEstimador2, 95)

    res = np.array([
        vEstimador1.mean(), Percent5E1, Percent95E1,
        vEstimador2.mean(), Percent5E2, Percent95E2
    ])
    return res


def main():
    generator = Generador()
    mu = 0
    sigma = 1
    seed = stats.randint.rvs(50, 10000)
    sizePob = 500000

    print(seed)
    poblacion = generator.genNorm(mu, sigma, sizePob, seed)
    mediaReal = np.mean(poblacion)
    varianzaReal = np.var(poblacion)
    desvestReal = np.std(poblacion)
    print(desvestReal)

    def Tabular():
        v_sizes = [10, 50, 100, 200, 1000, 10000]
        v_data = np.empty((len(v_sizes), 6))
        for i, size in enumerate(v_sizes):
            v_data[i] = evEst(generator, poblacion, 1000, size)

        filas = v_sizes
        columnas = [
            'Promedio Estimaciones Sn', 'Percentil 5% Sn', 'Percentil 95% Sn',
            'Promedio Estimaciones Dn', 'Percentil 5% Dn', 'Percentil 95% Dn'
        ]
        df = pd.DataFrame(v_data, columns=columnas, index=filas)
        print(df)
        df = df.round(6)
        df.to_csv('Tabla.csv', index=False)
        print("ok tabular")

    def HistPob():
        bins = 200

        hist, binEdges = np.histogram(poblacion, bins=bins)
        distHist = stats.rv_histogram((hist, binEdges))
        ejeX = np.linspace(min(poblacion), max(poblacion), bins)

        # Crea una distribución normal suavizada
        pdfSmooth = stats.norm.pdf(ejeX, mu, sigma)

        plt.hist(poblacion, bins=bins, density=True, label="Histograma", color='#00DE00')

        # Línea vertical en la media

        plt.axvline(x=mediaReal, color='#FF7400', linestyle='--', label="μ = " + str(round(mediaReal, 2)))
        plt.axvline(x=mediaReal + desvestReal, color='#FF00CE', linestyle='--',
                    label="σ = " + str(round(desvestReal, 2)))
        plt.axvline(x=mediaReal - desvestReal, color='#FF00CE', linestyle='--')

        plt.plot(ejeX, pdfSmooth, label="PDF Normal", linewidth=1, color='#5723E9')  # Utiliza la PDF suavizada

        plt.title("Distribución de población")
        plt.xlabel("Valores")
        plt.ylabel("Frecuencia relativa")

        plt.legend()

        # Guardar la imagen como PNG
        plt.savefig('HistPob1.png')
        plt.clf()
        # plt.show()
        print("ok graficar")

    def GrafAsintot():
        nV = 400
        ini = 5
        fn = 10000 + ini

        x = np.linspace(ini, fn, nV)
        y_data = np.empty((nV, 6))

        for i, size in enumerate(range(ini, fn, 25)):
            vectorTotal = evEstNoPlots(generator, poblacion, 1000, size)
            y_data[i] = vectorTotal

            # if ( i % 21 == 0):
            # print(i)
            print(i)
        y1, y2, y3, y4, y5, y6 = y_data.T

        plt.plot(x, y1, color='red', label='Promedio Sn')
        plt.plot(x, y2, color='red', linestyle='dashed', label='Perc 5% Sn')
        plt.plot(x, y3, color='red', linestyle='dotted', label='Perc 95% Sn')
        plt.plot(x, y4, color='green', label='Promedio Dn')
        plt.plot(x, y5, color='green', linestyle='dashed', label='Perc 5% Dn')
        plt.plot(x, y6, color='green', linestyle='dotted', label='Perc 95% Dn')
    
        plt.axhline(y=desvestReal, color='black', linestyle='-', linewidth=1, label="σ = " + str(round(desvestReal, 6)))
    
        plt.xlabel('n  (50 steps)')
        plt.ylabel('Valor del Estimador')
        plt.title('Estimaciones con Sn y Dn de acuerdo a n')
    
        plt.legend()
        plt.savefig('GrafMediaPercEstim.png')    
        plt.show()
        
    
        plt.plot(x, y1, color='red', label='Promedio Sn')
        plt.plot(x, y2, color='red', linestyle='dashed', label='Perc 5% Sn')
        plt.plot(x, y3, color='red', linestyle='dotted', label='Perc 95% Sn')
        plt.plot(x, y4, color='green', label='Promedio Dn')
        plt.plot(x, y5, color='green', linestyle='dashed', label='Perc 5% Dn')
        plt.plot(x, y6, color='green', linestyle='dotted', label='Perc 95% Dn')
    
        plt.axhline(y=desvestReal, color='black', linestyle='-', linewidth=1, label="σ = " + str(round(desvestReal, 6)))
    
        h  = 0.001 
        plt.ylim(desvestReal - h, desvestReal + h)
    
        plt.xlabel('n   (50 steps)')
        plt.ylabel('Valor del Estimador')
        plt.title('Estimaciones con Sn y Dn de acuerdo a n')
    
        plt.legend()
        plt.savefig('GrafEstimRestric.png')
        plt.show()
        plt.clf()
        print("ok GrafAsintot")

    Tabular()
    HistPob()
    GrafAsintot()


if __name__ == "__main__":
    main()
    
    