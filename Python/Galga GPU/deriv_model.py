import sympy as sp
from pathlib import Path

def generar_derivadas_modelo(modelo, variables, exportar_tex=False, ruta_tex=None):
    """
    Calcula e imprime las derivadas parciales de un modelo simbólico.
    
    Parámetros:
    - modelo: expresión simbólica de SymPy
    - variables: lista de variables simbólicas
    - exportar_tex: bool, si se desea exportar el resultado a LaTeX
    - ruta_tex: ruta completa donde guardar el .tex (Path o str). Si es None, se usa una ruta por defecto.
    """
    deriv_python = {}
    deriv_latex = {}

    for var in variables:
        deriv = sp.diff(modelo, var)
        deriv_python[str(var)] = deriv
        deriv_latex[str(var)] = f"\\[\n\\frac{{\\partial\\,f}}{{\\partial\\,{sp.latex(var)}}} = {sp.latex(deriv)}\n\\]"

    print("=== DERIVADAS EN FORMATO PYTHON ===\n")
    for var, expr in deriv_python.items():
        print(f"d(model)/d({var}) = {expr}\n")

    if exportar_tex:
        if ruta_tex is None:
            ruta_tex = Path.home() / "Documents" / "derivadas_modelo.tex"
        else:
            ruta_tex = Path(ruta_tex)

        latex_document = r"""
\documentclass[12pt]{article}
\usepackage{amsmath}
\usepackage{geometry}
\geometry{margin=2.5cm}

\title{Derivadas Parciales del Modelo}
\author{}
\date{}

\begin{document}

\maketitle

\section*{Función del Modelo}
\begin{equation*}
""" + sp.latex(modelo) + r"""
\end{equation*}

\section*{Derivadas Parciales}
"""

        for expr in deriv_latex.values():
            latex_document += expr + "\n"

        latex_document += r"\end{document}"

        ruta_tex.write_text(latex_document, encoding='utf-8')
        print(f"\nArchivo .tex guardado en: {ruta_tex}")


# === DEFINICIÓN DE MODELOS ===

def dist():
    d_mean, delta_0, delta_paral, delta_F, delta_desg, delta_h = sp.symbols('d_mean delta_0 delta_paral delta_F delta_desg delta_h')
    theta, T, T0 = sp.symbols('theta T T0')
    alpha_instr, alpha_obj = sp.symbols('alpha_instr alpha_obj')

    distance = (d_mean - delta_0 + delta_paral + delta_F + delta_desg + delta_h) / sp.cos(theta)
    temp_error = (1 + alpha_instr * (T - T0)) / (1 + alpha_obj * (T - T0))
    model = distance * temp_error

    variables = [d_mean, delta_0, delta_paral, delta_F, delta_desg, delta_h, theta, T, T0, alpha_instr, alpha_obj]
    generar_derivadas_modelo(model, variables, exportar_tex=True)


def gaug():
    Vlect, R1, R2, R3, RL, RG, Vi, GF = sp.symbols("V_lect R1 R2 R3 RL RG Vi GF")
    v, phi = sp.symbols("v phi")
    hg, m, g, L, x, E, b, h = sp.symbols("hg m g L x E b h")
    lg = sp.symbols("lg")

    delta_V = Vlect - ((R3 / (R3 + RG + RL)) - (R2 / (R1 + R2)))
    epsilon = (-4 * (delta_V / Vi)) / (GF * (1 + 2 * (delta_V / Vi)))
    error_misalignment = ((1 - v + (1 + v) * sp.cos(2 * phi)) / 2) - 1
    error_curvature = (12 * hg * m * g * (L - x)) / (E * b * h**3)
    error_gauge_long = (lg / L) - 1
    error_bridge = (1 + RL / RG)

    model = epsilon * error_bridge * error_misalignment * error_curvature * error_gauge_long
    variables = [Vlect, R1, R2, R3, RL, RG, Vi, GF, v, phi, hg, m, g, L, x, E, b, h, lg]
    generar_derivadas_modelo(model, variables, exportar_tex=True)


# === LLAMADA DEL MODELO (CAMBIA AQUÍ PARA PROBAR OTRO) ===
if __name__ == "__main__":
    # Usa uno u otro llamando su función:
    # dist()  # ← Modelo de distancia y temperatura
    gaug()    # ← Modelo de galga extensiométrica
