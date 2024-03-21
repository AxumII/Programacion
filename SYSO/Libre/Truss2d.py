import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


class Truss2DAnalyzer:
    def __init__(self, Nodos, Elementos, Uex, Fex, E, A, Fluencia,Nombre):
        self.Nodos = Nodos
        self.Elementos = Elementos.astype(int)  # Asegurándonos de que los índices de los elementos sean enteros
        self.Uex = Uex.astype(int)  # Asegurándonos de que los índices de Uex sean enteros
        self.Fex = Fex.astype(int)  # Asegurándonos de que los índices de Fex sean enteros
        self.E = E
        self.A = A
        self.Fluencia = Fluencia
        self.Nombre = Nombre
   
    def analyze(self):
        NumGDL = 2
        NumNodEles = 2
        NumNods, Dim = self.Nodos.shape
        NumEles, _ = self.Elementos.shape
        NumUex, _ = self.Uex.shape
        NumFex, _ = self.Fex.shape

        K = np.zeros((NumNods * NumGDL, NumNods * NumGDL))
        F = np.zeros(NumNods * NumGDL)

        for k1 in range(NumEles):
            i = self.Elementos[k1, 0]
            j = self.Elementos[k1, 1]
            xi = self.Nodos[i-1, :]
            xj = self.Nodos[j-1, :]
            Ke = self._Truss2DElemental(self.E[k1], self.A[k1], xi, xj)

            for k2 in range(NumNodEles):
                FilEle = k2 * NumGDL
                FilGlo = (self.Elementos[k1, k2] - 1) * NumGDL
                for k3 in range(NumNodEles):
                    ColEle = k3 * NumGDL
                    ColGlo = (self.Elementos[k1, k3] - 1) * NumGDL
                    for k4 in range(NumGDL):
                        for k5 in range(NumGDL):
                            K[FilGlo + k4, ColGlo + k5] += Ke[FilEle + k4, ColEle + k5]

        for k1 in range(NumFex):
            Fil = (self.Fex[k1, 0] - 1) * NumGDL + self.Fex[k1, 1] - 1  # Corrección: Restando 1 para obtener el índice correcto
            F[Fil] += self.Fex[k1, 2]

        Kaux = K.copy()
        for k1 in range(NumUex):
            Fil = (self.Uex[k1, 0] - 1) * NumGDL + self.Uex[k1, 1] - 1  # Corrección: Restando 1 para obtener el índice correcto
            Kaux[Fil, :] = 0
            Kaux[Fil, Fil] = 1
            F[Fil] = self.Uex[k1, 2]

        U = np.linalg.solve(Kaux, F)
        R = np.dot(K, U)
        S = np.zeros(NumEles)
        
        for k1 in range(NumEles):
            i = self.Elementos[k1, 0]
            j = self.Elementos[k1, 1]
            xi = self.Nodos[i-1, :]
            xj = self.Nodos[j-1, :]
            Ue = U[(i-1) * NumGDL:(i-1) * NumGDL + NumGDL]  # Corrección: Incluyendo el desplazamiento v
            Ue = np.append(Ue, U[(j-1) * NumGDL:(j-1) * NumGDL + NumGDL])  # y aquí para el nodo j
            S[k1] = self._EsfuerzoTruss2D(self.E[k1], xi, xj, Ue)
            
        #Factor Seguridad
        
        EMax = np.amax(S)    
        
        FactS = (self.Fluencia)/(EMax)
        
        
        Umax = np.amax(U)
        Rmax = np.amax(R)
        
        
        self.export_results_to_csv(U, R, S, Umax, EMax, Rmax, FactS)
        
        self.graf()
        
        
        
        return U, R, S, FactS
    
        

   
    def _Truss2DElemental(self, E, A, xi, xj):
        Le = np.sqrt((xj[0] - xi[0])**2 + (xj[1] - xi[1])**2)
        l = (xj[0] - xi[0]) / Le
        m = (xj[1] - xi[1]) / Le
        Ke = E * A / Le * np.array([[ l**2,   l*m,  -l**2, -l*m],
                                    [ l*m,   m**2,  -l*m,  -m**2],
                                    [-l**2,  -l*m,   l**2,  l*m],
                                    [-l*m,  -m**2,   l*m,   m**2]])
        return Ke

    def _EsfuerzoTruss2D(self, E, xi, xj, Ue):
        Le = np.sqrt((xj[0] - xi[0])**2 + (xj[1] - xi[1])**2)
        l = (xj[0] - xi[0]) / Le
        m = (xj[1] - xi[1]) / Le
        S = E / Le * np.array([-l, -m, l, m]) @ Ue
        return S

    def graf(self):
        # Crear un gráfico
        fig, ax = plt.subplots()

        # Dibujar los nodos y numerarlos
        for idx, nodo in enumerate(self.Nodos, start=1):  # empezamos la enumeración en 1
            ax.plot(nodo[0], nodo[1], 'o',  markersize=10, color="black")  # 'ko' crea un punto negro en la posición del nodo
            # Anotar el número del nodo con un pequeño desplazamiento
            ax.text(nodo[0] + 0.05, nodo[1] + 0.05, str(idx), verticalalignment='bottom', horizontalalignment='left', fontsize=9, color='blue')

        # Dibujar los elementos como líneas entre los nodos
        for elemento in self.Elementos:
            punto_inicio = self.Nodos[elemento[0] - 1]  # Los índices en Python son base 0, los ajustamos
            punto_final = self.Nodos[elemento[1] - 1]
            ax.plot([punto_inicio[0], punto_final[0]], [punto_inicio[1], punto_final[1]], 'k-', linewidth=2)  # 'k-' crea una línea negra

        # Configurar límites si es necesario
        ax.set_xlim(min(self.Nodos[:, 0]) - 1, max(self.Nodos[:, 0]) + 1)
        ax.set_ylim(min(self.Nodos[:, 1]) - 1, max(self.Nodos[:, 1]) + 1)
        ax.set_title('Diagrama de Nodos del ' + self.Nombre)
        ax.grid(True)
        plt.show()
        

    def export_results_to_csv(self, U, R, S, Umax, Emax, Rmax, FactS):
        # Exportar desplazamientos (U)
        df_U = pd.DataFrame(U, columns=['Desplazamiento'])
        df_U.to_csv(self.Nombre + 'Desplazamientos.csv', index_label='GDL')

        # Exportar fuerzas de reacción (R)
        df_R = pd.DataFrame(R, columns=['Reacciones'])
        df_R.to_csv(self.Nombre + 'Reacciones.csv', index_label='GDL')

        # Exportar esfuerzos (S)
        df_S = pd.DataFrame(S, columns=['Esfuerzos'])
        df_S.to_csv(self.Nombre + 'Esfuerzos.csv', index_label='Elemento')

        # Exportar resumen
        df_summary = pd.DataFrame({
            'Umax': [Umax],
            'Emax': [Emax],
            'Rmax': [Rmax],
            'FactS': [FactS]
        })
        df_summary.to_csv(self.Nombre + '_Resumen.csv', index=False)

        print("Los archivos CSV han sido creados y guardados con éxito.")
        
        print("Deformaciones", df_U)
        print("Reacciones", df_R)
        print("Esfuerzos",df_S)
        print("Resumen Maximos", df_summary)


################################################################################################################################################################################
################################################################################################################################################################################
################################################################################################################################################################################
################################################################################################################################################################################




