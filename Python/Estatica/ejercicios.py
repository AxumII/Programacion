import numpy as np
from structures import Structures as st
from vectorObject import Vector_Object as vt
from wrench import Wrench as wr
from rigidCalculator import Rigid_Static_Calculator as rsc
from graf import Graphication as graph  




#x,y,z, en el libro seria i,k,j
#Ejercicio 3.140
    
def ej3140():
    structures = st()
    var = 1
    P = 10
    A = vt(coords=[0 , 18*var, 0])
    B = vt(coords=[0 , 0 , 24*var])
    C = vt(coords=[15*var, 0, 0])
    D = vt(coords=[0 , 0 , 20*var])
    E = vt(coords=[-9*var, -12*var, 0 ])


    structures.add_distance(A)
    structures.add_distance(C)
    structures.add_distance(E)


    dir1 =  vt(coords=[np.subtract(A.get_coords(), B.get_coords())]) #A-B
    dir2 =  vt(coords=[np.subtract(C.get_coords(), D.get_coords())]) #C-D
    dir3 =  vt(coords=[np.subtract(E.get_coords(), D.get_coords())]) #E-D


    f1 = vt(coords= dir1.get_angles()*P, next = A )
    f2 = vt(coords= dir2.get_angles()*P, next = C )
    f3 = vt(coords= dir3.get_angles()*P, next = E )

    structures.add_force(f1)
    structures.add_force(f2)
    structures.add_force(f3)


    calculator = rsc(structures)
    calculator.clasif()
    structures.calculate_totals()


    ######################################################################
    # Verificar resultados
    print("\nDistArray:")
    for dist in structures.distArray:
        print(dist.get_coords())

    print("\nForceArray:")
    for force in structures.forceArray:
        print(force.get_coords())

    print("\nTotalForceArray:")
    for force in structures.totalforce:
        print(force.get_coords())

    print("\nMomentArray:")
    for moment in structures.momentArray:
        print(moment.get_coords())

    print("\nTotalMomentArray:")
    for moment in structures.totalmoment:
        print(moment.get_coords())

    structures.sum_f_m()
    print("\nSumas:")
    print("Total F:", structures.totalSumForce, "\n")
    print("Total M", structures.totalSumMoment, "\n")
    TotalF =structures.totalSumForce
    TotalM =structures.totalSumMoment

    ###########################################################################
    print(TotalM,TotalF)
    wrt = wr(TotalF,TotalM)
    wrt.positions
    valid_positions = wrt.verify_positions()  # Asegúrate de invocar el método con paréntesis
    print("Momento T, objetivo ",wrt.TMoment, "\n")
    print(f"Posiciones Validadas: {valid_positions}\n")


#ej3140()

def ej3139():
    structures = st()
    
    #x horizontal, y verticual, z horizontal

    A = vt(coords=[0 , 0, 12])
    B = vt(coords=[9 , 0, 0])


    C = vt(coords=[6, 2, 9])
    D = vt(coords=[14 , 2 , 5])
    
    IF1I = 1650
    IF2I = 1500

    structures.add_distance(A)
    structures.add_distance(B)


    f1 = vt(coords= C.get_angles()*IF1I, next = A )
    f2 = vt(coords= D.get_angles()*IF2I, next = B )

    structures.add_force(f1)
    structures.add_force(f2)


    calculator = rsc(structures)
    calculator.clasif()
    structures.calculate_totals()


    ######################################################################
    # Verificar resultados
    print("\nDistArray:")
    for dist in structures.distArray:
        print(dist.get_coords())

    print("\nForceArray:")
    for force in structures.forceArray:
        print(force.get_coords())

    print("\nTotalForceArray:")
    for force in structures.totalforce:
        print(force.get_coords())

    print("\nMomentArray:")
    for moment in structures.momentArray:
        print(moment.get_coords())

    print("\nTotalMomentArray:")
    for moment in structures.totalmoment:
        print(moment.get_coords())

    structures.sum_f_m()
    print("\nSumas:")
    print("Total F:", structures.totalSumForce, "\n")
    print("Total M", structures.totalSumMoment, "\n")
    TotalF =structures.totalSumForce
    TotalM =structures.totalSumMoment

    ###########################################################################
    print(TotalM,TotalF)
    wrt = wr(TotalF,TotalM)
    wrt.positions
    valid_positions = wrt.verify_positions()  # Asegúrate de invocar el método con paréntesis
    print("Momento T, objetivo ",wrt.TMoment, "\n")
    print(f"Posiciones Validadas: {valid_positions}\n")

    print("Momento Paralelo",wrt.IIMoment)
    print("Momento Perpendicular",wrt.TMoment)


ej3139()