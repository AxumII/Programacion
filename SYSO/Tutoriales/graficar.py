import matplotlib.pyplot as plt
import numpy as np





def grafFuncionBasica():
    #define vectores como las variables
    x = np.linspace(0, 10, 100)#es la independiente
    y = np.sin(2 * x)#es la dependiente

    # Crear una figura vacía, en sí es el lienzo
    fig = plt.figure()

    # Agregar un conjunto de ejes (subplots) a la figura, ax es un subplot
    ax1 = fig.add_subplot(1, 1, 1)  # 1 fila, 1 columna, primer subplot

    # Trazar los datos en los ejes
    ax1.plot(x, y, linewidth=2.0, label="leyenda", color="red", linestyle="dashdot")

    # el metodo set permite modificar varias cosas en el plot ax
    # x lim y y lim permiten limitar hasta qué número se grafica
    ax1.set(xlim=(0, 8), ylim=(-8, 8))

    ax1.set_title("Titulo principal")
    ax1.set_xlabel("Titulo Eje X", fontsize=12, fontstyle="italic")
    ax1.set_ylabel("Titulo Eje Y", fontsize=12, fontstyle="italic")

    # Crea una malla para ver la escala mejor
    ax1.grid(True)

    # muestra un punto, pone una flecha
    ax1.annotate("Punto Interesante", 
                 xy=(4, 0.5),       # Coordenadas del punto de datos
                 xytext=(3, 2),     # Coordenadas del texto de la anotación
                 arrowprops=dict(facecolor="black", shrink=0.1, width=0.5, headwidth=8),#shrink es cuanto se encoje la flecha, width es el ancho
                 fontsize=10,       # Tamaño de fuente del texto de la anotación
                 color="blue",      # Color del texto de la anotación
                 horizontalalignment="left",  # Alineación horizontal del texto
                 verticalalignment="bottom",   # Alineación vertical del texto
                 bbox=dict(boxstyle="round,pad=0.3", edgecolor="gray", facecolor="lightgray"))  # Estilo del cuadro alrededor del texto

    # Añadir un punto en la punta de la flecha
    ax1.plot(4, 0.5, marker="o", markersize=4, color="black")

    # Permite guardar la gráfica
    # fig.savefig("grafico_seno.png", dpi=300)  # Guardar como PNG con 300 dpi

    ax1.legend(fontsize=10, loc="upper right")
    plt.show()


