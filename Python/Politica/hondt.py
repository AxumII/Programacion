import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Hondt:
    def __init__(self, ballot_list,n_seat,p_threshold = 3):
        
        self.ballot_list = ballot_list  # Original
        self.aux_ballot_list = ballot_list.copy()   # Copia
        
        self.seat_list = self.ballot_list[['Partido']].copy()   
        self.seat_list['Curules'] = 0   # Lista de curules inicializada
                
        self.n_seat = n_seat    # Numero de curules
        
        total_ballot = self.ballot_list['Cantidad'].sum()    #Numero de votos totales
        self.ballot_threshold = total_ballot*p_threshold / 100
        
        
        
        
        
    def discard_seat(self):
        self.aux_ballot_list = self.aux_ballot_list[self.aux_ballot_list['Cantidad'] >= self.ballot_threshold].copy()       
    
    
    def allocator(self):
        for i in range(self.n_seat):
            self.aux_ballot_list = self.aux_ballot_list.sort_values(by = ['Cantidad'], ascending  = False)
            group = self.aux_ballot_list.iloc[0]['Partido']
            
            self.seat_list.loc[self.seat_list['Partido']== group, 'Curules'] += 1  #Asignar curul al de mayor votacion en la iteracion
            
            ballot_group  = self.ballot_list.loc[self.ballot_list['Partido'] == group, 'Cantidad'].values[0]
            seat_group = self.seat_list.loc[self.seat_list['Partido'] == group, 'Curules'].values[0]
            hondt_quotient  = ballot_group / (seat_group + 1) #Halla el cociente de hondt 
            
            self.aux_ballot_list.loc[self.aux_ballot_list['Partido'] == group,'Cantidad' ] = hondt_quotient #Asigna el cociente para reducir el valor e iterar


    def results(self):
        # 1. Unimos los votos originales con las curules ganadas
        df_res = pd.merge(self.ballot_list, self.seat_list, on='Partido')
        df_res.rename(columns={'Cantidad': 'Votos'}, inplace=True) 
        
        # 2. Verificamos si supera el umbral (Booleano temporal para cálculos)
        df_res['Supera Umbral_Bool'] = df_res['Votos'] >= self.ballot_threshold
        
        # --- LA CORRECCIÓN CLAVE ---
        # Calculamos la "Bolsa de votos válidos" sumando solo a los que pasaron el umbral
        votos_reparto = df_res.loc[df_res['Supera Umbral_Bool'], 'Votos'].sum()
        
        # 3. Calculamos el escaño proporcional
        df_res['Escaño Proporcional'] = 0.0  # Todos arrancan en 0
        
        # Solo a los que superaron el umbral se les calcula la proporción real
        df_res.loc[df_res['Supera Umbral_Bool'], 'Escaño Proporcional'] = (
            df_res.loc[df_res['Supera Umbral_Bool'], 'Votos'] / votos_reparto
        ) * self.n_seat
        
        df_res['Escaño Proporcional'] = df_res['Escaño Proporcional'].round(2)
        
        # Convertimos el Booleano a 'Sí' / 'No' para que se vea bien en la tabla final
        df_res['Supera Umbral'] = df_res['Supera Umbral_Bool'].map({True: 'Sí', False: 'No'})
        df_res.drop(columns=['Supera Umbral_Bool'], inplace=True) # Borramos la columna auxiliar
        
        # 4. Creamos la fila de TOTAL
        total_votos = df_res['Votos'].sum()
        fila_total = pd.DataFrame({
            'Partido': ['TOTAL'],
            'Votos': [total_votos],
            'Curules': [df_res['Curules'].sum()],
            'Supera Umbral': ['-'], 
            'Escaño Proporcional': [df_res['Escaño Proporcional'].sum().round(0)]
        })
        
        # 5. Añadimos la fila al final del DataFrame
        df_res = pd.concat([df_res, fila_total], ignore_index=True)
        
        return df_res
    
    def plot_results(self):
        df_res = self.results()
        
        # Excluimos la fila 'TOTAL' para la gráfica
        df_grafica = df_res[df_res['Partido'] != 'TOTAL']
        
        # Aumenté un poco el tamaño de la figura (12, 10) para dar espacio a los nombres largos
        fig, (ax_grafico, ax_tabla) = plt.subplots(nrows=2, figsize=(12, 10), gridspec_kw={'height_ratios': [2, 1]})
        
        # --- GRÁFICO ---
        colores = ['#1f77b4' if supera == 'Sí' else '#d62728' for supera in df_grafica['Supera Umbral']]
        barras = ax_grafico.bar(df_grafica['Partido'], df_grafica['Votos'], color=colores)
        
        ax_grafico.axhline(y=self.ballot_threshold, color='red', linestyle='--', linewidth=2, 
                           label=f'Umbral Mínimo ({int(self.ballot_threshold):,} votos)')
        
        ax_grafico.set_title('Votos por Partido y Umbral Electoral', fontsize=14, fontweight='bold')
        ax_grafico.set_ylabel('Número de Votos')
        
        # 1. SOLUCIÓN A LOS NÚMEROS APROXIMADOS
        # Apagamos la notación científica (e+06) en el eje Y
        ax_grafico.ticklabel_format(style='plain', axis='y')
        
        # Forzamos a que el número sobre la barra sea el entero exacto (sin decimales ni e+06)
        # Usamos '{:,.0f}' para ponerle comas separadoras de miles y que sea más fácil de leer
        ax_grafico.bar_label(barras, padding=3, fmt='{:,.0f}')
        
        # 2. SOLUCIÓN A LOS NOMBRES SOLAPADOS
        # Rotamos las etiquetas 45 grados y las alineamos a la derecha
        ax_grafico.set_xticks(range(len(df_grafica['Partido'])))
        ax_grafico.set_xticklabels(df_grafica['Partido'], rotation=45, ha='right')
        
        ax_grafico.legend()
        
        # --- TABLA ---
        ax_tabla.axis('tight')
        ax_tabla.axis('off')
        
        tabla = ax_tabla.table(
            cellText=df_res.values, 
            colLabels=df_res.columns, 
            loc='center', 
            cellLoc='center'
        )
        
        tabla.auto_set_font_size(False)
        tabla.set_fontsize(10)
        tabla.scale(1, 1.5)
        
        for (row, col), cell in tabla.get_celld().items():
            if row == 0:
                cell.set_text_props(weight='bold')
                cell.set_facecolor('#f0f0f0')
                
        # tight_layout hace que Matplotlib recalcule los espacios para que nada quede por fuera
        plt.tight_layout()
        plt.show()


