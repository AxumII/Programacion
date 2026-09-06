from kinetic_3d_analisys import RobotDOF_3D as r3d

# Constantes de longitud (m)
L1, L2, L3, L4 = 0.132, 0.3043, 0.218, 0.103
# Constantes de offset lateral (m)
W1, W2, W3, W4 = 0.00475, -0.027, -0.030, -0.003

def caso4gof(alpha_target=1.0, m_load=0):
    m_5840_31zy = 400/1000
    m_jgy370 = 180/1000

    robot_def = [
        {'axis': 'z', 'offset': [W1, 0.0, L1], 'm_servo': m_jgy370,   'm_link': 50/1000,  'com_link': [0, 0, L1/2],  't_rated': 21.0},
        {'axis': 'y', 'offset': [L2, W2, 0.0], 'm_servo': m_5840_31zy,'m_link': 200/1000, 'com_link': [L2/2, 0, 0], 't_rated': 70.0},
        {'axis': 'y', 'offset': [L3, W3, 0.0], 'm_servo': m_jgy370,   'm_link': 150/1000, 'com_link': [L3/2, 0, 0], 't_rated': 21.0},
        {'axis': 'y', 'offset': [L4, W4, 0.0], 'm_servo': m_jgy370,   'm_link': 60/1000,  'com_link': [L4/2, 0, 0], 't_rated': 21.0}
    ]

    arm_4dof = r3d(joints=robot_def, alpha_target=alpha_target, m_load=m_load)
    arm_4dof.analyze_pose([45.0, 30.0, -30.0, -45.0])

def caso4_pol_gof(alpha_target=1.0, m_load=0):
    m_5840_31zy = 400/1000
    m_jgy370 = 180/1000
    m_gripper = 200/1000   

    robot_def = [
        {'axis': 'z', 'offset': [W1, 0.0, L1], 'm_servo': m_jgy370,   'm_link': 50/1000,            'com_link': [0, 0, L1/2],  't_rated': 21.0},
        {'axis': 'y', 'offset': [L2, W2, 0.0], 'm_servo': m_5840_31zy,'m_link': 60/1000 + m_jgy370, 'com_link': [L2/2, 0, 0], 't_rated': 60.0},
        {'axis': 'y', 'offset': [L3, W3, 0.0], 'm_servo': 10/1000,    'm_link': 30/1000,            'com_link': [L3/2, 0, 0], 't_rated': 21.0},
        {'axis': 'y', 'offset': [L4, W4, 0.0], 'm_servo': m_jgy370,   'm_link': m_gripper,          'com_link': [L4/2, 0, 0], 't_rated': 21.0}
    ]

    arm_4dof2 = r3d(joints=robot_def, alpha_target=alpha_target, m_load=m_load)
    arm_4dof2.analyze_pose([0, 0, 0, 0])

def caso2_pol_gof():
    m_jgy370 = 180/1000
    m_load = 20 /1000 
    m_polea = 15/1000
    m_aluminio = 60/1000

    robot_def = [
        {'axis': 'z', 'offset': [W1, 0.0, L1], 'm_servo': m_jgy370,     'm_link': 0.1,               'com_link': [0, 0, L1/2],  't_rated': 1.0},
        {'axis': 'y', 'offset': [L2, W2, 0.0], 'm_servo': m_jgy370 * 2, 'm_link': m_aluminio + m_polea, 'com_link': [L2/2, 0, 0], 't_rated': 1.0},
        {'axis': 'y', 'offset': [L3, W3, 0.0], 'm_servo': 10/1000,      'm_link': m_aluminio,        'com_link': [L3/2, 0, 0], 't_rated': 1.0},
    ]

    arm_2dof = r3d(joints=robot_def, alpha_target=5.0, m_load=m_load)
    arm_2dof.analyze_pose([0, 0, 0])

def caso2gof():
    m_jgy370 = 180/1000
    m_load = 20 /1000 

    robot_def = [
        {'axis': 'z', 'offset': [W1, 0.0, L1], 'm_servo': m_jgy370, 'm_link': 0.1,     'com_link': [0, 0, L1/2],  't_rated': 1.0},
        {'axis': 'y', 'offset': [L2, W2, 0.0], 'm_servo': m_jgy370, 'm_link': 70/1000, 'com_link': [L2/2, 0, 0], 't_rated': 1.0},
        {'axis': 'y', 'offset': [L3, W3, 0.0], 'm_servo': m_jgy370, 'm_link': 70/1000, 'com_link': [L3/2, 0, 0], 't_rated': 1.0},
    ]

    arm_2dof = r3d(joints=robot_def, alpha_target=5.0, m_load=m_load)
    arm_2dof.analyze_pose([0, 0, 0])


if __name__ == "__main__":
    caso4gof(alpha_target=10, m_load=0.2)