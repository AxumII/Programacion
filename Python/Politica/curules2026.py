from hondt import Hondt as Ht
import pandas as pd

#Senado
def Senado(partidos,votos):
    df_votos = pd.DataFrame({
    'Partido': partidos,
    'Cantidad': votos
    })

    eleccion = Ht(df_votos, n_seat=100, p_threshold = 3)
    eleccion.discard_seat()
    eleccion.allocator()
    eleccion.plot_results()
    



partidos = [
    "Partido de la U",
    "Fuerza Ciudadana",
    "Centro Democrático",
    "Pacto Histórico",
    "Partido Conservador",
    "Partido Oxígeno",
    "Patriotas",
    "Lista de Oviedo",
    "Cambio Radical",
    "Alianza por Colombia",
    "Creemos",
    "Salvación Nacional",
    "MIRA - Nuevo Liberalismo",
    "Partido Liberal",
    "Frente Amplio",
    "Colombia Segura"
]

votos = [
    1565786,   # Partido de la U
    114722,    # Fuerza Ciudadana
    3035715,   # Centro Democrático
    4413636,   # Pacto Histórico
    1859663,   # Partido Conservador
    27879,     # Partido Oxígeno
    10755,     # Patriotas 
    105393,    # Oviedo (La Lista de Oviedo - Con Toda por Colombia)
    1248021,   # Cambio Radical (Coalición Cambio Radical - ALMA)
    1904154,   # Alianza por Colombia
    227957,    # Creemos
    705924,    # Salvación Nacional
    900606,    # MIRA - Nuevo Liberalismo (Ahora Colombia)
    2275182,   # Partido Liberal
    396042,    # Frente Amplio Unitario
    10754      # Colombia Segura
]

Senado(partidos, votos)

Senado(partidos,votos)







