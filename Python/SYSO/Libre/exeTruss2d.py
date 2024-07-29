import numpy as np
from Truss2d import Truss2DAnalyzer as Tr


def EjemploClase():
    
    Nodos = np.array([[0, 0],
                  [1.5, 0],
                  [1.5, 1.5],
                  [0, 1.5]])

    Elementos = np.array([[1, 2],
                        [1, 3],
                        [3, 4],
                        [2, 3]])

    Uex = np.array([[1, 1, 0],
                    [1, 2, 0],
                    [4, 1, 0],
                    [4, 2, 0]])

    Fex = np.array([[3, 1, 5e3],
                    [3, 2, 3e3]])


    E = 69e9 * np.ones((4, 1))
    A = 2.25e-4 * np.ones((4, 1))
    Fluencia = 240e6
    Nombre = "Ejemplo"


    truss = Tr(Nodos, Elementos, Uex, Fex, E, A, Fluencia,Nombre)


    U, R, S, FactS = truss.analyze()
    
    

    print("Factor de Seguridad", FactS)
        
def TrussDouglas():
    Nodos = np.array([[1.60, 5.20],
                  [2.60, 5.20],
                  [0.80, 4.60],
                  [1.60, 4.60],
                  [2.60, 4.60],
                  [3.40, 4.60],
                  [1.60, 3.80],
                  [2.60, 3.80],
                  [0.80, 3.40],
                  [3.40, 3.40],
                  [0.00, 3.00],
                  [0.80, 3.00],
                  [1.60, 3.00],
                  [2.60, 3.00],
                  [3.40, 3.00],
                  [4.20, 3.00],
                  [1.30, 1.80],
                  [2.90, 1.80],
                  [1.30, 0.00],
                  [2.90, 0.00]
                ])


    Elementos = np.array([[1, 2],
                      [1, 3],
                      [1, 4],
                      [2, 4],
                      [2, 5],
                      [2, 6],
                      [3, 4],
                      [4, 5],
                      [5, 6],
                      [4, 8],
                      [5, 8],
                      [4, 7],
                      [7, 8],
                      [7, 9],
                      [9, 11],
                      [11, 12],
                      [12, 13],
                      [9 , 12],
                      [9, 13],
                      [7, 13],
                      [8, 13],
                      [8, 14],
                      [10, 14],
                      [8, 10],
                      [10, 16],
                      [10, 15],
                      [14, 15],
                      [15, 16],
                      [13, 14],
                      [13, 17],
                      [13, 18],
                      [14, 18],
                      [17, 18],
                      [17, 19],
                      [18, 19],
                      [18, 20],
                      [19, 20]
                    ])



    #Vector Estatico
    #[Nodo,Eje,0]
    #Eje 1 = x Eje 2 = y
    Uex = np.array([[19, 1, 0],
                    [19, 2, 0],
                    [20, 1, 0],
                    [20, 2, 0]])

    #Vector de Cargas
    #[Nodo, Eje, Carga] 
    #Eje 1 = x Eje 2 = y

    Fex = np.array([[3 ,2 ,-1e3 ],
                    [6 ,2 ,-1e3 ],
                    [11 ,2 ,-(7)*1e3 ], #Poner digito cedula en parentesis
                    [16 ,2 ,-(7)*1e3 ]])
                    
            

    E = 13.1e9 * np.ones((Elementos.shape[0], 1)) #Pa
    A = ((25e-3) * (25e-3)) * np.ones((Elementos.shape[0], 1)) #m²
    Fluencia = 55.8e6  
    Nombre = "Truss_Torre_con_Douglas"



    truss = Tr(Nodos, Elementos, Uex, Fex, E, A,Fluencia,Nombre)


    U, R, S, FactS = truss.analyze()

def TrussAcero():
    Nodos = np.array([[1.60, 5.20],
                  [2.60, 5.20],
                  [0.80, 4.60],
                  [1.60, 4.60],
                  [2.60, 4.60],
                  [3.40, 4.60],
                  [1.60, 3.80],
                  [2.60, 3.80],
                  [0.80, 3.40],
                  [3.40, 3.40],
                  [0.00, 3.00],
                  [0.80, 3.00],
                  [1.60, 3.00],
                  [2.60, 3.00],
                  [3.40, 3.00],
                  [4.20, 3.00],
                  [1.30, 1.80],
                  [2.90, 1.80],
                  [1.30, 0.00],
                  [2.90, 0.00]
                ])


    Elementos = np.array([[1, 2],
                        [1, 3],
                        [1, 4],
                        [2, 4],
                        [2, 5],
                        [2, 6],
                        [3, 4],
                        [4, 5],
                        [5, 6],
                        [4, 8],
                        [5, 8],
                        [4, 7],
                        [7, 8],
                        [7, 9],
                        [9, 11],
                        [11, 12],
                        [12, 13],
                        [9 , 12],
                        [9, 13],
                        [7, 13],
                        [8, 13],
                        [8, 14],
                        [10, 14],
                        [8, 10],
                        [10, 16],
                        [10, 15],
                        [14, 15],
                        [15, 16],
                        [13, 14],
                        [13, 17],
                        [13, 18],
                        [14, 18],
                        [17, 18],
                        [17, 19],
                        [18, 19],
                        [18, 20],
                        [19, 20]
                        ])



    #Vector Estatico
    #[Nodo,Eje,0]
    #Eje 1 = x Eje 2 = y
    Uex = np.array([[19, 1, 0],
                    [19, 2, 0],
                    [20, 1, 0],
                    [20, 2, 0]])

    #Vector de Cargas
    #[Nodo, Eje, Carga] 
    #Eje 1 = x Eje 2 = y

    Fex = np.array([[3 ,2 ,-1e3 ],
                    [6 ,2 ,-1e3 ],
                    [11 ,2 ,-(8)*1e3 ], #Poner digito cedula en parentesis
                    [16 ,2 ,-(8)*1e3 ]])
                    
            

    E = 200e9 * np.ones((Elementos.shape[0], 1)) #Pa
    A = ((25e-3) * (25e-3)) * np.ones((Elementos.shape[0], 1)) #m²
    Fluencia = 240e6  
    Nombre = "Truss_Torre_con_Acero"



    truss = Tr(Nodos, Elementos, Uex, Fex, E, A,Fluencia,Nombre)


    U, R, S, FactS = truss.analyze()



def Parcialp5():
  
    Nodos = np.array([[0, 0],
                    [5, 0],
                    [5, 5],
                    [0, 5]])

    Elementos = np.array([[1, 2], #I
                          [2, 3], #II
                          [3, 4], #III
                          [1, 4], #IV
                          [1, 3]]) #V
                        

    Uex = np.array([[1, 1, 0],
                    [1, 2, 0],                    
                    [2, 2, 0]])

    Fex = np.array([[4, 2, -7e3],
                    [3, 1, -7e3],
                    [3, 2, -7e3]])


    
    E = np.array([[200e9],
                  [250e9],
                  [300e9],
                  [250e9],
                  [200e9]])
    
    
   
    
    A = np.array([[4e-4],
                  [2e-4],
                  [4e-4],
                  [4e-4],
                  [1e-4]])
    
    
    Fluencia = 240e6
    Nombre = "Ejemplo"


    truss = Tr(Nodos, Elementos, Uex, Fex, E, A, Fluencia,Nombre)


    U, R, S, FactS = truss.analyze()
    
    

    print("Factor de Seguridad", FactS)







#EjemploClase()

Parcialp5()



