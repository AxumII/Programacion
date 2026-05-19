import torch
import torch.nn as nn
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from torch.utils.data import TensorDataset, DataLoader
from sklearn.preprocessing import StandardScaler

# Importar los modelos que creamos en los otros archivos
from master_LSTM import MasterLSTM
from master_GRU import MasterGRU

# ==========================================
# 1. CARGA Y PREPARACIÓN DE DATOS
# ==========================================
def preparar_jena_dataloaders(filepath, seq_length=144, target_col='T (degC)', batch_size=256):
    print("▶ Cargando Jena Climate Dataset...")
    df = pd.read_csv(filepath)
    df = df.drop('Date Time', axis=1) 
    
    data = df.values
    target_idx = df.columns.get_loc(target_col)
    
    # Normalización (Entrenado solo con la primera mitad para evitar trampa/leakage)
    num_train_samples = int(0.5 * len(data))
    scaler = StandardScaler()
    scaler.fit(data[:num_train_samples])
    data_scaled = scaler.transform(data)
    
    print(f"▶ Creando ventanas temporales (Secuencia: {seq_length} pasos)...")
    X, y = [], []
    for i in range(seq_length, len(data_scaled)):
        X.append(data_scaled[i-seq_length:i, :]) 
        y.append(data_scaled[i, target_idx])     
        
    X, y = np.array(X), np.array(y)
    
    # Splits: 50% Train, 25% Val, 25% Test
    val_split = int(0.5 * len(X))
    test_split = int(0.75 * len(X))
    
    X_train, y_train = X[:val_split], y[:val_split]
    X_val, y_val = X[val_split:test_split], y[val_split:test_split]
    X_test, y_test = X[test_split:], y[test_split:]
    
    train_loader = DataLoader(TensorDataset(torch.tensor(X_train, dtype=torch.float32), 
                                            torch.tensor(y_train, dtype=torch.float32)), 
                              batch_size=batch_size, shuffle=True)
                              
    val_loader = DataLoader(TensorDataset(torch.tensor(X_val, dtype=torch.float32), 
                                          torch.tensor(y_val, dtype=torch.float32)), 
                            batch_size=batch_size, shuffle=False)
                            
    test_loader = DataLoader(TensorDataset(torch.tensor(X_test, dtype=torch.float32), 
                                           torch.tensor(y_test, dtype=torch.float32)), 
                             batch_size=batch_size, shuffle=False)
    
    print(f"✔ DataLoaders listos. Variables de entrada (Features): {X_train.shape[2]}")
    return train_loader, val_loader, test_loader, scaler, X_train.shape[2]

# ==========================================
# 2. GENERADOR DE REPORTES COMPARATIVOS
# ==========================================
def generar_reporte_comparativo(modelo_lstm, hist_lstm, res_lstm, 
                                modelo_gru, hist_gru, res_gru, 
                                test_loader, device, num_muestras=150):
    if not os.path.exists("resultados_plots"):
        os.makedirs("resultados_plots")

    print("\n▶ Generando gráficas comparativas LSTM vs GRU...")
    
    # --- A) Curvas de Pérdida ---
    plt.figure(figsize=(14, 5))
    plt.subplot(1, 2, 1)
    plt.plot(hist_lstm['t_loss'], label='LSTM Train', color='blue')
    plt.plot(hist_gru['t_loss'], label='GRU Train', color='darkorange')
    plt.title('Pérdida en Entrenamiento (Train Loss)')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(hist_lstm['v_loss'], label='LSTM Val', color='blue', linestyle='--')
    plt.plot(hist_gru['v_loss'], label='GRU Val', color='darkorange', linestyle='--')
    plt.title('Pérdida en Validación (Val Loss)')
    plt.legend()
    plt.savefig("resultados_plots/01_Comparacion_Perdidas.png")
    plt.close()

    # --- B) Comparación de Métricas ---
    metricas = ['MAE', 'RMSE', 'MAPE', 'Sensibilidad_Ruido']
    val_lstm = [res_lstm[m] for m in metricas]
    val_gru = [res_gru[m] for m in metricas]

    x = np.arange(len(metricas))
    width = 0.35

    plt.figure(figsize=(10, 6))
    plt.bar(x - width/2, val_lstm, width, label='LSTM', color='royalblue', edgecolor='black')
    plt.bar(x + width/2, val_gru, width, label='GRU', color='darkorange', edgecolor='black')
    plt.ylabel('Valor de la Métrica')
    plt.title('Rendimiento: LSTM vs GRU (Más bajo es mejor)')
    plt.xticks(x, metricas)
    plt.legend()
    for i in range(len(metricas)):
        plt.text(x[i] - width/2, val_lstm[i], f'{val_lstm[i]:.2f}', ha='center', va='bottom', fontsize=9)
        plt.text(x[i] + width/2, val_gru[i], f'{val_gru[i]:.2f}', ha='center', va='bottom', fontsize=9)
    plt.savefig("resultados_plots/02_Comparacion_Metricas.png")
    plt.close()

    # --- C) Visualización Temporal ---
    modelo_lstm.eval()
    modelo_gru.eval()
    y_true, y_pred_lstm, y_pred_gru = [], [], []
    
    with torch.no_grad():
        for ti, tl in test_loader:
            ti = ti.to(device)
            y_true.extend(tl.cpu().numpy())
            y_pred_lstm.extend(modelo_lstm(ti).squeeze(-1).cpu().numpy())
            y_pred_gru.extend(modelo_gru(ti).squeeze(-1).cpu().numpy())
            if len(y_true) >= num_muestras: break

    y_true, y_pred_lstm, y_pred_gru = np.array(y_true[:num_muestras]), np.array(y_pred_lstm[:num_muestras]), np.array(y_pred_gru[:num_muestras])
    errores_lstm, errores_gru = y_true - y_pred_lstm, y_true - y_pred_gru

    plt.figure(figsize=(16, 8))
    plt.subplot(2, 1, 1)
    plt.plot(y_true, label='Real (Target)', color='black', linewidth=2)
    plt.plot(y_pred_lstm, label='LSTM', color='blue', alpha=0.7, linestyle='--')
    plt.plot(y_pred_gru, label='GRU', color='darkorange', alpha=0.7, linestyle='-.')
    plt.title(f'Predicciones Temporales vs Reales (Muestra de {num_muestras} pasos)')
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(errores_lstm, label='Error LSTM', color='blue', alpha=0.6)
    plt.plot(errores_gru, label='Error GRU', color='darkorange', alpha=0.6)
    plt.axhline(0, color='black', linewidth=1.5, linestyle='--')
    plt.title('Estabilidad Temporal: Residuos del Error')
    plt.legend()
    plt.tight_layout()
    plt.savefig("resultados_plots/03_Visualizacion_Temporal.png")
    plt.close()
    
    print("✔ Reportes guardados en la carpeta 'resultados_plots'.")

# ==========================================
# 3. FLUJO DE EJECUCIÓN PRINCIPAL
# ==========================================
if __name__ == "__main__":
    # Configuración de Hardware
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"🖥️  Entrenando en: {device}")

    # 1. Cargar Datos
    csv_path = 'jena_climate_2009_2016.csv' # Asegúrate de que el CSV esté en la carpeta
    train_dl, val_dl, test_dl, scaler, num_features = preparar_jena_dataloaders(
        filepath=csv_path, 
        seq_length=144, # 24 horas (asumiendo 6 mediciones por hora)
        batch_size=256
    )

    # Parámetros compartidos para una comparación justa
    epocas = 1 # Puedes subirlo a 40 cuando estés listo para el entrenamiento final
    lr = 0.001
    criterio = nn.MSELoss()

    # 2. Instanciar y Entrenar LSTM
    print("\n" + "="*40)
    modelo_lstm = MasterLSTM(input_size=num_features, hidden_size=64, num_layers=2, output_size=1, epochs=epocas).to(device)
    opt_lstm = torch.optim.Adam(modelo_lstm.parameters(), lr=lr)
    
    hist_lstm = modelo_lstm.fit(train_dl, val_dl, opt_lstm, criterio, device)
    res_lstm = modelo_lstm.evaluate(hist_lstm, test_dl, device, exp_name="LSTM_Jena", verbose=False)

    # 3. Instanciar y Entrenar GRU
    print("\n" + "="*40)
    modelo_gru = MasterGRU(input_size=num_features, hidden_size=64, num_layers=2, output_size=1, epochs=epocas).to(device)
    opt_gru = torch.optim.Adam(modelo_gru.parameters(), lr=lr)
    
    hist_gru = modelo_gru.fit(train_dl, val_dl, opt_gru, criterio, device)
    res_gru = modelo_gru.evaluate(hist_gru, test_dl, device, exp_name="GRU_Jena", verbose=False)

    # 4. Generar la Comparativa Cara a Cara
    print("\n" + "="*40)
    generar_reporte_comparativo(
        modelo_lstm, hist_lstm, res_lstm, 
        modelo_gru, hist_gru, res_gru, 
        test_dl, device, num_muestras=200
    )