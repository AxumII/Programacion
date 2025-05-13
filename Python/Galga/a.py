def sobol_analysis(self):
        problem = {
    'num_vars': 20,
    'names': ['Vlect','K','R1','R2','R3','RG','RL','Vi','GF','v',
              'phi','hg','m','g','L','x','E','b','h','lg'],
    'bounds': [
        [0.00028, 0.00032],   # Vlect
        [1.9, 2.1],           # K
        [110, 130],           # R1
        [110, 130],           # R2
        [110, 130],           # R3
        [110, 130],           # RG
        [110, 130],           # RL
        [4.9, 5.1],           # Vi
        [2.0, 2.2],           # GF
        [0.28, 0.32],         # v
        [0.0, np.pi/2],       # phi
        [0.01, 0.015],        # hg
        [0.01, 0.015],        # m
        [9.79, 9.81],         # g
        [0.09, 0.11],         # L
        [0.04, 0.06],         # x
        [180e9, 210e9],       # E
        [0.009, 0.011],       # b
        [0.0009, 0.0011],     # h
        [0.02, 0.03]          # lg
    ]






}
        param_values = saltelli.sample(problem, 1000, calc_second_order=False)

        Y = np.zeros(param_values.shape[0])

        for i, row in enumerate(param_values):
            Y[i] = modelo(*row)

        Si = sobol.analyze(problem, Y, calc_second_order=False)

        print("Índices de primer orden:", Si['S1'])
        print("Índices de orden total:", Si['ST'])
