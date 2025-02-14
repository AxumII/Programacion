import numpy as np
import matplotlib.pyplot as plt


class Proyecto:
    def __init__(self, L=0.85, diam=0.0254, esp=0.002, t1=0.002, h1=0.03, w1=0, 
                 t2=0.002, h2=0.03, w2=0.07, t3 = 0.001, h3 = 0.01, w3 = 0.01, 
                 kind_1=("redon", "A913"), kind_2=("rect", "302"), kind_3=("cuad", "7075")):  # En metros
        self.L = L
        self.diam = diam
        self.esp = esp
        self.t1 = t1
        self.h1 = h1
        self.w1 = w1
        self.t2 = t2
        self.h2 = h2
        self.w2 = w2
        self.t3 = t3
        self.h3 = h3
        self.w3 = w3
        self.kind_1 = {"tipo": kind_1[0], "material": kind_1[1]}
        self.kind_2 = {"tipo": kind_2[0], "material": kind_2[1]}
        self.kind_3 = {"tipo": kind_3[0], "material": kind_3[1]}
        


        self.material_A913 = {
            "nombre": "ASTM A913",
            "G": 76_000 * 10**6,  # MPa
            "sigma_vs": 470 * 10**6,  # Límite elástico en MPa
            "sigma_u": 560 * 10**6,  # Resistencia última en MPa
        }

        self.material_302 = {
            "nombre": "AISI 302",
            "G": 72_000 * 10**6,
            "sigma_u": 860 * 10**6,
            "sigma_vs": 540 * 10**6,
        }

        self.material_7075 = {
            "nombre": "7075 T6",
            "G": 28_000 * 10**6,
            "sigma_vs": 520 * 10**6,
            "sigma_u": 580 * 10**6,
        }
###############################################################################
    # Métodos de cálculos geométricos
    def J_tubo_redondo(self):
        return (np.pi / 32) * (self.diam**4 - (self.diam - 2 * self.esp)**4)

    def J_tubo_rect(self, t, h, w):
        return ((2 * t) * ((h - t) ** 2) * ((w - t) ** 2)) / (h + w - 2 * t)

    def Zp_rect(self, t, h, w):
        return (2 * t) * (h - t) * (w - t)
###########################################################################
    # Métodos de cálculos resistivos
    def angle_twist(self, T, J1, J2, J3, G1, G2, G3):
        return (T * self.L) / (J1 * G1 + J2 * G2 + J3 * G3)

    def tao(self, kind, T, coef_inercia):
        if kind["tipo"] == "redon":  # USAR J en inercia
            return (T * (self.diam) / 2) / coef_inercia
        elif kind["tipo"] in ["rect", "cuad"]:  # USAR Zp en inercia
            return T / coef_inercia
        else:
            raise ValueError("Tipo de eje no reconocido en la función tao()")

        
        

#############################################################################################

    def plot_angle(self, steps=50):
        T_E1 = np.arange(0, 101, steps)
        T_E2 = np.arange(100, 301, steps)
        T_E3 = np.arange(300, 801, steps)
    ########################################################################################
        #Etapa 1
        def Arr_E1():
            #Seleccion J1
            if self.kind_1["tipo"] == "redon": #USAR J en inercia
                J1 = self.J_tubo_redondo()  
            elif self.kind_1["tipo"] ==  "rect": 
                J1 = self.J_tubo_rect(self.t2, self.h2, self.w2)
                Zp1 = self.Zp_rect(self.t2, self.h2, self.w2)
            elif self.kind_1["tipo"] ==  "cuad":
                J1 = self.J_tubo_rect(self.t1, self.h1, self.h1)
                Zp1 = self.Zp_rect(self.t1, self.h1, self.h1)
            else:
                print("Falta parametro en etapa 1 parte 1")

            #Identificacion G1
            if self.kind_1["material"] == "A913":
                G1 = self.material_A913["G"]
            if self.kind_1["material"] == "302":
                G1 = self.material_302["G"]
            if self.kind_1["material"] == "7075":
                G1 = self.material_7075["G"]
            
            #Angulo 
            return self.angle_twist(T_E1, J1 = J1, J2 = 0, J3 = 0, G1 = G1, G2 = 0, G3 = 0)
    #########################################################################################
        #Etapa 2
        def Arr_E2():
            #Seleccion J1
            if self.kind_1["tipo"] == "redon": #USAR J en inercia
                J1 = self.J_tubo_redondo()  
            elif self.kind_1["tipo"] ==  "rect": 
                J1 = self.J_tubo_rect(self.t2, self.h2, self.w2)
                Zp1 = self.Zp_rect(self.t2, self.h2, self.w2)
            elif self.kind_1["tipo"] ==  "cuad":
                J1 = self.J_tubo_rect(self.t1, self.h1, self.h1)
                Zp1 = self.Zp_rect(self.t1, self.h1, self.h1)
            else:
                print("Falta parametro en etapa 2 parte 1")
        #Seleccion J2
            if self.kind_2["tipo"] == "redon": 
                J2 = self.J_tubo_redondo()  
            elif self.kind_2["tipo"] == "rect": 
                J2 = self.J_tubo_rect(self.t2, self.h2, self.w2)
                Zp2 = self.Zp_rect(self.t2, self.h2, self.w2)
            elif self.kind_2["tipo"] == "cuad":
                J2 = self.J_tubo_rect(self.t1, self.h1, self.h1)
                Zp2 = self.Zp_rect(self.t1, self.h1, self.h1)   
            else:
                print("Falta parametro en etapa 2 parte 2")

        #Identificacion G1
            if self.kind_1["material"] == "A913":
                G1 = self.material_A913["G"]
            if self.kind_1["material"] == "302":
                G1 = self.material_302["G"]
            if self.kind_1["material"] == "7075":
                G1 = self.material_7075["G"]
        #Identificacion G2
            if self.kind_2["material"] == "A913":
                G2 = self.material_A913["G"]
            if self.kind_2["material"] == "302":
                G2 = self.material_302["G"]
            if self.kind_2["material"] == "7075":
                G2 = self.material_7075["G"]
            
        #Angulo 
            return self.angle_twist(T_E2, J1 = J1, J2 = J2, J3 = 0, G1 = G1, G2 = G2, G3 = 0)

    #########################################################################################
        #Etapa 3
        def Arr_E3():
            #Seleccion J1
            if self.kind_1["tipo"] == "redon": #USAR J en inercia
                J1 = self.J_tubo_redondo()  
            elif self.kind_1["tipo"] ==  "rect": 
                J1 = self.J_tubo_rect(self.t2, self.h2, self.w2)
                Zp1 = self.Zp_rect(self.t2, self.h2, self.w2)
            elif self.kind_1["tipo"] ==  "cuad":
                J1 = self.J_tubo_rect(self.t1, self.h1, self.h1)
                Zp1 = self.Zp_rect(self.t1, self.h1, self.h1)
            else:
                print("Falta parametro en etapa 3 parte 1")


            #Seleccion J2
            if self.kind_2["tipo"] == "redon": 
                J2 = self.J_tubo_redondo()  
            elif self.kind_2["tipo"] == "rect": 
                J2 = self.J_tubo_rect(self.t2, self.h2, self.w2)
                Zp2 = self.Zp_rect(self.t2, self.h2, self.w2)
            elif self.kind_2["tipo"] == "cuad":
                J2 = self.J_tubo_rect(self.t1, self.h1, self.h1)
                Zp2 = self.Zp_rect(self.t1, self.h1, self.h1)   
            else:
                print("Falta parametro en etapa 3 parte 2")

            #Seleccion J3
            if self.kind_3["tipo"] == "redon": 
                J3 = self.J_tubo_redondo()  
            elif self.kind_3["tipo"] == "rect": 
                J3 = self.J_tubo_rect(self.t2, self.h2, self.w2)
                Zp3 = self.Zp_rect(self.t2, self.h2, self.w2)
            elif self.kind_3["tipo"] == "cuad":
                J3 = self.J_tubo_rect(self.t1, self.h1, self.h1)
                Zp3 = self.Zp_rect(self.t1, self.h1, self.h1)  
            elif self.kind_3["tipo"] == "rect2":
                J3 = self.J_tubo_rect(self.t3, self.h3, self.w3) 
                Zp3 = self.Zp_rect(self.t3, self.h3, self.w3) 
                
            else:
                print("Falta parametro en etapa 3 parte 3")
                



            #Identificacion G1
            if self.kind_1["material"] == "A913":
                G1 = self.material_A913["G"]
            if self.kind_1["material"] == "302":
                G1 = self.material_302["G"]
            if self.kind_1["material"] == "7075":
                G1 = self.material_7075["G"]
            #Identificacion G2
            if self.kind_2["material"] == "A913":
                G2 = self.material_A913["G"]
            if self.kind_2["material"] == "302":
                G2 = self.material_302["G"]
            if self.kind_2["material"] == "7075":
                G2 = self.material_7075["G"]
            #Identificacion G3
            if self.kind_3["material"] == "A913":
                G3 = self.material_A913["G"]
            if self.kind_3["material"] == "302":
                G3 = self.material_302["G"]
            if self.kind_3["material"] == "7075":
                G3 = self.material_7075["G"]
            
            #Angulo maximo
            return self.angle_twist(T_E3, J1 = J1, J2 = J2, J3 = J3, G1 = G1, G2 = G2, G3 = G3)

    #######################################################################################
        #Generacion Plot

        Ang_E1 = Arr_E1()
        Ang_E2 = Arr_E2() 
        Ang_E3 = Arr_E3() 
        
        
        plt.figure()
        plt.plot(T_E1, Ang_E1, label='Torsion vs Angulo 1 Eje', color='blue')
        plt.plot(T_E2, Ang_E2, label='Torsion vs Angulo 2 Eje', color='purple')
        plt.plot(T_E3, Ang_E3, label='Torsion vs Angulo 3 Eje', color='blue')
        
        # Puntos a tener en cuenta
        T_Obj = np.array([100, 300, 700])
        ang_Obj = np.array([0.0872665, 0.174533, 0.2618])
        plt.scatter(T_Obj, ang_Obj, color='red', label='Objetivo de diseño', marker='X')

        # Configuración
        plt.xlabel('Torsion (N*m)')
        plt.ylabel('Angulo de giro (rad)')
        plt.title('Torsion vs Angulo de giro en brida')
        plt.legend()
        plt.show()

    ######################################################################################
    def plot_sections(self):
        fig, ax = plt.subplots(figsize=(6, 6))
        
        # **Tubo Redondo**
        circle = plt.Circle((0, 0), self.diam / 2, color='blue', fill=False, linewidth=2, label="Tubo Redondo")
        inner_circle = plt.Circle((0, 0), (self.diam - 2 * self.esp) / 2, color='blue', fill=False, linestyle='dashed', linewidth=2)
        ax.add_patch(circle)
        ax.add_patch(inner_circle)

        # **Tubo Cuadrado**
        square = plt.Rectangle((-self.h1/2, -self.h1/2), self.h1, self.h1, color='red', fill=False, linewidth=2, label="Tubo Cuadrado")
        inner_square = plt.Rectangle((-self.h1/2 + self.t1, -self.h1/2 + self.t1), self.h1 - 2*self.t1, self.h1 - 2*self.t1, color='red', fill=False, linestyle='dashed', linewidth=2)
        ax.add_patch(square)
        ax.add_patch(inner_square)

        # **Tubo Rectangular**
        rect = plt.Rectangle((-self.w2/2, -self.h2/2), self.w2, self.h2, color='green', fill=False, linewidth=2, label="Tubo Rectangular")
        inner_rect = plt.Rectangle((-self.w2/2 + self.t2, -self.h2/2 + self.t2), self.w2 - 2*self.t2, self.h2 - 2*self.t2, color='green', fill=False, linestyle='dashed', linewidth=2)
        ax.add_patch(rect)
        ax.add_patch(inner_rect)

        # **Tubo Rectangular 2**
        rect = plt.Rectangle((-self.w3/2, -self.h3/2), self.w3, self.h3, color='purple', fill=False, linewidth=2, label="Tubo Rectangular 2")
        inner_rect = plt.Rectangle((-self.w3/2 + self.t3, -self.h3/2 + self.t3), self.w3 - 2*self.t3, self.h3 - 2*self.t3, color='purple', fill=False, linestyle='dashed', linewidth=2)
        ax.add_patch(rect)
        ax.add_patch(inner_rect)

        ax.set_xlim(-self.w2 / 2 - 0.015, self.w2 / 2 + 0.015)
        ax.set_ylim(-self.h2 / 2 - 0.015, self.h2 / 2 + 0.015)
        ax.set_aspect('equal')
        ax.grid()
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title("Secciones Transversales Superpuestas")
        ax.legend()
        plt.show()

###########################################################################################################################################################
# Uso del código

#medidas en milimetros
L_ = 600 / 1000
#Circulo
diametro = (100) / 1000
espesor_circulo = (1) / 1000

#Cuadrado
lado = (15) / 1000
espesor_cuadrado = (1.5) / 1000

#Rectangulo
espesor_rect = (1) / 1000
altura = (30) / 1000
ancho = (30) / 1000

#Rectangulo 2

espesor_rect2 = (0.8) / 1000
altura2 = (22) / 1000
ancho2 = (22) / 1000


# Crear una instancia del proyecto
proyecto = Proyecto( L = L_, diam= diametro, esp= espesor_circulo,
                     t1 = espesor_cuadrado, h1 = lado, 
                     t2 = espesor_rect, h2 = altura, w2 = ancho,
                     t3 = espesor_rect2, h3 = altura2, w3 = ancho2,
                     kind_1=("rect", "7075"), 
                     kind_2=("cuad", "A913"), 
                     kind_3=("rect2", "A913")
                    )

# Ejecutar 

proyecto.plot_angle()
proyecto.plot_sections()

# A913, 302, 7075
