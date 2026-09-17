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
        
        
        // AÑADIDOS LOS PULSOS Y LIMITES DEL SERVO 4
        int p1s1, p2s1, p1s2, p2s2, p1s3, p2s3, p1s4, p2s4; 
        int maxAngle1, maxAngle2, maxAngle3, maxAngle4; 
        
        int angSpeed; 
        char profile; 
    public:
    
        Kinematic* _kinematic; 
        ServoControlling(Kinematic* kinPtr);                
        
        // settings actualizado con todos los defaults
        bool settings(int _ps1, int _p2s1, int _ps2, int _p2s2, int _ps3, int _p2s3, 
                     int _ps4 = -1, int _p2s4 = -1, 
                     int _maxA1 = 180, int _maxA2 = 180, int _maxA3 = 180, int _maxA4 = 180, 
                     int _angSpeed = 20, char _profile = '4');
                     
        bool isServo4;

        float getAngle(int numServo);
        V3 getPos();
        int getAngSpeed();
        bool goHome(); 
        bool goExtendedHome();
        int getMaxAngle(int calibServo);
        // t4 es ahora opcional (valor por defecto 0.0)
        bool checkLimits(float t1, float t2, float t3, float t4 = 0.0);

        // Agregado theta4 opcional a las firmas de movimiento
        bool ReachForAnglesAndStop(float theta1, float theta2, float theta3, float theta4 = 0.0, int speed = -1);
        bool ReachForAnglesContinuous(float theta1, float theta2, float theta3, float theta4 = 0.0, int speed = -1);
        
        // Corrección de firmas para que coincidan con el .cpp
        bool moveJ(V3 target, int speed, float phi_in = 0.0, float theta4_in = 0.0); 
        bool moveJTrigg(V3 target, int speed, float phi_in = 0.0, float theta4_in = 0.0); 
        bool moveL(V3 initPos, V3 targetPos, int steps);
        bool moveSingleServo(int calibServo, int angle);
        bool configAttach(int newp1, int newp2, int calibServo, int angle, bool liveUpdate = false);
        int getPulseLimit(int servoNum, int angle);
        void moveToNeutralForCalibration(int activeServo);
        void setupGripper(int p1, int p2, int maxA);
        void setGripperAngle(float angle);
};

extern ServoEasing Servo1; 
extern ServoEasing Servo2;
extern ServoEasing Servo3;
extern ServoEasing Servo4; 
extern ServoEasing Servo5; // Instancia global para el gripper

#endif