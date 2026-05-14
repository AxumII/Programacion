import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random

# Importamos la clase desde nuestro otro archivo (asegúrate de haber guardado master_cnn.py)
from master_cnn import MasterCNN

# ==========================================
# 1. FUNCIONES DE EXPLORACIÓN VISUAL
# ==========================================
def visualizar_muestras_cifar(dataset_raw, clases):
    print("⏳ Generando grid de muestras de CIFAR-10...")
    muestras = {i: [] for i in range(10)}
    for img, label in dataset_raw:
        if len(muestras[label]) < 10:
            muestras[label].append(img)
        if all(len(v) == 10 for v in muestras.values()):
            break

    fig, axes = plt.subplots(10, 10, figsize=(12, 12))
    fig.suptitle("Muestras del dataset CIFAR-10 — 10 clases, 10 imágenes c/u", fontsize=14, y=1.02)
    
    for class_idx in range(10):
        for img_idx in range(10):
            ax = axes[class_idx, img_idx]
            ax.imshow(muestras[class_idx][img_idx])
            ax.set_xticks([])
            ax.set_yticks([])
            
            if img_idx == 0:
                ax.set_ylabel(clases[class_idx], fontsize=10, rotation=0, labelpad=30, ha='center')
            if class_idx == 0:
                ax.set_title(f"#{img_idx}", fontsize=8)
                
    plt.tight_layout()
    plt.show()

def analizar_distribucion_clases(dataset, clases):
    print("⏳ Analizando distribución de clases (esto puede tardar unos segundos)...")
    labels = [label for _, label in dataset]
    counts = pd.Series(labels).value_counts().sort_index()

    print(f"\nTotal clases             : {counts.shape[0]}")
    print(f"Min muestras por clase   : {counts.min()}")
    print(f"Max muestras por clase   : {counts.max()}")
    print(f"Dataset balanceado       : {counts.min() == counts.max()}\n")

    fig, ax = plt.subplots(figsize=(12, 4))
    ax.bar(clases, counts.values, color="steelblue", edgecolor="black", linewidth=0.5)
    ax.set_xlabel("Clase (Nombre)")
    ax.set_ylabel("# muestras")
    ax.set_title("Distribución de clases en CIFAR-10")
    ax.set_xticks(range(len(clases)))
    ax.set_ylim(0, counts.max() * 1.15) 
    
    for i, v in enumerate(counts.values):
        ax.text(i, v + (counts.max()*0.02), str(v), ha='center', va='bottom', fontsize=9)
        
    plt.tight_layout()
    plt.show()

# ==========================================
# 2. GENERADOR DE RANDOM SEARCH (ACTUALIZADO)
# ==========================================
def generar_grid_random_search(num_experimentos=5, semilla=42):
    random.seed(semilla)
    np.random.seed(semilla)
    
    configuraciones = []
    
    for i in range(num_experimentos):
        lr_exponent = random.uniform(-5, -2)
        lr = 10**lr_exponent
        dropout_p = random.uniform(0.1, 0.5)
        depth = random.randint(2, 5)
        
        # ▶ NUEVO: Batch size como entero aleatorio en intervalo [32, 512]
        batch_size = random.randint(32, 512) 
        
        # ▶ NUEVO: Opciones para optimizador y activación
        optimizador = random.choice(['Adam', 'SGD', 'RMSprop'])
        activacion = random.choice(['ReLU', 'ELU', 'Tanh', 'LeakyReLU'])
        
        base_f = random.choice([32, 64])
        filters = [base_f * (2**j) for j in range(depth)]
        kernel_sizes = [3] * depth
        pool_sizes = [2] * depth
        
        config = {
            'exp_id': f"Exp_RS_{i+1:02d}",
            'depth': depth,
            'filters': filters,
            'kernel_sizes': kernel_sizes,
            'pool_sizes': pool_sizes,
            'fc_layers': random.choice([[512], [512, 256]]),
            'dropout_p': round(dropout_p, 3), 
            'lr': round(lr, 6),               
            'batch_size': batch_size,
            'optimizer': optimizador,    # Añadido
            'activation': activacion     # Añadido
        }
        configuraciones.append(config)
        
    return configuraciones

# ==========================================
# 3. FUNCIÓN PRINCIPAL (ACTUALIZADA)
# ==========================================
def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"🚀 Iniciando picker.py usando dispositivo: {device}")
    
    clases_cifar = ['Avión', 'Auto', 'Pájaro', 'Gato', 'Ciervo', 'Perro', 'Rana', 'Caballo', 'Barco', 'Camión']

    dataset_visual = torchvision.datasets.CIFAR10(root='./data', train=True, download=True)
    # visualizar_muestras_cifar(dataset_visual, clases_cifar)
    # analizar_distribucion_clases(dataset_visual, clases_cifar)
    
    transform_train = transforms.Compose([
        transforms.RandomCrop(32, padding=4),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)), 
    ])

    transform_test = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
    ])

    train_dataset = torchvision.datasets.CIFAR10(root='./data', train=True, download=True, transform=transform_train)
    test_dataset = torchvision.datasets.CIFAR10(root='./data', train=False, download=True, transform=transform_test)

    # --- DICCIONARIO DE FUNCIONES DE ACTIVACIÓN ---
    mapa_activaciones = {
        'ReLU': nn.ReLU,
        'ELU': nn.ELU,
        'Tanh': nn.Tanh,
        'LeakyReLU': nn.LeakyReLU
    }

    num_experimentos = 10
    epocas_por_experimento = 15 
    experimentos = generar_grid_random_search(num_experimentos=num_experimentos, semilla=2026) 
    
    resultados_ranking = [] 
    
    print(f"\n⏳ Iniciando Búsqueda ({num_experimentos} experimentos, {epocas_por_experimento} épocas c/u)...")
    
    for conf in experimentos:
        print(f"  Entrenando {conf['exp_id']} (Batch: {conf['batch_size']}, LR: {conf['lr']}, Opt: {conf['optimizer']}, Act: {conf['activation']})...")
        
        train_loader = DataLoader(train_dataset, batch_size=conf['batch_size'], shuffle=True, num_workers=2)
        test_loader = DataLoader(test_dataset, batch_size=conf['batch_size'], shuffle=False, num_workers=2)
        
        # Recuperamos la clase real de la función de activación desde el diccionario
        funcion_activacion_elegida = mapa_activaciones[conf['activation']]
        
        modelo_cnn = MasterCNN(
            input_shape=(3, 32, 32),
            num_classes=10,
            depth=conf['depth'],
            filters=conf['filters'],
            kernel_sizes=conf['kernel_sizes'],
            pool_sizes=conf['pool_sizes'],
            activation_fn=funcion_activacion_elegida, # Usamos la función dinámica
            use_batchnorm=True,
            fc_layers=conf['fc_layers'],
            dropout_p=conf['dropout_p'],
            epochs=epocas_por_experimento
        ).to(device)

        criterion = nn.NLLLoss()
        
        # ▶ INSTANCIACIÓN DINÁMICA DEL OPTIMIZADOR
        if conf['optimizer'] == 'Adam':
            optimizer = optim.Adam(modelo_cnn.parameters(), lr=conf['lr'], weight_decay=1e-4)
        elif conf['optimizer'] == 'SGD':
            optimizer = optim.SGD(modelo_cnn.parameters(), lr=conf['lr'], weight_decay=1e-4, momentum=0.9)
        elif conf['optimizer'] == 'RMSprop':
            optimizer = optim.RMSprop(modelo_cnn.parameters(), lr=conf['lr'], weight_decay=1e-4)

        historial = modelo_cnn.fit(train_loader, test_loader, optimizer, criterion, device, verbose=False)
        metricas = modelo_cnn.evaluate(historial, test_loader, device, exp_name=conf['exp_id'], verbose=False)
        
        # Guardamos en el ranking incluyendo Optim y Activación
        resultados_ranking.append({
            'ID Exp': conf['exp_id'],
            'Accuracy': metricas['accuracy'],
            'F1 Macro': metricas['f1_macro'],
            'Tiempo(s)': round(metricas['tiempo_seg'], 1),
            'Depth': conf['depth'],
            'LR': conf['lr'],
            'Batch': conf['batch_size'],
            'Optim': conf['optimizer'],
            'Activ': conf['activation']
        })

    # --- FASE 4: RESULTADOS FINALES ---
    print("\n" + "="*80)
    print("🏆 RANKING DE MEJORES HIPERPARÁMETROS 🏆")
    print("="*80)
    
    df_ranking = pd.DataFrame(resultados_ranking)
    df_ranking = df_ranking.sort_values(by='Accuracy', ascending=False).reset_index(drop=True)
    
    df_ranking['Accuracy'] = (df_ranking['Accuracy'] * 100).apply(lambda x: f"{x:.2f}%")
    df_ranking['F1 Macro'] = (df_ranking['F1 Macro'] * 100).apply(lambda x: f"{x:.2f}%")
    
    # Imprimimos la tabla con pandas
    print(df_ranking.to_string(index=True))
    
    df_ranking.to_csv("resultados_plots/ranking_experimentos.csv", index=False)
    print("\n✅ Ranking guardado en 'resultados_plots/ranking_experimentos.csv'")

if __name__ == "__main__":
    main()