import numpy as np
import cupy as cp
import time
from scipy.stats import skew, kurtosis


# === CPU (NumPy) ===
def estimadores_cpu(datos):
    media = np.mean(datos)
    varianza = np.var(datos, ddof=1)
    sesgo = skew(datos)
    curt = kurtosis(datos)
    return media, varianza, sesgo, curt


# === GPU (CuPy) ===
def estimadores_gpu(n_iteraciones, n_muestras):
    resultados = []
    for _ in range(n_iteraciones):
        datos = cp.random.normal(0, 1, size=n_muestras)
        media = cp.mean(datos)
        varianza = cp.var(datos, ddof=1)
        std = cp.std(datos, ddof=1)
        sesgo = cp.asnumpy(cp.mean(((datos - media) ** 3))) / cp.asnumpy(std)**3
        curt = cp.asnumpy(cp.mean(((datos - media) ** 4))) / cp.asnumpy(varianza)**2 - 3
        resultados.append((float(media), float(varianza), float(sesgo), float(curt)))
    return np.mean(resultados, axis=0)


# === MAIN ===
if __name__ == "__main__":
    n_iteraciones = int(1e5)     
    n_muestras = int(1e5)        

    print(f"Tamaño de muestra por iteración: {n_muestras}")
    print(f"Total de iteraciones: {n_iteraciones}\n")

    # ----------- CPU (NumPy) ------------
    print("🔹 CPU (NumPy)")
    t0 = time.perf_counter()
    resultados_cpu = []
    for _ in range(n_iteraciones):
        datos = np.random.normal(0, 1, size=n_muestras)
        resultados_cpu.append(estimadores_cpu(datos))
    prom_cpu = np.mean(resultados_cpu, axis=0)
    t1 = time.perf_counter()
    print(f"Media: {prom_cpu[0]:.5f}, Var: {prom_cpu[1]:.5f}, Sesgo: {prom_cpu[2]:.5f}, Curtosis: {prom_cpu[3]:.5f}")
    print(f"⏱️ Tiempo CPU: {t1 - t0:.4f} s\n")

    # ----------- GPU (CuPy) ------------
    print("🔹 GPU (CuPy)")
    t0 = time.perf_counter()
    prom_gpu = estimadores_gpu(n_iteraciones, n_muestras)
    cp.cuda.Device(0).synchronize()
    t1 = time.perf_counter()
    print(f"Media: {prom_gpu[0]:.5f}, Var: {prom_gpu[1]:.5f}, Sesgo: {prom_gpu[2]:.5f}, Curtosis: {prom_gpu[3]:.5f}")
    print(f"⏱️ Tiempo GPU: {t1 - t0:.4f} s\n")
