import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class SimpleAnalysis:
    def __init__(self, data_dir: str) -> None:
        self.data_dir = data_dir
        self.data = {}
        self.temp_mean = {}

    def load_data(self, file_name: str) -> None:
        file_path = os.path.join(self.data_dir, file_name)
        with open(file_path, 'r') as file:
            lines = file.readlines()
        grouped_data = {}
        current_group = None
        for line in lines:
            if "Muestra" in line:
                current_group = line.strip()
                grouped_data[current_group] = []
            else:
                grouped_data[current_group].append(line.strip().split(','))
        for group, rows in grouped_data.items():
            df = pd.DataFrame(rows)
            df = df.apply(pd.to_numeric, errors='ignore')
            df.columns = ['Muestra', 'Acc_X', 'Acc_Y', 'Acc_Z', 'Gyr_X', 'Gyr_Y', 'Gyr_Z', 'Temp']
            self.data[group] = df
            self.temp_mean[group] = df['Temp'].mean()

    def calculate_statistics(self, group: str) -> pd.DataFrame:
        df = self.data[group]
        columns = df.columns[1:-1]
        stats_dict = {
            "Estadísticos": ["Media Muestral", "Desviación Estándar", "Media - 3*STD", "Media + 3*STD"]
        }
        for col in columns:
            mean = df[col].mean()
            std = df[col].std()
            stats_dict[col] = [
                round(mean, 6),
                round(std, 6),
                round(mean - 3 * std, 6),
                round(mean + 3 * std, 6)
            ]
        df_stats = pd.DataFrame(stats_dict)
        return df_stats

    def plot_data(self, group: str) -> None:
        df = self.data[group]
        columns = df.columns[1:-1]
        num_plots = len(columns)
        fig, axs = plt.subplots((num_plots + 1) // 2, 2, figsize=(12, num_plots * 2))
        axs = axs.flatten()
        for i, col in enumerate(columns):
            axs[i].plot(df.index, df[col], label=f'{col} (Media={df[col].mean():.3f})')
            axs[i].axhline(df[col].mean(), color='r', linestyle='-', linewidth=1, label='Media')
            axs[i].set_xlabel("Número de Dato")
            axs[i].set_ylabel(col)
            axs[i].set_title(f"Datos de {col}")
            axs[i].legend()
        for i in range(num_plots, len(axs)):
            fig.delaxes(axs[i])
        plt.tight_layout()
        plt.show()

    def plot_dataframe(self, df: pd.DataFrame, title: str) -> None:
        fig, ax = plt.subplots(figsize=(14, 8))
        ax.axis('tight')
        ax.axis('off')
        table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1.2, 1.2)
        plt.title(title, fontsize=16)
        plt.show()

# Uso de la clase
data_directory = os.path.join(os.getcwd(), 'Samples')
os.makedirs(data_directory, exist_ok=True)

analyzer = SimpleAnalysis(data_dir=data_directory)
analyzer.load_data('DATALOG.CSV')

# Iterar sobre los grupos y realizar análisis
results = {}
for group in analyzer.data.keys():
    stats_df = analyzer.calculate_statistics(group)
    results[group] = stats_df

    # Mostrar DataFrame como gráfico en lugar de guardar en CSV
    analyzer.plot_dataframe(stats_df, f"Estadísticas para {group}")

    # Generar gráficos
    analyzer.plot_data(group)

# Mostrar la media de la temperatura
temp_means = {group: analyzer.temp_mean[group] for group in analyzer.data.keys()}
temp_means_df = pd.DataFrame.from_dict(temp_means, orient='index', columns=['Media de Temperatura'])
analyzer.plot_dataframe(temp_means_df, "Media de Temperatura por Grupo")
