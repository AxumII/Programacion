import numpy as np
import matplotlib.pyplot as plt

def punto1():
    h = 0.2
    x = np.arange(0, 1 + h, h)
    u1_init = 1/10
    def dudx(x, u):
        return (np.exp(-2*x)) - 2*u

    usolve = eulersingle(x  = x, u1_init= u1_init, dudx = dudx)
    print(usolve)
    
def punto2():
    h = 0.2
    x = np.arange(0, 2 + h, h)
    u1_init = 1
    
    
    def du1dx(x,u1):
        return x**2 - u1
    
    def solve_analitic(x):
        return (-1* np.exp(-x)) + (x**2) - (2*x) + 2
    
    u1_num = rk4single(x = x, u1_init= u1_init, du1dx= du1dx)
    u1_an = solve_analitic(x = x)
    
    plt.plot(x,u1_num)
    plt.plot(x,u1_an)
    plt.grid()
    plt.show()
    
    print("u1_num", u1_num)
    print("u1_an", u1_an)
    
    ve= np.abs(u1_an - u1_num)
    print("vector error", ve)
    vu = np.sum(ve)
    print(vu)
    
def punto3():
    #resolver por diferencias finitas
    #x´´ = 
    pass
    
def punto4():
    h = 0.05
    x = np.arange(0, 1.2 + h, h)
    print(len(x))
    u1_init = 1
    u2_init = 1
    def du1dx(x, u1,u2):
        return -4*u1 +u2
    def du2dx(x, u1,u2):
        return u1 + u2
    
    u1,u2 = rk4_2s(x = x, u1_init= u1_init, u2_init= u2_init, du1dx= du1dx, du2dx=du2dx)
    print("Solucion u1",u1)
    print("Solucion u2",u2)
    print(len(u1))
    
    
    
    
    
    
def eulersingle(x,u1_init,dudx):
    
    def dudx(x, u):
        return ((np.exp(-2*x)) - 2*u)
    
    u = np.zeros_like(x)
    u[0] = u1_init
    h = x[1] - x[0]
    
     
    
    for i in range(len(x) - 1):
        
        f = dudx(x=x[i], u= u[i])        
       
        u_next = u[i] + h*f
        
        u[i+1] = u_next
        
        
    return u

def rk4single(x,u1_init,du1dx):
    u1 = np.zeros_like(x)
    u1[0] = u1_init
    h = x[1] - x[0]
    
    
    
    for i in range(len(x) - 1):
        
        k1 =du1dx(x[i], u1[i])

        k2 = du1dx(x[i] + (h/2), u1[i] + (h/2)*k1)

        k3 = du1dx(x[i] + (h/2), u1[i] + (h/2)*k2)

        k4 = du1dx(x[i] + h, u1[i] + h*k3 )      
        
        u1_next = u1[i] + (h/6)*(k1+2*k2+2*k3+k4)
        
        u1[i+1] = u1_next
       
        
    return u1

def rk4_2s(x, u1_init, u2_init,du1dx,du2dx):
    
    u1 = np.zeros_like(x)
    u2 = np.zeros_like(x)
    u1[0] = u1_init
    u2[0] = u2_init
    h = x[1] - x[0]
    
    
    
    for i in range(len(x) - 1):
        
        k1 =du1dx(x[i], u1[i], u2[i])
        j1 =du2dx(x[i], u1[i], u2[i])

        k2 = du1dx(x[i] + (h/2), u1[i] + (h/2)*k1, u2[i] + (h/2)*j1)
        j2 = du2dx(x[i] + (h/2), u1[i] + (h/2)*k1, u2[i] + (h/2)*j1)

        k3 = du1dx(x[i] + (h/2), u1[i] + (h/2)*k2, u2[i] + (h/2)*j2)
        j3 = du2dx(x[i] + (h/2), u1[i] + (h/2)*k2, u2[i] + (h/2)*j2)

        k4 = du1dx(x[i] + h, u1[i] + h*k3, u2[i] + h*j3)
        j4 = du2dx(x[i] + h, u1[i] + h*k3, u2[i] + h*j3)
        
        
        u1_next = u1[i] + (h/6)*(k1+2*k2+2*k3+k4)
        u2_next = u2[i] + (h/6)*(j1+2*j2+2*j3+j4)
        
        u1[i+1] = u1_next
        u2[i+1] = u2_next
        
    return u1,u2

#punto1()
punto4()
#punto2()