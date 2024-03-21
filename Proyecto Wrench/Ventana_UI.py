from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


tamaño = [14,48,31,5,45]

fig, axs = plt.subplots(1,2, dpi = 80, figsize=(13,4), sharey = True, facecolor = "gray")

axs[0].plot(tamaño, color = "blue")
axs[1].plot(tamaño, color = "blue")



class Ventana(Frame):
       
    def __init__(self, master=None):
        super().__init__(master,width=1920, height=1080)
        self.master = master
        self.pack()
        self.create_widgets()

    def Exe(self):
        print("se ejecuta el boton")

    def create_widgets(self):

        #Fondos
        FrameP = Frame(self, bg="red")
        FrameP.place(x=0,y=0,width=400, height=100) 
        FrameF = Frame(self,bg="orange" )
        FrameF.place(x=400,y=0,width=500, height=100) 
        FrameG = Frame(self,bg="darkgreen" )
        FrameG.place(x=0,y=100,width=900, height=620) 
        Frameplt = Frame(self,bg="gray" )
        Frameplt.place(x=900,y=0,width=680, height=720) 

#####################################################################################################################################################################################
        
        #Entrada de datos
        #Posicion
        lbl_typepos = Label(FrameP,text="Type")
        lbl_typepos.place(x=25,y=5)        
        self.txt_typepos = Entry(FrameP)
        self.txt_typepos.place(x=15,y=25,width=50, height=20) 

        lbl_xpos = Label(FrameP,text="x coordenate")
        lbl_xpos.place(x=85,y=5)        
        self.txtxpos = Entry(FrameP)
        self.txtxpos.place(x=100,y=25,width=50, height=20)  

        lbl_ypos = Label(FrameP,text="y coordenate")
        lbl_ypos.place(x=185,y=5)        
        self.txtypos = Entry(FrameP)
        self.txtypos.place(x=200,y=25,width=50, height=20) 

        lbl_zpos = Label(FrameP,text="z coordenate")
        lbl_zpos.place(x=285,y=5)        
        self.txtzpos = Entry(FrameP)
        self.txtzpos.place(x=300,y=25,width=50, height=20) 

        
        #Fuerza
        lbl_xforce = Label(FrameF,text="Type")
        lbl_xforce.place(x=15,y=5)        
        self.txtxforce = Entry(FrameF)
        self.txtxforce.place(x=5,y=25,width=50, height=20)  

        lbl_xforce = Label(FrameF,text="x coordenate")
        lbl_xforce.place(x=85,y=5)        
        self.txtxforce = Entry(FrameF)
        self.txtxforce.place(x=100,y=25,width=50, height=20)  
        
        lbl_xforce = Label(FrameF,text="x coordenate")
        lbl_xforce.place(x=185,y=5)        
        self.txtxforce = Entry(FrameF)
        self.txtxforce.place(x=200,y=25,width=50, height=20)  

        lbl_xforce = Label(FrameF,text="x coordenate")
        lbl_xforce.place(x=285,y=5)        
        self.txtxforce = Entry(FrameF)
        self.txtxforce.place(x=300,y=25,width=50, height=20)  

        lbl_xforce = Label(FrameF,text="Magnitude")
        lbl_xforce.place(x=385,y=5)        
        self.txtxforce = Entry(FrameF)
        self.txtxforce.place(x=390,y=25,width=50, height=20)  


        
########################################################################################################################################################################################
        
        #Botones

        self.btnAdd=Button(FrameP,text="Add Position and Force", command=self.Exe, bg="black", fg="white")
        self.btnAdd.place(x=25,y=50,width=150, height=30 )

        self.btnGen=Button(FrameF,text="Generate", command=self.Exe, bg="black", fg="white")
        self.btnGen.place(x=25,y=50,width=150, height=30 )

        

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
        self.gridp.place(x=50,y=150,width=230, height=250)

        self.gridp.insert("",END,text=0,values = ("0","sa",7588))#Es util pa un bucle
        
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
        self.gridf.place(x=300,y=150,width=290, height=250)

        self.gridf.insert("",END,text=0,values = (45,"sa","asa",7))#Es util pa un bucle
        

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
        self.gridm.place(x=600,y=150,width=230, height=250)

        self.gridm.insert("",END,text=0,values = ("0","sa",45))#Es util pa un bucle

        #Grid Resultantes
        self.gridr = ttk.Treeview(self, columns=("col1","col2","col3","col4"))        
        self.gridr.column("#0",width=50)
        self.gridr.column("col1",width=100, anchor=CENTER)
        self.gridr.column("col2",width=100, anchor=CENTER)
        self.gridr.column("col3",width=100, anchor=CENTER) 
        self.gridr.column("col4",width=100, anchor=CENTER)   
        self.gridr.heading("#0", text="Type", anchor=CENTER)
        self.gridr.heading("col1", text="Fuerza Total", anchor=CENTER)
        self.gridr.heading("col2", text="Momento Total", anchor=CENTER)
        self.gridr.heading("col3", text="Momento II", anchor=CENTER)     
        self.gridr.heading("col4", text="Momento T", anchor=CENTER) 
        self.gridr.place(x=50,y=450,width=450, height=50)

        self.gridr.insert("",END,text=0,values = (45,55445,"asa",7))#Es util pa un bucle


        #Grid Posiciones
        self.gridp = ttk.Treeview(self, columns=("col1","col2","col3"))        
        self.gridp.column("#0",width=50)
        self.gridp.column("col1",width=80, anchor=CENTER)
        self.gridp.column("col2",width=80, anchor=CENTER)
        self.gridp.column("col3",width=80, anchor=CENTER)    
        self.gridp.heading("#0", text="Type", anchor=CENTER)
        self.gridp.heading("col1", text="X", anchor=CENTER)
        self.gridp.heading("col2", text="Y", anchor=CENTER)
        self.gridp.heading("col3", text="Z", anchor=CENTER)     
        self.gridp.place(x=550,y=450,width=290, height=150)

    ###########################################################################################################
        #graficas
        canvas = FigureCanvasTkAgg(fig,master = Frameplt)
        canvas.draw()
        canvas.get_tk_widget().grid(column=0,row=0,columnspan=2)

        
        







    





def main():
    root = Tk()
    root.wm_title("Wrench Generator")
    app = Ventana(root) 
    app.mainloop()

main()