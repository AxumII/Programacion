import sympy as sp

class Derivation:
    def __init__(self, model_class, input_values):
        self.model_class = model_class
        self.input_values = input_values
        self.symbols = {}
        self.expressions = {}

    def build_symbolic_model(self):
        # Obtener nombres de los argumentos del constructor
        params = self.model_class.__init__.__code__.co_varnames[1:self.model_class.__init__.__code__.co_argcount]
        self.symbols = {name: sp.Symbol(name) for name in params}

        # Instanciar el modelo con símbolos
        model_instance = self.model_class(**self.symbols)

        # Calcular el modelo (devuelve expresión simbólica si se usa sympy internamente)
        expr = model_instance.calculate()

        # Guardar la expresión simbólica del modelo
        self.model_expr = expr
        return expr

    def compute_derivatives(self):
        if not hasattr(self, 'model_expr'):
            self.build_symbolic_model()

        derivadas = {}
        for var in self.symbols.values():
            derivadas[str(var)] = sp.diff(self.model_expr, var)
        self.expressions = derivadas
        return derivadas

    def evaluate_derivatives(self):
        if not self.expressions:
            self.compute_derivatives()

        sustituciones = {self.symbols[k]: v for k, v in self.input_values.items() if k in self.symbols}
        evaluadas = {}
        for var, expr in self.expressions.items():
            try:
                evaluadas[var] = float(expr.evalf(subs=sustituciones))
            except Exception as e:
                evaluadas[var] = f"Error: {str(e)}"
        return evaluadas
