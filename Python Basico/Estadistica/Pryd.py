import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import pandas as pd
import statsmodels.api as sm


print("Puntos D y 4")

df = pd.read_csv('B:\Programacion\Python\Estadistica\dataset.csv')
print(df)

######################################################################################
#a calcular proporciones de raza de madre y estimadores

def PA():
    raza = df['race']
    smokerM = df["smoker"]
    
    raza0 = []
    raza1 = []
    raza2 = []
    raza3 = []
    
    for i in range(len(raza)):
        print(i+2)
        if raza[i] == 0:
            raza0.append(smokerM[i])            
        elif raza[i] == 1:
            raza1.append(smokerM[i])            
        elif raza[i] == 2:
            raza2.append(smokerM[i])            
        elif raza[i] == 3:
            raza3.append(smokerM[i])
            
    XbarraR0 = np.mean(raza0)
    XbarraR1 = np.mean(raza1)
    XbarraR2 = np.mean(raza2)
    XbarraR3 = np.mean(raza3)
    
    print("Mean of raza0:", XbarraR0)
    print("Mean of raza1:", XbarraR1)
    print("Mean of raza2:", XbarraR2)
    print("Mean of raza3:", XbarraR3)
    
    data = {
    'Raza': ['raza0', 'raza1', 'raza2', 'raza3'],
    'Mean': [XbarraR0, XbarraR1, XbarraR2, XbarraR3]
    }

    dfX = pd.DataFrame(data)

    dfX.to_csv('mediaMBer.csv', index=False)
    
    #################################
    
    plt.hist(raza, bins=[0, 1, 2, 3, 4], align='left', rwidth=0.8, color="orange")
    plt.xlabel('Raza')
    plt.ylabel('Frecuencia')
    plt.xticks([0, 1, 2, 3], ["Blanca", "Negra", "Latina", "Asiatica"])
    plt.title('Histograma de Valores de Raza')

    # Agregar valores numéricos a cada barra
    for i, v in enumerate(raza):
        count = sum(raza == v)
        plt.text(v-0.2, count+0.5, str(count))
    plt.savefig('histRazas' + '.png')
    plt.show()
    
    

    # Tabla de frecuencia de 0 y 1 para cada valor de 'raza'
    df_table = pd.crosstab(raza, smokerM)

    # Exportar la tabla a un archivo CSV sin estilos
    df_table.to_csv('tabla_frecuencia.csv')

    # Modificar estilo de la tabla
    df_table_styled = df_table.style \
        .set_caption('Tabla de Frecuencia') \
        .set_table_styles([
            {'selector': 'caption', 'props': [('font-size', '18px'), ('font-weight', 'bold')]},
            {'selector': 'th', 'props': [('background-color', 'lightgray')]}
        ])

    # Mostrar la tabla con estilo
    df_table_styled
    
    print(df_table)
    
    ax = df_table.plot(kind='bar', stacked=True)
    plt.xlabel('Raza')
    plt.ylabel('Cantidad')
    plt.xticks(rotation=0)
    plt.title('Cantidad de 0 y 1 por Valor de Raza')
    plt.legend(title='smoker', loc='upper right')

    # Cambiar nombres de las etiquetas en el eje x
    ax.set_xticklabels(["Blanca", "Negra", "Latina", "Asiatica"])

    # Agregar valores numéricos a cada barra
    for c in ax.containers:
        ax.bar_label(c, label_type='edge', fontsize=8)
        
        
    plt.savefig('histRazasFum' + '.png')
    plt.show()
    

def PB():
    #b calcular padres no fumadores por IC
    bins = 7
    cPadres = df["fnocig"]
    print(cPadres)
    
    cPadres = df["fnocig"]
    
    smokerP = [0 if elemento == 0 else 1 for elemento in cPadres]
    print(smokerP)
    
    smokerM = df["smoker"]
    print(smokerM)

    smokerBoth = [1 if p == 1 and m == 1 else 0 for p, m in zip(smokerP, smokerM)]
    print(smokerBoth)
    
    frecuencias = [smokerBoth.count(1), smokerBoth.count(0)]
    etiquetas = ['Si', 'No']
    colores = ['orange', 'green']

    plt.bar(etiquetas, frecuencias, color=colores)
    for i in range(len(etiquetas)):
        plt.text(i, frecuencias[i], str(frecuencias[i]), ha='center', va='bottom')

    plt.xlabel('¿Ambos padres fuman?')
    plt.ylabel('Frecuencia')
    plt.title('Histograma de si ambos padres son fumadores')  
    plt.savefig("histogramaAmbosPadresFumadores"+ '.png')     
    plt.show()
    
    resultados = sm.stats.diagnostic.lilliefors(smokerBoth)

    # Imprimir los resultados
    print("Estadístico de prueba:", resultados[0])
    print("Valor p:", resultados[1])    
            
    print(np.mean(smokerBoth))
      
def P4():
    cPadres = df["fnocig"]
    print(cPadres)
    
    cPadres = df["fnocig"]
    
    smokerP = [0 if elemento == 0 else 1 for elemento in cPadres]
    
    xbarra = np.mean(smokerP)
    print(xbarra)
    
    print(smokerP)
    
    count_0 = smokerP.count(0)
    count_1 = smokerP.count(1)
    total = len(smokerP)
    
    print("Cantidad de 0:", count_0)
    print("Cantidad de 1:", count_1)
    
    # Crear la gráfica de barras
    labels = ['0', '1']
    quantities = [count_0, count_1]
    colors = ['blue', 'orange']
    
    plt.bar(labels, quantities, color=colors)
    plt.xlabel('Valores')
    plt.ylabel('Cantidad')
    plt.title('Gráfica de barras de smokerP')
    
    # Añadir texto en las barras
    for i in range(len(labels)):
        plt.text(i, quantities[i], str(quantities[i]), ha='center', va='bottom')
    plt.savefig('histPadres' + '.png')
    plt.show()
    
    
        
#PA()
PB()
#P4()