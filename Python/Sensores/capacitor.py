import numpy as np

class Capacitor:
    def __init__(self, d_s=10e-3, A=None, e_d=None):
        self.d_s = float(d_s)
        self.A = np.array(A) if A is not None else np.array([1.0])  # área por defecto
        self.e_d = np.array(e_d) if e_d is not None else np.array([1.0])  # permitividad relativa por defecto

        # Constante
        self.e_0 = 8.854e-12  # permitividad del vacío [F/m]

        # Capacitancia
        self.c = self.cap()

    def cap(self):
        c = 0
        for i in range(self.e_d.size):
            c += (self.A[i] * self.e_0 * self.e_d[i]) / self.d_s
        return c
    
    def t_5tao(self, r):
        return 5 * r * self.c
    
    def f_min(self, r):
        t5 = self.t_5tao(r)
        return 1 / t5  

#---------------------------------------------------------------------------------------------------------------
irregular = lambda h_right, h_left, w_up, w_down: (h_right*w_up)/2 + (h_left*w_down)/2
rectangle = lambda h, b: h * b
complement = lambda A_t, A_m: A_t - A_m


# Ejemplo de uso
R = 1e5  #Ω
d_s = 1.5/1000 #mm


h_right_cooper = 41.2/1000
h_left_cooper = 39.5/1000
w_up_cooper = 99.1/1000
w_down_cooper = 99.1/1000
A_total = irregular(h_right=h_right_cooper,h_left=h_left_cooper,w_up=w_up_cooper,w_down=w_down_cooper)

h_pla = 90/1000
b_pla = 35/1000
h_in = 30/1000
b_in = 17.5/1000
A_pla = rectangle(h=h_pla, b=b_pla) -4*(rectangle(h=h_in,b=b_in))

A_air = complement(A_t=A_total,A_m=A_pla)

e_a = 1.00058986
e_pla = 2.88    

areas = [A_air, A_pla]
e_dielectricos = [e_a, e_pla]
print("Materiales y parámetros:")
for i, (A, e) in enumerate(zip(areas, e_dielectricos), start=1):
    print(f"  - Material {i}: Área = {A:.3e} m² | εr = {e}")

c1 = Capacitor(d_s= d_s, A= areas, e_d= e_dielectricos)  
print(c1.c)                         # valor en Faradios
print(f"{c1.c*1e12:.3f} pF")        # valor en pF
print(f"t_5τ = {c1.t_5tao(R)* 1e6:.3f} µs")
print(f"f_min = {c1.f_min(R)/1e3:.2f} kHz")
