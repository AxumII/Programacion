import matplotlib.pyplot as plt

# Definir los encabezados y los datos
columnas = ["Variable / señal", "Dirección", "Periférico", "GPIO", "Escala / función"]

datos = [
    ["Var. analógica 1 (potL)", "Entrada", "ADC", "35", "0–200 cm"],
    ["Var. analógica 2 (potSP)", "Entrada", "ADC", "34", "61–180 cm"],
    ["Var. analógica 3 (adc_dac)", "Entrada", "ADC", "32", "Realimentación (0–4095)"],
    ["Pulsador (button)", "Entrada", "GPIO IN", "27", "Interrupción (bajada)"],
    ["Indicador 1 (ledRojo)", "Salida", "GPIO OUT", "14", "Alerta / Estado (ON/OFF)"],
    ["Indicador 2 (ledVerde)", "Salida", "GPIO OUT", "12", "Estado normal (ON/OFF)"],
    ["Salida analógica (dac)", "Salida", "DAC", "26", "0–255 (Proporcional)"],
    ["Actuador simulado (pwm)", "Salida", "PWM", "13", "0–1023 (Duty), 1000 Hz"]
]

# Crear la figura y ocultar los ejes
fig, ax = plt.subplots(figsize=(10, 4))
ax.axis('tight')
ax.axis('off')

# Generar la tabla
tabla = ax.table(cellText=datos, colLabels=columnas, loc='center', cellLoc='center')

# Ajustar el estilo de la tabla
tabla.auto_set_font_size(False)
tabla.set_fontsize(10)
tabla.scale(1.2, 1.8) # Ajustar el ancho y alto de las celdas

# Aplicar estilo naranja a los encabezados para mantener tu diseño
for (fila, columna), celda in tabla.get_celld().items():
    if fila == 0:
        celda.set_text_props(weight='bold', color='white')
        celda.set_facecolor('#E65100') # Fondo naranja para el encabezado
    else:
        celda.set_facecolor('#FFF3E0') # Fondo naranja muy claro para los datos

plt.title("Tabla de asignación de pines", fontweight="bold", fontsize=14, color="#E65100", pad=20)
plt.tight_layout()
plt.show()