import numpy as np
import matplotlib.pyplot as plt
from desbalance_rotor import Desbalance as Db
from vibracion import MAFS as MAFS


################################################################################################################

class General:
    def __init__(self):
        g = -9.81
        m_tornillo = 8/1000 #Gramos
        self.masa_t = (3*(36)) + (0.18) + ((15) + (15)) +((6)* (m_tornillo))  #3discos + Eje + 2 rodamientos + n Masas  EN GRAMOS
        self.W_peso_t = (self.masa_t*g)/1000
        self.k_h = 1500
        self.k_v = 1500
        self.w_t  = (1500)*(np.pi/30) #rpm a rad/s
        self.alpha = 0
        self.r_ctr_d = 0.035
        self.L = 0.31
        self.L_n = [0.0739, 0.1546, 0.235]
        self.L_ctr = 0.31/2
        self.D1_ex=[0, 1, 1, 1]
        self.D1_m=[0, m_tornillo, m_tornillo, m_tornillo]
        self.D2_ex=[0, 1, 0, 0]
        self.D2_m=[0, m_tornillo, 0, 0]
        #self.D3_ex=[1, 0, 1, 0]
        #self.D3_m=[m_tornillo, 0, m_tornillo, 0]
        self.D3_ex=[0, 0, 0, 0]
        self.D3_m=[0, 0, 0, 0]

    def info_gen_db(self, theta_in = 0):
        
        rotor = Db(W_peso = self.W_peso_t, 
                                   
                        k_h=self.k_h, 
                        k_v=self.k_v ,
                        w_t=self.w_t, 
                        alpha= self.alpha, 
                        r_ctr_d = self.r_ctr_d, 
                        L_n=self.L_n, 
                        L= self.L,
                        L_ctr= self.L_ctr, 
                        D1_ex= self.D1_ex, D1_m=self.D1_m,
                        D2_ex= self.D2_ex, D2_m=self.D2_m, 
                        D3_ex= self.D3_ex, D3_m=self.D3_m,
                        theta_init= theta_in)
        print("\n--- Masa total---")
        print(f"Masa total (gramos): {self.masa_t}")

        InA, InB = rotor.Inercia()
        Ixz_A, Iyz_A = InA
        Ixz_B, Iyz_B = InB        
        print("\n--- Inercia ---")
        print(f"Inercia A -> Ixz: {Ixz_A:.6e}, Iyz: {Iyz_A:.6e}")
        print(f"Inercia B -> Ixz: {Ixz_B:.6e}, Iyz: {Iyz_B:.6e}")

        [Ax_D, Ay_D], [Bx_D, By_D] = rotor.solve_reacciones_din()
        print("\n--- Reacciones Dinámicas (N) ---")
        print(f"Ax_D: {Ax_D}, Ay_D: {Ay_D}")
        print(f"Bx_D: {Bx_D}, By_D: {By_D}")

        Ay_E, By_E = rotor.solver_reacciones_est()
        print("\n--- Reacciones Estáticas (N) ---")
        print(f"Ay_E: {Ay_E}, By_E: {By_E}")

        [X_a, Y_a], [X_b, Y_b] = rotor.distancias_desbalance()
        X_a, Y_a = X_a * 1000, Y_a * 1000
        X_b, Y_b = X_b * 1000, Y_b * 1000
        print("\n--- Distancias de Desbalance (mm) ---")
        print(f"X_a: {X_a}, Y_a: {Y_a}")
        print(f"X_b: {X_b}, Y_b: {Y_b}") 

        print("Elongacion del resorte dado un K y una masa de 200g", rotor.cal_k())     

    def graf_db_tot(self, n=180):
        theta = np.linspace(0, 361 ,n ) + 33.5
        #Vectores fuerzas
        Ax_D_Val = np.array([])
        Ay_D_Val = np.array([])
        Bx_D_Val = np.array([])
        By_D_Val = np.array([])
        Ay_E_Val = np.array([])
        By_E_Val = np.array([])
        #Vectores desplazamientos
        X_a_Val = np.array([])
        Y_a_Val = np.array([])
        X_b_Val = np.array([])
        Y_b_Val = np.array([])

        for theta_i in theta:
            rotor = Db(W_peso = self.W_peso_t,               
                        k_h=self.k_h, 
                        k_v=self.k_v ,
                        w_t=self.w_t, 
                        alpha= self.alpha, 
                        r_ctr_d = self.r_ctr_d, 
                        L_n=self.L_n, 
                        L= self.L,
                        L_ctr= self.L_ctr, 
                        D1_ex= self.D1_ex, D1_m=self.D1_m,
                        D2_ex= self.D2_ex, D2_m=self.D2_m, 
                        D3_ex= self.D3_ex, D3_m=self.D3_m,
                        theta_init= theta_i)

            [Ax_D, Ay_D], [Bx_D, By_D]  = rotor.solve_reacciones_din()
            Ay_E, By_E = rotor.solver_reacciones_est()
            [X_a, Y_a], [X_b, Y_b] = rotor.distancias_desbalance()
            
            Ax_D_Val = np.append(Ax_D_Val, Ax_D)
            Ay_D_Val = np.append(Ay_D_Val, Ay_D)
            Bx_D_Val = np.append(Bx_D_Val, Bx_D)
            By_D_Val = np.append(By_D_Val, By_D)
            Ay_E_Val = np.append(Ay_E_Val, Ay_E)
            By_E_Val = np.append(By_E_Val, By_E)

            X_a_Val = np.append(X_a_Val, X_a)
            Y_a_Val = np.append(Y_a_Val, Y_a)
            X_b_Val = np.append(X_b_Val, X_b)
            Y_b_Val = np.append(Y_b_Val, Y_b)

        #Conversion a mm de desplazamientos
        X_a_Val *=  1000
        Y_a_Val *=  1000
        X_b_Val *=  1000
        Y_b_Val *=  1000

        #Calculos para graficos
        min_Ax, max_Ax = np.min(Ax_D_Val), np.max(Ax_D_Val)
        min_Ay, max_Ay = np.min(Ay_D_Val + Ay_E_Val), np.max(Ay_D_Val + Ay_E_Val)
        min_Bx, max_Bx = np.min(Bx_D_Val), np.max(Bx_D_Val)
        min_By, max_By = np.min(By_D_Val + By_E_Val), np.max(By_D_Val + By_E_Val)

        # Graficos
        fig, axs = plt.subplots(2, 2, figsize=(12, 10))

        # Definir los centros de las elipses
        Cx_A, Cy_A = 0, Ay_E_Val[0] 
        Cx_B, Cy_B = 0, By_E_Val[0]

        # Cálculo del ángulo del punto inicial respecto a su centro
        angulo_A = np.degrees(np.arctan2((Ay_D_Val[0] + Ay_E_Val[0]) - Cy_A, Ax_D_Val[0] - Cx_A))
        angulo_B = np.degrees(np.arctan2((By_D_Val[0] + By_E_Val[0]) - Cy_B, Bx_D_Val[0] - Cx_B))

        # Plot 1: Fuerzas dinámicas en A
        axs[0, 0].plot(Ax_D_Val, Ay_D_Val + Ay_E_Val, label="Fuerzas totales en A", linestyle="-", color="g")
        axs[0, 0].scatter(Ax_D_Val[0], Ay_D_Val[0] + Ay_E_Val[0], color='black',
                        label=f'Punto inicial ({Ax_D_Val[0]:.4f}, {Ay_D_Val[0] + Ay_E_Val[0]:.3f}), θ={angulo_A:.2f}°')
        axs[0, 0].scatter(max_Ax, Ay_E_Val[0], color='black', label=f'Punto Máximo ({max_Ax:.4f}, {Ay_E_Val[0]:.3f})')
        axs[0, 0].scatter(0, max_Ay, color='black', label=f'Punto Máximo (0, {max_Ay:.3f})')
        axs[0, 0].scatter(min_Ax, Ay_E_Val[0], color='black', label=f'Punto Mínimo ({min_Ax:.4f}, {Ay_E_Val[0]:.3f})')
        axs[0, 0].scatter(0, min_Ay, color='black', label=f'Punto Mínimo (0, {min_Ay:.3f})')
        axs[0, 0].scatter(0, Ay_E_Val[0], color='black', label=f'Centro (0, {Ay_E_Val[0]:.3f})')
        axs[0, 0].set_xlabel("Ax (Newtons)")
        axs[0, 0].set_ylabel("Ay (Newtons)")
        axs[0, 0].set_title("Gráfico de Ax vs Ay")
        axs[0, 0].legend()
        axs[0, 0].grid()
        #axs[0, 0].set_xlim([-0.1, 0.1])
        

        # Plot 2: Fuerzas dinámicas en B
        axs[0, 1].plot(Bx_D_Val, By_D_Val + By_E_Val, label="Fuerzas Totales en B", linestyle="-", color="r")
        axs[0, 1].scatter(Bx_D_Val[0], By_D_Val[0] + By_E_Val[0], color='black',
                        label=f'Punto inicial ({Bx_D_Val[0]:.4f}, {By_D_Val[0] + By_E_Val[0]:.3f}), θ={angulo_B:.2f}°')
        axs[0, 1].scatter(max_Bx, By_E_Val[0], color='black', label=f'Punto Máximo ({max_Bx:.4f}, {By_E_Val[0]:.3f})')
        axs[0, 1].scatter(0, max_By, color='black', label=f'Punto Máximo (0, {max_By:.3f})')
        axs[0, 1].scatter(min_Bx, By_E_Val[0], color='black', label=f'Punto Mínimo ({min_Bx:.4f}, {By_E_Val[0]:.3f})')
        axs[0, 1].scatter(0, min_By, color='black', label=f'Punto Mínimo (0, {min_By:.3f})')
        axs[0, 1].scatter(0, By_E_Val[0], color='black', label=f'Centro (0, {By_E_Val[0]:.3f})')
        axs[0, 1].set_xlabel("Bx (Newtons)")
        axs[0, 1].set_ylabel("By (Newtons)")
        axs[0, 1].set_title("Gráfico de Bx vs By")
        axs[0, 1].legend()
        axs[0, 1].grid()


        

        
        # Plot 3: Desbalances en A
        Cy_Xa = (max(Y_a_Val) + min(Y_a_Val))/2
        axs[1, 0].plot(X_a_Val, Y_a_Val, label="Desbalance en A", linestyle="-", color="g")
        axs[1, 0].scatter(max(X_a_Val), Cy_Xa, color='black', label=f'Punto Máximo ({max(X_a_Val):.4f}, {max(Y_a_Val):.3f})')
        axs[1, 0].scatter(0, max(Y_a_Val), color='black', label=f'Punto Máximo (0, {max(Y_a_Val):.3f})')
        axs[1, 0].scatter(min(X_a_Val), Cy_Xa, color='black', label=f'Punto Mínimo ({min(X_a_Val):.4f}, {min(Y_a_Val):.3f})')
        axs[1, 0].scatter(0, min(Y_a_Val), color='black', label=f'Punto Mínimo (0, {min(Y_a_Val):.3f})')
        axs[1, 0].set_xlabel("X_a (mm)")
        axs[1, 0].set_ylabel("Y_a (mm)")
        axs[1, 0].set_title("Gráfico de Desbalance en A")
        axs[1, 0].legend()
        axs[1, 0].grid()
        
        # Plot 4: Desbalances en B
        Cy_Xb = (max(Y_b_Val) + min(Y_b_Val))/2
        axs[1, 1].plot(X_b_Val, Y_b_Val, label="Desbalance en B", linestyle="-", color="r")
        axs[1, 1].scatter(max(X_b_Val), Cy_Xb, color='black', label=f'Punto Máximo ({max(X_b_Val):.4f}, {max(Y_b_Val):.3f})')
        axs[1, 1].scatter(0, max(Y_b_Val), color='black', label=f'Punto Máximo (0, {max(Y_b_Val):.3f})')
        axs[1, 1].scatter(min(X_b_Val), Cy_Xb, color='black', label=f'Punto Mínimo ({min(X_b_Val):.4f}, {min(Y_b_Val):.3f})')
        axs[1, 1].scatter(0, min(Y_b_Val), color='black', label=f'Punto Mínimo (0, {min(Y_b_Val):.3f})')
        axs[1, 1].set_xlabel("X_b (mm)")
        axs[1, 1].set_ylabel("Y_b (mm)")
        axs[1, 1].set_title("Gráfico de Desbalance en B")
        axs[1, 1].legend()
        axs[1, 1].grid()
        

        # Ajustar diseño
        plt.tight_layout()
        plt.show()

    def maf(self):
        theta_principal_x = 33.5
        rotor = Db(W_peso = self.W_peso_t,               
                        k_h=self.k_h, 
                        k_v=self.k_v ,
                        w_t=self.w_t, 
                        alpha= self.alpha, 
                        r_ctr_d = self.r_ctr_d, 
                        L_n=self.L_n, 
                        L= self.L,
                        L_ctr= self.L_ctr, 
                        D1_ex= self.D1_ex, D1_m=self.D1_m,
                        D2_ex= self.D2_ex, D2_m=self.D2_m, 
                        D3_ex= self.D3_ex, D3_m=self.D3_m,
                        theta_init= theta_principal_x )
        

        [Ax_D, Ay_D], [Bx_D, By_D] = rotor.solve_reacciones_din()
        Ay_E, By_E = rotor.solver_reacciones_est()
        [X_a, Y_a], [X_b, Y_b] = rotor.distancias_desbalance()
        X_a, Y_a = X_a * 1000, Y_a * 1000
        X_b, Y_b = X_b * 1000, Y_b * 1000

        Pa_dx = 0.7
        Pa_dy = 0.7
        Pb_dx = 0.4
        Pb_dy = 0.4
        

        an_mafs = MAFS(m_s = self.masa_t, k_h= self.k_h, k_v= self.k_v, Pa_dx = Pa_dx, Pa_dy = Pa_dy , Pb_dx= Pb_dx , Pb_dy= Pb_dy ,w_f= self.w_t)
        an_mafs.reson_x()
        X_a_V, X_b_V = an_mafs.amplitud()
        X_a_V *= 1000
        X_b_V *= 1000
        print("La amplitud maxima en mm de  X en A es de ",X_a_V)
        print("La amplitud maxima en mm de  X en B es de ",X_b_V)

        print("\n--- Distancias de Desbalance (mm) ---")
        print(f"X_a: {X_a}, Y_a: {Y_a}")
        print(f"X_b: {X_b}, Y_b: {Y_b}")  


        

        

Exe = General()
Exe.graf_db_tot()
Exe.info_gen_db(theta_in= 0)
Exe.maf()
