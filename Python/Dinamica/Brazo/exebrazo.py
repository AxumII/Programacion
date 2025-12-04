from analisis_brazo import Analisis as bz
import numpy as np
import scipy.stats as st # Completé la importación
size = 500
size_z_1 = 150
size_z_2 = 314
size_long = size*2
t_end_1 = 1.54
t_end_2 = 1.27


L1 = 144.96/1000 #Distancia m de Hombro a codo
L2 = 146/1000#Distancia  de codo a pinza

def agarrar():
    t = np.linspace(0,t_end_1,size)
    amp_n_deg = 0.000001

    #theta2_base = np.deg2rad(np.linspace(0, 0, size-size_z_1))

    theta1_base = np.deg2rad(np.linspace(83, 60, size-size_z_1))
    theta1_base = np.concatenate((theta1_base, np.full(int(size_z_1), theta1_base[-1], dtype=theta1_base.dtype)))
    theta2_base = np.deg2rad(np.linspace(200, 250, size))

    ruido = np.deg2rad(np.random.normal(loc=0.0, scale=amp_n_deg, size=size))
    
    theta1 = theta1_base + ruido
    theta2 = theta2_base + ruido

    modelo = bz(t, theta1, theta2, L1, L2)

def depositar():
    t = np.linspace(0,t_end_2,size)
    amp_n_deg = 0.000001
    theta1_base =  np.deg2rad(np.linspace(60, 70,  size-size_z_2))
    theta1_base = np.concatenate((theta1_base, np.full(int(size_z_2), theta1_base[-1], dtype=theta1_base.dtype)))
    theta2_base = np.deg2rad(np.linspace(250, 210, size))

    ruido = np.deg2rad(np.random.normal(loc=0.0, scale=amp_n_deg, size=size))
    
    theta1 = theta1_base + ruido
    theta2 = theta2_base + ruido

    modelo = bz(t, theta1, theta2, L1, L2)

    
def completo():
    t_long = np.linspace(0,t_end_1 + t_end_2,size_long)
    amp_n_deg = 0.001
    ruido = np.deg2rad(np.random.normal(loc=0.0, scale=amp_n_deg, size=size_long))
    
    theta1_base_init = np.deg2rad(np.linspace(83, 60, 500))
    theta2_base_init = np.deg2rad(np.linspace(200, 250, 500))

    theta1_base_end = np.deg2rad(np.linspace(60, 70, 500))
    theta2_base_end = np.deg2rad(np.linspace(250, 210, 500))
    
    theta1_base_completo = np.concatenate((theta1_base_init, theta1_base_end))
    theta2_base_completo = np.concatenate((theta2_base_init, theta2_base_end))
    
    theta1 = theta1_base_completo + ruido
    theta2 = theta2_base_completo + ruido

    modelo = bz(t_long, theta1, theta2, L1, L2)

#agarrar()
depositar()
#completo()