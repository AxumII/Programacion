from kinetic_3d_analisys import RobotDOF_3D as r3d

def caso6gof(alpha_target=1.0, m_load=0):
    
    m_5840_31zy = 360/1000
    m_jgy370 = 170/1000

    m_gripper = 150/1000   

    robot_def = [
        {'axis': 'z', 'offset': [0.15, 0, 0],       'm_servo': m_jgy370, 'm_link': 0.1, 'com_link': [0, 0, 0.05], 't_rated':21.0 },
        {'axis': 'y', 'offset': [0, 0, 0.25],    'm_servo': m_5840_31zy, 'm_link': 60/100, 'com_link': [0.05, 0, 0], 't_rated': 60.0},
        {'axis': 'y', 'offset': [0.20, 0, 0],    'm_servo': m_jgy370, 'm_link': 30/1000, 'com_link': [0.07, 0, 0], 't_rated': 21.0},
        {'axis': 'x', 'offset': [0.07, 0, 0],    'm_servo': m_jgy370, 'm_link': 30/1000, 'com_link': [0.02, 0, 0], 't_rated': 21.0},
        {'axis': 'y', 'offset': [0.07, 0, 0],       'm_servo': m_jgy370,         'm_link': 20/1000, 'com_link': [0.02, 0, 0], 't_rated': 21.0},
        {'axis': 'z', 'offset': [0.07, 0, 0.0],     'm_servo': m_jgy370,         'm_link': m_gripper, 'com_link': [0, 0, 0.02], 't_rated': 21.0}
    ]

    # Inicializamos con una aceleración que VAMOS A PROBAR (ej: 15 rad/s^2)
    arm_6dof = r3d(joints=robot_def, alpha_target=alpha_target, m_load=m_load)

    # Posición horizontal extrema
    arm_6dof.analyze_pose([0, 0, 0, 0, 0, 0])

    # Posición plegada
    #arm_6dof.analyze_pose([0, -45, 90, 0, -45, 0])
    
def caso6_pol_gof(alpha_target=1.0, m_load=0):
    
    m_5840_31zy = 360/1000
    m_jgy370 = 170/1000

    m_gripper = 150/1000   

    robot_def = [
        {'axis': 'z', 'offset': [0.15, 0, 0],       'm_servo': m_jgy370, 'm_link': 0.1, 'com_link': [0, 0, 0.05], 't_rated':21.0 },
        {'axis': 'y', 'offset': [0, 0, 0.25],    'm_servo': m_5840_31zy, 'm_link': 60/100 + m_jgy370, 'com_link': [0.05, 0, 0], 't_rated': 60.0},
        {'axis': 'y', 'offset': [0.20, 0, 0],    'm_servo': 20/1000, 'm_link': 30/1000, 'com_link': [0.07, 0, 0], 't_rated': 21.0},
        {'axis': 'x', 'offset': [0.07, 0, 0],    'm_servo': m_jgy370, 'm_link': 30/1000, 'com_link': [0.02, 0, 0], 't_rated': 21.0},
        {'axis': 'y', 'offset': [0.07, 0, 0],       'm_servo': m_jgy370,         'm_link': 20/1000, 'com_link': [0.02, 0, 0], 't_rated': 21.0},
        {'axis': 'z', 'offset': [0.07, 0, 0.0],     'm_servo': m_jgy370,         'm_link': m_gripper, 'com_link': [0, 0, 0.02], 't_rated': 21.0}
    ]

    # Inicializamos con una aceleración que VAMOS A PROBAR (ej: 15 rad/s^2)
    arm_6dof2 = r3d(joints=robot_def, alpha_target=alpha_target, m_load=m_load)

    # Posición horizontal extrema
    arm_6dof2.analyze_pose([0, 0, 0, 0, 0, 0])

    # Posición plegada
    #arm_6dof.analyze_pose([0, -45, 90, 0, -45, 0])

def caso4gof(alpha_target=1.0, m_load=0):
    m_5840_31zy = 400/1000
    m_jgy370 = 180/1000

    m_gripper = 100/1000   

    robot_def = [
        {'axis': 'z', 'offset': [0.15, 0, 0],    'm_servo': m_jgy370,   'm_link': 50/1000,  'com_link': [0, 0, 0.12], 't_rated': 21.0},
        {'axis': 'y', 'offset': [0, 0, 0.30],    'm_servo': m_5840_31zy,'m_link': 200/1000,  'com_link': [0.12, 0, 0], 't_rated': 70.0},
        {'axis': 'y', 'offset': [0.25, 0, 0],    'm_servo': m_jgy370,   'm_link': 150/1000,   'com_link': [0.05, 0, 0], 't_rated': 21.0},
        {'axis': 'y', 'offset': [0.12, 0, 0],     'm_servo': m_jgy370,   'm_link': 60/1000,  'com_link': [0.05, 0, 0], 't_rated': 21.0},
        {'axis': 'x', 'offset': [0.02, 0, 0.0],  'm_servo': 10/1000,    'm_link': m_gripper,'com_link': [0.02, 0, 0], 't_rated': 21.0}
    ]

    # Inicializamos con una aceleración que VAMOS A PROBAR (ej: 15 rad/s^2)
    arm_4dof = r3d(joints=robot_def, alpha_target=alpha_target, m_load=m_load)

    # Posición horizontal extrema
    arm_4dof.analyze_pose([0, 0, 0, 0, 0, 0])
    
"""
def caso4gof(alpha_target=1.0, m_load=0):
    m_servo_ds3240 = 58/1000   
    m_gripper = 100/1000   

    robot_def = [
        {'axis': 'z', 'offset': [0.015, 0, 0],    'm_servo': m_servo_ds3240 ,   'm_link': 50/1000,  'com_link': [0, 0, 0.075], 't_rated': 36.0},
        {'axis': 'y', 'offset': [0, 0, 0.1],      'm_servo': m_servo_ds3240 ,   'm_link': 50/1000,  'com_link': [0.05, 0, 0], 't_rated': 36.0},
        {'axis': 'y', 'offset': [0.07, 0, 0],     'm_servo': m_servo_ds3240 ,   'm_link': 30/1000,   'com_link':[0.07/2, 0, 0], 't_rated': 36.0},
        {'axis': 'y', 'offset': [0.05, 0, 0],     'm_servo': m_servo_ds3240 ,   'm_link': 20/1000,  'com_link': [0.01, 0, 0], 't_rated': 36.0},
        {'axis': 'y', 'offset': [0.014, 0, 0.0],   'm_servo': m_servo_ds3240 ,   'm_link': m_gripper,'com_link': [0.0, 0, 0], 't_rated': 0.0}
    ]

    arm_4dof = r3d(joints=robot_def, alpha_target=alpha_target, m_load=m_load)

    # Posición horizontal extrema
    arm_4dof.analyze_pose([0, 0, 0, 0, 0, 0])
"""
def caso4_pol_gof(alpha_target=1.0, m_load=0):
    m_5840_31zy = 400/1000
    m_jgy370 = 180/1000

    m_gripper = 200/1000   

    robot_def = [
        {'axis': 'z', 'offset': [0.15, 0, 0],    'm_servo': m_jgy370,   'm_link': 50/1000,  'com_link': [0, 0, 0.12], 't_rated': 21.0},
        {'axis': 'y', 'offset': [0, 0, 0.3],    'm_servo': m_5840_31zy,'m_link': 60/1000 + m_jgy370,  'com_link': [0.04, 0, 0], 't_rated': 60.0},
        {'axis': 'y', 'offset': [0.2, 0, 0],    'm_servo': 10/1000,    'm_link': 30/1000,  'com_link': [0.05, 0, 0], 't_rated': 21.0},
        {'axis': 'y', 'offset': [0.1, 0, 0],     'm_servo': m_jgy370,   'm_link': 20/1000,  'com_link': [0.05, 0, 0], 't_rated': 21.0},
        {'axis': 'y', 'offset': [0.07, 0, 0.0],  'm_servo': 10/1000,    'm_link': m_gripper,'com_link': [0.02, 0, 0], 't_rated': 21.0}
    ]

    # Inicializamos con una aceleración que VAMOS A PROBAR (ej: 15 rad/s^2)
    arm_4dof2 = r3d(joints=robot_def, alpha_target=alpha_target, m_load=m_load)

    # Posición horizontal extrema
    arm_4dof2.analyze_pose([0, 0, 0, 0, 0, 0])


def caso4_pol2_gof(alpha_target=1.0, m_load=0):
    m_5840_31zy = 400/1000
    m_jgy370 = 180/1000
    m_gripper = 200/1000   

    robot_def = [
        {'axis': 'z', 'offset': [0.15, 0, 0],    'm_servo': m_jgy370,   'm_link': 50/1000,  'com_link': [0, 0, 0.12], 't_rated': 21.0},
        {'axis': 'y', 'offset': [0, 0, 0.3],    'm_servo': m_5840_31zy,'m_link': 60/1000 ,  'com_link': [0.04, 0, 0], 't_rated': 60.0},
        {'axis': 'y', 'offset': [0.2, 0, 0],    'm_servo': m_jgy370,    'm_link': 30/1000 + m_jgy370,  'com_link': [0.05, 0, 0], 't_rated': 21.0},
        {'axis': 'y', 'offset': [0.1, 0, 0],     'm_servo': 0,   'm_link': 20/1000,  'com_link': [0.05, 0, 0], 't_rated': 21.0},
        {'axis': 'y', 'offset': [0.07, 0, 0.0],  'm_servo': 10/1000,    'm_link': m_gripper,'com_link': [0.02, 0, 0], 't_rated': 21.0}
    ]

    # Inicializamos con una aceleración que VAMOS A PROBAR (ej: 15 rad/s^2)
    arm_4dof2 = r3d(joints=robot_def, alpha_target=alpha_target, m_load=m_load)

    # Posición horizontal extrema
    arm_4dof2.analyze_pose([0, 0, 0, 0, 0, 0])


def caso2_pol_gof():

    m_jgy370 = 180/1000

    m_load = 20 /1000 
    
    m_polea = 15/1000
    
    m_aluminio = 60/1000
    
    m_PLA = 20/1000

    robot_def = [
        {'axis': 'z', 'offset': [0.15, 0, 0],       'm_servo': m_jgy370, 'm_link': 0.1, 'com_link': [0, 0, 0.05], 't_rated':1.0 },
        {'axis': 'y', 'offset': [0.2, 0, 0],    'm_servo': m_jgy370 * 2, 'm_link': m_aluminio + m_polea , 'com_link': [0.1, 0, 0], 't_rated': 1.0},
        {'axis': 'y', 'offset': [0.2, 0, 0],       'm_servo': 10/1000,         'm_link': m_aluminio, 'com_link': [0.1, 0, 0], 't_rated': 1.0},
    ]

    # Inicializamos con una aceleración que VAMOS A PROBAR (ej: 15 rad/s^2)
    arm_6dof = r3d(joints=robot_def, alpha_target=5.0, m_load=m_load)

    # Posición horizontal extrema
    arm_6dof.analyze_pose([0, 0, 0, 0, 0, 0])


def caso2gof():
    m_5840_31zy = 360/1000
    m_jgy370 = 180/1000

    m_gripper = 50/1000   
    m_load = 20 /1000 

    robot_def = [
        {'axis': 'z', 'offset': [0.15, 0, 0],       'm_servo': m_jgy370, 'm_link': 0.1, 'com_link': [0, 0, 0.05], 't_rated':1.0 },
        {'axis': 'y', 'offset': [0.2, 0, 0],    'm_servo': m_jgy370, 'm_link': 70/1000, 'com_link': [0.1, 0, 0], 't_rated': 1.0},
        {'axis': 'y', 'offset': [0.2, 0, 0],       'm_servo': m_jgy370,         'm_link': 70/1000, 'com_link': [0.1, 0, 0], 't_rated': 1.0},
    ]

    # Inicializamos con una aceleración que VAMOS A PROBAR (ej: 15 rad/s^2)
    arm_6dof = r3d(joints=robot_def, alpha_target=5.0, m_load=m_load)

    # Posición horizontal extrema
    arm_6dof.analyze_pose([0, 0, 0, 0, 0, 0])



<<<<<<< HEAD
#caso6gof(alpha_target=10, m_load=0.1)
#caso6_pol_gof(alpha_target=10, m_load=0.1)
caso4gof(alpha_target=10, m_load=0.2)
#caso4_pol_gof(alpha_target=10, m_load=0.1)
#caso4_pol2_gof(alpha_target=10, m_load=0.1)
=======











#caso6gof()
#caso6_pol_gof()
#caso4gof()
#caso4_pol_gof()
caso2_pol_gof()

>>>>>>> 4a6bc8aa7dc2dcbc004644f902c3895268dc5510

