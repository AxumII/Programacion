from Fresado import Fresado_d_rectos
from Fresado import Fresado_circular

# ---------------------
# EJEMPLO 1: Fresado de dientes rectos
# ---------------------
fresado_recto = Fresado_d_rectos(
    Dc=8,
    Zn=4,
    Kr=90,
    ang_desp=10,
    Vc=80,
    ac_max=90,
    ap=1
)
Kc1 = 1
mc = 1

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
