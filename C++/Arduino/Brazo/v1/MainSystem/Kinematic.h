#ifndef Kinematic_H
#define Kinematic_H
#include <Arduino.h>
#include <ArduinoEigenDense.h>

class Kinematic {
    private: // Agregado :
        float l1, l2, loffset;
        float w1,w2;
        using V1x3 = Eigen::Vector3f;
        using M4x4 = Eigen::Matrix4f;


    public:
        Kinematic(float _l1, float _l2, float _loffset, float _w1, float _w2);
        bool pos2Angle(float x, float y, float z, float &th1, float &th2, float &th3);
        bool angle2Pos(float theta1, float theta2, float theta3, M4x4 &resMatrix);
        M4x4 getDH(float theta, float alpha, float d, float a);

};

#endif