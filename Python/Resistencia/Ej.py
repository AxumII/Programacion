import sympy as sp
import sympy.plotting as syp

def ej(mb, md, L, k):
    theta = sp.Symbol('theta')
    g = 9.81  
    
    # Definimos las ecuaciones
    em1 = (1/2) * mb * g * L * sp.sin(sp.rad(50)) + (1/2) * k * L**2 * sp.sin(sp.rad(50))**2
    
    wb = sp.sqrt((2 * em1 - (mb * g * L * sp.sin(theta) + k * L**2 * sp.sin(theta)**2)) / ((8 * mb * L**2 + 9 * md * L**2 * sp.sin(theta)**2) / 24))
    
    # Graficamos la ecuación wb respecto a theta
    syp.plot(wb, (theta, 0, sp.pi), title='Gráfica de wb en función de θ (rad)', ylabel='wb', xlabel='θ (rad)')
    syp.plot(wb.subs(theta, sp.rad(theta)), (theta, 0, 90), title='Gráfica de wb en función de θ (deg)', ylabel='wb', xlabel='θ (deg)')

ej(mb=4, md=5, L=0.32, k=400)
