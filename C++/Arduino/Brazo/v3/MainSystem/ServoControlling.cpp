#define USE_PCA9685_SERVO_EXPANDER
#include "ServoControlling.h"
#include <Arduino.h>     
#include <ArduinoEigenDense.h>
#include <ServoEasing.h>
#include "Kinematic.h"

ServoControlling::ServoControlling(Kinematic* kinPtr) {
    _kinematic = kinPtr;
}

bool ServoControlling::settings(int _ps1, int _p2s1, int _ps2, int _p2s2, int _ps3, int _p2s3, int _ps4, int _p2s4,
    int _maxA1, int _maxA2, int _maxA3, int _maxA4, 
    int _angSpeed, char _profile) {     
    
    p1s1 = _ps1; p2s1 = _p2s1; 
    p1s2 = _ps2; p2s2 = _p2s2; 
    p1s3 = _ps3; p2s3 = _p2s3;
    p1s4 = _ps4; p2s4 = _p2s4;    
    
    maxAngle1 = _maxA1; maxAngle2 = _maxA2; maxAngle3 = _maxA3; maxAngle4 = _maxA4;
    angSpeed = _angSpeed; profile = _profile;

    Servo1.attach(0, 90, p1s1, p2s1);
    Servo2.attach(1, 90, p1s2, p2s2);
    Servo3.attach(2, 90, p1s3, p2s3);

    int easeType = EASE_QUARTIC_IN_OUT; 
    switch(profile) {
        case 'L': easeType = EASE_LINEAR;            break;
        case 'S': easeType = EASE_SINE_IN_OUT;       break;
        case '2': easeType = EASE_QUADRATIC_IN_OUT;  break;
        case '3': easeType = EASE_CUBIC_IN_OUT;      break;
        case '4': easeType = EASE_QUARTIC_IN_OUT;    break;
        default:  easeType = EASE_QUARTIC_IN_OUT;    break;
    }

    if (p1s4 != -1 && p2s4 != -1) {
        Servo4.attach(3, 0, p1s4, p2s4);
        Servo4.setEasingType(easeType);
        isServo4 = true; 
    } else {
        isServo4 = false;
    }

    Servo1.setEasingType(easeType);
    Servo2.setEasingType(easeType);
    Servo3.setEasingType(easeType);
    return true;
}

int ServoControlling::getMaxAngle(int calibServo) {
    if (calibServo == 1) return maxAngle1;
    if (calibServo == 2) return maxAngle2;
    if (calibServo == 3) return maxAngle3;
    if (calibServo == 4 && isServo4) return maxAngle4;
    return 180; 
}

int ServoControlling::getAngSpeed() { return angSpeed; }

float ServoControlling::getAngle(int numServo) {
    float angle = 0.0f;
    switch(numServo) {
        case 1: angle = Servo1.getCurrentAngle() - 90.0; break;
        case 2: angle = Servo2.getCurrentAngle(); break;
        case 3: angle = -Servo3.getCurrentAngle();break;
        case 4:
            if (isServo4) angle = Servo4.getCurrentAngle() - 90.0;
            break;
    }
    return angle;
 
}

ServoControlling::V3 ServoControlling::getPos() {
    float q1 = getAngle(1);
    float q2 = getAngle(2);
    float q3 = getAngle(3);    
    Eigen::Matrix4f currentMatrix;

    if (isServo4){
        float q4 = getAngle(4); 
        // SINTAXIS CORREGIDA:
        _kinematic->angle2Pos(q1, q2, q3, q4, currentMatrix);
    } else {
        _kinematic->angle2Pos(q1, q2, q3, currentMatrix);    
    }
    
    float x = currentMatrix(0, 3);
    float y = currentMatrix(1, 3);
    float z = currentMatrix(2, 3);
    
    return V3(x, y, z);
}

bool ServoControlling::goHome() {
    if (isServo4) {
        return ReachForAnglesAndStop(0, 90, -90, 0); 
    } else {
        return ReachForAnglesAndStop(0, 90, -90); 
    }
}

bool ServoControlling::goExtendedHome() {
    if (isServo4) {
        return ReachForAnglesAndStop(0, 0, 0, 0); 
    } else {
        return ReachForAnglesAndStop(0, 0, 0); 
    }
}

bool ServoControlling::checkLimits(float t1, float t2, float t3, float t4) {
    if (abs(t1) > maxAngle1) { Serial.println("Limit Error: Q1"); return false; }
    if (t2 < 0 || t2 > maxAngle2) { Serial.println("Limit Error: Q2"); return false; }
    
    // t3 debe ser negativo o cero, y no menor al límite negativo
    if (t3 < -maxAngle3 || t3 > 0.0f) { 
        Serial.print("Limit Error: Q3 value: "); Serial.println(t3);
        return false; 
    }
    
    if (isServo4 && abs(t4) > maxAngle4) { Serial.println("Limit Error: Q4"); return false; }
    return true;
}

bool ServoControlling::ReachForAnglesContinuous(float theta1, float theta2, float theta3, float theta4, int speed) {    
    theta1 = constrain(theta1, -90.0f, (float)maxAngle1 - 90.0f);
    theta2 = constrain(theta2, 0.0f, (float)maxAngle2);
    theta3 = constrain(theta3, -(float)maxAngle3, 0.0f);
    if (isServo4) theta4 = constrain(theta4, -90.0f, (float)maxAngle4 - 90.0f);
    // 2. Mapeo a los Servos Físicos
    float f1 = theta1 + 90.0;
    float f2 = theta2;      
    float f3 = -theta3; 
    float f4 = theta4 + 90.0;

    int finalSpeed = (speed == -1) ? angSpeed : speed;
    Servo1.setEaseTo(f1, finalSpeed);
    Servo2.setEaseTo(f2, finalSpeed);
    Servo3.setEaseTo(f3, finalSpeed);
    if (isServo4) Servo4.setEaseTo(f4, finalSpeed);   
    
    synchronizeAllServosAndStartInterrupt();
    return true; 
}

bool ServoControlling::ReachForAnglesAndStop(float theta1, float theta2, float theta3, float theta4, int speed) {
    theta1 = constrain(theta1, -90.0f, (float)maxAngle1 - 90.0f);
    theta2 = constrain(theta2, 0, maxAngle2);
    theta3 = constrain(theta3, -maxAngle3, 0.0f);
    if (isServo4) theta4 = constrain(theta4, -90.0f, (float)maxAngle4 - 90.0f);

    float f1 = theta1 + 90.0;
    float f2 = theta2;      
    float f3 = -theta3; 
    float f4 = theta4 + 90.0;

    int finalSpeed = (speed == -1) ? angSpeed : speed;
    Servo1.setEaseTo(f1, finalSpeed);
    Servo2.setEaseTo(f2, finalSpeed);
    Servo3.setEaseTo(f3, finalSpeed);
    if (isServo4) Servo4.setEaseTo(f4, finalSpeed);   
    
    synchronizeAllServosStartAndWaitForAllServosToStop();
    return true; 
}

bool ServoControlling::moveJ(V3 target, int speed, float phi_in, float theta4_in) {
    float q1, q2, q3;
    if (isServo4){
        float q4;
        if (_kinematic->pos2Angle(target.x(), target.y(), target.z(), q1, q2, q3, q4, phi_in)) {        
            return ReachForAnglesAndStop(q1, q2, q3, q4, speed);
        }
    } else {
        if (_kinematic->pos2Angle(target.x(), target.y(), target.z(), q1, q2, q3, theta4_in)) {        
            return ReachForAnglesAndStop(q1, q2, q3, theta4_in, speed);
        }
    }
    return false;
}

bool ServoControlling::moveJTrigg(V3 target, int speed, float phi_in, float theta4_in) {
    float q1, q2, q3;
    if (isServo4){
        float q4;
        if (_kinematic->pos2Angle(target.x(), target.y(), target.z(), q1, q2, q3, q4, phi_in)) {        
            return ReachForAnglesContinuous(q1, q2, q3, q4, speed);
        }
    } else {
        if (_kinematic->pos2Angle(target.x(), target.y(), target.z(), q1, q2, q3, theta4_in)) {        
            return ReachForAnglesContinuous(q1, q2, q3, theta4_in, speed);
        }
    }
    return false;
}

//--------------------------------------------- CALIBRATE ---------------------------------------------------------------------------------
bool ServoControlling::moveSingleServo(int calibServo, int angle) {
    // Velocidad suave (grados por segundo)
    float speed = 20.0; 

    switch(calibServo) {
        case 1: 
            Servo1.startEaseTo(angle, speed); // Inicia el movimiento sin bloquear
            return true;
        case 2: 
            Servo2.startEaseTo(angle, speed);
            return true;
        case 3: 
            Servo3.startEaseTo(angle, speed);
            return true;
        case 4: 
            if (isServo4) { 
                Servo4.startEaseTo(angle, speed);; 
                return true; 
            }
            break;
    }
    return false;
}

bool ServoControlling::configAttach(int newp1, int newp2, int calibServo, int angle, bool liveUpdate) {
    if (calibServo == 1) { p1s1 = newp1; p2s1 = newp2; }
    if (calibServo == 2) { p1s2 = newp1; p2s2 = newp2; }
    if (calibServo == 3) { p1s3 = newp1; p2s3 = newp2; }
    if (isServo4 && calibServo == 4) { p1s4 = newp1; p2s4 = newp2; }
    
    if (liveUpdate) {
        int pulse = (angle == 0) ? newp1 : newp2;
        if (calibServo == 1) Servo1.write(pulse); 
        if (calibServo == 2) Servo2.write(pulse);
        if (calibServo == 3) Servo3.write(pulse);
        if (isServo4 && calibServo == 4) Servo4.write(pulse);
        return true;
    } 
    else {
        if (calibServo == 1) Servo1.attach(0, angle, p1s1, p2s1);
        if (calibServo == 2) Servo2.attach(1, angle, p1s2, p2s2);
        if (calibServo == 3) Servo3.attach(2, angle, p1s3, p2s3);
        if (isServo4 && calibServo == 4) Servo4.attach(3, angle, p1s4, p2s4);
        
        return moveSingleServo(calibServo, angle);
    }
}

int ServoControlling::getPulseLimit(int servoNum, int angle) {
    if (angle == 0) { 
        if (servoNum == 1) return p1s1;
        if (servoNum == 2) return p1s2;
        if (servoNum == 3) return p1s3;
        if (servoNum == 4) return p1s4;
    } else { 
        if (servoNum == 1) return p2s1;
        if (servoNum == 2) return p2s2;
        if (servoNum == 3) return p2s3;
        if (servoNum == 4) return p2s4;
    }
    return 0;
}

void ServoControlling::moveToNeutralForCalibration(int activeServo) {
    float speed = 10.0; 

    if (activeServo != 1) Servo1.setEaseTo(90, speed);
    if (activeServo != 2) Servo2.setEaseTo(90, speed);
    if (activeServo != 3) Servo3.setEaseTo(90, speed);
    if (isServo4 && activeServo != 4) Servo4.setEaseTo(90, speed);
    synchronizeAllServosStartAndWaitForAllServosToStop();
}