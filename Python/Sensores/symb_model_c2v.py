
import sympy as sp

class SymbModel: 
    def __init__(self):
        self.R1, self.R2, self.Rs, self.Rl, self.Rt = sp.symbols('R1 R2 Rl ', positive=True)
        self.C1, self.C2, self.Cs, self.Cl = sp.symbols('C1 C2 Cs Cl', positive=True)
        self.Vz = sp.symbols('Vz', positive = True)

        self.params = [
            self.R1, self.R2, self.Rl, 
            self.C1, self.C2, self.Cs, self.Cl,self.Vz
        ]

    def calculate(self):
        wn = 1 / sp.sqrt(self.R1 * self.R2 * (self.C1 + self.Cs) * self.C2)
        K = sp.Rational(209, 100)
        Vo = (wn/(2*sp.pi))*self.Vz*self.Cl*self.Rl


        return sp.simplify(Vo)
    
    def _norm_values(self, values: dict):
        if not values: return {}
        name2sym = {str(s): s for s in self.params}
        out = {}
        for k, v in values.items():
            out[name2sym[k] if isinstance(k, str) and k in name2sym else k] = v
        return out
    
    def sens_coeffs(self, wrt=None):
        """Derivadas simbólicas: {var: dVo/dvar}."""
        Vo = self.calculate()
        if wrt is None:
            wrt = [p for p in self.params if Vo.has(p)]
        return {v: sp.simplify(sp.diff(Vo, v)) for v in wrt}

    def eval_sens_coeffs(self, values: dict, wrt=None):
        """Derivadas evaluadas numéricamente (dict de floats)."""
        vals = self._norm_values(values)
        out = {}
        for v, expr in self.sens_coeffs(wrt=wrt).items():
            expr_sub = sp.N(expr.subs(vals))
            free = expr_sub.free_symbols
            if free:
                missing = ", ".join(sorted(str(s) for s in free))
                raise ValueError(f"Faltan valores para: {missing} (en dVo/d{v})")
            out[str(v)] = float(expr_sub)
        return out

    def eval_vo(self, values: dict):
        return sp.N(self.calculate().subs(values))

    def print_derivatives(self, values: dict = None, wrt=None, pretty=True):
        Vo = self.calculate()
        if pretty:
            sp.pprint(Vo)
        else:
            print("Vo =", Vo)

        print("\nDerivadas de Vo:")
        c_sym = self.sens_coeffs(wrt=wrt)  
        vals = self._norm_values(values) if values is not None else None

        for v, dexpr in c_sym.items():
            if pretty:
                print(f"dVo/d{v} =")
                sp.pprint(dexpr)
            else:
                print(f"dVo/d{v} = {dexpr}")

            if vals is not None:
                num = sp.N(dexpr.subs(vals))
                if num.free_symbols:
                    missing = ", ".join(sorted(str(s) for s in num.free_symbols))
                    print(f"    -> faltan valores para: {missing}")
                else:
                    print(f"    -> evaluada: {float(num)}")