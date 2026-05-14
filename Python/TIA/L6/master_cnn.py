
import torch
import torch.nn as nn
import time
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix

class MasterCNN(nn.Module):
    def __init__(self, input_shape=(3, 32, 32), num_classes=10, 
                 depth=3, filters=[32, 64, 128], kernel_sizes=[3, 3, 3], 
                 pool_sizes=[2, 2, 2], activation_fn=nn.ReLU, 
                 use_batchnorm=True, fc_layers=[512, 256], dropout_p=0.4, epochs=40):
        super(MasterCNN, self).__init__()
        self.epochs = epochs
        
        assert depth == len(filters) == len(kernel_sizes) == len(pool_sizes), \
            "La longitud de filters, kernel_sizes y pool_sizes debe coincidir con 'depth'."
            
        conv_blocks = []
        in_channels = input_shape[0]
        
        for i in range(depth):
            conv_blocks.append(nn.Conv2d(in_channels, filters[i], 
                                         kernel_size=kernel_sizes[i], padding='same'))
            if use_batchnorm:
                conv_blocks.append(nn.BatchNorm2d(filters[i]))
            conv_blocks.append(activation_fn())
            if pool_sizes[i] > 1:
                conv_blocks.append(nn.MaxPool2d(kernel_size=pool_sizes[i]))
            in_channels = filters[i]
            
        self.feature_extractor = nn.Sequential(*conv_blocks)
        
        dummy_input = torch.zeros(1, *input_shape)
        dummy_output = self.feature_extractor(dummy_input)
        flattened_size = dummy_output.view(1, -1).size(1)
        
        fc_blocks = []
        in_features = flattened_size
        
        for fc_dim in fc_layers:
            fc_blocks.append(nn.Linear(in_features, fc_dim))
            fc_blocks.append(activation_fn())
            if dropout_p > 0:
                fc_blocks.append(nn.Dropout(dropout_p))
            in_features = fc_dim
            
        fc_blocks.append(nn.Linear(in_features, num_classes))
        fc_blocks.append(nn.LogSoftmax(dim=1)) 
        
        self.classifier = nn.Sequential(*fc_blocks)
        
    def forward(self, x):
        x = self.feature_extractor(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x
    

    def fit(self, train_loader, val_loader, optimizer, criterion, device, verbose=True):
        history = {'t_loss': [], 'v_loss': [], 't_acc': [], 'v_acc': []}
        start_time = time.time()
        
        if verbose:
            print(f"▶ Iniciando entrenamiento CNN por {self.epochs} épocas...")
        
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
            
            if verbose and ((epoch+1) % 5 == 0 or epoch == 0):
                print(f"Época {epoch+1:02d} | Train Loss: {history['t_loss'][-1]:.4f} | Val Acc: {history['v_acc'][-1]:.2f}%")
                
        tiempo_total = time.time() - start_time
        if verbose:
            print(f"✔ Finalizado en: {tiempo_total:.2f}s")
            
        history['time'] = tiempo_total 
        return history

    def evaluate(self, history, test_loader, device, exp_name="CIFAR10_CNN", verbose=True):
        if not os.path.exists("resultados_plots"):
            os.makedirs("resultados_plots")

        # [Toda tu lógica de gráficos con matplotlib se mantiene igual aquí]
        # (Omito el código de plt.plot y plt.savefig para no hacer la respuesta gigante,
        # asegúrate de mantener tus plt.savefig() aquí dentro)
        # ...
        
        self.eval() 
        y_true, y_pred = [], []
        with torch.no_grad():
            for ti, tl in test_loader:
                ti = ti.to(device)
                out = self(ti)
                _, p = torch.max(out, 1)
                y_true.extend(tl.cpu().numpy()) 
                y_pred.extend(p.cpu().numpy())

        clases_cifar = ['Avión', 'Auto', 'Pájaro', 'Gato', 'Ciervo', 'Perro', 'Rana', 'Caballo', 'Barco', 'Camión']
        report = classification_report(y_true, y_pred, target_names=clases_cifar, output_dict=True, zero_division=0)
        
        # Extraer métricas clave para devolverlas
        acc_global = report['accuracy']
        f1_macro = report['macro avg']['f1-score']
        f1_weighted = report['weighted avg']['f1-score']
        
        if verbose:
            print(f"📊 Reportes de {exp_name} generados. Acc: {acc_global:.4f} | F1: {f1_macro:.4f}")
            
        # NUEVO: Retornar los resultados
        return {
            "accuracy": acc_global,
            "f1_macro": f1_macro,
            "f1_weighted": f1_weighted,
            "tiempo_seg": history.get('time', 0)
        }
        if not os.path.exists("resultados_plots"):
            os.makedirs("resultados_plots")

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

        self.eval() 
        y_true, y_pred = [], []
        with torch.no_grad():
            for ti, tl in test_loader:
                ti = ti.to(device)
                out = self(ti)
                _, p = torch.max(out, 1)
                y_true.extend(tl.cpu().numpy()) 
                y_pred.extend(p.cpu().numpy())

        clases_cifar = ['Avión', 'Auto', 'Pájaro', 'Gato', 'Ciervo', 'Perro', 'Rana', 'Caballo', 'Barco', 'Camión']
        report = classification_report(y_true, y_pred, target_names=clases_cifar, output_dict=True, zero_division=0)
        
        plt.figure(figsize=(12, 10))
        cm = confusion_matrix(y_true, y_pred)
        sns.heatmap(cm, cmap='Blues', annot=True, fmt='d', xticklabels=clases_cifar, yticklabels=clases_cifar)
        plt.title(f'Matriz de Confusión - {exp_name}')
        plt.xlabel('Predicción')
        plt.ylabel('Real')
        plt.savefig(f"resultados_plots/{exp_name}_matriz.png")
        plt.close()
        
        print(f"📊 Reportes de {exp_name} generados exitosamente en la carpeta 'resultados_plots'.")