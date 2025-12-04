import os
import pandas as pd
import matplotlib.pyplot as plt

def libre():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ruta = os.path.join(base_dir,
        "Libre - sin amortiguamiento",
        "Libre - sin amortiguamiento_1.csv"
    )

    df = pd.read_csv(
        ruta,
        sep=";",
        decimal=",",
        skiprows=[1, 2],  # unidades y línea vacía
    )

    # Convertir a arrays numpy
    tiempo = df["Tiempo"].to_numpy()
    canal_a = df["Canal A"].to_numpy()
    canal_b = df["Canal B"].to_numpy()

    
    print("Tiempo:", tiempo[:10])
    print("Canal B:", canal_b[:10])

    # Gráfica de ambos canales
    #plt.plot(tiempo, canal_a, label="Canal A")
    plt.plot(tiempo, canal_b, label="Canal B")

    plt.xlabel("Tiempo (ms)")
    plt.ylabel("Amplitud ")
    plt.title("Libre - sin amortiguamiento 1")
    plt.grid(True)
    plt.legend()
    plt.show() 
    return tiempo, canal_a, canal_b


# Obtener arrays
t, x, y = libre()

# 
