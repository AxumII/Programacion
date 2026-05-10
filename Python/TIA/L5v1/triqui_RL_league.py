import numpy as np
import time
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt 
import pandas as pd
import itertools

from L5v2.triqui import Game as g 
from L5v2.master_RL import MasterDQN, MasterSARSA, MotorRL, EpsilonGreedy

# =====================================================================
# 1. ENTORNO DE LIGA
# =====================================================================
class LeagueGameRL:
    def __init__(self, opponent_model=None, device="cpu", seed=None):
        if seed is not None:
            np.random.seed(seed)
            torch.manual_seed(seed)
        self.observation_space = type('obj', (object,), {'shape': (9,)}) 
        self.action_space = type('obj', (object,), {'n': 9})
        self.juego = None
        self.agent_role = 2 
        self.opponent = opponent_model 
        self.device = device

    def reset(self):
        self.juego = g()
        self.agent_role = 1 if self.agent_role == 2 else 2
        if self.agent_role == 2: self._play_opponent(role=1)
        return self._get_state(), {}

    def step(self, action):
        row, col = action // 3, action % 3
        if self.juego.get_game_matrix()[row, col] != 0:
            return self._get_state(), -10.0, True, False, {}
        
        if self.agent_role == 1: self.juego.play1(row, col)
        else: self.juego.play2(row, col)
        
        if self.juego.game_over:
            ganador = self._get_winner(self.juego.get_game_matrix())
            reward = 3.0 if ganador == self.agent_role else 1.0 
            return self._get_state(), reward, True, False, {}

        opp_role = 2 if self.agent_role == 1 else 1
        self._play_opponent(role=opp_role)
        
        if self.juego.game_over:
            ganador = self._get_winner(self.juego.get_game_matrix())
            reward = -3.0 if ganador == opp_role else 1.0 
            return self._get_state(), reward, True, False, {}

        return self._get_state(), 0.0, False, False, {}

    def _play_opponent(self, role):
        libres = self.juego.available_positions()
        if len(libres) == 0: return

        if self.opponent is None:
            pos = libres[np.random.randint(0, len(libres))]
            row, col = pos[0], pos[1]
        else:
            state = self.juego.get_game_matrix().flatten().astype(np.float32)
            state_t = torch.FloatTensor(state).unsqueeze(0).to(self.device)
            with torch.no_grad(): q_values = self.opponent(state_t).squeeze()
            indices_libres = [r*3 + c for r, c in libres]
            mejor_accion = indices_libres[q_values[indices_libres].argmax().item()]
            row, col = mejor_accion // 3, mejor_accion % 3

        if role == 1: self.juego.play1(row, col)
        else: self.juego.play2(row, col)

    def _get_state(self):
        return self.juego.get_game_matrix().flatten().astype(np.float32)

    def _get_winner(self, matrix):
        for p in [1, 2]:
            t = 3 * p
            if np.any(matrix.sum(axis=0)==t) or np.any(matrix.sum(axis=1)==t) or \
               matrix.diagonal().sum()==t or np.fliplr(matrix).diagonal().sum()==t:
                return p
        return 0

# =====================================================================
# 2. FUNCIONES DE EVALUACIÓN Y ENTRENAMIENTO PARAMETRIZADO
# =====================================================================
def evaluate_agent(agente, env_eval, episodios=200, device="cpu"):
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
    agente.train()
    return {k: (v/episodios)*100 for k, v in res.items()}

def entrenar_con_metricas(nombre, config, oponente, device, total_eps=4000, eval_freq=1000):
    print(f"\n⚙️ Entrenando [{nombre}] vs [{'Random' if oponente is None else 'Bot_Maestro'}]...")
    
    agente = MasterDQN(
        input_size=9, action_dim=9, 
        hidden_layers=config["hidden_layers"],
        activation_fn=config["activation"] 
    ).to(device)

    env_train = LeagueGameRL(opponent_model=oponente, device=device)
    env_eval = LeagueGameRL(opponent_model=oponente, device=device, seed=84)
    
    exploracion = EpsilonGreedy(start=1.0, end=0.01, decay=config["epsilon_decay"])
    OptimizadorClase = config["optimizer"] 
    optimizador = OptimizadorClase(agente.parameters(), lr=config["lr"])
    
    motor = MotorRL(
        agent=agente, env=env_train, optimizer=optimizador, 
        device=device, exploration_strategy=exploracion, 
        batch_size=config["batch_size"]
    )

    hist_rew = []
    metricas_evol = []
    
    start_time = time.time()
    for i in range(total_eps // eval_freq):
        hist_rew.extend(motor.train(episodes=eval_freq, log_freq=eval_freq+1)) 
        m = evaluate_agent(agente, env_eval, episodios=300, device=device)
        m["Episodio"] = (i+1) * eval_freq
        metricas_evol.append(m)
        print(f"   > Eps {(i+1)*eval_freq}: Win {m['Victorias']:.1f}% | Loss {m['Derrotas']:.1f}% | Ilegal {m['Ilegales']:.1f}%")
        
    print(f"✅ {nombre} finalizado en {time.time() - start_time:.2f}s")
    df_metricas = pd.DataFrame(metricas_evol)
    return agente, hist_rew, df_metricas

# =====================================================================
# 3. TORNEO Y GRÁFICAS (DASHBOARDS) - ACTUALIZADO
# =====================================================================

def gran_torneo(agentes_dict, episodios_torneo=500, device="cpu"):
    print("\n" + "🏆"*20)
    print(" INICIANDO GRAN TORNEO DE AGENTES ")
    print("🏆"*20)
    nombres = list(agentes_dict.keys())
    
    # Separar matrices para Victorias y Empates
    matriz_texto = {p1: {} for p1 in nombres}
    matriz_win = {p1: {} for p1 in nombres}
    matriz_draw = {p1: {} for p1 in nombres}
    
    for ag1 in nombres:
        for ag2 in nombres:
            if ag1 == ag2:
                matriz_texto[ag1][ag2] = "-"
                matriz_win[ag1][ag2] = np.nan
                matriz_draw[ag1][ag2] = np.nan
            else:
                env_test = LeagueGameRL(opponent_model=agentes_dict[ag2], device=device)
                m = evaluate_agent(agentes_dict[ag1], env_test, episodios=episodios_torneo, device=device)
                
                matriz_texto[ag1][ag2] = f"W:{m['Victorias']:.0f}% D:{m['Empates']:.0f}%"
                matriz_win[ag1][ag2] = m['Victorias']
                matriz_draw[ag1][ag2] = m['Empates']
                
    df_texto = pd.DataFrame(matriz_texto).T
    df_win = pd.DataFrame(matriz_win).T
    df_draw = pd.DataFrame(matriz_draw).T
    
    print(f"\n📊 MATRIZ DE RESULTADOS ({episodios_torneo} partidas | Fila juega vs Columna):")
    print(df_texto.to_string())
    
    # Retornamos ambas matrices para la gráfica
    return df_win, df_draw

def graficar_torneo(df_win, df_draw):
    """Genera el mapa de calor mostrando Victorias (W) y Empates (D)."""
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # El color representa la suma de W + D para ver quién es más sólido globalmente
    df_total_exito = df_win + df_draw
    cax = ax.matshow(df_total_exito, cmap='RdYlGn', vmin=0, vmax=100)
    fig.colorbar(cax, label='Tasa de Éxito (Victorias + Empates) %')
    
    ax.set_xticks(range(len(df_win.columns)))
    ax.set_yticks(range(len(df_win.index)))
    ax.set_xticklabels(df_win.columns, rotation=45, ha='left')
    ax.set_yticklabels(df_win.index)
    
    for i in range(len(df_win.index)):
        for j in range(len(df_win.columns)):
            w_val = df_win.iloc[i, j]
            d_val = df_draw.iloc[i, j]
            if not np.isnan(w_val):
                # Mostramos ambos datos en la celda
                texto_celda = f"W: {w_val:.1f}%\nD: {d_val:.1f}%"
                ax.text(j, i, texto_celda, va='center', ha='center', 
                        color='black', weight='bold', fontsize=9)
                
    plt.title("Rendimiento del Torneo: Victorias vs Empates", pad=30, weight='bold')
    plt.tight_layout()
    plt.show()

def graficar_dashboard_completo(diccionario_hist_rew, diccionario_df_evol):
    """Genera las gráficas de evolución temporal de los agentes durante el entrenamiento."""
    n_agentes = len(diccionario_hist_rew)
    
    # 1. Gráfica de Ganancia Promedio (Reward)
    plt.figure(figsize=(12, 5))
    for nombre, recompensas in diccionario_hist_rew.items():
        media_movil = pd.Series(recompensas).rolling(200).mean()
        plt.plot(media_movil, label=f'Reward: {nombre}', linewidth=1.5)
    plt.title("Ganancia Promedio de Recompensa (Media Móvil 200 eps)")
    plt.xlabel("Episodios Jugados")
    plt.ylabel("Recompensa")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

    # 2. Panel de Evolución (Win, Draw, Loss, Ilegales)
    fig, axes = plt.subplots(n_agentes, 1, figsize=(10, 4 * n_agentes), sharex=True)
    if n_agentes == 1: axes = [axes]
    
    for ax, (nombre, df) in zip(axes, diccionario_df_evol.items()):
        ax.plot(df['Episodio'], df['Victorias'], label='Win', color='green', marker='o')
        ax.plot(df['Episodio'], df['Empates'], label='Draw', color='blue', marker='s')
        ax.plot(df['Episodio'], df['Derrotas'], label='Loss', color='red', marker='v')
        ax.plot(df['Episodio'], df['Ilegales'], label='Ilegal', color='black', linestyle='--')
        ax.set_title(f"Evolución: {nombre}")
        ax.set_ylabel("Porcentaje (%)")
        ax.set_ylim(-5, 105)
        ax.grid(True, linestyle=':', alpha=0.6)
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    plt.xlabel("Episodios")
    plt.tight_layout()
    plt.show()
# =====================================================================
# 4. MODOS DE JUEGO (Humano y Bot Espectador)
# =====================================================================
def play_vs_player(agente, nombre_agente, device="cpu"):
    agente.eval()
    juego = g()
    print(f"\n🎮 VS {nombre_agente.upper()}")
    humano_rol = 1 if input("¿Juegas primero? (s/n): ").lower() == 's' else 2
    ia_rol = 2 if humano_rol == 1 else 1
    
    while not juego.game_over:
        print(f"\nTablero:\n{juego.get_game_matrix()}")
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
            libres = [r*3+c for r,c in juego.available_positions()]
            accion = libres[q[libres].argmax().item()]
            if ia_rol == 1: juego.play1(accion//3, accion%3)
            else: juego.play2(accion//3, accion%3)
            
    print(f"\nFinal:\n{juego.get_game_matrix()}")
    matriz = juego.get_game_matrix()
    ganador = 0
    for p in [1, 2]:
        t = 3 * p
        if np.any(matriz.sum(axis=0)==t) or np.any(matriz.sum(axis=1)==t) or \
           matriz.diagonal().sum()==t or np.fliplr(matriz).diagonal().sum()==t:
            ganador = p
            
    if ganador == humano_rol: print("🎉 ¡Le ganaste a la máquina!")
    elif ganador == ia_rol: print("💀 La IA te ha derrotado.")
    else: print("🤝 Empate. Bien jugado.")

def play_bot_vs_bot(ag1, nom1, ag2, nom2, device="cpu"):
    ag1.eval(); ag2.eval()
    juego = g()
    print(f"\n🤖 BATALLA DE MENTES: {nom1.upper()} (X) vs {nom2.upper()} (O) 🤖")
    
    while not juego.game_over:
        print(f"\nTablero Actual:\n{juego.get_game_matrix()}")
        time.sleep(1.2) # Pausa dramática para ver el movimiento
        
        state = juego.get_game_matrix().flatten().astype(np.float32)
        state_t = torch.FloatTensor(state).unsqueeze(0).to(device)
        libres = [r*3+c for r,c in juego.available_positions()]
        
        if juego.current_player == 1:
            with torch.no_grad(): q = ag1(state_t).squeeze()
            accion = libres[q[libres].argmax().item()]
            print(f"> [{nom1}] juega en: {accion}")
            juego.play1(accion//3, accion%3)
        else:
            with torch.no_grad(): q = ag2(state_t).squeeze()
            accion = libres[q[libres].argmax().item()]
            print(f"> [{nom2}] juega en: {accion}")
            juego.play2(accion//3, accion%3)
            
    print(f"\nTablero Final:\n{juego.get_game_matrix()}")
    matriz = juego.get_game_matrix()
    ganador = 0
    for p in [1, 2]:
        t = 3 * p
        if np.any(matriz.sum(axis=0)==t) or np.any(matriz.sum(axis=1)==t) or \
           matriz.diagonal().sum()==t or np.fliplr(matriz).diagonal().sum()==t:
            ganador = p
            
    if ganador == 1: print(f"🏆 ¡Victoria para {nom1} (X)!")
    elif ganador == 2: print(f"🏆 ¡Victoria para {nom2} (O)!")
    else: print("🤝 ¡Un empate perfecto!")

# =====================================================================
# 5. ORQUESTADOR MAESTRO
# =====================================================================
if __name__ == "__main__":
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # -----------------------------------------------------------------
    # CONTROL DE VARIABLES GLOBALES (Modifica estas a tu gusto)
    # -----------------------------------------------------------------
    EPS_TRAIN_MAESTRO = 1000   # Episodios para que el Master aprenda lo básico vs Random
    EPS_TRAIN_AGENTES = 1000   # Episodios para que cada agente entrene vs Master
    FREQ_EVALUACION   = 1000   # Cada cuántos episodios evaluar y guardar métricas
    EPS_TORNEO_MATCH  = 1000    # Partidas jugadas por CADA emparejamiento en el torneo final
    # -----------------------------------------------------------------
    
    config_maestro = {
        "hidden_layers": [256, 256], "activation": nn.ReLU, "optimizer": optim.Adam,
        "lr": 0.0005, "epsilon_decay": 0.9995, "batch_size": 128
    }

    configuraciones_n = {
        "Agente_Rapido_RMS": {
            "hidden_layers": [64, 64], "activation": nn.ELU, "optimizer": optim.RMSprop,
            "lr": 0.001, "epsilon_decay": 0.99, "batch_size": 64
        },
        "Agente_Denso_AdamW": {
            "hidden_layers": [256, 256], "activation": nn.LeakyReLU, "optimizer": optim.AdamW,
            "lr": 0.0003, "epsilon_decay": 0.999, "batch_size": 128
        },
        "Agente_Profundo_Lento DQn": {
            "hidden_layers": [1024, 512, 256], "activation": nn.ReLU, "optimizer": optim.Adam,
            "lr": 0.0001, "epsilon_decay": 0.9998, "batch_size": 256
        },
        "SARSA_Explorador": {
            "agent_class": MasterSARSA, 
            "hidden_layers": [256, 256], "activation": nn.ReLU, "optimizer": optim.Adam,
            "lr": 0.0005, "epsilon_decay": 0.9995, "batch_size": 128
        }
    }
    
    coleccion_modelos = {}
    todos_los_hist_rew = {}
    todos_los_df_evol = {}

    # --- FASE 1: ENTRENAR AL BOT MAESTRO ---
    print(f"🚀 FASE 1: ENTRENANDO BOT MAESTRO VS RANDOM ({EPS_TRAIN_MAESTRO} eps)")
    bot_maestro, rew_bot, df_bot = entrenar_con_metricas(
        nombre="Bot_Maestro", config=config_maestro, oponente=None, 
        device=device, total_eps=EPS_TRAIN_MAESTRO, eval_freq=FREQ_EVALUACION
    )
    coleccion_modelos["Bot_Maestro"] = bot_maestro
    todos_los_hist_rew["Bot_Maestro"] = rew_bot
    todos_los_df_evol["Bot_Maestro"] = df_bot
    
    print("\n📋 TABLA EVOLUTIVA DEL BOT MAESTRO:")
    print(df_bot.to_string(index=False))

    # --- FASE 2: ENTRENAR LOS N AGENTES ---
    print(f"\n🚀 FASE 2: ENTRENANDO TUS {len(configuraciones_n)} AGENTES VS BOT MAESTRO ({EPS_TRAIN_AGENTES} eps c/u)")
    bot_maestro.eval() 
    
    for nombre, config in configuraciones_n.items():
        agente_entrenado, rew, df = entrenar_con_metricas(
            nombre=nombre, config=config, oponente=bot_maestro, 
            device=device, total_eps=EPS_TRAIN_AGENTES, eval_freq=FREQ_EVALUACION
        )
        coleccion_modelos[nombre] = agente_entrenado
        todos_los_hist_rew[nombre] = rew
        todos_los_df_evol[nombre] = df
        
        print(f"\n📋 TABLA EVOLUTIVA DE {nombre.upper()}:")
        print(df.to_string(index=False))

    # --- FASE 3: TORNEO ---
    df_win_torneo, df_draw_torneo = gran_torneo(coleccion_modelos, episodios_torneo=EPS_TORNEO_MATCH, device=device)

    # --- FASE 4: MENÚ INTERACTIVO ---
    while True:
        print("\n" + "="*45)
        print("🤖 PANEL DE CONTROL DEL LABORATORIO RL")
        print("="*45)
        print("[1] Ver Dashboard Evolución (Curvas Train)")
        print("[2] Ver Dashboard Torneo (Mapa de Calor)")
        print("[3] Jugar: Humano vs Bot")
        print("[4] Espectador: Bot vs Bot (Turno a Turno)")
        print("[0] Salir")
        
        op = input("\nElige una opción: ")
        if op == "0": break
        
        elif op == "1":
            graficar_dashboard_completo(todos_los_hist_rew, todos_los_df_evol)
            
        elif op == "2":
            graficar_torneo(df_win_torneo, df_draw_torneo)
            
        elif op == "3":
            nombres = list(coleccion_modelos.keys())
            print("\nSelecciona a tu oponente:")
            for i, n in enumerate(nombres): print(f"[{i+1}] {n}")
            try:
                idx = int(input("> ")) - 1
                if 0 <= idx < len(nombres):
                    play_vs_player(coleccion_modelos[nombres[idx]], nombres[idx], device)
            except ValueError: pass
            
        elif op == "4":
            nombres = list(coleccion_modelos.keys())
            print("\nSelecciona al P1 (X):")
            for i, n in enumerate(nombres): print(f"[{i+1}] {n}")
            try:
                idx1 = int(input("> ")) - 1
                print("\nSelecciona al P2 (O):")
                idx2 = int(input("> ")) - 1
                
                if 0 <= idx1 < len(nombres) and 0 <= idx2 < len(nombres):
                    play_bot_vs_bot(
                        coleccion_modelos[nombres[idx1]], nombres[idx1],
                        coleccion_modelos[nombres[idx2]], nombres[idx2],
                        device
                    )
            except ValueError: pass