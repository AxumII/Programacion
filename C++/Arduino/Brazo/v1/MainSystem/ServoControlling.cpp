#define USE_PCA9685_SERVO_EXPANDER
#include "ServoControlling.h"
#include <Arduino.h>     
#include <ArduinoEigenDense.h>
#include <ServoEasing.h>
#include "Kinematic.h"

ServoControlling::ServoControlling(Kinematic* kinPtr) {
    _kinematic = kinPtr;
}

bool ServoControlling::settings(int _ps1, int _p2s1, int _ps2, int _p2s2, int _ps3, int _p2s3, int _maxA1, int _maxA2, int _maxA3, int _angSpeed, char _profile) {     
    p1s1 = _ps1; p2s1 = _p2s1; 
    p1s2 = _ps2; p2s2 = _p2s2; 
    p1s3 = _ps3; p2s3 = _p2s3;
    
    maxAngle1 = _maxA1; maxAngle2 = _maxA2; maxAngle3 = _maxA3;
    angSpeed = _angSpeed; profile = _profile;

    // --- VERIFICACIÓN 1: I2C Físico ---
    //Wire.beginTransmission(0x40);   
    // Calibración de pulsos (Canal, Ángulo inicial, Min, Max)
    Servo1.attach(0, 90, p1s1, p2s1);
    Servo2.attach(1, 90, p1s2, p2s2);
    Servo3.attach(2, 90, p1s3, p2s3);

    // Asignación básica de perfil de aceleración
    int easeType = EASE_QUARTIC_IN_OUT; // Inicial
    switch(profile) {
    case 'L': easeType = EASE_LINEAR;            break;
    case 'S': easeType = EASE_SINE_IN_OUT;      break;
    case '2': easeType = EASE_QUADRATIC_IN_OUT; break;
    case '3': easeType = EASE_CUBIC_IN_OUT;     break;
    case '4': easeType = EASE_QUARTIC_IN_OUT;   break;
    default:  easeType = EASE_QUARTIC_IN_OUT;     break;
}

    Servo1.setEasingType(easeType);
    Servo2.setEasingType(easeType);
    Servo3.setEasingType(easeType);
    

    return true;
}

//-----------------------------------------------GETTERS-------------------------------------------------------
float ServoControlling::getAngle(int numServo) {
    // Usamos el método nativo de ServoEasing
    if (numServo == 1) return Servo1.getCurrentAngle();
    if (numServo == 2) return Servo2.getCurrentAngle();
    if (numServo == 3) return Servo3.getCurrentAngle();
    //if (numServo == 4) return Servo4.getCurrentAngle();
    return 0.0f; 
}

ServoControlling::V3 ServoControlling::getPos() {
    float q1 = getAngle(1);
    float q2 = getAngle(2);
    float q3 = getAngle(3);
    
    Eigen::Matrix4f currentMatrix;
    _kinematic->angle2Pos(q1, q2, q3, currentMatrix);    
    // Extraemos la traslación de la matriz homogénea
    float x = currentMatrix(0, 3);
    float y = currentMatrix(1, 3);
    float z = currentMatrix(2, 3);
    
    return V3(x, y, z);
}

//---------------------------------------------- PRESET MOVEMENT -------------------------------------------------
void ServoControlling::goHome() {
    Serial.println(F("Moviendo a HOME..."));
    ReachForAnglesAndStop(90, 90, 90); 
    Serial.println(F("Robot en HOME."));
}

void ServoControlling::goExtendedHome() {
    Serial.println(F("Moviendo a posición EXTENDED HOME..."));
    ReachForAnglesAndStop(0, 0, 0); 
    Serial.println(F("Robot en EXTENDED HOME."));
}
//---------------------------------------------- MOVE METHODES -------------------------------------------------
bool ServoControlling::checkLimits(float t1, float t2, float t3) {
    if (abs(t1) > maxAngle1 || abs(t2) > maxAngle2 || abs(t3) > maxAngle3) {
        Serial.println(F("!!! ERROR: Límite de ángulo excedido. Movimiento bloqueado."));
        return false;
    }
    return true;
}

bool ServoControlling::ReachForAnglesAndStop(float theta1, float theta2, float theta3, int speed) {
    if (!checkLimits(theta1, theta2, theta3)) return false; 
    int finalSpeed = (speed == -1) ? angSpeed : speed;
    Servo1.setEaseTo(theta1, finalSpeed);
    Servo2.setEaseTo(theta2, finalSpeed);
    Servo3.setEaseTo(theta3, finalSpeed);    
    synchronizeAllServosStartAndWaitForAllServosToStop();
    return true; 
}

bool ServoControlling::ReachForAnglesContinuous(float theta1, float theta2, float theta3, int speed) {
    if (!checkLimits(theta1, theta2, theta3)) return false;     
    int finalSpeed = (speed == -1) ? angSpeed : speed;
    Servo1.setEaseTo(theta1, finalSpeed);
    Servo2.setEaseTo(theta2, finalSpeed);
    Servo3.setEaseTo(theta3, finalSpeed);    
    synchronizeAllServosAndStartInterrupt();
    return true; 
}

//---------------------------------------------- MOVE METHODES TO CODING -------------------------------------------------


bool ServoControlling::moveJ(V3 target,int speed) {
    float q1, q2, q3;
    if (_kinematic->pos2Angle(target.x(), target.y(), target.z(), q1, q2, q3)) {        
        if (ReachForAnglesAndStop(q1, q2, q3, speed)) {
            return true;
        } else {
            return false; 
        }
    } else {
        return false;
    }
}

bool ServoControlling::moveJTrigg(V3 target,int speed){
    float q1, q2, q3;
    if (_kinematic->pos2Angle(target.x(), target.y(), target.z(), q1, q2, q3)) {        
        if (ReachForAnglesContinuous(q1, q2, q3, speed)) {
            return true;
        } else {
            return false; 
        }
    } else {
        return false;
    }
}



bool ServoControlling::moveL(V3 initPos, V3 targetPos, int steps) {
    float q1, q2, q3;
    for (int i = 1; i <= steps; i++) {
        float t = (float)i / steps;
        
        // Interpolación lineal
        V3 interim(
            initPos.x() + t * (targetPos.x() - initPos.x()),
            initPos.y() + t * (targetPos.y() - initPos.y()),
            initPos.z() + t * (targetPos.z() - initPos.z())
        );

        // Calcular cinemática y mover en cada paso del bucle
        if (_kinematic->pos2Angle(interim.x(), interim.y(), interim.z(), q1, q2, q3)) {
            //moveServo(q1, q2, q3);
        } else {
            Serial.println(F("Trayectoria lineal interrumpida: punto inalcanzable."));
            return false;
        }
    }
    return true;
}