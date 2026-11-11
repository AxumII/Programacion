import numpy as np

class Kinematic:
    def __init__(self, joints):
        """
        :param joints: Lista de diccionarios con 'axis', 'offset' y 'com_link'
        """
        self.joints = joints

    def _translation(self, offset):
        T = np.eye(4)
        T[:3, 3] = offset
        return T

    def _rot_x(self, theta):
        c, s = np.cos(theta), np.sin(theta)
        return np.array([
            [1, 0,  0, 0],
            [0, c, -s, 0],
            [0, s,  c, 0],
            [0, 0,  0, 1]
        ])

    def _rot_y(self, theta):
        c, s = np.cos(theta), np.sin(theta)
        return np.array([
            [ c, 0, s, 0],
            [ 0, 1, 0, 0],
            [-s, 0, c, 0],
            [ 0, 0, 0, 1]
        ])

    def _rot_z(self, theta):
        c, s = np.cos(theta), np.sin(theta)
        return np.array([
            [c, -s, 0, 0],
            [s,  c, 0, 0],
            [0,  0, 1, 0],
            [0,  0, 0, 1]
        ])

    def calculate_kinematic(self, thetas):
        """
        Calcula toda la cinemática directa.
        :param thetas: Lista de ángulos articulares en radianes.
        :return: Diccionario con arrays de NumPy listos para usar.
        """
        T = np.eye(4)
        
        positions = []
        rot_axes = []      # Ejes de rotación en coordenadas globales
        com_positions = []
        T_matrices = []
        
        for i, joint in enumerate(self.joints):
            # 1. Trasladar al origen de la articulación actual usando el método local
            T = T @ self._translation(joint['offset'])
            
            # Guardar la posición (origen de la articulación)
            positions.append(T[:3, 3])
            
            # 2. Extraer el eje de rotación global y aplicar la rotación
            if joint['axis'] == 'x':
                rot_axes.append(T[:3, 0])
                T = T @ self._rot_x(thetas[i])
            elif joint['axis'] == 'y':
                rot_axes.append(T[:3, 1])
                T = T @ self._rot_y(thetas[i])
            elif joint['axis'] == 'z':
                rot_axes.append(T[:3, 2])
                T = T @ self._rot_z(thetas[i])
            else:
                raise ValueError(f"Eje no reconocido: {joint['axis']}")
            
            # 3. Guardar la matriz de transformación completa del frame actual
            T_matrices.append(T.copy())
            
            # 4. Calcular el Centro de Masas (desde el frame ya rotado)
            T_com = T @ self._translation(joint['com_link'])
            com_positions.append(T_com[:3, 3])
            
        # Posición final del extremo del robot
        p_tcp = T[:3, 3]
        
        return {
            'positions': np.array(positions),
            'rot_axes': np.array(rot_axes),
            'com_positions': np.array(com_positions),
            'p_tcp': p_tcp,
            'T_matrices': np.array(T_matrices)
        }