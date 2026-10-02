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
        float l4, w4, theta4_internal, phi;
        using M4x4 = Eigen::Matrix4f;

    public:
        EIGEN_MAKE_ALIGNED_OPERATOR_NEW
        using Matrix4f = Eigen::Matrix4f; 

        Kinematic(float _l1, float _l2, float _l3, 
                float _w1, float _w2, float _w3, 
                float _l4, float _w4);
        
        // Cinemática Inversa
        bool pos2Angle(float x, float y, float z, float &th1, float &th2, float &th3, float theta4_in = 0.0, bool elbowUp = true);
        bool pos2Angle(float x, float y, float z, float &th1, float &th2, float &th3, float &th4, float phi_in, bool elbowUp = true);

        // Cinemática Directa
        bool angle2Pos(float theta1, float theta2, float theta3, float theta4, M4x4 &resMatrix);
        
        //Pseudo Inversa del Jacobiano
        Eigen::MatrixXf Jacobian3x4(float th1, float th2, float th3, float th4);
        Eigen::MatrixXf Jacobian4x4(float th1, float th2, float th3, float th4);
        Eigen::MatrixXf pseudoInverse(const Eigen::MatrixXf& M);

        // Metodo DH estandarizado
        M4x4 getDH(float theta, float alpha, float d, float a);
};

#endif