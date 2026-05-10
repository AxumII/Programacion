import numpy as np
import time
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt 
import pandas as pd

from triqui_train import Train
from triqui_championship import Championship
from master_RL import MasterDQN, MasterSARSA, MotorRL, EpsilonGreedy
from triqui_algorithm import Algorithm 

def main():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"🚀 Iniciando Sistema General de Triqui en: {device}")

    # 1. INSTANCIAS GLOBALES
    env = Train(device=device, rewards_config=[3.0, 1.0, -3.0, -10.0])
    lr = 0.0001
    eps_decay = 0.9995

    # =================================================================
    # FASE 0: ENTRENAMIENTO DEL MAESTRO
    # =================================================================
    print("\n" + "🎓"*5 + " FASE 0: ENTRENANDO AL MAESTRO " + "🎓"*5)
    maestro = MasterDQN(input_size=9, action_dim=9, hidden_layers=[128, 128]).to(device)
    opt_m = optim.Adam(maestro.parameters(), lr=lr)
    motor_m = MotorRL(agent=maestro, env=env, optimizer=opt_m, 
                      exploration_strategy=EpsilonGreedy(1.0, 0.01, eps_decay), device=device)
    
    env.opponent = None # Entrena contra random
    motor_m.train(episodes=200, log_freq=200)
    maestro.eval() # Lo fijamos como experto

    # =================================================================
    # PREPARACIÓN DE LOS 3 ALUMNOS
    # =================================================================
    # Alumno 1: DQN con capas estándar
    dqn_1 = MasterDQN(input_size=9, action_dim=9, hidden_layers=[64, 64]).to(device)
    # Alumno 2: DQN con arquitectura diferente (más profunda)
    dqn_2 = MasterDQN(input_size=9, action_dim=9, hidden_layers=[128, 64]).to(device)
    # Alumno 3: Agente SARSA
    sarsa_bot = MasterSARSA(input_size=9, action_dim=9, hidden_layers=[64, 64]).to(device)

    # Creamos sus motores de entrenamiento
    # MotorRL(dqn_1, env, opt, exploracion, device)

    motores = {
        "DQN_Alumno_1": MotorRL(dqn_1, env, optim.Adam(dqn_1.parameters(), lr=lr), 
                                device, EpsilonGreedy(1.0, 0.01, eps_decay)),
        "DQN_Alumno_2": MotorRL(dqn_2, env, optim.Adam(dqn_2.parameters(), lr=lr), 
                                device, EpsilonGreedy(1.0, 0.01, eps_decay)),
        "SARSA_Alumno": MotorRL(sarsa_bot, env, optim.Adam(sarsa_bot.parameters(), lr=lr), 
                                device, EpsilonGreedy(1.0, 0.01, eps_decay))
    }
    # Diccionario organizado para guardar la evolución completa
    historicos = {
        nombre: {
            "recompensas": [],
            "epsilons": [],
            "resultados": []
        } for nombre in motores.keys()
    }

    # Definición de oponentes para las etapas
    def bot(juego):
        alg = Algorithm(juego)
        if juego.turns_played % 2 == 0:
            move = alg.play1()
        else:
            move = alg.play2()            
        if move: 
            return move[0], move[1]        
        # FALLBACK FINAL OBLIGATORIO:
        return alg.randommovement()


    etapas = [
        {"nombre": "VS MAESTRO", "oponente": maestro, "eps": 200},
        {"nombre": "VS ALGORITMO", "oponente": bot, "eps": 200},
        {"nombre": "VS RANDOM", "oponente": None, "eps": 200}
    ]

    # =================================================================
    # EJECUCIÓN DEL CURRÍCULUM SECUENCIAL
    # =================================================================
    for etapa in etapas:
        print(f"\n" + "🟦"*5 + f" INICIANDO ETAPA: {etapa['nombre']} " + "🟦"*5)
        env.opponent = etapa["oponente"]
        
        for nombre, motor in motores.items():
            print(f"🤖 Entrenando {nombre}...")
            # El motor ahora devuelve un diccionario con las 3 listas
            metricas_etapa = motor.train(episodes=etapa["eps"], log_freq=200)
            
            # Acumulamos cada métrica usando extend
            historicos[nombre]["recompensas"].extend(metricas_etapa["recompensas"])
            historicos[nombre]["epsilons"].extend(metricas_etapa["epsilons"])
            historicos[nombre]["resultados"].extend(metricas_etapa["resultados"])
    # =================================================================
    # BLOQUE DE GRÁFICAS: DASHBOARD DE ENTRENAMIENTO
    # =================================================================
    print("\n📊 Generando Dashboard de Entrenamiento...")
    fig, axs = plt.subplots(3, 1, figsize=(12, 15))
    
    for nombre, h in historicos.items():
        # 1. Gráfica de Recompensas (Suavizada)
        rew_series = pd.Series(h["recompensas"])
        axs[0].plot(rew_series.rolling(window=100).mean(), label=nombre)
        
        # 2. Gráfica de Epsilon (Decaimiento)
        axs[1].plot(h["epsilons"], label=f"Epsilon {nombre}")
        
        # 3. Tasa de éxito evolutiva (WinRate + DrawRate)
        res_series = pd.Series(h["resultados"])
        # Calculamos efectividad: (Victoria=1, Empate=0.5, Derrota/Ilegal=0)
        puntos = res_series.map({"W": 1.0, "D": 0.5, "L": 0.0})
        efectividad = puntos.rolling(window=200).mean() * 100
        axs[2].plot(efectividad, label=f"Efectividad {nombre}")

    # Estética de las gráficas
    titulos = ["Evolución de Recompensas", "Decaimiento de Epsilon", "% Efectividad Evolutiva (Wins + 0.5*Draws)"]
    for i, ax in enumerate(axs):
        ax.set_title(titulos[i], fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        # Dibujar líneas de etapas
        total_acumulado = 0
        for etapa in etapas:
            total_acumulado += etapa["eps"]
            ax.axvline(x=total_acumulado, color='r', linestyle='--', alpha=0.3)

    plt.tight_layout()
    plt.show()
# =================================================================
    # FASE FINAL: CAMPEONATO
    # =================================================================
    print("\n" + "🏆"*5 + " GRAN TORNEO FINAL " + "🏆"*5)
    participantes = {
        "Maestro": maestro,
        "DQN_1": dqn_1,
        "DQN_2": dqn_2,
        "SARSA": sarsa_bot
    }

    campeonato = Championship(agents_dict=participantes, env_instance=env, device=device)
    campeonato.run_tournament(episodes_per_matchup=400)

    # 1. Tabla Global (Puntos, Wins, Draws, Losses)
    print("\n⭐ TABLA DE POSICIONES GLOBAL")
    print(campeonato.get_global_leaderboard())

    # 2. Tablas por Iniciativa (WinRate, DrawRate y el nuevo LossRate)
    df_ini, df_seg = campeonato.get_initiative_leaderboards()
    print("\n📈 RENDIMIENTO POR INICIATIVA (Desglose %)")
    print("Iniciando:\n", df_ini)
    print("\nSiendo Segundo:\n", df_seg)

    # 3. Única llamada para las Matrices Visuales
    # Esta función ya genera los dos Heatmaps (Iniciando/Segundo) con anotaciones W/D/L
    print("\n🤝 GENERANDO ANÁLISIS VISUAL DE ENFRENTAMIENTOS...")
    campeonato.plot_heatmaps()

if __name__ == "__main__":
    main()