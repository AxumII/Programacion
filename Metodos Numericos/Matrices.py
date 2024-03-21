import numpy as np

class Matrices:
    def __init__(self, A, B, scaled=False, step=False, LU=False):
        assert A.shape[0] == A.shape[1], "A debe ser una matriz cuadrada"
        self.A = A
        self.B = B
        self.scaled = scaled
        self.step = step
        self.LU = LU
        self.L = np.eye(A.shape[0])  # Inicializar L como una matriz identidad

    def Gauss_pivot(self):
        A = self.A.copy()
        B = self.B.copy()
        L = self.L.copy()
        rows, cols = A.shape

        if abs(np.linalg.det(A)) < 1e-10:
            print("La matriz es singular y no tiene una inversa.")
            return False

        for j in range(cols - 1):
            pivot_row = np.argmax(np.abs(A[j:, j])) + j
            if pivot_row != j:
                A[[j, pivot_row]], A[[pivot_row, j]] = A[[pivot_row, j]], A[[j, pivot_row]]
                B[[j, pivot_row]], B[[pivot_row, j]] = B[[pivot_row, j]], B[[j, pivot_row]]

            for i in range(j+1, rows):
                if A[j, j] == 0:
                    continue
                factor_k = A[i, j] / A[j, j]
                A[i, j:] -= factor_k * A[j, j:]
                B[i] -= factor_k * B[j]
                L[i, j] = factor_k

                if self.step:
                    print(f"Eliminación en fila {i+1} con factor {factor_k}")
                    print("Matriz A después de la eliminación:\n", A)
                    print("Vector B después de la eliminación:\n", B)
                    print("Matriz L después de la actualización:\n", L)

        if self.step:
            print("Proceso de eliminación completado.")
        
        return A, B, L

# Ejemplo de uso
A = np.array([[3, 2, -4, 7], [2, 3, 3, 8], [5, -3, 1, 6], [5, -3, 1, 7]], dtype=float)
B = np.array([3, 15, 14, 1], dtype=float)
matrices = Matrices(A, B, step=True, LU=True)
A_mod, B_mod, L = matrices.Gauss_pivot()

print(A,B)

print("A_mod (U):\n", A_mod)
print("B_mod:\n", B_mod)
print("L:\n", L)

if isinstance(A_mod, np.ndarray):  # Verifica que la eliminación fue exitosa antes de calcular LU
    print("Factor LU final:\n", L @ A_mod)
