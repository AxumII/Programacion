import torch
import torch.nn as nn
import numpy as np
import time
import os
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, mean_absolute_percentage_error

class MasterLSTM(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers=2, output_size=1, 
                 fc_layers=[128, 64], dropout_p=0.3, activation_fn=nn.ReLU, epochs=40):
        super(MasterLSTM, self).__init__()
        self.epochs = epochs
        
        # Capa LSTM
        self.lstm = nn.LSTM(input_size=input_size, 
                            hidden_size=hidden_size, 
                            num_layers=num_layers, 
                            batch_first=True, 
                            dropout=dropout_p if num_layers > 1 else 0)
        
        # Clasificador / Regresor (Capas Densas)
        fc_blocks = []
        in_features = hidden_size
        for fc_dim in fc_layers:
            fc_blocks.append(nn.Linear(in_features, fc_dim))
            fc_blocks.append(activation_fn())
            if dropout_p > 0:
                fc_blocks.append(nn.Dropout(dropout_p))
            in_features = fc_dim
            
        fc_blocks.append(nn.Linear(in_features, output_size))
        self.regressor = nn.Sequential(*fc_blocks)
        
    def forward(self, x):
        out, (h_n, c_n) = self.lstm(x)
        out = out[:, -1, :] # Tomar solo la predicción del último paso temporal
        out = self.regressor(out)
        return out

    def fit(self, train_loader, val_loader, optimizer, criterion, device, verbose=True):
        history = {'t_loss': [], 'v_loss': []}
        start_time = time.time()
        
        if verbose:
            print(f"▶ Iniciando entrenamiento LSTM por {self.epochs} épocas...")
            
        for epoch in range(self.epochs):
            self.train()
            r_loss = 0.0
            for inputs, labels in train_loader:
                inputs, labels = inputs.to(device), labels.to(device)
                optimizer.zero_grad()
                outputs = self(inputs).squeeze(-1) # Adaptar para regresión
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()
                r_loss += loss.item()
                
            self.eval()
            rv_loss = 0.0
            with torch.no_grad():
                for vi, vl in val_loader:
                    vi, vl = vi.to(device), vl.to(device)
                    vo = self(vi).squeeze(-1)
                    rv_loss += criterion(vo, vl).item()
            
            history['t_loss'].append(r_loss / len(train_loader))
            history['v_loss'].append(rv_loss / len(val_loader))
            
            if verbose and ((epoch+1) % 5 == 0 or epoch == 0):
                print(f"Época {epoch+1:02d} | Train Loss: {history['t_loss'][-1]:.4f} | Val Loss: {history['v_loss'][-1]:.4f}")
                
        history['time'] = time.time() - start_time
        if verbose:
            print(f"✔ Entrenamiento LSTM Finalizado en: {history['time']:.2f}s")
        return history

    def evaluate(self, history, test_loader, device, exp_name="MasterLSTM", verbose=True):
        if not os.path.exists("resultados_plots"):
            os.makedirs("resultados_plots")

        self.eval() 
        y_true, y_pred = [], []
        
        with torch.no_grad():
            for ti, tl in test_loader:
                ti = ti.to(device)
                out = self(ti).squeeze(-1)
                y_true.extend(tl.cpu().numpy()) 
                y_pred.extend(out.cpu().numpy())

        y_true, y_pred = np.array(y_true), np.array(y_pred)

        # Prueba de sensibilidad al ruido (5%)
        y_pred_noisy = []
        with torch.no_grad():
            for ti, _ in test_loader:
                ti = ti.to(device)
                noise = torch.randn_like(ti) * 0.05 
                out_noisy = self(ti + noise).squeeze(-1)
                y_pred_noisy.extend(out_noisy.cpu().numpy())
                
        # --- MÉTRICAS ---
        mae = mean_absolute_error(y_true, y_pred)
        mse = mean_squared_error(y_true, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_true, y_pred)
        mape = mean_absolute_percentage_error(y_true, y_pred) * 100
        
        errores = y_true - y_pred
        estabilidad_temp = np.std(errores)
        mse_noisy = mean_squared_error(y_true, y_pred_noisy)
        degradacion_ruido = ((mse_noisy - mse) / mse) * 100
        
        # Diagnóstico de ajuste
        t_loss_end, v_loss_end = history['t_loss'][-1], history['v_loss'][-1]
        if v_loss_end > t_loss_end * 1.3: ajuste = "Sobreajuste Alto"
        elif v_loss_end > t_loss_end * 1.1: ajuste = "Ligero Sobreajuste"
        elif t_loss_end > v_loss_end * 1.2: ajuste = "Subajuste"
        else: ajuste = "Óptimo"

        if verbose:
            print(f"\n📊 --- REPORTES DE {exp_name} ---")
            print(f"MAE: {mae:.4f} | MSE: {mse:.4f} | RMSE: {rmse:.4f} | R²: {r2:.4f} | MAPE: {mape:.2f}%")
            print(f"Diagnóstico: {ajuste} | Estabilidad Temp (Std): {estabilidad_temp:.4f}")
            print(f"Sensibilidad al Ruido: +{degradacion_ruido:.2f}% degradación en MSE")

        # --- PLOTS INDIVIDUALES ---
        plt.figure(figsize=(18, 5))
        
        # Curvas de Pérdida
        plt.subplot(1, 3, 1)
        plt.plot(history['t_loss'], label='Train Loss')
        plt.plot(history['v_loss'], label='Val Loss')
        plt.title(f'Pérdida - {exp_name}')
        plt.legend()

        # Reales vs Predichas (100 datos max)
        plt.subplot(1, 3, 2)
        m = min(100, len(y_true))
        plt.plot(y_true[:m], label='Real', marker='o', markersize=4)
        plt.plot(y_pred[:m], label='Predicho', marker='x', linestyle='--', markersize=4)
        plt.title(f'Real vs Predicho ({m} muestras)')
        plt.legend()

        # Visualización temporal de errores
        plt.subplot(1, 3, 3)
        plt.bar(range(m), errores[:m], color=['red' if e > 0 else 'green' for e in errores[:m]])
        plt.axhline(0, color='black')
        plt.title('Error Temporal (Real - Predicción)')
        
        plt.tight_layout()
        plt.savefig(f"resultados_plots/{exp_name}_analisis.png")
        plt.close()

        return {"Modelo": exp_name, "MAE": mae, "MSE": mse, "RMSE": rmse, "R2": r2, "MAPE": mape, 
                "Estabilidad": estabilidad_temp, "Sensibilidad_Ruido": degradacion_ruido}