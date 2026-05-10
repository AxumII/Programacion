import numpy as np
import time
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt 
import pandas as pd

from triqui import Game as g
from triqui_train import Train
from triqui_championship import Championship
from master_RL import MasterDQN, MasterSARSA, MotorRL, EpsilonGreedy
from triqui_algorithm import Algorithm 

def mostrar_analisis_estrategico(agente, nombre_agente, episodios=1000, device="cpu"):
    print("\n" + "="*65)
    print(f"🧠 RADIOGRAFÍA ESTRATÉGICA POR TURNOS: {nombre_agente}")
    print("="*65)
    
    # Clasificador de posiciones
    def clasificar_jugada(r, c):
        if r == 1 and c == 1: return "center"
        elif (r, c) in [(0, 0), (0, 2), (2, 0), (2, 2)]: return "corner"
        else: return "edge"

    # Diccionario maestro para rastrear todo del Turno 1 al 5
    analisis = {
        "Agent_Starts": {f"Move_{i}": {"center": {"W":0, "D":0, "L":0}, "corner": {"W":0, "D":0, "L":0}, "edge": {"W":0, "D":0, "L":0}} for i in range(1, 6)},
        "Opponent_Starts": {f"Move_{i}": {"center": {"W":0, "D":0, "L":0}, "corner": {"W":0, "D":0, "L":0}, "edge": {"W":0, "D":0, "L":0}} for i in range(1, 6)}
    }

    # Bucle de partidas
    for partida in range(episodios):
        juego = g()
        oponente_algoritmo = Algorithm(juego) 

        agent_starts = (partida < episodios // 2)
        iniciativa = "Agent_Starts" if agent_starts else "Opponent_Starts"
        
        id_agente = 1 if agent_starts else 2
        id_oponente = 2 if agent_starts else 1
        
        agent_moves = [] 

        while not juego.game_over:
            if juego.current_player == id_agente:
                # 🧠 EL AGENTE PIENSA Y JUEGA
                state = juego.game_matrix.flatten()
                state_tensor = torch.FloatTensor(state).unsqueeze(0).to(device)
                with torch.no_grad():
                    q_vals = agente(state_tensor)
                
                valid_actions = juego.available_positions()
                if len(valid_actions) == 0: break
                
                valid_indices = [pos[0] * 3 + pos[1] for pos in valid_actions]
                q_vals_valid = q_vals[0, valid_indices]
                action_idx = valid_indices[torch.argmax(q_vals_valid).item()]
                
                r, c = action_idx // 3, action_idx % 3
                
                agent_moves.append(clasificar_jugada(r, c))
                
                if id_agente == 1:
                    juego.play1(r, c)
                else:
                    juego.play2(r, c)
                
            else:
                # 🤖 EL ALGORITMO JUEGA
                valid_actions = juego.available_positions()
                if len(valid_actions) == 0: break
                
                if id_oponente == 1:
                    movimiento = oponente_algoritmo.play1()
                else:
                    movimiento = oponente_algoritmo.play2()
                
                if movimiento is not None:
                    r, c = movimiento
                    if juego.game_matrix[r, c] == 0:
                        if id_oponente == 1: 
                            juego.play1(r, c)
                        else: 
                            juego.play2(r, c)

        if juego.win_condition():
            resultado = "W" if juego.current_player == id_agente else "L"
        else:
            resultado = "D" 

        for i, move_type in enumerate(agent_moves):
            if i < 5: 
                analisis[iniciativa][f"Move_{i+1}"][move_type][resultado] += 1

    # ================= IMPRIMIR TABLAS COMPLETAS =================
    for iniciativa in ["Agent_Starts", "Opponent_Starts"]:
        texto_ini = "INICIA" if iniciativa == "Agent_Starts" else "ES SEGUNDO"
        print(f"\n🎯 Cuando el agente {texto_ini}:")
        
        datos_tabla = []
        for turno in range(1, 6): # Turnos del 1 al 5 garantizados
            clave_turno = f"Move_{turno}"
            for posicion in ["center", "corner", "edge"]:
                stats = analisis[iniciativa][clave_turno][posicion]
                w, d, l = stats["W"], stats["D"], stats["L"]
                total = w + d + l
                
                # Cálculo de porcentajes manejando el 0
                if total > 0:
                    win_rate = (w / total) * 100
                    draw_rate = (d / total) * 100
                    loss_rate = (l / total) * 100
                else:
                    win_rate = 0.0
                    draw_rate = 0.0
                    loss_rate = 0.0
                    
                datos_tabla.append([
                    f"Turno {turno}", posicion.capitalize(), total, 
                    f"{win_rate:.1f}%", f"{draw_rate:.1f}%", f"{loss_rate:.1f}%"
                ])
                    
        # Renderizamos el DataFrame sin ocultar ninguna fila
        df = pd.DataFrame(datos_tabla, columns=["Turno", "Posición", "Veces Elegida", "WinRate", "DrawRate", "LossRate"])
        print(df.to_string(index=False))
    
def graficar_comparativa_entrenamiento(historicos, etapas):
    # 3 Paneles: Recompensa, Epsilon y WinRate Modificado
    fig, axes = plt.subplots(3, 1, figsize=(15, 12), sharex=True)
    colores = plt.cm.get_cmap('tab10', len(historicos))
    
    for i, (nombre, data) in enumerate(historicos.items()):
        color = colores(i)
        rew = pd.Series(data["recompensas"])
        eps = data["epsilons"]
        
        # 1. Recompensa Promedio (Suavizada)
        axes[0].plot(rew.rolling(window=50).mean(), label=nombre, color=color, linewidth=2)
        
        # 2. Epsilon (Decaimiento)
        axes[1].plot(eps, color=color, linestyle='--', alpha=0.7)
        
        # 3. WinRate Modificado (W=1.0, D=0.5, L=0)
        # Calculamos el éxito basado en tus recompensas [3, 1, -3, -10]
        success = rew.apply(lambda r: 1.0 if r >= 3.0 else (0.5 if r >= 1.0 else 0.0))
        axes[2].plot(success.rolling(window=100).mean() * 100, color=color, linewidth=2)

    # Configuración de estética
    axes[0].set_title("🏆 Recompensa Promedio por Episodio", fontweight='bold')
    axes[1].set_title("📉 Decaimiento de Epsilon (Exploración)", fontweight='bold')
    axes[2].set_title("🎯 Efectividad de Juego % (Win + 0.5*Draw)", fontweight='bold')
    
    axes[0].legend(loc='upper left', bbox_to_anchor=(1, 1))
    
    # Marcar las Etapas (Maestro, Algoritmo, Random)
    total_ac = 0
    for etapa in etapas:
        total_ac += etapa["eps"]
        for ax in axes:
            ax.axvline(x=total_ac, color='red', linestyle=':', alpha=0.5)
            ax.grid(True, alpha=0.2)
            
    plt.tight_layout()
    plt.show()
                
def main():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"🚀 Iniciando Sistema General de Triqui en: {device}")

    # 1. DICCIONARIO DE CONFIGURACIONES PERSONALIZADAS
    configuraciones_n = {
        "DQN_Rapido": {
            "agent_class": MasterDQN,
            "hidden_layers": [64, 64], "activation": nn.ELU, "optimizer": optim.RMSprop,
            "lr": 0.001, "epsilon_decay": 0.99, "batch_size": 64
        },
        "DQN_Denso": {
            "agent_class": MasterDQN,
            "hidden_layers": [512, 256, 256], "activation": nn.LeakyReLU, "optimizer": optim.AdamW,
            "lr": 0.0003, "epsilon_decay": 0.999, "batch_size": 128
        },
        "SARSA_Explorador": {
            "agent_class": MasterSARSA, 
            "hidden_layers": [256, 256], "activation": nn.ReLU, "optimizer": optim.Adam,
            "lr": 0.005, "epsilon_decay": 0.9995, "batch_size": 256
        },
        "SARSA_Denso": {
            "agent_class": MasterSARSA, 
            "hidden_layers": [512, 256, 256], "activation": nn.LeakyReLU, "optimizer": optim.Adam,
            "lr": 0.0005, "epsilon_decay": 0.9995, "batch_size": 256
        }
    }

    # 2. INSTANCIACIÓN DINÁMICA DE AGENTES Y MOTORES
    alumnos = {}
    motores = {}
    
    env = Train(device=device)
    env.opponent = None 

    for nombre, cfg in configuraciones_n.items():
        # Crear la red neuronal personalizada
        model = cfg["agent_class"](
            input_size=9, 
            action_dim=9, 
            hidden_layers=cfg["hidden_layers"],
            activation_fn=cfg["activation"] 
        ).to(device)
        
        # Crear su optimizador específico
        opt = cfg["optimizer"](model.parameters(), lr=cfg["lr"])
        
        # Crear su estrategia de exploración
        esp = EpsilonGreedy(decay=cfg["epsilon_decay"])
        
        # Crear su Motor de aprendizaje
        motor = MotorRL(agent=model, env=env, optimizer=opt, exploration_strategy=esp, device=device)
        
        alumnos[nombre] = model
        motores[nombre] = motor

    # =================================================================
    # FASE 0: ENTRENAMIENTO DEL MAESTRO (Independiente)
    # =================================================================
    print("\n🎓 FASE 0: ENTRENANDO AL MAESTRO")
    maestro = MasterDQN(input_size=9, action_dim=9, hidden_layers=[128, 128]).to(device)
    opt_m = optim.Adam(maestro.parameters(), lr=0.0001)
    
    motor_m = MotorRL(agent=maestro, env=env, optimizer=opt_m, exploration_strategy=EpsilonGreedy(decay=0.9995), device=device)
    motor_m.train(episodes=200)

    # =================================================================
    # CURRICULUM LIGUILLA: ENTRENAMIENTO POR ETAPAS
    # =================================================================
    
    # ¡NUEVO!: FUNCIÓN ENVOLTORIO PARA EL ALGORITMO
    def bot_wrapper(juego_instancia):
        # Esta función recibe el juego actual, evalúa de quién es el turno
        # y devuelve la tupla (row, col) que triqui_train está esperando.
        alg = Algorithm(juego_instancia)
        if juego_instancia.current_player == 1:
            return alg.play1()
        else:
            return alg.play2()

    etapas = [
        {"nombre": "VS MAESTRO", "oponente": maestro, "eps": 200},
        {"nombre": "VS ALGORITMO", "oponente": bot_wrapper, "eps": 200},  # Usamos la función wrapper aquí
        {"nombre": "VS RANDOM", "oponente": None, "eps": 200}
    ]

    historicos_globales = {nombre: {"recompensas": [], "epsilons": []} for nombre in alumnos}

    for etapa in etapas:
        print(f"\n🟦 INICIANDO ETAPA: {etapa['nombre']}")
        env.opponent = etapa["oponente"]
        
        for nombre, motor in motores.items():
            print(f"🤖 Entrenando {nombre}...")
            # Entrenamos y extraemos desde el diccionario de retorno
            resultados_entrenamiento = motor.train(
                episodes=etapa["eps"], 
                log_freq= 200 
            )
            historicos_globales[nombre]["recompensas"].extend(resultados_entrenamiento["recompensas"])
            historicos_globales[nombre]["epsilons"].extend(resultados_entrenamiento["epsilons"])

    # Gráficas del entrenamiento
    print("\n📈 GENERANDO GRÁFICAS DE ENTRENAMIENTO...")
    graficar_comparativa_entrenamiento(historicos_globales, etapas)

    # =================================================================
    # FASE FINAL: CAMPEONATO Y ANÁLISIS ESTRATÉGICO
    # =================================================================
    print("\n🏆 GRAN TORNEO FINAL")
    participantes = {"Maestro": maestro, **alumnos}
    
    campeonato = Championship(agents_dict=participantes, env_instance=env, device=device)
    campeonato.run_tournament(episodes_per_matchup=400)
    print(campeonato.get_global_leaderboard())
    
    print("\n🤝 GENERANDO ANÁLISIS VISUAL DE LA LIGA...")
    campeonato.plot_heatmaps()

    # 3. Radiografía Quirúrgica (Tablas de métricas por turno fuera del entrenamiento)
    print("\n🔍 EVALUACIÓN DE ESTRATEGIAS (VS ALGORITMO)")
    for nombre, modelo in alumnos.items():
        mostrar_analisis_estrategico(modelo, nombre, episodios=1000, device=device)

if __name__ == "__main__":
    main()