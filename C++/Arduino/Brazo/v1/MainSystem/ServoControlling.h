#ifndef ServoControlling_H
#define ServoControlling_H
#define USE_PCA9685_SERVO_EXPANDER

#include <ServoEasing.h>
#include <Arduino.h>
#include <ArduinoEigenDense.h>
#include "Kinematic.h" 

class ServoControlling { 
    private: 
        using V3 = Eigen::Vector3f;
        Kinematic* _kinematic; // Puntero a kinematic
        int p1s1, p2s1, p1s2, p2s2, p1s3, p2s3;
        int maxAngle1, maxAngle2, maxAngle3;
        int angSpeed; 
        char profile; 

    public:
        // Constructor actualizado
        ServoControlling(Kinematic* kinPtr);                
        bool settings(int _ps1, int _p2s1, int _ps2, int _p2s2, int _ps3, int _p2s3, int _maxA1, int _maxA2, int _maxA3, int _angSpeed, char _profile);
        float getAngle(int numServo);
        V3 getPos();
        bool checkLimits(float t1, float t2, float t3);
        void goHome(); 
        void goExtendedHome();
        bool ReachForAnglesAndStop(float theta1, float theta2, float theta3, int speed = -1);
        bool ReachForAnglesContinuous(float theta1, float theta2, float theta3, int speed = -1);
        bool moveJ(V3 target,int speed); 
        bool moveJTrigg(V3 target,int speed); 
        bool moveL(V3 initPos, V3 targetPos, int steps);
        bool moveSingleServo(int calibServo, int angle);
        bool configAttach(int newp1, int newp2, int calibServo, int angle, bool liveUpdate = false);
        int getPulseLimit(int servoNum, int angle);
};

extern ServoEasing Servo1; 
extern ServoEasing Servo2;
extern ServoEasing Servo3;

#endif