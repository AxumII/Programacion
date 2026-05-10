import torch
import torch.nn as nn

class MasterPerceptron(nn.Module):
    def __init__(self, input_size=4096, hidden_layers=[1024, 512], num_classes=40, 
                 activation_fn=nn.ReLU, dropout_p=0.0, epochs=40):
        super(MasterPerceptron, self).__init__()
        self.epochs = epochs
        layers = []
        in_dim = input_size 
        
        for h_dim in hidden_layers:
            layers.append(nn.Linear(in_dim, h_dim))
            layers.append(activation_fn())
            if dropout_p > 0:
                layers.append(nn.Dropout(dropout_p))
            in_dim = h_dim
            
        self.hidden_net = nn.Sequential(*layers)
        self.classifier = nn.Linear(in_dim, num_classes)
        
    def forward(self, x):
        x = self.hidden_net(x)
        return self.classifier(x)
    
    def fit(self, train_loader, val_loader, optimizer, criterion, device):
        import time
        history = {'t_loss': [], 'v_loss': [], 't_acc': [], 'v_acc': []}
        start_time = time.time()
        print(f"▶ Iniciando entrenamiento por {self.epochs} épocas...")
        
        for epoch in range(self.epochs):
            self.train()
            r_loss, correct_t, total_t = 0.0, 0, 0
            for inputs, labels in train_loader:
                inputs, labels = inputs.to(device), labels.to(device)
                optimizer.zero_grad()
                outputs = self(inputs)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()
                r_loss += loss.item()
                _, pred = torch.max(outputs, 1)
                correct_t += (pred == labels).sum().item()
                total_t += labels.size(0)
                
            self.eval()
            rv_loss, correct_v, total_v = 0.0, 0, 0
            with torch.no_grad():
                for vi, vl in val_loader:
                    vi, vl = vi.to(device), vl.to(device)
                    vo = self(vi)
                    rv_loss += criterion(vo, vl).item()
                    _, vp = torch.max(vo, 1)
                    correct_v += (vp == vl).sum().item()
                    total_v += vl.size(0)
            
            history['t_loss'].append(r_loss/len(train_loader))
            history['v_loss'].append(rv_loss/len(val_loader))
            history['t_acc'].append(100 * correct_t/total_t)
            history['v_acc'].append(100 * correct_v/total_v)
            
            if (epoch+1) % 10 == 0:
                print(f"Época {epoch+1:02d} | Train Loss: {history['t_loss'][-1]:.4f} | Val Acc: {history['v_acc'][-1]:.2f}%")
                
        tiempo_total = time.time() - start_time
        print(f"✔ Finalizado en: {tiempo_total:.2f}s")
        # Guardamos el tiempo directamente aquí
        history['time'] = tiempo_total 
        return history

    def evaluate(self, history, test_loader, device, exp_name="experimento"):
        import os
        import pandas as pd
        import seaborn as sns
        import matplotlib.pyplot as plt
        from sklearn.metrics import classification_report, confusion_matrix
        import torch

        if not os.path.exists("resultados_plots"):
            os.makedirs("resultados_plots")

        # 1. Gráficas de Aprendizaje + Tiempo de Entrenamiento
        plt.figure(figsize=(14, 5))        
        plt.subplot(1, 2, 1)
        plt.plot(history['t_loss'], label='Train Loss')
        plt.plot(history['v_loss'], label='Val Loss')
        plt.title(f'Pérdida - {exp_name}')
        plt.legend()

        plt.subplot(1, 2, 2)
        plt.plot(history['t_acc'], label='Train Acc')
        plt.plot(history['v_acc'], label='Val Acc')
        
        tiempo_total = history.get('time', 0) 
        plt.title(f'Precisión (Tiempo: {tiempo_total:.2f}s)')
        plt.legend()
        plt.savefig(f"resultados_plots/{exp_name}_curvas.png")
        plt.close() 

        # 2. Predicciones en CUDA (1660 Super)
        self.eval() 
        y_true, y_pred = [], []
        with torch.no_grad():
            for ti, tl in test_loader:
                ti = ti.to(device)
                out = self(ti)
                _, p = torch.max(out, 1)
                y_true.extend(tl.cpu().numpy()) 
                y_pred.extend(p.cpu().numpy())

        # 3. Reporte Visual con Precision, Recall y F1-score
        report = classification_report(y_true, y_pred, output_dict=True, zero_division=0)
        df_report = pd.DataFrame(report).transpose()
        df_report.columns = ['Precision', 'Recall', 'F1-score', 'Support']

        f1_macro = report['macro avg']['f1-score']
        f1_weighted = report['weighted avg']['f1-score']
        acc_global = report['accuracy']

        df_classes = df_report.drop(index=['accuracy', 'macro avg', 'weighted avg'], errors='ignore')

        plt.figure(figsize=(12, 16))
        sns.heatmap(df_classes[['Precision', 'Recall', 'F1-score']], 
                    annot=True, cmap='RdYlGn', fmt='.2f')
        
        plt.title(f'Métricas: {exp_name}\nAcc: {acc_global:.2f} | F1 Macro: {f1_macro:.2f} | F1 Weighted: {f1_weighted:.2f}')
        plt.tight_layout()
        plt.savefig(f"resultados_plots/{exp_name}_reporte_metricas.png")
        plt.close()

        # 4. Matriz de Confusión
        plt.figure(figsize=(12, 10))
        cm = confusion_matrix(y_true, y_pred)
        sns.heatmap(cm, cmap='viridis', annot=False)
        plt.title(f'Matriz de Confusión - {exp_name}')
        plt.savefig(f"resultados_plots/{exp_name}_matriz.png")
        plt.close()
        
        print(f"📊 Reportes de {exp_name} generados exitosamente.")