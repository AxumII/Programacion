import numpy as np

from FTP2 import F_Transferencia as F_T 
from analisisP2 import Analizador as A_z


ft = F_T()
az = A_z()

def P1():
    R1_val, R2_val, R3_val, C_val = 20000, 100, 10000, 0.1e-6

    H_num, H_sym = ft.FTP1(R1_val, R2_val, R3_val, C_val)
    
    print('\n')
    print(f"Función de transferencia H(s): {H_sym}") #Da la funcion de transferencia simbolica
    print(f"Función de transferencia H(s) reemplazado: {H_num}", "\n") #Da la funcion de trasnferencia numerica
    
    
    C_A1 = ft.C_Amort(H_num)
    print("Coeficiente de Amortiguamiento (ζ) P1: ", C_A1, "\n") #calcula el coeficiente
    
    #az.graf_Bode(H_num, "pasabanda") #Grafica el bode y extrae los valores necesarios
    
    #T_values = [1e-4, 5e-4, 1e-5, 5e-5]#Valores de prueba
    #az.graf_comparacion(H_num, T_values)#graficas de comparacion
    print("Transformada Bilineal 1: ", az.bilineal(H_num, 1e-5), "\n")
    
    
    w_val = 7000 * 2 * np.pi #convertido a Radianes
    
         
    solveP1 = ft.Design1(w_val, C_val, R1_val, R2_val, R3_val) #soluciona para que tenga la resonancia y el coef requerido
    print(" C: ", solveP1, "\n")





def P2():
    R1_val, R2_val, R3_val,R4_val, C_val = 5100 , 5100, 1000, 1080 , 0.1e-6
    
    
    H_num2, H_sym2 =ft.FTP2(R1_val, R2_val, R3_val,R4_val, C_val)

    print('\n')
    print(f"Función de transferencia H(s): {H_sym2}")
    print(f"Función de transferencia H(s) reemplazado: {H_num2}","\n")
    
    C_A2 = ft.C_Amort(H_num2)
    print("Coeficiente de Amortiguamiento (ζ) P2: ",C_A2,"\n")
        
    #az.graf_Bode(H_num2, "rechazabanda") #Grafica el bode y extrae los valores necesarios
    
    #T_values = [1e-4, 5e-4, 1e-5, 5e-5]#Valores de prueba
    #az.graf_comparacion(H_num2, T_values)#graficas de comparacion
    #print("Transformada Bilineal 2: ", az.bilineal(H_num2, 1e-5), "\n")
    
    
    w_val = 10000*2*np.pi
    


    solveP2 = ft.Design2(w_val ,R1_val, R2_val, R3_val,R4_val)
    print(" C: ",  solveP2, "\n")
    
    
    
    

P1()
P2()