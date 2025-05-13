import pandas as pd
import numpy as np

class Generator:
    def __init__(self, label_specs, n, filename="unnamed"):
        """
        label_specs: lista de diccionarios con claves 'name', 'mean' y 'std'
        n: número de muestras por variable
        filename: nombre del archivo CSV a exportar
        """
        self.label_specs = label_specs
        self.n = n
        self.filename = filename
        self.data = {}
        self.norm_gen()
        self.export_to_csv()

    def norm_gen(self):
        """
        Genera datos normales para todos los labels definidos.
        """
        for spec in self.label_specs:
            name = spec["name"]
            mean = spec["mean"]
            std = spec["std"]
            self.data[name] = np.random.normal(loc=mean, scale=std, size=self.n)

    def create_dataframe(self):
        """
        Crea un DataFrame con los datos generados.
        """
        return pd.DataFrame(self.data)

    def export_to_csv(self, index=False):
        """
        Exporta el DataFrame a un archivo CSV con el nombre definido en el constructor.
        """
        df = self.create_dataframe()
        df.to_csv(f"{self.filename}.csv", index=index)

# === EJECUCIÓN ===

archivos = [
    "voltage_measurement", "mass", "angle", "phi", "T","theta",
    "L_force", "base_cell", "high_cell", "L_def", "high_grid", "voltage_input"
]

# Generar un CSV para cada nombre con una columna que tenga su mismo nombre
for name in archivos:
    label_specs = [{"name": name, "mean": 7, "std": 0.5}]
    gen = Generator(label_specs, n=10, filename=name)
    print(f"CSV generado como {name}.csv")
