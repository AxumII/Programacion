import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal


class Parcial:
    def __init__(self):
        # Definir símbolos como atributos
        self.t, self.s, self.jw, self.X, self.Y = sp.symbols('t s jw X Y')

        # Definir funciones como atributos
        self.V_In = sp.Function('V_In')(self.t)
        self.V_Out = sp.Function('V_Out')(self.t)
        self.V_Node = sp.Function('V_Node')(self.t)


    def Punto1_FTransferencia(self, R1,R2,R3,C):
        # Hallar Vn Simbolicamente
        eqn = sp.Eq(C * sp.diff(self.V_Node, self.t), self.V_Out/-R3)
        Vnode_as_Vout = sp.dsolve(eqn, self.V_Node)

        Vnode_expr = Vnode_as_Vout.rhs
        print(Vnode_expr)
        #Planteamiento ecuaciones (LEER NOTA)
        """
        NOTA: PLANTEO LAS ECUACIONES SOLO PARA TENERLAS ESCRITAS; SOLO VOY A RESOLVER DESDE SYMPY LAS VARIABLES YA CONVERTIDAS A LAPLACE SOLO PARA DESPEJAR RAPIDO
        """
        I1 = (self.V_In - Vnode_expr) / R1
        I2 = Vnode_expr / R2
        IC1 = C * sp.diff(Vnode_expr - self.V_Out, self.t)
        IC2 = C * sp.diff(Vnode_expr, self.t)

        """
        # Simplificar las expresiones de las corrientes e imprimir
        I1_simplified = sp.simplify(I1)
        I2_simplified = sp.simplify(I2)
        IC1_simplified = sp.simplify(IC1)
        IC2_simplified = sp.simplify(IC2)

        print("I1", I1_simplified, "\n")
        print("I2", I2_simplified, "\n")
        print("I3", IC1_simplified, "\n")
        print("I4", IC2_simplified, "\n")"""


        #Se aplica Laplace a las funciones
        """
        Recordando propiedades de Laplace

        L[diff(f,t)] = s*L[]
        L[integ(f,t)] = F(s)/s
        """
        # x = L[V_in]
        # y = L[V_out]
        VnL = (-500)*(self.Y/self.s)
        I1L = ((self.X - VnL) / R1)
        I2L = (VnL / R2)
        IC1L = ((5e-5*self.Y) - (1e-7)*(self.Y*self.s))
        IC2L = (5e-5*self.Y)
        
        print(I1L,"\n",I2L,"\n",IC1L,"\n",IC2L,"\n")

        # Ecuación en Laplace
        eq1 = sp.Eq(I1L, I2L + IC1L + IC2L)
        Y_as_X = sp.solve(eq1, self.Y)

        # Si H es la función de transferencia
        H = Y_as_X[0] / self.X

        return H, sp.simplify(H)

    def Punto2_FTransferencia():
        pass
    
    def ConversorH(self, H):
        # Extraer numerador y denominador
        numerador, denominador = sp.fraction(H)

        # Convertirlos en arreglos
        numerador_array = [float(coef) for coef in numerador.as_poly().all_coeffs()]
        denominador_array = [float(coef) for coef in denominador.as_poly().all_coeffs()]

        return numerador_array, denominador_array
    
      
    def bode(self, H):
        # Obtener polos y ceros
        polos = sp.roots(sp.denom(H), self.s)
        ceros = sp.roots(sp.numer(H), self.s)

        # Determinar el tipo de filtro
        if len(ceros) == 0 and len(polos) > 0:
            filter_type = "pasabajas"
        elif len(polos) == 0 and len(ceros) > 0:
            filter_type = "pasaaltas"
        elif len(ceros) > 0 and len(polos) > 0:
            if all(p.is_real for p in polos) and all(z.is_real for z in ceros):
                filter_type = "rechazabanda"
            else:
                filter_type = "pasabanda"
        else:
            filter_type = "No determinable por este metodo"

        
        # Definir omega_range en un ámbito accesible
        omega_range = np.logspace(-2, 6, 10000)

        # Transformar H(s) a H(jω)
        H_jw = H.subs(self.s, 1j * self.jw)
        H_jw_func = sp.lambdify(self.jw, sp.Abs(H_jw), 'numpy')

        # Evaluar en un rango de frecuencias
        H_values = H_jw_func(omega_range)

        # Inicializar variables para resultados
        resonant_freq = None
        bandwidth = None
        Q = None
        f_c = []

        # Cálculos según el tipo de filtro
        if filter_type == "pasabanda" or filter_type == "rechazabanda":
            resonant_freq = omega_range[np.argmax(H_values)] / (2 * np.pi)
            half_max = np.max(H_values) / np.sqrt(2)

            # Encontrar frecuencias de corte
            idx_bandwidth = np.where(H_values >= half_max)[0]
            if len(idx_bandwidth) > 1:
                f_lower = omega_range[idx_bandwidth[0]] / (2 * np.pi)
                f_upper = omega_range[idx_bandwidth[-1]] / (2 * np.pi)
                bandwidth = f_upper - f_lower

                if resonant_freq is not None and bandwidth is not None:
                    Q = resonant_freq / bandwidth
                    print(f"Factor de Calidad (Q): {Q}")

        elif filter_type in ["pasaaltas", "pasabajas"]:
            half_max = np.max(H_values) / np.sqrt(2)

            # Encontrar frecuencia de corte
            f_c = omega_range[np.abs(H_values - half_max).argmin()] / (2 * np.pi)
            bandwidth = f_c if filter_type == "pasabajas" else "infinito"

        if filter_type == "pasabanda" or filter_type == "rechazabanda":
            f_c = [f_lower, f_upper]
            
        elif filter_type == "pasaaltas":
            f_c = [f_cutoff]
        elif filter_type == "pasabajas":
            f_c = [f_cutoff]  

        return filter_type, resonant_freq, bandwidth, Q, np.array(f_c)

    def graf_Bode(self, H):
        # Usar el método ConversorH para obtener los coeficientes
        numerador, denominador = self.ConversorH(H)

        # Crear un sistema lineal en tiempo continuo con los coeficientes
        system = signal.TransferFunction(numerador, denominador)

        # Definir el rango de frecuencias
        w = np.logspace(-1, 6, num=1000)

        # Calcular la respuesta en frecuencia
        w, mag, phase = signal.bode(system, w=w)

        # Convertir frecuencias de rad/s a Hz
        w_hz = w / (2 * np.pi)

        # Calcular características del filtro usando el método bode
        filter_type, resonant_freq, bandwidth, Q, f_c = self.bode(H)

        # Graficar el diagrama de Bode
        plt.figure(figsize=(12, 6))

        # Graficar la magnitud
        plt.subplot(2, 1, 1)
        plt.semilogx(w_hz, mag)
        plt.title('Diagrama de Bode')
        plt.ylabel('Magnitud [dB]')
        plt.grid(True)

        # Marcar frecuencia de resonancia y frecuencias de corte si están presentes
        if resonant_freq:
            plt.axvline(x=resonant_freq, color='green', linestyle='--', label=f'Resonancia: {resonant_freq:.2f} Hz')
        for fc in f_c:
            plt.axvline(x=fc, color='red', linestyle='--', label=f'Corte: {fc:.2f} Hz')

        plt.legend()

        # Graficar la fase
        plt.subplot(2, 1, 2)
        plt.semilogx(w_hz, phase)
        plt.xlabel('Frecuencia [Hz]')
        plt.ylabel('Fase [grados]')
        plt.grid(True)

        plt.show()

    def bilineal(self, H, fs):
        # Transformada Bilineal
        s = self.s
        z = sp.symbols('z')
        H_z = H.subs(s, 2 * fs * (z - 1) / (z + 1))

        # Simplificar H(z)
        H_z_simplified = sp.simplify(H_z)

        # Extraer numerador y denominador de H(z)
        numerador_z, denominador_z = self.ConversorH(H_z_simplified)

        # Definir rango de frecuencias desde mHz hasta MHz
        w = np.logspace(-3, 6, num=1000)  # Desde mHz hasta MHz

        # Calcular la respuesta en frecuencia para H(z)
        w, h = signal.freqz(numerador_z, denominador_z, worN=w)

        # Calcular la respuesta en frecuencia para H(s)
        numerador, denominador = self.ConversorH(H)
        system_s = signal.TransferFunction(numerador, denominador)
        w_s, mag_s, phase_s = signal.bode(system_s, w=w)

        # Graficar las respuestas en frecuencia
        plt.figure(figsize=(12, 6))
        plt.semilogx(w/(2*np.pi), 20 * np.log10(abs(h)), label='Discreta (H(z))')
        plt.semilogx(w/(2*np.pi), mag_s, label='Continua (H(s))', linestyle='--')
        plt.title('Comparación de Funciones de Transferencia')
        plt.xlabel('Frecuencia [Hz]')
        plt.ylabel('Magnitud [dB]')
        plt.grid(True)
        plt.legend()
        plt.show()

        return H_z_simplified



    
    
        
    
    
# Uso de la clase
parcial = Parcial()
#Constantes
R1,R2,R3, C = 10000 , 100, 20000, 0.1e-6

H_num, H_sym = parcial.Punto1_FTransferencia(R1, R2, R3, C)
print(f"Función de transferencia H(s): {H_sym}")

#parcial.graf_Bode(H_sym)

#filter_type, resonant_freq, bandwidth, Q, f_c = parcial.bode(H_sym)

parcial.bilineal(H_sym, 0.01)

