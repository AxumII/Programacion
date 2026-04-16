#ifndef Kinematic_H
#define Kinematic_H
#include <Arduino.h>
#include <ArduinoEigenDense.h>

class Kinematic {
    private: 
        float l1, l2, l3;
        float w1, w2, w3;
        using V1x3 = Eigen::Vector3f;
        using M4x4 = Eigen::Matrix4f;
        int toolType;
        float lTool, wTool, theta4, phi;
        int p2atype;

    public:
        Kinematic(float _l1, float _l2, float _l3, 
                     float _w1, float _w2, float _w3, 
                     int _toolType, float _lTool, float _wTool, float _thetaTool = 0.0, float* _phi) ;
        bool pos2Angle(float x, float y, float z, float &th1, float &th2, float &th3);
        bool angle2Pos(float theta1, float theta2, float theta3, M4x4 &resMatrix);
        M4x4 getDH(float theta, float alpha, float d, float a);
};


#endif