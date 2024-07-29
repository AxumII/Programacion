import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

class Analizador:
    def __init__(self):
        # Definir símbolos como atributos
         self.t, self.s, self.jw , self.z= sp.symbols('t s jw z')  # Agregar jw como símbolo

        
        
   
    def ConversorH(self, H):
        # Extraer numerador y denominador
        numerador, denominador = sp.fraction(H)

        # Convertirlos en objetos polinómicos, tratando constantes como polinomios de grado 0
        numerador_poly = sp.poly(numerador, self.s) if numerador else sp.poly(0, self.s)
        denominador_poly = sp.poly(denominador, self.s) if denominador else sp.poly(1, self.s)

        # Convertirlos en arreglos
        numerador_array = [float(coef) for coef in numerador_poly.all_coeffs()]
        denominador_array = [float(coef) for coef in denominador_poly.all_coeffs()]

        return numerador_array, denominador_array
    
    def bode(self, H, filter_type):
        

        # Determinar el tipo de filtro
        poles = sp.roots(sp.denom(H), self.s)
        zeros = sp.roots(sp.numer(H), self.s)

        # Contar el número de polos y ceros
        num_poles = len(poles)
        num_zeros = len(zeros)

           
        
            
        # Definir omega_range en un ámbito accesible
        omega_range = np.logspace(-2, 6, 10000)

        # Transformar H(s) a H(jω) y calcular la magnitud de H(jω)
        H_jw = H.subs(self.s, 1j * self.jw)
        H_jw_func = sp.lambdify(self.jw, sp.Abs(H_jw), 'numpy')
        H_values = H_jw_func(omega_range)

        # Inicializar variables para resultados
        resonant_freq = None
        bandwidth = None
        Q = None
        f_c = []
        peak_mag = None
        
        
        def frequency_from_dB(magnitude_dB, frequencies):
            # Convertir la magnitud de dB a escala lineal
            magnitude_linear = 10 ** (magnitude_dB / 20.0)

            # Encontrar el índice de la frecuencia más cercana en escala lineal
            idx = np.argmin(np.abs(magnitude_linear - frequencies))

            # Devolver la frecuencia correspondiente
            return frequencies[idx]

        # Cálculos según el tipo de filtro
        if filter_type == "pasabanda":
            resonant_freq = omega_range[np.argmax(H_values)] / (2 * np.pi)
            peak_mag = np.max(H_values)
            half_max = peak_mag / np.sqrt(2)

            # Frecuencias de corte en -3 dB del pico
            idx_bandwidth = np.where(H_values >= half_max)[0]
            f_lower = omega_range[idx_bandwidth[0]] / (2 * np.pi)
            f_upper = omega_range[idx_bandwidth[-1]] / (2 * np.pi)
            bandwidth = f_upper - f_lower
            f_c = [f_lower, f_upper]

        if filter_type == "rechazabanda":
            resonant_freq = omega_range[np.argmin(H_values)] / (2 * np.pi)
            
            
            peak_mag = np.max(H_values)
            half_max = 1/ np.sqrt(2)

            # Frecuencias de corte en -3 dB del pico
            idx_bandwidth = np.where(H_values <= half_max)[0]
            f_lower = omega_range[idx_bandwidth[0]] / (2 * np.pi)
            f_upper = omega_range[idx_bandwidth[-1]] / (2 * np.pi)
            bandwidth = f_upper - f_lower
            f_c = [f_lower, f_upper]
    
    
            

            

            

        # Calcular el factor de calidad Q si es aplicable
        if filter_type in ["pasabanda", "rechazabanda"]:
            Q = bandwidth / resonant_freq if resonant_freq and bandwidth else None

        print("Tipo:", filter_type ,"\n")
        print("Resonancia:", resonant_freq ,"\n")
        print("Q:", Q ,"\n")
        print("Fc:", f_c,"\n")
        print("Ancho de Banda:", bandwidth,"\n")
        

        return filter_type, resonant_freq, bandwidth, Q, np.array(f_c)

    def graf_Bode(self, H, filter_type):
        
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
        filter_type, resonant_freq, bandwidth, Q, f_c = self.bode(H, filter_type)

        # Graficar el diagrama de Bode
        plt.figure(figsize=(12, 6))

        # Graficar la magnitud
        plt.subplot(2, 1, 1)
        plt.semilogx(w_hz, mag, color = "purple")
        plt.title('Diagrama de Bode')
        plt.ylabel('Magnitud [dB]')
        plt.grid(True)

        # Marcar frecuencia de resonancia y frecuencias de corte si están presentes
        if resonant_freq:
            plt.axvline(x=resonant_freq, color='green', linestyle='--', label=f'Resonancia: {resonant_freq:.2f} Hz')
        for fc in f_c:
            if fc is not None:  # Verificar que fc no sea None antes de intentar graficar
                plt.axvline(x=fc, color='red', linestyle='--', label=f'Corte: {fc:.2f} Hz')

        plt.legend()

        # Graficar la fase
        plt.subplot(2, 1, 2)
        plt.semilogx(w_hz, phase, color = "green")
        plt.xlabel('Frecuencia [Hz]')
        plt.ylabel('Fase [grados]')
        plt.grid(True)

        plt.show()
        
    def bilineal(self, H, T):
        # Transformación bilineal s = (2/T) * (z - 1) / (z + 1)
        H_z = H.subs(self.s, (2 / T) * (self.z - 1) / (self.z + 1))
        
        H_z_simplified = sp.simplify(H_z)
        return H_z_simplified
    
    def graf_comparacion(self, H, T_values):
        # Coeficientes de H(s)
        numerador, denominador = self.ConversorH(H)
        system = signal.TransferFunction(numerador, denominador)

        # Respuesta en frecuencia de H(s)
        w_cont, mag_cont, phase_cont = signal.bode(system, w=np.logspace(-1, 6, num=1000))
        w_hz_cont = w_cont / (2 * np.pi)

        for T in T_values:
            # Convertir H(s) a H(z)
            H_z = self.bilineal(H, T)

            # Función numérica para H(z)
            H_z_func = sp.lambdify(self.z, H_z, 'numpy')

            # Rango de frecuencias para H(z)
            w_disc = np.linspace(0, np.pi / T, 1000)
            z = np.exp(1j * w_disc * T)

            # Magnitud y fase de H(z)
            H_z_mag = np.abs(H_z_func(z))
            H_z_phase = np.unwrap(np.angle(H_z_func(z)))  #Un ajuste extra de la fase

            # Otro Ajuste extra de la fase
            phase_difference = phase_cont[0] - np.degrees(H_z_phase[0])
            H_z_phase_adjusted = np.degrees(H_z_phase) + phase_difference

            
            plt.figure(figsize=(12, 12))

            # Magnitud
            plt.subplot(2, 1, 1)
            plt.semilogx(w_hz_cont, mag_cont, label='Continua H(s)')
            plt.plot(w_disc / (2 * np.pi), 20 * np.log10(H_z_mag), label=f'Discreta H(z) - T = {T}', color = "orange")
            plt.title('Comparación de Respuestas Discreta - Continua')
            plt.ylabel('Magnitud [dB]')
            plt.grid(True)
            plt.legend()
            if np.any(20 * np.log10(H_z_mag) < -45):
                plt.ylim(bottom=-45)  # Aplicar límite si la magnitud cae por debajo de -100 dB


            # Fase
            plt.subplot(2, 1, 2)
            plt.semilogx(w_hz_cont, phase_cont, label='Continua H(s)')
            plt.plot(w_disc / (2 * np.pi), H_z_phase_adjusted, label=f'Discreta H(z) - T = {T}', color = "purple")
            plt.xlabel('Frecuencia [Hz / rad/s]')
            plt.ylabel('Fase [grados]')
            plt.grid(True)
            plt.legend()

            plt.show()
    
################################################################################################################################################################################   
    
    

