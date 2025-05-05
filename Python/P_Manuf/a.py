import numpy as np


#La clase fresado define todos los metodos para hallar cada valor, todos son iguales excepto el dt
#fresado no se usa, se usan son los hijos que heredan sus clases y luego con polimorfismo use dt
#me dio pereza copiar y pegar xdxdxd

class Fresado:
    def __init__(self, Dc, Zn, Kr, ang_desp, Vc, ac_max, ap):
        self.Dc = Dc              # Diámetro de la fresa (mm)
        self.Zn = Zn              # Número de dientes
        self.Kr = Kr              # Ángulo de ataque κr: (grados)
        self.ang_desp = ang_desp  # Ángulo de desprendimiento γ0 (grados) 
        self.Vc = Vc              # Velocidad de corte (m/min)
        self.ac_max = ac_max      # Espesor máximo viruta no deformada (mm)
        self.ap = ap              # Profundidad de corte axial (mm)

    def diam_ef_fres(self): #dt
        raise NotImplementedError("Este método debe implementarse en una subclase.")
    #no la defini aca, use polimorfismo ya que es el mismo metodo para el redondo y el cuadrado 
    #y me dio pereza hacerlo 2 veces todo
    def prof_c_rad(self): #ae
        dt = self.diam_ef_fres()
        return 2 * dt / 3

    def frec_rot(self): #nt
        dt = self.diam_ef_fres()
        return (self.Vc * 1000) / (np.pi * dt)

    def av_diente(self):  #fz
        return self.ac_max / (np.sin(np.radians(self.ang_desp + 1e-6)) * np.sin(np.radians(self.Kr)))

    def vel_avance(self): #vf
        fz = self.av_diente()
        return fz * self.Zn * self.frec_rot()

    def tasa_remocion(self): #Zw
        ae = self.prof_c_rad()
        vf = self.vel_avance()
        return ae * self.ap * vf

    def ang_entrada(self):  #φ1 °    
        raise NotImplementedError("Este método debe implementarse en una subclase.")
    #no la defini aca, use polimorfismo ya que es el mismo metodo para el redondo y el cuadrado 
    #y me dio pereza hacerlo 2 veces todo

    def esp_vir_no_def_entrada(self): #ac
        fz = self.av_diente()
        phi = self.ang_entrada()
        return fz * np.sin(np.radians(phi)) * np.sin(np.radians(self.Kr))

    def esp_vir_no_def_media(self): #am
        dt = self.diam_ef_fres()
        fz = self.av_diente()
        ae = self.prof_c_rad()
        return fz * np.sin(np.radians(self.Kr)) * np.sqrt(ae / dt)

    def f_esp_corte(self, Kc1, mc): #Kc
        am = self.esp_vir_no_def_media()
        return Kc1 * (am ** (-mc)) * (1 - (self.ang_desp / 100))

    def pot_corte(self, Kc1, mc): #Pc
        kc = self.f_esp_corte(Kc1, mc)
        ae = self.prof_c_rad()
        vf = self.vel_avance()
        return (kc * self.ap * ae * vf) / (60 * 10**6)  # kW

    def par_corte(self, Kc1, mc): #Mc
        Pc = self.pot_corte(Kc1, mc)
        return (Pc * 30 * 10**3) / (np.pi * self.frec_rot())  # Nm

#Hijo N1, solo defino el dt y ya
class Fresado_d_rectos(Fresado):
    def diam_ef_fres(self): #dt recto
        return self.Dc + (2 * self.ap / np.tan(np.radians(self.Kr)))
    
    def ang_entrada(self):  #φ1 ° 
        dt = self.diam_ef_fres()
        ae = self.prof_c_rad()
        return (    np.arccos((ae-(dt/2))/(dt/2)))

#Hijo N2, aca añado en el cosntructor el iC, y luego se define el metodo de dt
#Tambien se cambia el Kr porque toca hallarlo
class Fresado_circular(Fresado):
    def __init__(self, Dc, Zn, ang_desp, Vc, ac_max, ap, iC):
        super().__init__(Dc, Zn, ang_desp, Vc, ac_max, ap)
        self.iC = iC
        self.kr = self.ang_filo_p()

    def diam_ef_fres(self): #dt circular
        return self.Dc + np.sqrt(self.iC**2 - (self.iC - 2 * self.ap)**2)
    
    def ang_filo_p(self): #Kr
        return np.arccos( ((0.5*self.iC)- self.ap) / (0.5*self.iC))

    def ang_entrada(self):  #φ1 ° 
        dt = self.diam_ef_fres()
        ae = self.prof_c_rad()
        return ( np.radians(180) -   np.arccos((ae-(dt/2))/(dt/2)))
    

# ---------------------
# EJEMPLO 1: Fresado de dientes rectos
# ---------------------
fresado_recto = Fresado_d_rectos(
    Dc=75,
    Zn=6,
    Kr=60,
    ang_desp=0,
    Vc=265,
    ac_max=0.2,
    ap=7
)
Kc1 = 750
mc = 0.41
print("→ Ejemplo 1: Fresado de dientes rectos")
print(f"Frecuencia de rotación: {fresado_recto.frec_rot():.2f} rpm")
print(f"Velocidad de avance: {fresado_recto.vel_avance():.2f} mm/min")
print(f"Tasa de remoción: {fresado_recto.tasa_remocion():.2f} mm³/min")
print(f"Potencia de corte: {fresado_recto.pot_corte(Kc1=Kc1, mc=mc):.4f} kW")
print(f"Par de corte: {fresado_recto.par_corte(Kc1=Kc1, mc=mc):.2f} Nm\n")


# ---------------------
# EJEMPLO 2: Fresado circular
# ---------------------
fresado_circular = Fresado_circular(
    Dc=125, #
    iC=10,#
    Zn=9,#
    ang_desp=5,#
    Vc=55,#
    ac_max=0.2,#
    ap=4#
)
Kc1 = 1700
mc = 0.25
print("→ Ejemplo 2: Fresado circular")
print(f"Frecuencia de rotación: {fresado_circular.frec_rot():.2f} rpm")
print(f"Velocidad de avance: {fresado_circular.vel_avance():.2f} mm/min")
print(f"Tasa de remoción: {fresado_circular.tasa_remocion():.2f} mm³/min")
print(f"Potencia de corte: {fresado_circular.pot_corte(Kc1=Kc1, mc=mc):.4f} kW")
print(f"Par de corte: {fresado_circular.par_corte(Kc1=Kc1, mc=mc):.2f} Nm")
