import numpy as np

p1 = 2.98
p2 = 4.5
p3 = 9.98
p4 = 4.49
p5 = 6.87

productos = np.array([p1,p2,p3,p4,p5])
ventas1 = np.array([10.0,18,36,0,10])
ventas2 = np.array([104.0,8,6,20,1])
ventas3 = np.array([37.0,2,10,210,7])






def ventasdias(productos,ventas):
    totalv = np.zeros_like(productos)
    for i in range(len(productos) - 1):
        
        prod = productos[i]
        v = ventas[i]
        totalv[i] = prod*v
        
        

    return np.sum(totalv)

dia1 = ventasdias(productos = productos,ventas=ventas1)
dia2 = ventasdias(productos = productos,ventas=ventas2)
dia3 = ventasdias(productos = productos,ventas=ventas3)

print("total",np.sum([dia1,dia2,dia3]))