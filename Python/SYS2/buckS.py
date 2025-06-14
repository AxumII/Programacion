import numpy as np
import sympy as sp
import pandas as pd
from scipy.signal import ss2tf,tf2zpk
import matplotlib.pyplot as plt


class Analisys:
    def __init__(self, C_val, L_val, R_val=[10, 500], u=12):
        self.C_val = np.array(C_val)
        self.L_val = np.array(L_val)
        self.R_val = np.array(R_val)
        self.u = u

    def gen_matrix(self,C,L,R):
        A_m = np.array([[0, -1 / L],
                      [1 / C, -1 / (R * C)]])
        C_m = np.array([[0, 1]])
        D_m = np.array([[0]])
        B_m = np.array([[1 / L], [0]])
        return A_m,B_m,C_m,D_m

    def tf_num(self,A,B,C,D):
        return ss2tf(A,B,C,D)

    def zpk_num(self,A,B,C,D):
        num,den = self.tf_num(A,B,C,D)
        return tf2zpk(num,den)
    
    def spect(self,A):
        return np.linalg.eigvals(A)
    
    def ts(self,polos):
        polos = np.array(polos)
        stable = [p for p in polos if np.real(p) < 0]
        p_dominante = min(stable, key=lambda x: abs(np.real(x)))
        return 4/ abs(np.real(p_dominante))
            
    
    def poles_graf_real_vs_C(self):
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = ['blue', 'orange', 'green', 'purple', 'brown']
        color_idx = 0

        for R_it in self.R_val:
            for L_it in self.L_val:
                C_data = []
                real_parts_1 = []
                real_parts_2 = []
                for C_it in self.C_val:
                    A_m, B_m, C_m, D_m = self.gen_matrix(C=C_it, L=L_it, R=R_it)
                    polos = self.spect(A_m)
                    C_data.append(C_it * 1e6)  # convertir a µF
                    real_parts_1.append(np.real(polos[0]))
                    real_parts_2.append(np.real(polos[1]))

                label_prefix = f'R={R_it}Ω, L={L_it*1e6:.0f}µH'
                ax.plot(C_data, real_parts_1, label=f'{label_prefix} (p1)', color=colors[color_idx % len(colors)])
                ax.plot(C_data, real_parts_2, linestyle='--', label=f'{label_prefix} (p2)', color=colors[color_idx % len(colors)])
                color_idx += 1

        ax.set_title('Parte real de los polos vs Capacitancia')
        ax.set_xlabel('Capacitancia (µF)')
        ax.set_ylabel('Parte real de los polos')
        ax.axhline(0, color='gray', linestyle='--')
        ax.grid(True)
        ax.legend()
        plt.tight_layout()
        plt.show()

    
    def ts_table(self):
        ts_tabla = []
        for R_it in self.R_val:
            for L_it in self.L_val:
                for C_it in self.C_val:
                    A_m, B_m, C_m, D_m = self.gen_matrix(C=C_it, L=L_it, R=R_it)
                    polos = self.spect(A_m)
                    ts_val = self.ts(polos=polos)
                    ts_tabla.append({
                        "R (Ω)": R_it,
                        "L (µH)": L_it * 1e6,
                        "C (µF)": C_it * 1e6,
                        "t_s (s)": ts_val
                    })
        return pd.DataFrame(ts_tabla)



    def espectro_table(self):
        espectro_tabla = []
        for R_it in self.R_val:
            for L_it in self.L_val:
                for C_it in self.C_val:
                    A_m, B_m, C_m, D_m = self.gen_matrix(C=C_it, L=L_it, R=R_it)
                    polos = self.spect(A_m)
                    espectro_tabla.append({
                        "R (Ω)": R_it,
                        "L (µH)": L_it * 1e6,
                        "C (µF)": C_it * 1e6,
                        "Polo 1": polos[0],
                        "Parte real 1": np.real(polos[0]),
                        "Polo 2": polos[1],
                        "Parte real 2": np.real(polos[1])
                    })
        return pd.DataFrame(espectro_tabla)

    def Gs(self):
    # Definir símbolos
        s, C, L, R = sp.symbols('s C L R', positive=True, real=True)

        # Matrices simbólicas
        A = sp.Matrix([[0, -1/L],
                    [1/C, -1/(R*C)]])
        B = sp.Matrix([[1/L],
                    [0]])
        C_ = sp.Matrix([[0, 1]])
        D = sp.Matrix([[0]])

        # Calcular G(s)
        I = sp.eye(2)
        Gs_expr = C_ * (s * I - A).inv() * B + D


        char_poly = (s * I - A).det()
        polos = sp.solve(char_poly, s)

        return sp.simplify(Gs_expr[0]), polos



        

# Ejecutamos con valores de ejemplo
C_vals = [10e-6, 33e-6, 330e-6]
L_vals = [2e-6, 100e-6, 470e-6]
R_vals = [10, 500]

analizador = Analisys(C_vals, L_vals, R_vals)
#analizador.poles_graf_real_vs_C()
#print(analizador.ts_table())
#print(analizador.espectro_table())
sp.pprint(analizador.Gs())


    #polos reales negativos
    #espectro
    #tiempo de asentamiento al 2%
