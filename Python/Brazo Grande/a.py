import matplotlib.pyplot as plt

# 1. Definir los datos de la tabla basados en Final.py
columnas = ["Variable / señal", "Dirección", "Periférico", "GPIO", "Escala / función"]
datos = [
    ["Potenciómetro (joy_pot)", "Entrada", "ADC", "35", "0–100 %"],
    ["Navegación menú (joy_nav)", "Entrada", "ADC", "34", "Control menú"],
    ["Sensor SDA (BMP180)", "Bidireccional", "I²C", "21", "Datos"],
    ["Sensor SCL (BMP180)", "Salida reloj", "I²C", "22", "Reloj"],
    ["TFT SCK (ST7789)", "Salida", "SPI", "18", "Reloj"],
    ["TFT MOSI (ST7789)", "Salida", "SPI", "23", "Datos"],
    ["TFT CS", "Salida", "GPIO/SPI", "5", "Control (Chip Select)"],
    ["TFT DC", "Salida", "GPIO/SPI", "2", "Control (Data/Command)"],
    ["TFT RST", "Salida", "GPIO/SPI", "4", "Control (Reset)"],
    ["Interfaz web", "Bidireccional", "Wi-Fi/HTTP", "No aplica", "HTML + JSON"]
]

# 2. Configurar la figura
fig, ax = plt.subplots(figsize=(12, 4.5))
ax.axis('tight')
ax.axis('off')

# 3. Crear la tabla
tabla = ax.table(cellText=datos, colLabels=columnas, loc='center', cellLoc='center')

# 4. Estilizar la tabla (tamaño y celdas)
tabla.auto_set_font_size(False)
tabla.set_fontsize(11)
tabla.scale(1, 1.8)

# Definir colores estilo "naranja"
color_encabezado = "#E36C0A"  # Naranja fuerte
color_fila_par = "#FCE4D6"    # Naranja claro (melocotón)
color_fila_impar = "#FFFFFF"  # Blanco

# 5. Aplicar colores a las celdas
for (fila, col), celda in tabla.get_celld().items():
    # Remover bordes gruesos para un aspecto más limpio
    celda.set_edgecolor('#E36C0A') 
    
    if fila == 0:
        # Fila de encabezado
        celda.set_text_props(weight='bold', color='white')
        celda.set_facecolor(color_encabezado)
    else:
        # Filas de datos (alternadas)
        if fila % 2 == 0:
            celda.set_facecolor(color_fila_impar)
        else:
            celda.set_facecolor(color_fila_par)

# 6. Añadir título principal
plt.title("Tabla de asignación de pines", fontweight="bold", color="#E36C0A", fontsize=16, pad=10)

# 7. Ajustar diseño y guardar la imagen
plt.tight_layout()
plt.savefig("tabla_pines_generada.png", dpi=300, bbox_inches='tight')
plt.show()