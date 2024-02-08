
#Librerias
import tkinter as tk
from tkinter import *
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
import math
from numpy import linalg as LA
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg




n = 10
SaveD = np.zeros((n,4))
SaveF = np.zeros((n,5))
SaveM = np.zeros((n,3))




class wr:
    def __init__(self,SaveD,SaveF,SaveM,TotF,TotM,ParallelM,PerpM):
       self.SaveD = np.zeros((n,4))
       self.SaveF = np.zeros((n,5))
       self.SaveM = np.zeros((n,3))
       self.TotF = np.array([0,0,0])
       self.TotM = np.array([0,0,0])
       self.ParallelM = np.array([0,0,0])
       self.PerpM = np.array([0,0,0])

    def Coor(Ty,x,y,z,m): #Modificar los input
        #print(m,"aca se rastrea en coor")
        #print(Ty,"aca se si se define el tipo")
        Tip1 = Ty
        
        #se elimina este texto
        #cadVec="vector" if Tip1<3 else "vector director"

        #print("Ingrese las coordenadas del ",cadVec)
        #hasta aca

        orCoor=[0]*3#crea una lista auxiliar

        orCoor[0] = x
        orCoor[1] = y
        orCoor[2] = z
        

        if Tip1==1 or Tip1==4:
            actCoor=wr.CilCar(orCoor)
        elif Tip1==2 or Tip1==5:
           actCoor=wr.EsfCar(orCoor)
        else:
            actCoor=orCoor
        if Tip1>=3:
            m
            z=np.array([actCoor[0],actCoor[1],actCoor[2]])
            normVD=LA.norm(z)
            for i in range(3):
               actCoor[i]*=round(m/normVD,3)
        return actCoor
    
    def EsfCar(x):
       #recibe vector tridimensional en coordenadas esfericas (r,tetha,phi), retorna vector tridimensional en coordenadas cartesianas
       y=x[:]
       y[0]=round(x[0]*math.cos(x[2])*math.sin(x[1]),3)
       y[1]=round(x[0]*math.sin(x[2])*math.cos(x[1]),3)
       y[2]=round(x[0]*math.cos(x[2]),3)
       return y
      
    def CilCar(x):
       #recibe vector tridimensional en coordenadas cilindricas (r,tetha,z) , retorna vector tridimensional en coordenadas cartesianas
       y=x[:]
       y[0]=round(x[0]*math.cos(x[1]),3)
       y[1]=round(x[0]*math.sin(x[1]),3)
       return y

    def CreateD(ty,x,y,z,m): #permite ingresar los valores de distancia y el tipo de dato, el tipo no implementad
        #print("\t\t Ingresando posición...")
        dist=wr.Coor(ty,x,y,z,m)
        Distancia = np.array([0,dist[0],dist[1],dist[2]])
        return Distancia

    def CreateF(ty,x,y,z,m):#Permite ingresar lso valores de fuerza y eol tipo, eso no esta impliementado, pero listos para el conversor
        #print("\t\t Ingresando fuerza...")
        #print(m,"aca se rastrea en CreateF")
        #print(ty,"aca se rastrea el ty en Create F")
        force=wr.Coor(ty,x,y,z,m)
        Fuerza = np.array([0,force[0],force[1],force[2],0])
        return Fuerza

    def SaveValues(ty,x,y,z,m,tyf,xf,yf,zf,mf,row): #Aca llama a los creadores y lso guarda en la matrices de distancias y fuerzas
        Distance = wr.CreateD(ty,x,y,z,m)
        Force = wr.CreateF(tyf,xf,yf,zf,mf)
        #print(mf,"aca se rastrea en SaveValues")
        #print(tyf,"Aca se rastrea el tyf")
        for i in range(4):
            SaveD[row,i] = Distance[i]
            SaveF[row,i] = Force[i]
        return SaveD,SaveF
    
    def FindMoments(SaveD,SaveF,SaveM):
        x = SaveD.shape
        for i in range(x[0]):
            D = np.array([SaveD[i,1],SaveD[i,2],SaveD[i,3]])
            F = np.array([SaveF[i,1],SaveF[i,2],SaveF[i,3]])
            M = np.cross(D,F)
            for j in range(3):
                SaveM[i,j] = M[j]

        #print(SaveM)
        return(SaveM)

    def SumMatrix(SaveF,SaveM):
        TotF = np.sum(SaveF,axis = 0)
        TotF = np.array([TotF[1],TotF[2],TotF[3]])
        TotM = np.sum(SaveM, axis = 0)
        #print("Imprime Totales\n",TotF,"\n",TotM)
        return TotF,TotM
    
    def FindWrench(TotF,TotM):
        try:
            UnitF = TotF/np.linalg.norm(TotF)
        except ZeroDivisionError:
            UnitF = 0
        Lambda = np.dot(UnitF,TotM)
        try:
            Lambda = round(Lambda)
        except:
            Lambda = 0
        ParallelM = np.dot(UnitF,Lambda)
        PerpM = np.array(TotM - ParallelM)
        #print(TotF,TotM,ParallelM,PerpM)
        return ParallelM,PerpM
        
    def PositionSolver(TotF,PerpM):
        #Existen 6 casos de resolucion, donde 3 son con dos ejes y 3 con un unico eje 
        #Matriz Principal 3x3, no tiene solucion porque el determinante es 0
        """
        Siendo el vector fuerza F = (a,b,c)
        x    y    z                   x    y    z
        0    c   -b                  0,0  0,1  0,2            0
        -c   0    a                  1,0  1,1  1,2            1
        b   -a    0                  2,0  2,1  2,2            2
        """
        SolveMatrix = np.array([[0,TotF[2],-1*TotF[1]],[-1*TotF[2],0,TotF[0]],[TotF[1],-1*TotF[0],0]])
        #print(SolveMatrix)

        def PlanoXY(): #sobre XY, Z = 0
            #print("Hallar la posicion donde el eje de la llave interseca en el plano XY")
            Ec1 = np.array([[0,SolveMatrix[0,1]],[SolveMatrix[2,0],SolveMatrix[2,1]]])
            Ec2 = np.array([[SolveMatrix[1,0],0],[SolveMatrix[2,0],SolveMatrix[2,1]]])
            S1 = np.array([PerpM[0],PerpM[2]])
            S2 = np.array([PerpM[1],PerpM[2]])

            try:
                A = np.linalg.solve(Ec1,S1)
                B = np.linalg.solve(Ec2,S2)
            except np.linalg.LinAlgError:
                print("error")
                A = np.array([0,0])
            #print(Ec1)
            #print(Ec2)
            #print(A,"es la primera solucion\n")
            #print(B,"es la segunda solucion\n")
            return A

        def PlanoXZ(): #sobre XZ, Y = 0
            #print("Hallar la posicion donde el eje de la llave interseca en el plano XZ, este es el que interesa")
            Ec1 = np.array([[0,SolveMatrix[0,2]],[SolveMatrix[1,0],SolveMatrix[1,2]]])
            Ec2 = np.array([[SolveMatrix[1,0],SolveMatrix[1,2]],[SolveMatrix[2,0],0]])
            S1 = np.array([PerpM[0],PerpM[1]])
            S2 = np.array([PerpM[1],PerpM[2]])
            try:
                A = np.linalg.solve(Ec1,S1)
                B = np.linalg.solve(Ec2,S2)
            except np.linalg.LinAlgError:
                print("error")
                A = np.array([0,0])
            """print(Ec1)
            print(Ec2)
            print(A,"es la primera solucion\n")
            print(B,"es la segunda solucion\n")"""
            return A

        def PlanoYZ(): #sobre YZ, X = 0
            #print("Hallar la posicion donde el eje de la llave interseca en el plano YZ")
            Ec1 = np.array([[SolveMatrix[0,1],SolveMatrix[0,2]],[0,SolveMatrix[1,2]]])
            Ec2 = np.array([[SolveMatrix[0,1],SolveMatrix[0,2]],[SolveMatrix[2,1],0]])
            
            S1 = np.array([PerpM[0],PerpM[1]])
            S2 = np.array([PerpM[0],PerpM[2]])
            try:
                A = np.linalg.solve(Ec1,S1)
                B = np.linalg.solve(Ec2,S2)
            except np.linalg.LinAlgError:
                print("error")
                A = np.array([0,0])
            """print(Ec1)
            print(Ec2)
            print(A,"es la primera solucion\n")
            print(B,"es la segunda solucion\n")"""
            return A
        
        p1 = PlanoXY() 
        p2 = PlanoXZ()
        p3 = PlanoYZ()
        InterCoor = np.array([p1,p2,p3])
        return InterCoor

    def FinalF(SaveD,SaveF,SaveM,TotF,TotM,ParallelM,PerpM,Intercoor):
        """print("MatrizDistancias\n",SaveD,"\n")
        print("MatrizFuerzas\n",SaveF,"\n")
        print("MatrizMomentos\n",SaveM,"\n")
        print("Total de Fuerza\n",TotF,"\n")
        print("Total de Momento\n",TotM,"\n")
        print("Momento Paralelo\n",ParallelM,"\n")
        print("Momento Perpendicular\n",PerpM,"\n")
        print("Matriz de distancias frente al eje\n",Intercoor,"\n") """
        return SaveD,SaveF,SaveM,TotF,TotM,ParallelM,PerpM,Intercoor



class Ventana(Frame):
       
    def __init__(self, master=None):
        super().__init__(master,width=1280, height=720)
        self.master = master
        self.pack()
        self.create_widgets()
        self.R = 0
        self.InputPos = 0
        self.InputForce = 0
        

    def TP0(self):
        self.InputPos = 0
        #print(self.InputPos)
    
    def TP1(self):
        self.InputPos = 1
        #print(self.InputPos)

    def TP2(self):
        self.InputPos = 2
        #print(self.InputPos)

    def TF0(self):
        self.InputForce = 0
        #print(self.InputForce,"Imprime despues de asignar")

    def TF1(self):
        self.InputForce = 1
        #print(self.InputForce,"Imprime despues de asignar")

    def TF2(self):
        self.InputForce = 2
        #print(self.InputForce,"Imprime despues de asignar")

    def TF3(self):
        self.InputForce = 3
        #print(self.InputForce,"Imprime despues de asignar")

    def TF4(self):
        self.InputForce = 4
        #print(self.InputForce,"Imprime despues de asignar")

    def TF5(self):
        self.InputForce = 5
        #print(self.InputForce,"Imprime despues de asignar")

############################################################################################################################################
    
    def CValues(self):
        i = self.R

        if  self.R < 9:
            #copia valores ingresados
            InpTy = self.InputPos
            Inpx = self.txtxpos.get()
            Inpy = self.txtypos.get()
            Inpz = self.txtzpos.get()
            Inpm = 0         

            #los convierte en valores numericos
            InpTy = int(InpTy)
            Inpx = float(Inpx)
            Inpy = float(Inpy)
            Inpz = float(Inpz)

            #eliminia el valor ingresado para poder proseguir
            self.txtxpos.delete(0,'end')
            self.txtypos.delete(0,'end')
            self.txtzpos.delete(0,'end')

            ################################################################################################################
            InfTy = self.InputForce
            InFx = self.txt_xforce.get()
            InFy = self.txt_yforce.get()
            InFz = self.txt_zforce.get()
            InFm = self.txt_mforce.get()


            InfTy = int(InfTy)
            InFx = float(InFx)
            InFy = float(InFy)
            InFz = float(InFz)
            InFm = float(InFm)

            self.txt_xforce.delete(0,'end')
            self.txt_yforce.delete(0,'end')
            self.txt_zforce.delete(0,'end')
            self.txt_mforce.delete(0,'end')
            self.txt_mforce.insert(0,0)

            #print(InFm,"aca se rastrea antes de llamar a la funcion")
            #print(InfTy,"aca se rastrea el tipo antes de llamar a la funcion")
            ################################################################################################################



            Exe1 = wr.SaveValues(InpTy,Inpx,Inpy,Inpz,Inpm,InfTy,InFx,InFy,InFz,InFm,self.R)
            def putValues():
                self.gridp.insert("",END,text=0,values = (SaveD[i,1],SaveD[i,2],SaveD[i,3]))
                self.gridf.insert("",END,text=0,values = (SaveF[i,1],SaveF[i,2],SaveF[i,3],SaveF[i,4]))
            putValues()
            self.R += 1
        else:
            pass

    def GenWrench(self):
        
        Exe2 = wr.FindMoments(SaveD,SaveF,SaveM)
        Exe3 = wr.SumMatrix(SaveF,Exe2)
        Exe4 = wr.FindWrench(Exe3[0],Exe3[1])
        Exe5 = wr.PositionSolver(Exe3[0],Exe4[1])
        Exe6 = wr.FinalF(SaveD,SaveF,Exe2,Exe3[0],Exe3[1],Exe4[0],Exe4[1],Exe5)

        for j in range(9):
            self.gridm.insert("",END,text=0,values = (SaveM[j,0],SaveM[j,1],SaveM[j,2]))

        self.gridr.insert("",END,text=0,values = (Exe3[0],Exe3[1],Exe4[0],Exe4[1]))#Es util pa un bucle

        self.grids.insert("",END,text="XY Axis",values = (Exe5[0,0],Exe5[0,1],0))
        self.grids.insert("",END,text="XZ Axis",values = (Exe5[1,0],0,Exe5[1,1]))
        self.grids.insert("",END,text="YZ Axis",values = (0,Exe5[2,0],Exe5[2,1]))

        
        def Graficacion():
            def GrafFuerzas(Dis,Fuer):
                # Dis es matriz de dimensión (n,4)
                # Fuer es matriz de dimensión (n,4)
                # grafica n vectores (de fuerza) y n vectores de posición, las coordenadas de la n-ésima cola de los de fuerza, que tambipén son las cabezas de los de posición son las posiciones 1,2,3 de la fila n de Dis, 
                # las coordenadas de la n-ésima cabeza son las posiciones 1,2,3 de la fila n de Fuer
                fig1 = plt.figure(figsize=(10,10)) #   fig = plt.figure(figsize=(15,15))
                ax = fig1.add_subplot(111, projection='3d')


                ax.plot(Dis[:,1], Dis[:,2], Dis[:,3], 'o', markersize=10, color='green', alpha=0.5)
                ax.plot(Fuer[:,1], Fuer[:,2], Fuer[:,3], 'o', markersize=10, color='red', alpha=0.5)
                

                for i in range(Dis.shape[0]):
                    if(i==0):
                        ax.plot([Dis[i,1], 0], [Dis[i,2], 0], [Dis[i,3], 0], color='green', alpha=0.8, lw=3, label="Posiciones")
                        ax.plot([Dis[i,1], Fuer[i,1]], [Dis[i,2], Fuer[i,2]], [Dis[i,3], Fuer[i,3]], color='red', alpha=0.8, lw=3,label="Fuerzas")
                    else:
                        ax.plot([Dis[i,1], 0], [Dis[i,2], 0], [Dis[i,3], 0], color='green', alpha=0.8, lw=3)
                        ax.plot([Dis[i,1], Fuer[i,1]], [Dis[i,2], Fuer[i,2]], [Dis[i,3], Fuer[i,3]], color='red', alpha=0.8, lw=3)
                ax.legend()
                ax.set_xlabel('x')
                ax.set_ylabel('y')
                ax.set_zlabel('z')
                
                plt.title('Vectores de posición y fuerza')
                ventana1=Tk()
                ventana1.geometry('700x325')
                ventana1.minsize(width=750,height=325)
                frame1=Frame(ventana1,bg='blue')
                frame1.grid()
                canvas=FigureCanvasTkAgg(fig1,master= frame1)
                canvas.draw()
                canvas.get_tk_widget().grid(column=0,row=0)
                ventana1.mainloop()
                #canvas=FigureCanvasTkAgg(fig1,master= Frameplt)
                #canvas.draw()
                #plt.draw()
                #plt.show()
                
                

            def GrafMomen(Mom,Dis,Fuer):
                # Dis es matriz de dimensión (n,4)
                # Fuer es matriz de dimensión (n,4)
                # Mom es matriz de dimensión (n,3)
                #Grafica los mismos vectores que GrafFuerzas, y adicionalmente n vectores de momentos
                # las coordenadas de la n-ésima cola (de vector momento )son las posiciones 1,2,3 de la fila n de Dis
                # las coordenadas de la n-ésima cabeza son las posiciones 0,1,2 de la fila n de Mom
                fig3 = plt.figure(figsize=(10,10)) #   fig = plt.figure(figsize=(15,15))
                ax3 = fig3.add_subplot(111, projection='3d')


                ax3.plot(Dis[:,1], Dis[:,2], Dis[:,3], 'o', markersize=10, color='green', alpha=0.5)
                ax3.plot(Fuer[:,1], Fuer[:,2], Fuer[:,3], 'o', markersize=10, color='red', alpha=0.5)
                ax3.plot(Mom[:,0], Mom[:,1], Mom[:,2], 'o', markersize=10, color='blue', alpha=0.5)
                

                for i in range(Dis.shape[0]):
                    if(i==0):
                        ax3.plot([Dis[i,1], Mom[i,0]], [Dis[i,2], Mom[i,1]], [Dis[i,3], Mom[i,2]], color='blue', alpha=0.8, lw=3, label="Momentos")
                        ax3.plot([Dis[i,1], 0], [Dis[i,2], 0], [Dis[i,3], 0], color='green', alpha=0.8, lw=3, label="Posiciones")
                        ax3.plot([Dis[i,1], Fuer[i,1]], [Dis[i,2], Fuer[i,2]], [Dis[i,3], Fuer[i,3]], color='red', alpha=0.8, lw=3, label="Fuerzas")
                    else: 
                        ax3.plot([Dis[i,1], Mom[i,0]], [Dis[i,2], Mom[i,1]], [Dis[i,3], Mom[i,2]], color='blue', alpha=0.8, lw=3)
                        ax3.plot([Dis[i,1], 0], [Dis[i,2], 0], [Dis[i,3], 0], color='green', alpha=0.8, lw=3)
                        ax3.plot([Dis[i,1], Fuer[i,1]], [Dis[i,2], Fuer[i,2]], [Dis[i,3], Fuer[i,3]], color='red', alpha=0.8, lw=3)
                ax3.legend()
                ax3.set_xlabel('x')
                ax3.set_ylabel('y')
                ax3.set_zlabel('z')
                
                plt.title('Vectores de posición, momento y fuerza')
                ventana3=Tk()
                ventana3.geometry('700x325')
                ventana3.minsize(width=750,height=325)
                frame3=Frame(ventana3,bg='blue')
                frame3.grid()
                canvas=FigureCanvasTkAgg(fig3,master= frame3)
                canvas.draw()
                canvas.get_tk_widget().grid(column=0,row=0)
                ventana3.mainloop()               
                
                #plt.draw()
                #plt.show()

            def MomEquiv(mEquiv,fEquiv,ProyX,ProyY):
                #Grafica los vectores mEquiv,fEquiv,ProyPar,ProyPer. Los últimos dos son las descomposiciones perpendicular y paralela a fEquiv del vector mEquiv
                fig4 = plt.figure(figsize=(15,10)) #   fig = plt.figure(figsize=(15,15))
                ax4 = fig4.add_subplot(111, projection='3d')


                ax4.plot([mEquiv[0],0], [mEquiv[1],0], [mEquiv[2],0], markersize=10, color='green', label='Momento', alpha=0.5)
                ax4.plot([fEquiv[0],0], [fEquiv[1],0], [fEquiv[2],0], markersize=10, color='red', alpha=0.5,label="Fuerza")
                ax4.plot([ProyX[0],0], [ProyX[1],0], [ProyX[2],0], markersize=10, color='black', alpha=0.5,label="Proy. de momento paralela a fuerza")
                ax4.plot([ProyY[0],0], [ProyY[1],0], [ProyY[2],0], markersize=10, color='blue', alpha=0.5,label="Proy. de momento perpendicular a fuerza")

                ax4.legend()
                ax4.set_xlabel('x')
                ax4.set_ylabel('y')
                ax4.set_zlabel('z')


                
                plt.title('Momento y fuerza resultantes')
                
                ventana4=Tk()
                ventana4.geometry('700x325')
                ventana4.minsize(width=750,height=325)
                frame4=Frame(ventana4,bg='blue')
                frame4.grid()
                canvas=FigureCanvasTkAgg(fig4,master= frame4)
                canvas.draw()
                canvas.get_tk_widget().grid(column=0,row=0)
                ventana4.mainloop()               
                
                #plt.draw()
                #plt.show()

            def puntoRes(interx,intery,interz):
                #Grafica los puntos interx,intery e interz, cada uno es la intersección con el eje que lleva su nombre
                fig5 = plt.figure(figsize=(13,10)) #   fig = plt.figure(figsize=(15,15))
                ax5 = fig5.add_subplot(111, projection='3d')

                

                ax5.plot([interx[0]], [interx[1]], [0], 'o', markersize=10, color='green', alpha=0.5,label= "Intersección eje z")
                ax5.plot([intery[0]], [0], [intery[1]], 'o', markersize=10, color='red', alpha=0.5,label= "Intersección eje y")
                ax5.plot([0], [interz[0]], [interz[1]], 'o', markersize=10, color='yellow', alpha=0.5,label= "Intersección eje x")

                ax5.legend()
                ax5.set_xlabel('x')
                ax5.set_ylabel('y')
                ax5.set_zlabel('z')
                plt.title('Puntos de anulación del momento perpendicular')
                
                ventana5=Tk()
                ventana5.geometry('700x325')
                ventana5.minsize(width=750,height=325)
                frame5=Frame(ventana5,bg='blue')
                frame5.grid()
                canvas=FigureCanvasTkAgg(fig5,master= frame5)
                canvas.draw()
                canvas.get_tk_widget().grid(column=0,row=0)
                ventana5.mainloop()               
                #plt.draw()
                #plt.show()


            GrafFuerzas(Exe6[0],Exe6[1])
            GrafMomen(Exe6[2],Exe6[1],Exe6[0])
            MomEquiv(Exe6[4],Exe6[3],Exe6[5],Exe6[6])

            IndexS = Exe6[7]
            puntoRes(IndexS[0],IndexS[1],IndexS[2])
        
        
        Graficacion()


    def create_widgets(self):

        #Fondos
        FrameP = Frame(self, bg="red")
        FrameP.place(x=0,y=0,width=500, height=170) 
        FrameF = Frame(self,bg="orange" )
        FrameF.place(x=500,y=0,width=1280, height=170) 
        FrameG = Frame(self,bg="darkgreen" )
        FrameG.place(x=0,y=170,width=1280, height=550) 
        

#####################################################################################################################################################################################
        
        #Entrada de datos
        #Posicion
        lbl_typepos = Label(FrameP,text="Type")
        lbl_typepos.place(x=40,y=5)        
        

        lbl_xpos = Label(FrameP,text="x coordenate")
        lbl_xpos.place(x=130,y=5)        
        self.txtxpos = Entry(FrameP)
        self.txtxpos.place(x=145,y=25,width=50, height=20)  

        lbl_ypos = Label(FrameP,text="y coordenate")
        lbl_ypos.place(x=250,y=5)        
        self.txtypos = Entry(FrameP)
        self.txtypos.place(x=265,y=25,width=50, height=20) 

        lbl_zpos = Label(FrameP,text="z coordenate")
        lbl_zpos.place(x=370,y=5)        
        self.txtzpos = Entry(FrameP)
        self.txtzpos.place(x=385,y=25,width=50, height=20) 

        
        #Fuerza
        lbl_tyforce = Label(FrameF,text="Type")
        lbl_tyforce.place(x=40,y=5)        

        lbl_xforce = Label(FrameF,text="x coordenate")
        lbl_xforce.place(x=185,y=5)        
        self.txt_xforce = Entry(FrameF)
        self.txt_xforce.place(x=200,y=25,width=50, height=20)  
        
        lbl_yforce = Label(FrameF,text="y coordenate")
        lbl_yforce.place(x=325,y=5)        
        self.txt_yforce = Entry(FrameF)
        self.txt_yforce.place(x=340,y=25,width=50, height=20)  

        lbl_zforce = Label(FrameF,text="z coordenate")
        lbl_zforce.place(x=455,y=5)        
        self.txt_zforce = Entry(FrameF)
        self.txt_zforce.place(x=470,y=25,width=50, height=20)  

        lbl_mforce = Label(FrameF,text="Magnitude")
        lbl_mforce.place(x=590,y=5)        
        self.txt_mforce = Entry(FrameF)
        self.txt_mforce.place(x=600,y=25,width=50, height=20)  


        lbl_Titlep = Label(FrameG,text="Positions")
        lbl_Titlep.place(x=200,y=10)   

        lbl_Titlep = Label(FrameG,text="Forces")
        lbl_Titlep.place(x=570,y=10)   

        lbl_Titlep = Label(FrameG,text="Moment")
        lbl_Titlep.place(x=1000,y=10)   
        
        lbl_Titlep = Label(FrameG,text="Proyection ll & T")
        lbl_Titlep.place(x=550,y=300)   

        lbl_Titlep = Label(FrameG,text="Intersection when MT = 0")
        lbl_Titlep.place(x=530,y=400)   


        
########################################################################################################################################################################################
        
        #Botones

        self.btnAdd=Button(FrameP,text="Add Position and Force", command=self.CValues, bg="black", fg="white")
        self.btnAdd.place(x=200,y=70,width=150, height=30 )

        self.btnGen=Button(FrameF,text="Generate", command=self.GenWrench, bg="black", fg="white")
        self.btnGen.place(x=300,y=70,width=150, height=30 )

        #tipos de entrada de posicion
        Opcion = IntVar()
        R0 = Radiobutton(FrameP, text="C Cartesianas", variable=Opcion, value=1,command=self.TP0,bg = "red")
        R0.place(x = 10, y = 30)

        R1 = Radiobutton(FrameP, text="C Cilindricas", variable=Opcion, value=2,command=self.TP1,bg = "red")
        R1.place(x = 10, y = 50)

        R2 = Radiobutton(FrameP, text="C Esfericas", variable=Opcion, value=3,command=self.TP2,bg = "red")
        R2.place(x = 10, y = 70)


        #tipos de entrada de fuerza
        Opcion2 = IntVar()
        RF0 = Radiobutton(FrameF, text="C Cartesianas", variable=Opcion2, value=1,bg = "orange",command=self.TF0)
        RF0.place(x = 10, y = 30)

        RF1 = Radiobutton(FrameF, text="C Cilindricas", variable=Opcion2, value=2,bg = "orange",command=self.TF1)
        RF1.place(x = 10, y = 50)

        RF2 = Radiobutton(FrameF, text="C Esfericas", variable=Opcion2, value=3,bg = "orange",command=self.TF2)
        RF2.place(x = 10, y = 70)

        RF3 = Radiobutton(FrameF, text="Vector Director Cartesiano y Magnitud", variable=Opcion2, value=4,bg = "orange",command=self.TF3)
        RF3.place(x = 10, y = 90)

        RF4 = Radiobutton(FrameF, text="Vector Director Cilindrico y Magnitud", variable=Opcion2, value=5,bg = "orange",command=self.TF4)
        RF4.place(x = 10, y = 110)

        RF5 = Radiobutton(FrameF, text="Vector Director Esferico y Magnitud", variable=Opcion2, value=6,bg = "orange",command=self.TF5)
        RF5.place(x = 10, y = 130)



        
        


        


        

###########################################################################################################################################################################################


        #Grids

                #Grid Posicion
        self.gridp = ttk.Treeview(self, columns=("col1","col2","col3"))        
        self.gridp.column("#0",width=50)
        self.gridp.column("col1",width=60, anchor=CENTER)
        self.gridp.column("col2",width=60, anchor=CENTER)
        self.gridp.column("col3",width=60, anchor=CENTER)    
        self.gridp.heading("#0", text="Type", anchor=CENTER)
        self.gridp.heading("col1", text="X", anchor=CENTER)
        self.gridp.heading("col2", text="Y", anchor=CENTER)
        self.gridp.heading("col3", text="Z", anchor=CENTER)     
        self.gridp.place(x=100,y=205,width=230, height=250)
        
        
        
        #Grid Fuerza
        self.gridf = ttk.Treeview(self, columns=("col1","col2","col3","col4"))        
        self.gridf.column("#0",width=50)
        self.gridf.column("col1",width=60, anchor=CENTER)
        self.gridf.column("col2",width=60, anchor=CENTER)
        self.gridf.column("col3",width=60, anchor=CENTER) 
        self.gridf.column("col4",width=60, anchor=CENTER)   
        self.gridf.heading("#0", text="Type", anchor=CENTER)
        self.gridf.heading("col1", text="X", anchor=CENTER)
        self.gridf.heading("col2", text="Y", anchor=CENTER)
        self.gridf.heading("col3", text="Z", anchor=CENTER)     
        self.gridf.heading("col4", text="Magn", anchor=CENTER) 
        self.gridf.place(x=450,y=205,width=290, height=250)

        

        #Grid Momentos
        self.gridm = ttk.Treeview(self, columns=("col1","col2","col3"))        
        self.gridm.column("#0",width=50)
        self.gridm.column("col1",width=60, anchor=CENTER)
        self.gridm.column("col2",width=60, anchor=CENTER)
        self.gridm.column("col3",width=60, anchor=CENTER)    
        self.gridm.heading("#0", text="Type", anchor=CENTER)
        self.gridm.heading("col1", text="X", anchor=CENTER)
        self.gridm.heading("col2", text="Y", anchor=CENTER)
        self.gridm.heading("col3", text="Z", anchor=CENTER)     
        self.gridm.place(x=900,y=205,width=230, height=250)


        #Grid Resultantes
        self.gridr = ttk.Treeview(self, columns=("col1","col2","col3","col4"))        
        self.gridr.column("#0",width=50)
        self.gridr.column("col1",width=250, anchor=CENTER)
        self.gridr.column("col2",width=250, anchor=CENTER)
        self.gridr.column("col3",width=250, anchor=CENTER) 
        self.gridr.column("col4",width=250, anchor=CENTER)   
        self.gridr.heading("#0", text="Type", anchor=CENTER)
        self.gridr.heading("col1", text="Total Force", anchor=CENTER)
        self.gridr.heading("col2", text=" Total Moment", anchor=CENTER)
        self.gridr.heading("col3", text="Moment ll", anchor=CENTER)     
        self.gridr.heading("col4", text="Moment T", anchor=CENTER) 
        self.gridr.place(x=100,y=500,width=1050, height=50)


        #Grid Posiciones
        self.grids = ttk.Treeview(self, columns=("col1","col2","col3"))        
        self.grids.column("#0",width=80)
        self.grids.column("col1",width=120, anchor=CENTER)
        self.grids.column("col2",width=120, anchor=CENTER)
        self.grids.column("col3",width=120, anchor=CENTER)    
        self.grids.heading("#0", text="Type", anchor=CENTER)
        self.grids.heading("col1", text="X", anchor=CENTER)
        self.grids.heading("col2", text="Y", anchor=CENTER)
        self.grids.heading("col3", text="Z", anchor=CENTER)     
        self.grids.place(x=350,y=600,width=440, height=100)



def main():
    root = Tk()
    root.wm_title("Wrench Generator")
    app = Ventana(root) 
    app.mainloop()

main()  