from master_perceptron import MasterPerceptron 
from sklearn.datasets import fetch_olivetti_faces
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset, random_split
import os
import time

#---- Verificar el dataset y convertir los datos---
def load_data():
    path_dataset = "./scikit_learn_data"
    if os.path.exists(path_dataset):
        print(f"El directorio '{path_dataset}' ya existe. Cargando datos locales...")
    else:
        print(f"El dataset no se encuentra en {path_dataset}. Iniciando descarga...")

    try:
        faces = fetch_olivetti_faces(data_home=path_dataset, download_if_missing=True)
        print("✅ Dataset listo para usar.")
        print(f"Imágenes cargadas: {len(faces.images)}")
    except Exception as e:
        print(f"❌ Error al procesar el dataset: {e}")
    # Matriz de NumPy con forma (400, 4096) inicialmente
    x_tensor = torch.FloatTensor(faces.data)
    y_tensor = torch.LongTensor(faces.target)
    return TensorDataset(x_tensor, y_tensor)

#---- Función principal de experimentación ---
def run_experiment(name, train_loader, val_loader, test_loader, 
                   hidden_layers, lr, weight_decay, epochs, 
                   activation_fn, opt_type, device):    
    print(f"\n🚀 {name} | Layers: {hidden_layers} | LR: {lr} | Opt: {opt_type}")
    modelo = MasterPerceptron(
        input_size=4096, 
        hidden_layers=hidden_layers, 
        num_classes=40,
        epochs=epochs,
        activation_fn=activation_fn 
    ).to(device)
    
    if opt_type.lower() == "adam":
        optimizer = optim.Adam(modelo.parameters(), lr=lr, weight_decay=weight_decay)
    elif opt_type.lower() == "sgd":
        optimizer = optim.SGD(modelo.parameters(), lr=lr, momentum=0.9)
    else:
        optimizer = optim.RMSprop(modelo.parameters(), lr=lr)        
    criterion = nn.CrossEntropyLoss()    
    # 1. Ejecutar Entrenamiento 
    historial = modelo.fit(train_loader, val_loader, optimizer, criterion, device)    
    # 2. Generar Reportes Visuales
    modelo.evaluate(historial, test_loader, device, exp_name=name)     
    return modelo, historial

if __name__ == "__main__":
    # 1. Configuracion del dispositivo
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Dispositivo de entrenamiento: {device}")    
    # 2. Cargar datos
    dataset = load_data()    
    # 3. Definir tamaños y dividir dataset
    train_size = int(0.7 * len(dataset))
    val_size = int(0.15 * len(dataset))
    test_size = len(dataset) - train_size - val_size
    train_set, val_set, test_set = random_split(dataset, [train_size, val_size, test_size])    
    # 4. Crear DataLoaders
    batch_size = 16
    train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_set, batch_size=batch_size)
    test_loader = DataLoader(test_set, batch_size=batch_size)
    # 5. Lista de configuraciones de tests 
    configuraciones = [
        {
            "name": "Exp_1a",
            "layers": [1024, 512], #2 capas ocultas
            "lr": 0.0001, #Idealmente este valor
            "wd": 1e-3, #Idealmente igual o menor
            "epochs": 50, # Mas de 20 epocas, si no genera un sobreajuste feo, no la pongo grande porque como son solo 400 datos, esta jodido
            "activation": nn.ELU,  
            "opt": "adam" #no usar sgd aca, funciona terrible 
        },
        {
            "name": "Exp_1b",
            "layers": [1024, 512],
            "lr": 0.0001,
            "wd": 1e-3,
            "epochs": 50,
            "activation": nn.ELU,  
            "opt": "sgd"
        },
        #EN EL CASO 1
        #La RELU funciona mucho mejor que la sigmoide, decaimiento mas rapido en la perdida y mas preciso
        #Tanh es mejor que relu
        #ELU tambien es mejor 
        
        {
            
            "name": "Exp_2a",
            "layers": [1024, 512, 256 ,128],
            "lr": 0.0001, # Obligatoriamente igual o menor a este numero
            "wd": 1e-3,#No afecta mucho, solo debe ser igual o menor
            "epochs": 50, #Mayor a 20, menor a 60
            "activation": nn.Tanh, 
            "opt": "RMSprop"
        },
        {
            "name": "Exp_2b",
            "layers": [1024, 512, 256 ,128],
            "lr": 0.0001,
            "wd": 1e-3,
            "epochs": 50,
            "activation": nn.Tanh, 
            "opt": "RMSprop"
        },
         #EN EL CASO 2
         #Aca la mejor es tanh, las demas casi ni funcionan, tanh es la unica qeu funciona
        #El numero de capas no parece ser taan relevante
        
    
        {
            "name": "Exp_3a",
            "layers": [4096,2048,1024],
            "lr": 0.01, # debe ser mayor a 0.001 y menor a 0.05
            "wd": 1e-1,# valido entre 1e-1 y 1e-3
            "epochs": 50, 
            "activation": nn.Tanh, 
            "opt": "sgd"
        },
        {
            "name": "Exp_3b",
            "layers": [4096,2048,1024],
            "lr": 0.01,
            "wd": 1e-3,
            "epochs": 50,
            "activation": nn.Tanh, 
            "opt": "sgd"
        }
        #EN EL CASO 3
        #el numero de neuronas si parece ayudar a mejorar pero levemente, no hacer el embudo tan pequeño porque habrian neuronas con sobrepeso
        #El learning rate es lo mas importante
        #Sigmoide no funciona aca, pesimo, tanh funciona perfecto, RELU funciona pero es mas lento, necesitaria mas datos
        #ELU no sirve 
    ]

    # 6. Ejecución en bucle
    for c in configuraciones:
        run_experiment(
            name=c["name"], 
            train_loader=train_loader, 
            val_loader=val_loader, 
            test_loader=test_loader,
            hidden_layers=c["layers"], 
            lr=c["lr"], 
            weight_decay=c["wd"], 
            epochs=c["epochs"], 
            activation_fn=c["activation"], 
            opt_type=c["opt"],
            device=device # Se pasa el dispositivo para evitar depender de variables globales
        )
        
 