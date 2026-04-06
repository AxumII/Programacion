import numpy as np
import sympy as sp
import pandas as pd

class A:
    def __init__(self):
        pass
    
    def DH(self, theta, d, a, alpha):
        theta_rad = np.radians(theta)
        alpha_rad = np.radians(alpha)

        A = np.array([[np.cos(theta_rad), -np.sin(theta_rad) * np.cos(alpha_rad),  np.sin(theta_rad) * np.sin(alpha_rad), a * np.cos(theta_rad)],
                      [np.sin(theta_rad),  np.cos(theta_rad) * np.cos(alpha_rad), -np.cos(theta_rad) * np.sin(alpha_rad), a * np.sin(theta_rad)],
                      [0,                 np.sin(alpha_rad),                   np.cos(alpha_rad),                  d],
                      [0,                 0,                                    0,                                   1]])
        
        return A
    
    def symbolic_DH(self, theta, d, a, alpha):
        theta_rad = sp.rad(theta)
        alpha_rad = sp.rad(alpha)

        A = sp.Matrix([[sp.cos(theta_rad), -sp.sin(theta_rad) * sp.cos(alpha_rad),  sp.sin(theta_rad) * sp.sin(alpha_rad), a * sp.cos(theta_rad)],
                       [sp.sin(theta_rad),  sp.cos(theta_rad) * sp.cos(alpha_rad), -sp.cos(theta_rad) * sp.sin(alpha_rad), a * sp.sin(theta_rad)],
                       [0,                 sp.sin(alpha_rad),                   sp.cos(alpha_rad),                  d],
                       [0,                 0,                                    0,                                   1]])
        A = sp.trigsimp(A)
        A = sp.simplify(A)
        return A
    
    def MTH(self, theta_list, d_list, a_list, alpha_list):
        T = np.eye(4)
        for theta, d, a, alpha in zip(theta_list, d_list, a_list, alpha_list):
            A = self.DH(theta, d, a, alpha)
            T = np.dot(T, A)
        return np.round(T, decimals=2)
    
    def symbolic_MTH(self, theta_list, d_list, a_list, alpha_list):
        T = sp.eye(4)
        for theta, d, a, alpha in zip(theta_list, d_list, a_list, alpha_list):
            A = self.symbolic_DH(theta, d, a, alpha)
            T = T * A
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
    
if __name__ == "__main__":
    a = A()
    theta_num = [0, 56.09, -121.17]
    d_num = [0, 0, 0]
    a_num = [0, 106, 97]
    alpha_num = [90, 0, 0]
    
    theta_sym = sp.symbols('theta1 theta2 theta3')
    d_sym = sp.symbols('l1 w2 0')  
    a_sym = sp.symbols('w1 l2 l3')
    alpha_sym = sp.symbols('sp.pi/2 0 0')

    T = a.MTH(theta_num, d_num, a_num, alpha_num)
    print("Matriz de Transformación Homogénea:")
    print(T)

    symbolic_T = a.symbolic_MTH(theta_sym, d_sym, a_sym, alpha_sym)
    print("\nMatriz de Transformación Homogénea Simbólica:")
    print(sp.latex(symbolic_T))

    df = a.DH_df(theta_num, d_num, a_num, alpha_num)
    print("\nDataFrame de Parámetros DH:")
    print(df)

    symbolic_df = a.symbolic_DH_df(theta_sym, d_sym, a_sym, alpha_sym)
    print("\nDataFrame de Parámetros DH Simbólicos:")
    print(symbolic_df)