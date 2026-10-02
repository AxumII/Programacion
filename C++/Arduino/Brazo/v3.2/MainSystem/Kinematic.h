#ifndef Kinematic_H
#define Kinematic_H

#include <Arduino.h>
#include <ArduinoEigenDense.h>

#ifndef PI
#define PI 3.14159265358979323846
#endif

class Kinematic {
    private:
        float l1, l2, l3;
        float w1, w2, w3;
        float lTool, wTool, theta4_internal, phi;
        using M4x4 = Eigen::Matrix4f;

    public:
        using Matrix4f = Eigen::Matrix4f; 

        Kinematic(float _l1, float _l2, float _l3, 
                float _w1, float _w2, float _w3, 
                float _lTool = 0.0, float _wTool = 0.0, float _thetaTool = 0.0, float _phi = 0.0);
        
        // Cinemática Inversa
        bool pos2Angle(float x, float y, float z, float &th1, float &th2, float &th3, float theta4_in = 0.0);
        bool pos2Angle(float x, float y, float z, float &th1, float &th2, float &th3, float &th4, float phi_in);

        // Cinemática Directa
        bool angle2Pos(float theta1, float theta2, float theta3, M4x4 &resMatrix);
        bool angle2Pos(float theta1, float theta2, float theta3, float theta4, M4x4 &resMatrix);
        
        // Métodos TCP (Normativa)
        bool angle2TCP(float th1, float th2, float th3, float th4, M4x4 &resMatrix);
        bool TCP2angle(const M4x4 &tcpMatrix, float &th1, float &th2, float &th3, float &th4);

        M4x4 getDH(float theta, float alpha, float d, float a);
};

#endif