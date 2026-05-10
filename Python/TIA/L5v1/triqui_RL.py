import numpy as np
import time
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt 
import pandas as pd
import os

from L5v2.triqui import Game as g 
from L5v2.master_RL import MasterDQN, MotorRL, EpsilonGreedy

# --- Entorno de Entrenamiento ---
class TrainGameRL:
    def __init__(self, seed=None):
        if seed is not None:
            np.random.seed(seed)
            torch.manual_seed(seed)
        self.observation_space = type('obj', (object,), {'shape': (9,)}) 
        self.action_space = type('obj', (object,), {'n': 9})
        self.juego = None
        self.agent_role = 2 

    def reset(self):
        self.juego = g()
        self.agent_role = 1 if self.agent_role == 2 else 2
        if self.agent_role == 2: self._play_random_opponent(role=1)
        return self._get_state(), {}

    def step(self, action):
        row, col = action // 3, action % 3
        # Penalización por movimiento ilegal
        if self.juego.get_game_matrix()[row, col] != 0:
            return self._get_state(), -10.0, True, False, {}
        
        # Turno Agente
        if self.agent_role == 1: self.juego.play1(row, col)
        else: self.juego.play2(row, col)
        
        if self.juego.game_over:
            ganador = self._get_winner(self.juego.get_game_matrix())
            reward = 3.0 if ganador == self.agent_role else 1.0 # Win o Empate
            return self._get_state(), reward, True, False, {}

        # Turno Oponente Aleatorio
        opp_role = 2 if self.agent_role == 1 else 1
        self._play_random_opponent(role=opp_role)
        
        if self.juego.game_over:
            ganador = self._get_winner(self.juego.get_game_matrix())
            reward = -3.0 if ganador == opp_role else 1.0 # Loss o Empate
            return self._get_state(), reward, True, False, {}

        return self._get_state(), 0.0, False, False, {}

    def _play_random_opponent(self, role):
        libres = self.juego.available_positions()
        if len(libres) > 0:
            pos = libres[np.random.randint(0, len(libres))]
            if role == 1: self.juego.play1(pos[0], pos[1])
            else: self.juego.play2(pos[0], pos[1])

    def _get_state(self):
        return self.juego.get_game_matrix().flatten().astype(np.float32)

    def _get_winner(self, matrix):
        for p in [1, 2]:
            t = 3 * p
            if np.any(matrix.sum(axis=0)==t) or np.any(matrix.sum(axis=1)==t) or \
               matrix.diagonal().sum()==t or np.fliplr(matrix).diagonal().sum()==t:
                return p
        return 0

# --- Evaluación ---
def evaluate_agent(agente, env_eval, episodios=500, device="cpu"):
    agente.eval()
    res = {"Victorias": 0, "Derrotas": 0, "Empates": 0, "Ilegales": 0}
    with torch.no_grad():
        for _ in range(episodios):
            state, _ = env_eval.reset()
            done = False
            while not done:
                state_t = torch.FloatTensor(state).unsqueeze(0).to(device)
                action = agente(state_t).argmax().item()
                state, reward, done, _, _ = env_eval.step(action)
                if done:
                    if reward == 3.0: res["Victorias"] += 1
                    elif reward == -3.0: res["Derrotas"] += 1
                    elif reward == 1.0: res["Empates"] += 1
                    elif reward == -10.0: res["Ilegales"] += 1
    # Retorna porcentajes[cite: 3]
    return {k: (v/episodios)*100 for k, v in res.items()}

# --- Visualización ---
def show_plots(df_metricas, df_recompensas):
    # Gráfica de Recompensa Acumulada
    plt.figure(figsize=(10, 4))
    plt.plot(df_recompensas['Recompensa'].rolling(200).mean(), color='orange', label='Media Móvil Reward')
    plt.title("Progreso de Recompensa Promedio")
    plt.grid(True, alpha=0.3)
    plt.legend(); plt.show()

    # Gráfica de Evolución Completa (Win, Draw, Loss, Illegal)[cite: 3]
    plt.figure(figsize=(10, 5))
    plt.plot(df_metricas['Episodio'], df_metricas['Victorias'], label='Victorias (Win)', marker='o', color='green', linewidth=2)
    plt.plot(df_metricas['Episodio'], df_metricas['Empates'], label='Empates (Draw)', marker='s', color='blue', linewidth=2)
    plt.plot(df_metricas['Episodio'], df_metricas['Derrotas'], label='Derrotas (Loss)', marker='v', color='red', linewidth=2)
    plt.plot(df_metricas['Episodio'], df_metricas['Ilegales'], label='Inválidas (Illegal)', marker='x', color='black', linestyle='--', linewidth=1.5)
    
    plt.title("Evolución del Rendimiento del Agente")
    plt.xlabel("Episodios de Entrenamiento")
    plt.ylabel("Porcentaje (%)")
    plt.ylim(-5, 105)
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.tight_layout()
    plt.show()

# --- Interacción ---
def play_vs_player(agente, device="cpu"):
    agente.eval()
    juego = g()
    humano_rol = 1 if input("\n¿Quieres jugar primero? (s/n): ").lower() == 's' else 2
    ia_rol = 2 if humano_rol == 1 else 1
    
    while not juego.game_over:
        print(f"\nTablero Actual:\n{juego.get_game_matrix()}")
        if juego.current_player == humano_rol:
            m = -1
            while m not in range(9):
                try:
                    m = int(input("Tu turno (0-8): "))
                    if juego.get_game_matrix()[m//3, m%3] != 0: m = -1
                except: pass
            if humano_rol == 1: juego.play1(m//3, m%3)
            else: juego.play2(m//3, m%3)
        else:
            state = juego.get_game_matrix().flatten().astype(np.float32)
            state_t = torch.FloatTensor(state).unsqueeze(0).to(device)
            with torch.no_grad(): q = agente(state_t).squeeze()
            # Filtrar solo jugadas legales para la demostración[cite: 2, 4]
            libres = [r*3+c for r,c in juego.available_positions()]
            accion = libres[q[libres].argmax().item()]
            if ia_rol == 1: juego.play1(accion//3, accion%3)
            else: juego.play2(accion//3, accion%3)
            
    print(f"\nTablero Final:\n{juego.get_game_matrix()}\n¡Partida Terminada!")

# --- Ejecución ---
if __name__ == "__main__":
    SEED = 42
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    env = TrainGameRL(seed=SEED); env_eval = TrainGameRL(seed=SEED+1)
    agente = MasterDQN(input_size=9, action_dim=9, hidden_layers=[512, 256]).to(device)
    exploracion = EpsilonGreedy(start=1.0, end=0.01, decay=0.9995)
    optimizador = optim.Adam(agente.parameters(), lr=0.0005)
    motor = MotorRL(agente, env, optimizador, device, exploracion)

    total_eps, b_size = 10000, 1000
    hist_rew, evol = [], []

    print(f"🚀 Iniciando entrenamiento de {total_eps} episodios...")
    start_t = time.time()
    
    for i in range(total_eps // b_size):
        # Entrenar bloque (silencioso)[cite: 3]
        hist_rew.extend(motor.train(episodes=b_size, log_freq=b_size+1))
        # Evaluar y guardar métricas[cite: 3]
        m = evaluate_agent(agente, env_eval, device=device)
        m["Episodio"] = (i+1)*b_size
        evol.append(m)
    
    # Persistencia y reporte[cite: 3]
    torch.save(agente.state_dict(), "modelo_triqui.pth")
    df_evol = pd.DataFrame(evol)
    print(f"\n✅ Entrenamiento completado en {time.time()-start_t:.2f}s")
    print("🧠 Modelo guardado como 'modelo_triqui.pth'")
    print("\n📊 REPORTE DE EVOLUCIÓN:")
    print(df_evol[["Episodio", "Victorias", "Empates", "Derrotas", "Ilegales"]].to_string(index=False))

    while True:
        op = input("\n[1] Ver Gráficas Completas [2] Jugar contra IA [3] Salir: ")
        if op == "1": show_plots(df_evol, pd.DataFrame({'Recompensa': hist_rew}))
        elif op == "2": play_vs_player(agente, device)
        elif op == "3": break