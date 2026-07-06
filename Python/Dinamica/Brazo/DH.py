import numpy as np
import sympy as sp
import pandas as pd
import matplotlib.pyplot as plt

class A:
    def __init__(self):
        pass
    
    def DH(self, theta, d, a, alpha):
        theta_rad = np.radians(theta)
        alpha_rad = np.radians(alpha)

        A_mat = np.array([[np.cos(theta_rad), -np.sin(theta_rad) * np.cos(alpha_rad),  np.sin(theta_rad) * np.sin(alpha_rad), a * np.cos(theta_rad)],
                      [np.sin(theta_rad),  np.cos(theta_rad) * np.cos(alpha_rad), -np.cos(theta_rad) * np.sin(alpha_rad), a * np.sin(theta_rad)],
                      [0,                 np.sin(alpha_rad),                   np.cos(alpha_rad),                  d],
                      [0,                 0,                                   0,                                  1]])
        
        return A_mat
    
    def symbolic_DH(self, theta, d, a, alpha):
        theta_rad = sp.rad(theta)
        alpha_rad = sp.rad(alpha)

        A_mat = sp.Matrix([[sp.cos(theta_rad), -sp.sin(theta_rad) * sp.cos(alpha_rad),  sp.sin(theta_rad) * sp.sin(alpha_rad), a * sp.cos(theta_rad)],
                       [sp.sin(theta_rad),  sp.cos(theta_rad) * sp.cos(alpha_rad), -sp.cos(theta_rad) * sp.sin(alpha_rad), a * sp.sin(theta_rad)],
                       [0,                 sp.sin(alpha_rad),                   sp.cos(alpha_rad),                  d],
                       [0,                 0,                                   0,                                  1]])
        A_mat = sp.trigsimp(A_mat)
        A_mat = sp.simplify(A_mat)
        return A_mat
    
    def MTH(self, theta_list, d_list, a_list, alpha_list):
        T = np.eye(4)
        for theta, d, a, alpha in zip(theta_list, d_list, a_list, alpha_list):
            A_mat = self.DH(theta, d, a, alpha)
            T = np.dot(T, A_mat)
        return np.round(T, decimals=2)
    
    def symbolic_MTH(self, theta_list, d_list, a_list, alpha_list):
        T = sp.eye(4)
        for theta, d, a, alpha in zip(theta_list, d_list, a_list, alpha_list):
            A_mat = self.symbolic_DH(theta, d, a, alpha)
            T = T * A_mat
        T = T.subs({sp.sin(0): 0, sp.cos(0): 1, sp.sin(sp.pi/2): 1, sp.cos(sp.pi/2): 0}).simplify()
        T = sp.trigsimp(T)
        T = sp.simplify(T)
        return T
    
    def DH_df(self, theta_list, d_list, a_list, alpha_list):
        df = pd.DataFrame({
            'theta': theta_list,
            'd': d_list,
            'a': a_list,
            'alpha': alpha_list
        })
        return df
    
    def symbolic_DH_df(self, theta_list, d_list, a_list, alpha_list):
        df = pd.DataFrame({
            'theta': theta_list,
            'd': d_list,
            'a': a_list,
            'alpha': alpha_list
        })
        return df

    # --- NUEVA FUNCIÓN DE GRAFICACIÓN ---
    def plot(self, theta_list, d_list, a_list, alpha_list):
        """Calcula los puntos intermedios y grafica el robot en 3D."""
        T = np.eye(4)
        
        # Iniciar en el origen (0,0,0)
        x_coords = [0.0]
        y_coords = [0.0]
        z_coords = [0.0]

        # Calcular transformaciones y guardar coordenadas de cada articulación
        for theta, d, a, alpha in zip(theta_list, d_list, a_list, alpha_list):
            A_mat = self.DH(theta, d, a, alpha)
            T = np.dot(T, A_mat)
            x_coords.append(T[0, 3])
            y_coords.append(T[1, 3])
            z_coords.append(T[2, 3])

        # Crear la figura 3D
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection='3d')
        
        # Trazar los eslabones (tramos) y los nodos (articulaciones)
        ax.plot(x_coords, y_coords, z_coords, '-o', linewidth=4, markersize=8, color='b', label='Eslabones')
        ax.plot([0], [0], [0], 'ro', markersize=10, label='Base') # Punto de la base

        # Ajustes visuales para que el gráfico no se distorsione
        max_range = np.array([max(x_coords)-min(x_coords), 
                              max(y_coords)-min(y_coords), 
                              max(z_coords)-min(z_coords)]).max() / 2.0
        
        mid_x = (max(x_coords) + min(x_coords)) * 0.5
        mid_y = (max(y_coords) + min(y_coords)) * 0.5
        mid_z = (max(z_coords) + min(z_coords)) * 0.5

        ax.set_xlim(mid_x - max_range, mid_x + max_range)
        ax.set_ylim(mid_y - max_range, mid_y + max_range)
        ax.set_zlim(mid_z - max_range, mid_z + max_range)

        # Etiquetas
        ax.set_xlabel('Eje X')
        ax.set_ylabel('Eje Y')
        ax.set_zlabel('Eje Z')
        ax.set_title('Configuración Espacial del Robot (Cinemática Directa)')
        ax.legend()
        
        plt.show()

if __name__ == "__main__":
    a_obj = A()
    
    theta_num = [0, 56.09, -121.17]
    d_num     = [0, 10, 0]
    a_num     = [7, 106, 97]
    alpha_num = [90, 0, 0]
    
    """theta_num = [  0,  0,  0,  0,  0, 0]
    d_num     = [265,  0,  0,470,101, 0]
    a_num     = [  0,444,110,  0, 80, 0]
    alpha_num = [-90,  0,-90, 90,-90, 0]
    """
    """theta_num = [  0,  0,  0,  0,  0, 0]
    d_num     = [265,  0,  0,470,  0,101]
    a_num     = [  0,444,110,  0,  0, 80]
    alpha_num = [ 90,  0,-90, 90,-90, 0]"""
    
    theta_sym = sp.symbols('theta1 theta2 theta3')
    d_sym = sp.symbols('l1 w2 0')  
    a_sym = sp.symbols('w1 l2 l3')
    alpha_sym = sp.symbols('sp.pi/2 0 0')

    T = a_obj.MTH(theta_num, d_num, a_num, alpha_num)
    print("Matriz de Transformación Homogénea:")
    print(T)

    """ 
    symbolic_T = a_obj.symbolic_MTH(theta_sym, d_sym, a_sym, alpha_sym)
    print("\nMatriz de Transformación Homogénea Simbólica:")
    print(sp.latex(symbolic_T))
    """
    df = a_obj.DH_df(theta_num, d_num, a_num, alpha_num)
    print("\nDataFrame de Parámetros DH:")
    print(df)

    symbolic_df = a_obj.symbolic_DH_df(theta_sym, d_sym, a_sym, alpha_sym)
    print("\nDataFrame de Parámetros DH Simbólicos:")
    print(symbolic_df)
    
    print("\nGenerando gráfico 3D...")
    a_obj.plot(theta_num, d_num, a_num, alpha_num)