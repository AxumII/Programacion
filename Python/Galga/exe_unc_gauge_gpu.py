import cupy as cp
from unc_gauge_gpu import UncGauge

# Funciones auxiliares para generar entradas
def generar_tipo_a_b(nombre, sensibilidad):
    muestra = cp.random.normal(loc=1.0, scale=0.01, size=10)
    resol = 0.001
    calib = 0.002
    return (muestra, nombre, resol, calib)

def generar_tipo_b(nombre, sensibilidad):
    resol = 0.001
    calib = 0.002
    return (nombre, resol, calib)

# Diccionarios de valores numéricos y derivadas
num_values_main = {
    "Vlect": 3,
    "R1": 1,
    "R2": 2,
    "R3": 1,
    "Vi": 0.5,
    "GF": 2,
    "RL": 2,
    "RG": 1,
    "v": 0.001,
    "E": 200000,
    "phi": 0.1,
    "m": 0.3,
    "g": 9.81,
    "lg": 0.5,
    "hg": 1,
    "L": 1,
    "x": 1,
    "b": 1,
    "h": 1
}


num_values_dist = {
    "T": 25,
    "T0": 20,
    "theta": 0.1,
    "alpha_instr": 0.00001,
    "alpha_obj": 0.000012,
    "d_mean": 10,
    "delta_0": 0.1,
    "delta_paral": 0.05,
    "delta_F": 0.02,
    "delta_desg": 0.01,
    "delta_h": 0.03,
}

derivadas_main ={
  "R1": "48*R2*g*hg*m*(-1 + lg/L)*(1 + RL/RG)*(L - x)*(-v/2 + (v + 1)*cos(2*phi)/2 - 1/2)/(E*GF*Vi*b*h**3*(1 + 2*(R2/(R1 + R2) - R3/(R3 + RG + RL) + Vlect)/Vi)*(R1 + R2)**2) - 96*R2*g*hg*m*(-1 + lg/L)*(1 + RL/RG)*(L - x)*(-v/2 + (v + 1)*cos(2*phi)/2 - 1/2)*(R2/(R1 + R2) - R3/(R3 + RG + RL) + Vlect)/(E*GF*Vi**2*b*h**3*(1 + 2*(R2/(R1 + R2) - R3/(R3 + RG + RL) + Vlect)/Vi)**2*(R1 + R2)**2)",
  "R2": "-48*g*hg*m*(-1 + lg/L)*(1 + RL/RG)*(L - x)*(-R2/(R1 + R2)**2 + 1/(R1 + R2))*(-v/2 + (v + 1)*cos(2*phi)/2 - 1/2)/(E*GF*Vi*b*h**3*(1 + 2*(R2/(R1 + R2) - R3/(R3 + RG + RL) + Vlect)/Vi)) + 96*g*hg*m*(-1 + lg/L)*(1 + RL/RG)*(L - x)*(-R2/(R1 + R2)**2 + 1/(R1 + R2))*(-v/2 + (v + 1)*cos(2*phi)/2 - 1/2)*(R2/(R1 + R2) - R3/(R3 + RG + RL) + Vlect)/(E*GF*Vi**2*b*h**3*(1 + 2*(R2/(R1 + R2) - R3/(R3 + RG + RL) + Vlect)/Vi)**2)",
  "R3": "-48*g*hg*m*(-1 + lg/L)*(1 + RL/RG)*(L - x)*(R3/(R3 + RG + RL)**2 - 1/(R3 + RG + RL))*(-v/2 + (v + 1)*cos(2*phi)/2 - 1/2)/(E*GF*Vi*b*h**3*(1 + 2*(R2/(R1 + R2) - R3/(R3 + RG + RL) + Vlect)/Vi)) + 96*g*hg*m*(-1 + lg/L)*(1 + RL/RG)*(L - x)*(R3/(R3 + RG + RL)**2 - 1/(R3 + RG + RL))*(-v/2 + (v + 1)*cos(2*phi)/2 - 1/2)*(R2/(R1 + R2) - R3/(R3 + RG + RL) + Vlect)/(E*GF*Vi**2*b*h**3*(1 + 2*(R2/(R1 + R2) - R3/(R3 + RG + RL) + Vlect)/Vi)**2)",
  "RL": "-48*R3*g*hg*m*(-1 + lg/L)*(1 + RL/RG)*(L - x)*(-v/2 + (v + 1)*cos(2*phi)/2 - 1/2)/(E*GF*Vi*b*h**3*(1 + 2*(R2/(R1 + R2) - R3/(R3 + RG + RL) + Vlect)/Vi)*(R3 + RG + RL)**2) + 96*R3*g*hg*m*(-1 + lg/L)*(1 + RL/RG)*(L - x)*(-v/2 + (v + 1)*cos(2*phi)/2 - 1/2)*(R2/(R1 + R2) - R3/(R3 + RG + RL) + Vlect)/(E*GF*Vi**2*b*h**3*(1 + 2*(R2/(R1 + R2) - R3/(R3 + RG + RL) + Vlect)/Vi)**2*(R3 + RG + RL)**2) - 48*g*hg*m*(-1 + lg/L)*(L - x)*(-v/2 + (v + 1)*cos(2*phi)/2 - 1/2)*(R2/(R1 + R2) - R3/(R3 + RG + RL) + Vlect)/(E*GF*RG*Vi*b*h**3*(1 + 2*(R2/(R1 + R2) - R3/(R3 + RG + RL) + Vlect)/Vi))",
  "RG": "-48*R3*g*hg*m*(-1 + lg/L)*(1 + RL/RG)*(L - x)*(-v/2 + (v + 1)*cos(2*phi)/2 - 1/2)/(E*GF*Vi*b*h**3*(1 + 2*(R2/(R1 + R2) - R3/(R3 + RG + RL) + Vlect)/Vi)*(R3 + RG + RL)**2) + 96*R3*g*hg*m*(-1 + lg/L)*(1 + RL/RG)*(L - x)*(-v/2 + (v + 1)*cos(2*phi)/2 - 1/2)*(R2/(R1 + R2) - R3/(R3 + RG + RL) + Vlect)/(E*GF*Vi**2*b*h**3*(1 + 2*(R2/(R1 + R2) - R3/(R3 + RG + RL) + Vlect)/Vi)**2*(R3 + RG + RL)**2) + 48*RL*g*hg*m*(-1 + lg/L)*(L - x)*(-v/2 + (v + 1)*cos(2*phi)/2 - 1/2)*(R2/(R1 + R2) - R3/(R3 + RG + RL) + Vlect)/(E*GF*RG**2*Vi*b*h**3*(1 + 2*(R2/(R1 + R2) - R3/(R3 + RG + RL) + Vlect)/Vi))",
  "Vi": "48*g*hg*m*(-1 + lg/L)*(1 + RL/RG)*(L - x)*(-v/2 + (v + 1)*cos(2*phi)/2 - 1/2)*(R2/(R1 + R2) - R3/(R3 + RG + RL) + Vlect)/(E*GF*Vi**2*b*h**3*(1 + 2*(R2/(R1 + R2) - R3/(R3 + RG + RL) + Vlect)/Vi)) - 96*g*hg*m*(-1 + lg/L)*(1 + RL/RG)*(L - x)*(-v/2 + (v + 1)*cos(2*phi)/2 - 1/2)*(R2/(R1 + R2) - R3/(R3 + RG + RL) + Vlect)**2/(E*GF*Vi**3*b*h**3*(1 + 2*(R2/(R1 + R2) - R3/(R3 + RG + RL) + Vlect)/Vi)**2)",
  "GF": "48*g*hg*m*(-1 + lg/L)*(1 + RL/RG)*(L - x)*(-v/2 + (v + 1)*cos(2*phi)/2 - 1/2)*(R2/(R1 + R2) - R3/(R3 + RG + RL) + Vlect)/(E*GF**2*Vi*b*h**3*(1 + 2*(R2/(R1 + R2) - R3/(R3 + RG + RL) + Vlect)/Vi))",
  "v": "-48*g*hg*m*(-1 + lg/L)*(1 + RL/RG)*(L - x)*(cos(2*phi)/2 - 1/2)*(R2/(R1 + R2) - R3/(R3 + RG + RL) + Vlect)/(E*GF*Vi*b*h**3*(1 + 2*(R2/(R1 + R2) - R3/(R3 + RG + RL) + Vlect)/Vi))",
  "phi": "48*g*hg*m*(-1 + lg/L)*(1 + RL/RG)*(L - x)*(v + 1)*(R2/(R1 + R2) - R3/(R3 + RG + RL) + Vlect)*sin(2*phi)/(E*GF*Vi*b*h**3*(1 + 2*(R2/(R1 + R2) - R3/(R3 + RG + RL) + Vlect)/Vi))",
  "hg": "-48*g*m*(-1 + lg/L)*(1 + RL/RG)*(L - x)*(-v/2 + (v + 1)*cos(2*phi)/2 - 1/2)*(R2/(R1 + R2) - R3/(R3 + RG + RL) + Vlect)/(E*GF*Vi*b*h**3*(1 + 2*(R2/(R1 + R2) - R3/(R3 + RG + RL) + Vlect)/Vi))",
  "m": "-48*g*hg*(-1 + lg/L)*(1 + RL/RG)*(L - x)*(-v/2 + (v + 1)*cos(2*phi)/2 - 1/2)*(R2/(R1 + R2) - R3/(R3 + RG + RL) + Vlect)/(E*GF*Vi*b*h**3*(1 + 2*(R2/(R1 + R2) - R3/(R3 + RG + RL) + Vlect)/Vi))",
  "g": "-48*hg*m*(-1 + lg/L)*(1 + RL/RG)*(L - x)*(-v/2 + (v + 1)*cos(2*phi)/2 - 1/2)*(R2/(R1 + R2) - R3/(R3 + RG + RL) + Vlect)/(E*GF*Vi*b*h**3*(1 + 2*(R2/(R1 + R2) - R3/(R3 + RG + RL) + Vlect)/Vi))",
  "L": "-48*g*hg*m*(-1 + lg/L)*(1 + RL/RG)*(-v/2 + (v + 1)*cos(2*phi)/2 - 1/2)*(R2/(R1 + R2) - R3/(R3 + RG + RL) + Vlect)/(E*GF*Vi*b*h**3*(1 + 2*(R2/(R1 + R2) - R3/(R3 + RG + RL) + Vlect)/Vi)) + 48*g*hg*lg*m*(1 + RL/RG)*(L - x)*(-v/2 + (v + 1)*cos(2*phi)/2 - 1/2)*(R2/(R1 + R2) - R3/(R3 + RG + RL) + Vlect)/(E*GF*L**2*Vi*b*h**3*(1 + 2*(R2/(R1 + R2) - R3/(R3 + RG + RL) + Vlect)/Vi))",
  "x": "48*g*hg*m*(-1 + lg/L)*(1 + RL/RG)*(-v/2 + (v + 1)*cos(2*phi)/2 - 1/2)*(R2/(R1 + R2) - R3/(R3 + RG + RL) + Vlect)/(E*GF*Vi*b*h**3*(1 + 2*(R2/(R1 + R2) - R3/(R3 + RG + RL) + Vlect)/Vi))",
  "E": "48*g*hg*m*(-1 + lg/L)*(1 + RL/RG)*(L - x)*(-v/2 + (v + 1)*cos(2*phi)/2 - 1/2)*(R2/(R1 + R2) - R3/(R3 + RG + RL) + Vlect)/(E**2*GF*Vi*b*h**3*(1 + 2*(R2/(R1 + R2) - R3/(R3 + RG + RL) + Vlect)/Vi))",
  "b": "48*g*hg*m*(-1 + lg/L)*(1 + RL/RG)*(L - x)*(-v/2 + (v + 1)*cos(2*phi)/2 - 1/2)*(R2/(R1 + R2) - R3/(R3 + RG + RL) + Vlect)/(E*GF*Vi*b**2*h**3*(1 + 2*(R2/(R1 + R2) - R3/(R3 + RG + RL) + Vlect)/Vi))",
  "h": "144*g*hg*m*(-1 + lg/L)*(1 + RL/RG)*(L - x)*(-v/2 + (v + 1)*cos(2*phi)/2 - 1/2)*(R2/(R1 + R2) - R3/(R3 + RG + RL) + Vlect)/(E*GF*Vi*b*h**4*(1 + 2*(R2/(R1 + R2) - R3/(R3 + RG + RL) + Vlect)/Vi))",
  "lg": "-48*g*hg*m*(1 + RL/RG)*(L - x)*(-v/2 + (v + 1)*cos(2*phi)/2 - 1/2)*(R2/(R1 + R2) - R3/(R3 + RG + RL) + Vlect)/(E*GF*L*Vi*b*h**3*(1 + 2*(R2/(R1 + R2) - R3/(R3 + RG + RL) + Vlect)/Vi))",
  "Vlect": "-48*g*hg*m*(-1 + lg/L)*(1 + RL/RG)*(L - x)*(-v/2 + (v + 1)*cos(2*phi)/2 - 1/2)/(E*GF*Vi*b*h**3*(1 + 2*(R2/(R1 + R2) - R3/(R3 + RG + RL) + Vlect)/Vi)) + 96*g*hg*m*(-1 + lg/L)*(1 + RL/RG)*(L - x)*(-v/2 + (v + 1)*cos(2*phi)/2 - 1/2)*(R2/(R1 + R2) - R3/(R3 + RG + RL) + Vlect)/(E*GF*Vi**2*b*h**3*(1 + 2*(R2/(R1 + R2) - R3/(R3 + RG + RL) + Vlect)/Vi)**2)"
}
derivadas_dist = {
    "d_mean":     "(alpha_instr*(T - T0) + 1)/((alpha_obj*(T - T0) + 1)*cos(theta))",
    "hg": "(alpha_instr*(T - T0) + 1)/((alpha_obj*(T - T0) + 1)*cos(theta))",
    "L":  "(alpha_instr*(T - T0) + 1)/((alpha_obj*(T - T0) + 1)*cos(theta))",
    "x":  "(alpha_instr*(T - T0) + 1)/((alpha_obj*(T - T0) + 1)*cos(theta))",
    "b":  "(alpha_instr*(T - T0) + 1)/((alpha_obj*(T - T0) + 1)*cos(theta))",
    "h":  "(alpha_instr*(T - T0) + 1)/((alpha_obj*(T - T0) + 1)*cos(theta))",
    
    "delta_0":    "-(alpha_instr*(T - T0) + 1)/((alpha_obj*(T - T0) + 1)*cos(theta))",
    "delta_paral":"(alpha_instr*(T - T0) + 1)/((alpha_obj*(T - T0) + 1)*cos(theta))",
    "delta_F":    "(alpha_instr*(T - T0) + 1)/((alpha_obj*(T - T0) + 1)*cos(theta))",
    "delta_desg": "(alpha_instr*(T - T0) + 1)/((alpha_obj*(T - T0) + 1)*cos(theta))",
    "delta_h":    "(alpha_instr*(T - T0) + 1)/((alpha_obj*(T - T0) + 1)*cos(theta))",
    "theta":      "((alpha_instr*(T - T0) + 1)*(d_mean - delta_0 + delta_F + delta_desg + delta_h + delta_paral)*sin(theta))/((alpha_obj*(T - T0) + 1)*cos(theta)**2)",
    "T":          "(alpha_instr*(d_mean - delta_0 + delta_F + delta_desg + delta_h + delta_paral))/((alpha_obj*(T - T0) + 1)*cos(theta)) - (alpha_obj*(alpha_instr*(T - T0) + 1)*(d_mean - delta_0 + delta_F + delta_desg + delta_h + delta_paral))/((alpha_obj*(T - T0) + 1)**2*cos(theta))",
    "T0":         "(-alpha_instr*(d_mean - delta_0 + delta_F + delta_desg + delta_h + delta_paral))/((alpha_obj*(T - T0) + 1)*cos(theta)) + (alpha_obj*(alpha_instr*(T - T0) + 1)*(d_mean - delta_0 + delta_F + delta_desg + delta_h + delta_paral))/((alpha_obj*(T - T0) + 1)**2*cos(theta))",
    "alpha_instr":"(T - T0)*(d_mean - delta_0 + delta_F + delta_desg + delta_h + delta_paral)/((alpha_obj*(T - T0) + 1)*cos(theta))",
    "alpha_obj":  "(-T + T0)*(alpha_instr*(T - T0) + 1)*(d_mean - delta_0 + delta_F + delta_desg + delta_h + delta_paral)/((alpha_obj*(T - T0) + 1)**2*cos(theta))"
}

# Datos de entrada DISTANCIA (solo necesitas definir 1 como ejemplo)
input_hg = {"muestra": cp.random.normal(1, 0.01, size=10), "name": "hg", "resol": 0.001, "calib": 0.002}
input_L = {"muestra": cp.random.normal(1, 0.01, size=10), "name": "L", "resol": 0.001, "calib": 0.002}
input_x = {"muestra": cp.random.normal(1, 0.01, size=10), "name": "x", "resol": 0.001, "calib": 0.002}
input_b = {"muestra": cp.random.normal(1, 0.01, size=10), "name": "b", "resol": 0.001, "calib": 0.002}
input_h = {"muestra": cp.random.normal(1, 0.01, size=10), "name": "h", "resol": 0.001, "calib": 0.002}

# Crear instancia
modelo = UncGauge(
    derivadas=derivadas_main,
    num_values=num_values_main,
    num_values_dist=num_values_dist,
    derivadas_dist=derivadas_dist,
    input_d_mean=[generar_tipo_a_b("d_mean", 1)],
    input_delta_0=[generar_tipo_b("delta_0", 1)],
    input_delta_paral=[generar_tipo_b("delta_paral", 1)],
    input_delta_F=[generar_tipo_b("delta_F", 1)],
    input_delta_desg=[generar_tipo_b("delta_desg", 1)],
    input_delta_h=[generar_tipo_b("delta_h", 1)],
    input_theta=[generar_tipo_b("theta", 1)],
    input_T=[generar_tipo_a_b("T", 1)],
    input_Vlect=[generar_tipo_a_b("Vlect", 1)],
    input_R1=[generar_tipo_b("R1", 1)],
    input_R2=[generar_tipo_b("R2", 1)],
    input_R3=[generar_tipo_b("R3", 1)],
    input_Vi=[generar_tipo_a_b("Vi", 1)],
    input_GF=[generar_tipo_b("GF", 1)],
    input_RL=[generar_tipo_b("RL", 1)],
    input_RG=[generar_tipo_b("RG", 1)],
    input_v=[generar_tipo_b("v", 1)],
    input_E=[generar_tipo_b("E", 1)],
    input_phi=[generar_tipo_a_b("phi", 1)],
    input_m=[generar_tipo_a_b("m", 1)],
    input_g=[generar_tipo_b("g", 1)],
    input_lg=[generar_tipo_b("lg", 1)],
    input_hg=input_hg,
    input_L=input_L,
    input_x=input_x,
    input_b=input_b,
    input_h=input_h
)

# Mostrar resultados
print("=== Tabla de Incertidumbres ===")
print(modelo.df_gen)
print("\n=== Incertidumbre Expandida (k=3) ===")
print(f"{modelo.unc_expanded(k=3):.6f}")
