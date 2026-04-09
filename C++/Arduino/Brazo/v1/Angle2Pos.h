#ifndef Angle2Pos_H
#define Angle2Pos_H 
#include <Arduino.h>
#include <ServoEasing.hpp>

class Angle2Pos {
    private: // Agregado :
        float l1, l2, loffset;
        int maxAngle;
        int speed;
        float finalTheta1, finalTheta2, finalTheta3;

    public:
        Angle2Pos(float _l1, float _l2, float _loffset, int _maxAngle, int _speed);
        bool inverseKinematic(float x, float y, float z);
        void moveServo(float x, float y, float z);
        void goHome(); 
};

// Declaramos que existe un objeto global llamado arm
extern Angle2Pos arm; 
extern ServoEasing Servo1; 
extern ServoEasing Servo2;
extern ServoEasing Servo3;
#endif