from unc_gauge_gpu import UncGauge as UncGauge




if __name__ == "__main__":
    # === Variables con Tipo A y B
    inputs_tipo_a_b = {
        "Vlect": (None, "Vlect", 0.0001, 0.0002, 1),
        "Vi": (None, "Vi", 0.001, 0.002, 1),
        "phi": (None, "phi", 0.001, 0.002, 0.01),
        "hg": (None, "hg", 0.001, 0.002, 0.02),
        "m": (None, "m", 0.001, 0.002, 0.01),
        "L": (None, "L", 0.001, 0.002, 0.03),
        "x": (None, "x", 0.001, 0.002, 0.04),
        "E": (None, "E", 0.001, 0.002, 0.01),
        "b": (None, "b", 0.001, 0.002, 0.05),
        "h": (None, "h", 0.001, 0.002, 0.07),
        "lg": (None, "lg", 0.001, 0.002, 0.01),
    }

    # === Variables con Tipo B puro
    inputs_tipo_b = {
        "GF": ("GF", 0.001, 0.002),
        "v": ("v", 0.001, 0.002),
        "g": ("g", 0.001, 0.002),
        "K": ("K", 0.001, 0.002),
        "R1": ("R1", 1.0, 1.0),
        "R2": ("R2", 1.0, 1.0),
        "R3": ("R3", 1.0, 1.0),
        "RG": ("RG", 1.0, 1.0),
        "RL": ("RL", 1.0, 1.0)
    }

    # === Submodelo (UncDistance): Tipo A + B
    inputs_tipo_a_b_dist = {
        "d_mean": (None, "d_mean", 0.001, 0.002, 0.01),
        "T": (None, "T", 0.1, 0.2, 0.5),
        "theta": (None, "theta", 0.001, 0.002, 0.01)
    }

    inputs_tipo_b_dist = {
        "delta_0": ("delta_0", 0.001, 0.002),
        "delta_paral": ("delta_paral", 0.001, 0.002),
        "delta_F": ("delta_F", 0.001, 0.002),
        "delta_desg": ("delta_desg", 0.001, 0.002),
        "delta_h": ("delta_h", 0.001, 0.002)
    }

    inputs_distance = ["hg","b","h","L", "x"]

    """# === Derivadas para TODO el sistema
    derivadas = {        
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
        "Vlect": "-48*g*hg*m*(-1 + lg/L)*(1 + RL/RG)*(L - x)*(-v/2 + (v + 1)*cos(2*phi)/2 - 1/2)/(E*GF*Vi*b*h**3*(1 + 2*(R2/(R1 + R2) - R3/(R3 + RG + RL) + Vlect)/Vi)) + 96*g*hg*m*(-1 + lg/L)*(1 + RL/RG)*(L - x)*(-v/2 + (v + 1)*cos(2*phi)/2 - 1/2)*(R2/(R1 + R2) - R3/(R3 + RG + RL) + Vlect)/(E*GF*Vi**2*b*h**3*(1 + 2*(R2/(R1 + R2) - R3/(R3 + RG + RL) + Vlect)/Vi)**2)",
        "d_mean":     "(alpha_instr*(T - T0) + 1)/((alpha_obj*(T - T0) + 1)*cos(theta))",
        "delta_0":    "-(alpha_instr*(T - T0) + 1)/((alpha_obj*(T - T0) + 1)*cos(theta))",
        "delta_paral":"(alpha_instr*(T - T0) + 1)/((alpha_obj*(T - T0) + 1)*cos(theta))",
        "delta_F":    "(alpha_instr*(T - T0) + 1)/((alpha_obj*(T - T0) + 1)*cos(theta))",
        "delta_desg": "(alpha_instr*(T - T0) + 1)/((alpha_obj*(T - T0) + 1)*cos(theta))",
        "delta_h":    "(alpha_instr*(T - T0) + 1)/((alpha_obj*(T - T0) + 1)*cos(theta))",
        "T":          "(alpha_instr*(d_mean - delta_0 + delta_F + delta_desg + delta_h + delta_paral))/((alpha_obj*(T - T0) + 1)*cos(theta)) - (alpha_obj*(alpha_instr*(T - T0) + 1)*(d_mean - delta_0 + delta_F + delta_desg + delta_h + delta_paral))/((alpha_obj*(T - T0) + 1)**2*cos(theta))",
        "T0":         "(-alpha_instr*(d_mean - delta_0 + delta_F + delta_desg + delta_h + delta_paral))/((alpha_obj*(T - T0) + 1)*cos(theta)) + (alpha_obj*(alpha_instr*(T - T0) + 1)*(d_mean - delta_0 + delta_F + delta_desg + delta_h + delta_paral))/((alpha_obj*(T - T0) + 1)**2*cos(theta))",
        "alpha_instr":"(T - T0)*(d_mean - delta_0 + delta_F + delta_desg + delta_h + delta_paral)/((alpha_obj*(T - T0) + 1)*cos(theta))",
        "alpha_obj":  "(-T + T0)*(alpha_instr*(T - T0) + 1)*(d_mean - delta_0 + delta_F + delta_desg + delta_h + delta_paral)/((alpha_obj*(T - T0) + 1)**2*cos(theta))"
    }
"""
    # === Valores base
    num_values = {
        "Vlect": 0.0003,
        "Vi": 5.0,
        "GF": 2.1,
        "v": 0.33,
        "phi": 0.1,
        "hg": 0.2,
        "m": 0.05,
        "g": 9.81,
        "L": 1.2,
        "x": 0.8,
        "E": 200e9,
        "b": 0.01,
        "h": 0.005,
        "lg": 0.6,
        "K": 0.01,
        "T": 25,
        "T0": 20,
        "theta": 0.1,
        "alpha_instr": 1e-5,
        "alpha_obj": 1.2e-5,
        "d_mean": 10,
        "delta_0": 0.1,
        "delta_paral": 0.05,
        "delta_F": 0.02,
        "delta_desg": 0.01,
        "delta_h": 0.03
    }



    sensitivity_dict = {
        "Vlect": 1.0, "Vi": 0.9, "phi": 1.1, "hg": 0.95,
        "m": 1.2, "L": 1.0, "x": 1.1, "E": 0.85,
        "b": 1.0, "h": 1.0, "lg": 0.9,
        "GF": 0.8, "v": 0.95, "g": 1.2, "K": 1.0,
        "R1": 1.0, "R2": 1.0, "R3": 1.0, "RG": 1.0, "RL": 1.0,
        "d_mean": 1.0, "T": 0.85, "theta": 1.1,
        "delta_0": 1.0, "delta_paral": 0.5, "delta_F": 1.0,
        "delta_desg": 1.0, "delta_h": 1.0
    }

    unc = UncGauge(
        num_values=num_values,
        inputs_tipo_a_b=inputs_tipo_a_b,
        inputs_tipo_b=inputs_tipo_b,
        inputs_tipo_a_b_dist=inputs_tipo_a_b_dist,
        inputs_tipo_b_dist=inputs_tipo_b_dist,
        inputs_distance=inputs_distance,
        sensitivity_dict=sensitivity_dict
    )

    unc.calculate()

    print("=== Tabla Final de Incertidumbres ===")
    print(unc.df_gen)
    print("\n=== Incertidumbre Expandida (k=3) ===")
    print(f"{unc.unc_expanded(k=3):.6f}")
