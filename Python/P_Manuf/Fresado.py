import numpy as np

# La clase Fresado define métodos base. Sus hijos definen dt y el ángulo de entrada según la geometría.
class Fresado:
    def __init__(self, Dc, Zn, Kr, ang_desp, Vc, ac_max, ap):
        self.Dc = Dc
        self.Zn = Zn
        self.Kr = Kr
        self.ang_desp = ang_desp
        self.Vc = Vc
        self.ac_max = ac_max
        self.ap = ap

    def diam_ef_fres(self):
        raise NotImplementedError("Este método debe implementarse en una subclase.")

    def prof_c_rad(self):
        raise NotImplementedError("Este método debe implementarse en una subclase.")


    def frec_rot(self):
        dt = self.diam_ef_fres()
        return (self.Vc * 1000) / (np.pi * dt)

    def av_diente(self):
        raise NotImplementedError("Este método debe implementarse en una subclase.")

    def vel_avance(self):
        fz = self.av_diente()
        return fz * self.Zn * self.frec_rot()

    def tasa_remocion(self):
        ae = self.prof_c_rad()
        vf = self.vel_avance()
        return ae * self.ap * vf

    def ang_entrada(self):
        raise NotImplementedError("Este método debe implementarse en una subclase.")

    def esp_vir_no_def_entrada(self):
        fz = self.av_diente()
        phi = self.ang_entrada()
        return fz * np.sin(np.radians(phi)) * np.sin(np.radians(self.Kr))

    def esp_vir_no_def_media(self):
        dt = self.diam_ef_fres()
        fz = self.av_diente()
        ae = self.prof_c_rad()
        return fz * np.sin(np.radians(self.Kr)) * np.sqrt(ae / dt)

    def f_esp_corte(self, Kc1, mc):
        am = self.esp_vir_no_def_media()
        return Kc1 * (am ** (-mc)) * (1 - (self.ang_desp / 100))

    def pot_corte(self, Kc1, mc):
        kc = self.f_esp_corte(Kc1, mc)
        ae = self.prof_c_rad()
        vf = self.vel_avance()
        return (kc * self.ap * ae * vf) / (60 * 10**6)

    def par_corte(self, Kc1, mc):
        Pc = self.pot_corte(Kc1, mc)
        return (Pc * 30 * 10**3) / (np.pi * self.frec_rot())


class Fresado_d_rectos(Fresado):
    def diam_ef_fres(self):
        return self.Dc + (2 * self.ap / np.tan(np.radians(self.Kr)))

    def ang_entrada(self):
        dt = self.diam_ef_fres()
        ae = self.prof_c_rad()
        return np.degrees(np.arccos((ae - (dt / 2)) / (dt / 2)))
    
    def prof_c_rad(self):
        dt = self.diam_ef_fres()
        return 2 * dt / 3
    
    def av_diente(self):
        return self.ac_max / (np.sin(np.radians(90)) * np.sin(np.radians(self.Kr)))



class Fresado_circular(Fresado):
    def __init__(self, Dc, Zn, ang_desp, Vc, ac_max, ap, iC):
        self.iC = iC
        Kr = np.degrees(np.arccos(((0.5 * iC) - ap) / (0.5 * iC)))
        super().__init__(Dc, Zn, Kr, ang_desp, Vc, ac_max, ap)

    def diam_ef_fres(self):
        return self.Dc + np.sqrt(self.iC ** 2 - (self.iC - 2 * self.ap) ** 2)

    def ang_filo_p(self):
        return self.Kr

    def ang_entrada(self):
        dt = self.diam_ef_fres()
        ae = self.prof_c_rad()
        return  np.degrees(np.arccos((ae - (dt / 2)) / (dt / 2)))
    
    def prof_c_rad(self):
        dt = self.diam_ef_fres()
        return 1 * dt / 3

    def av_diente(self):
        return self.ac_max / (np.sin(np.radians(self.ang_entrada())) * np.sin(np.radians(self.Kr)))


# ---------------------
# EJEMPLO 1: Fresado de dientes rectos
# ---------------------
fresado_recto = Fresado_d_rectos(
    Dc=35,
    Zn=7,
    Kr=15,
    ang_desp=10,
    Vc=200,
    ac_max=0.1,
    ap=6
)
Kc1 = 750
mc = 0.41

print("→ Ejemplo 1: Fresado de dientes rectos")
print(f"Diametro efectivo de fresado: {fresado_recto.diam_ef_fres():.6f} mm")
print(f"Profundidad de corte radial: {fresado_recto.prof_c_rad():.6f} mm")
print(f"Frecuencia de rotación: {fresado_recto.frec_rot():.6f} min-1")
print(f"Avance por diente: {fresado_recto.av_diente():.6f} mm")
print(f"Velocidad de avance: {fresado_recto.vel_avance():.6f} mm/min")
print(f"Tasa de remoción: {fresado_recto.tasa_remocion():.6f} mm³/min")
print(f"Angulo de entrada : {fresado_recto.ang_entrada():.6f} grad")
print(f"Espesor viruta no def a la entrada: {fresado_recto.esp_vir_no_def_entrada():.6f} mm")
print(f"Espesor Medio de la viruta no deformada: {fresado_recto.esp_vir_no_def_media():.6f} mm")
print(f"Fuerza especifica de corte: {fresado_recto.f_esp_corte(Kc1, mc):.6f} N/mm²")
print(f"Potencia de corte: {fresado_recto.pot_corte(Kc1=Kc1, mc=mc):.6f} kW")
print(f"Par de corte: {fresado_recto.par_corte(Kc1=Kc1, mc=mc):.6f} Nm\n")

# ---------------------
# EJEMPLO 2: Fresado circular
# ---------------------
fresado_circular = Fresado_circular(
    Dc=60,
    Zn=8,
    ang_desp=-7,
    Vc=240,
    ac_max=0.1,
    ap=3,
    iC=8
)
Kc1 = 650  #700
mc = 0.25  #0.25
print("→ Ejemplo 2: Fresado circular")
print(f"Angulo de pos filo principal: {fresado_circular.ang_filo_p():.6f} grad")
print(f"Diametro efectivo de fresado: {fresado_circular.diam_ef_fres():.6f} mm")
print(f"Profundidad de corte radial: {fresado_circular.prof_c_rad():.6f} mm")
print(f"Frecuencia de rotación: {fresado_circular.frec_rot():.6f} min-1")
print(f"Angulo de entrada : {fresado_circular.ang_entrada():.6f} grad")
print(f"Avance por diente: {fresado_circular.av_diente():.6f} mm")
print(f"Velocidad de avance: {fresado_circular.vel_avance():.6f} mm/min")
print(f"Tasa de remoción: {fresado_circular.tasa_remocion():.6f} mm³/min")
print(f"Espesor viruta no def a la entrada: {fresado_circular.esp_vir_no_def_entrada():.6f} mm")
print(f"Espesor Medio de la viruta no deformada: {fresado_circular.esp_vir_no_def_media():.6f} mm")
print(f"Fuerza especifica de corte: {fresado_circular.f_esp_corte(Kc1, mc):.6f} N/mm²")
print(f"Potencia de corte: {fresado_circular.pot_corte(Kc1=Kc1, mc=mc):.6f} kW")
print(f"Par de corte: {fresado_circular.par_corte(Kc1=Kc1, mc=mc):.6f} Nm\n")
