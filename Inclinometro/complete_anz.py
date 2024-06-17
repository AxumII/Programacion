from Analyze import Analysis
from Calc_Ang import Inclinometro
from vectorObject import Vector_Object as vt
import pandas as pd

g = 9.80665
nbits = 2e16
analisis = Analysis(resolution=(2*g/nbits))
analisis.load_data("datosMPU6050.csv")
estadisticos_basicos = analisis.calculate_statistics()
incertidumbres = analisis.calculate_uncertainties()
analisis.print_means()

print(estadisticos_basicos)
valores_media = estadisticos_basicos.iloc[0]
gvect1 = vt(coords=[
    valores_media['acc X'],
    valores_media['acc Y'],
    -valores_media['acc Z']
])
print("Vector medio:", gvect1.coords)

# Calcular ángulos con los valores medios
inclinometro = Inclinometro(gvect1)
angulos_media, angulo_xy_media = inclinometro.calculate()
inclinometro.graf()

print(incertidumbres)
analisis.plot_data()
analisis.plot_histograms()

# Obtener incertidumbre expandida (asumiendo fila 6 que es "Incertidumbre Expandida (Tipo B)")
inc_exp = incertidumbres.iloc[6]

# Crear gvect2 y gvect3 sumando y restando incertidumbre a gvect1
gvect2 = vt(coords=[
    gvect1.coords[0] - inc_exp['acc X'],  # Restando en lugar de sumar
    gvect1.coords[1] - inc_exp['acc Y'],  # Restando en lugar de sumar
    gvect1.coords[2] - inc_exp['acc Z']   # Restando en lugar de sumar
])

gvect3 = vt(coords=[
    gvect1.coords[0] + inc_exp['acc X'],  # Sumando en lugar de restar
    gvect1.coords[1] + inc_exp['acc Y'],  # Sumando en lugar de restar
    gvect1.coords[2] + inc_exp['acc Z']   # Sumando en lugar de restar
])

# Imprimir los vectores modificados
print("Vector medio - incertidumbre:", gvect3.coords)
print("Vector medio + incertidumbre:", gvect2.coords)

# Calcular ángulos con gvect2
inclinometro_inc1 = Inclinometro(gvect2)
angulos_inc1, angulo_xy_inc1 = inclinometro_inc1.calculate()
inclinometro_inc1.graf()

# Calcular ángulos con gvect3
inclinometro_inc2 = Inclinometro(gvect3)
angulos_inc2, angulo_xy_inc2 = inclinometro_inc2.calculate()
inclinometro_inc2.graf()

# Tabulación de los resultados
resultados = pd.DataFrame({
    'Condición': ['Media', 'Media - Incertidumbre', 'Media + Incertidumbre'],
    'Ángulo X': [angulos_media[0], angulos_inc2[0], angulos_inc1[0]],
    'Ángulo Y': [angulos_media[1], angulos_inc2[1], angulos_inc1[1]],
    'Ángulo Z': [angulos_media[2], angulos_inc2[2], angulos_inc1[2]],
    'Ángulo XY': [angulo_xy_media, angulo_xy_inc2, angulo_xy_inc1]
})

print(resultados)
