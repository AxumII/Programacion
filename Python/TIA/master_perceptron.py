import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset, random_split
import time
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix, f1_score
from sklearn.datasets import fetch_olivetti_faces
import seaborn as sns

class MasterPerceptron(nn.Module):
    def __init__(self, input_size=4096, hidden_layers=[1024, 512], num_classes=40, 
                 activation_fn=nn.ReLU, dropout_p=0.0, epochs=40):
        super(MasterPerceptron, self).__init__()
        self.epochs = epochs
        
        layers = [] # Capas
        in_dim = input_size # Tamaño del array de entrada 
        
        for h_dim in hidden_layers:
            layers.append(nn.Linear(in_dim, h_dim)) # Aplica la transformación lineal (pesos y sesgos)
            layers.append(activation_fn()) # Activación de la función (ej. ReLU, LeakyReLU)
            if dropout_p > 0: # Permite activar/desactivar el dropout
                layers.append(nn.Dropout(dropout_p))
            in_dim = h_dim
            
        self.hidden_net = nn.Sequential(*layers) # Empaqueta todas las capas para ejecutarlas secuencialmente
        self.classifier = nn.Linear(in_dim, num_classes) # Capa final de clasificación para las 40 clases
        
    def forward(self, x):
        x = self.hidden_net(x)
        return self.classifier(x)
    
    # Renombramos "train" a "fit" para no romper el comportamiento interno de nn.Module
    def fit(self, train_loader, val_loader, optimizer, criterion, device):
        history = {'t_loss': [], 'v_loss': [], 't_acc': [], 'v_acc': []}
        start_time = time.time()
        print("▶ Iniciando entrenamiento...")
        
        for epoch in range(self.epochs):
            self.train() # Usamos self.train() en vez de model.train()
            r_loss, correct_t, total_t = 0.0, 0, 0
            
            for inputs, labels in train_loader:
                inputs, labels = inputs.to(device), labels.to(device)
                
                optimizer.zero_grad()
                outputs = self(inputs) # Usamos self(inputs) en vez de model(inputs)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()
                
                r_loss += loss.item()
                _, pred = torch.max(outputs, 1)
                correct_t += (pred == labels).sum().item()
                total_t += labels.size(0)
                
            self.eval() # Usamos self.eval() en vez de model.eval()
            rv_loss, correct_v, total_v = 0.0, 0, 0
            with torch.no_grad():
                for vi, vl in val_loader:
                    vi, vl = vi.to(device), vl.to(device)
                    vo = self(vi) # Usamos self(vi) en vez de model(vi)
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
                
        total_time = time.time() - start_time
        print(f"\n✔ Entrenamiento finalizado en: {total_time:.2f} segundos.")
        return history

    # Se aplanó la función y se piden los parámetros externos que necesita (history, test_loader, device)
    def evaluate(self, history, test_loader, device):
        # 1. Análisis Visual de Sobreajuste
        plt.figure(figsize=(14, 5))
        
        plt.subplot(1, 2, 1)
        plt.plot(history['t_loss'], label='Entrenamiento (Train)')
        plt.plot(history['v_loss'], label='Validación (Val)')
        plt.title('Curvas de Pérdida: Análisis de Sobreajuste')
        plt.xlabel('Épocas')
        plt.ylabel('Loss')
        plt.legend()
        
        plt.subplot(1, 2, 2)
        plt.plot(history['t_acc'], label='Train Accuracy')
        plt.plot(history['v_acc'], label='Val Accuracy')
        plt.title('Evolución de la Precisión')
        plt.xlabel('Épocas')
        plt.ylabel('Accuracy %')
        plt.legend()
        plt.tight_layout()
        plt.show()

        # 2. Métricas en el conjunto de Test
        self.eval() # Usamos self.eval()
        y_true, y_pred = [], []
        with torch.no_grad():
            for ti, tl in test_loader:
                ti = ti.to(device)
                out = self(ti)
                _, p = torch.max(out, 1)
                
                # Se agregó .cpu() a tl por si los datos están en CUDA al pasarlos a Numpy
                y_true.extend(tl.cpu().numpy()) 
                y_pred.extend(p.cpu().numpy())

        # ▶ Accuracy, Precision, Recall y F1 por clase
        print("\n" + "="*60)
        print("REPORTE DE CLASIFICACIÓN DETALLADO")
        print("="*60)
        print(classification_report(y_true, y_pred))

        # ▶ F1 Macro y Micro
        micro = f1_score(y_true, y_pred, average='micro')
        macro = f1_score(y_true, y_pred, average='macro')
        print(f"▶ F1 Score (Micro): {micro:.4f}")
        print(f"▶ F1 Score (Macro): {macro:.4f}")
        print("="*60)
        
        # ▶ Matriz de Confusión
        plt.figure(figsize=(12, 10))
        cm = confusion_matrix(y_true, y_pred)
        sns.heatmap(cm, cmap='viridis', annot=False)
        plt.title('Matriz de Confusión Final (Análisis por Clase)')
        plt.xlabel('Predicción del Modelo')
        plt.ylabel('Clase Real')
        plt.show()
        
        
####################################################3
#

# --- PASO 1: Descargar y cargar Olivetti Faces ---
print("Descargando dataset Olivetti Faces...")
faces = fetch_olivetti_faces()

X_real = faces.data   # Matriz de NumPy con forma (400, 4096)
y_real = faces.target # Array de NumPy con forma (400,) con etiquetas del 0 al 39

print(f"Total de imágenes: {X_real.shape[0]}, Características por imagen: {X_real.shape[1]}")

# --- PASO 2: Convertir a tensores y preparar lotes ---
# ¡ATENCIÓN! Olivetti Faces ya viene normalizado [0, 1], así que no dividimos por 255
X_tensor = torch.FloatTensor(X_real)
y_tensor = torch.LongTensor(y_real)

dataset = TensorDataset(X_tensor, y_tensor)

# Olivetti Faces tiene solo 400 imágenes.
# Dividimos: 70% tren (280 imgs), 15% val (60 imgs), 15% test (60 imgs)
train_size = int(0.7 * len(dataset))
val_size = int(0.15 * len(dataset))
test_size = len(dataset) - train_size - val_size

train_set, val_set, test_set = random_split(dataset, [train_size, val_size, test_size])

# Reducimos el batch_size a 32 (como el dataset es pequeño, 64 daría muy pocos pasos por época)
BATCH_SIZE = 32
train_loader = DataLoader(train_set, batch_size=BATCH_SIZE, shuffle=True)
val_loader = DataLoader(val_set, batch_size=BATCH_SIZE)
test_loader = DataLoader(test_set, batch_size=BATCH_SIZE)

# --- PASO 3: Configurar el modelo ---
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Dispositivo de entrenamiento: {device}")

# Instanciamos el modelo con 100 épocas (al ser pocos datos, puede necesitar más épocas)
modelo = MasterPerceptron(
    input_size=4096, 
    hidden_layers=[1024, 512], 
    num_classes=40,
    epochs=100  
).to(device)

# --- PASO 4: Definir optimizador y pérdida ---
# Aumentamos un poco el Weight Decay (L2) porque con 400 imágenes es muy fácil sobreajustar
optimizer = optim.Adam(modelo.parameters(), lr=0.001, weight_decay=1e-3)
criterion = nn.CrossEntropyLoss()

# --- PASO 5: ¡ENTRENAR! ---
historial = modelo.fit(train_loader, val_loader, optimizer, criterion, device)

# --- PASO 6: EVALUAR ---
modelo.evaluate(historial, test_loader, device)