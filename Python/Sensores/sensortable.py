import pandas as pd
import matplotlib.pyplot as plt
import textwrap

class SensorTable:
    def __init__(self, title: str, info_rows: list[dict]):
        self.title = title
        self.info_rows = info_rows

        # Auto-wrap en TODAS las columnas cuando el texto > 35 caracteres
        max_width = 35
        for row in self.info_rows:
            for key, value in row.items():
                if isinstance(value, str) and len(value) > max_width:
                    row[key] = "\n".join(textwrap.wrap(value, width=max_width))

        self.df = pd.DataFrame(self.info_rows)

    def show(self, base_fontsize: int = 10, dpi: int = 110):
        n_cols = len(self.df.columns)
        n_rows = len(self.df)

        # Tamaño de figura (sin limitar el alto, solo calculado)
        fig_width = min(max(10, n_cols * 1.2), 18)
        fig_height = n_rows * 0.8 + 2   # un poco más alto para dar margen

        # Ajuste de tamaño de letra
        fontsize = max(6, base_fontsize - max(0, n_cols - 7) * 0.4)

        fig, ax = plt.subplots(figsize=(fig_width, fig_height), dpi=dpi)
        ax.set_axis_off()

        # Crear tabla
        table = ax.table(
            cellText=self.df.values,
            colLabels=self.df.columns,
            loc="center"
        )

        table.auto_set_font_size(False)
        table.set_fontsize(fontsize)

        # 👉 AUMENTAR ALTURA DE TODAS LAS FILAS (clave para que no se solape)
        table.scale(1.0, 1.8)  # x, y  (puedes probar 1.5–2.0 en y)

        # Ajustar ancho de columnas
        table.auto_set_column_width(col=list(range(n_cols)))

        ax.set_title(self.title, pad=20, fontsize=fontsize + 2)
        plt.subplots_adjust(left=0.02, right=0.98, top=0.9, bottom=0.05)

        return fig, ax
