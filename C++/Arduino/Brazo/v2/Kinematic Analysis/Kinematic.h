#ifndef Kinematic_H
#define Kinematic_H

#include <iostream>
#include <cmath>
#include <Eigen/Dense> // Cambio aquí para C++ estándar

#ifndef PI
#define PI 3.14159265358979323846
#endif

class Kinematic {
    private: 
        float l1, l2, l3;
        float w1, w2, w3;
        // Definimos M4x4 usando Eigen estándar
        using M4x4 = Eigen::Matrix4f;
        int toolType;
        float lTool, wTool, theta4;

    public:
        using Matrix4f = Eigen::Matrix4f; // Para acceso externo
        Kinematic(float _l1, float _l2, float _l3, 
                float _w1, float _w2, float _w3, 
                int _toolType = -1, float _lTool = 0.0, float _wTool = 0.0, float _thetaTool = 0.0);
        
        bool pos2Angle(float x, float y, float z, float &th1, float &th2, float &th3);
        bool angle2Pos(float theta1, float theta2, float theta3, M4x4 &resMatrix);
        M4x4 getDH(float theta, float alpha, float d, float a);
};

#endif