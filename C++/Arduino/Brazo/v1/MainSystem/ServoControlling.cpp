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
    Serial.println(F("\n--- Inicio el Settings ---"));   
    p1s1 = _ps1; p2s1 = _p2s1; 
    p1s2 = _ps2; p2s2 = _p2s2; 
    p1s3 = _ps3; p2s3 = _p2s3;
    
    maxAngle1 = _maxA1; maxAngle2 = _maxA2; maxAngle3 = _maxA3;
    angSpeed = _angSpeed; profile = _profile;

    // --- VERIFICACIÓN 1: I2C Físico ---
    Wire.beginTransmission(0x40);
    if (Wire.endTransmission() == 0) {
        Serial.println(F("Confirmacion I2C: Dispositivo detectado en 0x40."));
    } else {
        Serial.println(F("ADVERTENCIA I2C: No detectado en 0x40."));
    }

    // --- VERIFICACIÓN 2: Librería ---
    if (checkI2CConnection(0x40, &Serial)) {
        Serial.println(F("Libreria: PCA9685 reconocida y lista."));
    } else {
        // Es normal que falle aquí si la tarjeta está en modo "Sleep"
        Serial.println(F("Libreria: PCA detectada pero requiere despertar. Procediendo..."));
    }

    Serial.println(F("Ejecutando Attach de motores..."));
    
    // Calibración de pulsos (Canal, Ángulo inicial, Min, Max)
    Servo1.attach(0, 90, p1s1, p2s1);
    Servo2.attach(1, 90, p1s2, p2s2);
    Servo3.attach(2, 90, p1s3, p2s3);

    // Asignación básica de perfil de aceleración
    int easeType = EASE_CUBIC_IN_OUT; // Perfil por defecto
    if (profile == 'L') easeType = EASE_LINEAR;
    
    Servo1.setEasingType(easeType);
    Servo2.setEasingType(easeType);
    Servo3.setEasingType(easeType);

    return true;
}

void ServoControlling::moveServo(float theta1, float theta2, float theta3) {
    // Protección contra ángulos fuera de los límites máximos permitidos
    if (abs(theta1) > maxAngle1) theta1 = (theta1 > 0) ? maxAngle1 : -maxAngle1;
    if (abs(theta2) > maxAngle2) theta2 = (theta2 > 0) ? maxAngle2 : -maxAngle2;
    if (abs(theta3) > maxAngle3) theta3 = (theta3 > 0) ? maxAngle3 : -maxAngle3;

    Servo1.setEaseTo(theta1, angSpeed);
    Servo2.setEaseTo(theta2, angSpeed);
    Servo3.setEaseTo(theta3, angSpeed);
    
    synchronizeAllServosStartAndWaitForAllServosToStop();
}

void ServoControlling::goHome() {
    Serial.println(F("Moviendo a HOME..."));
    moveServo(90, 90, 90); 
    Serial.println(F("Robot en HOME."));
}

void ServoControlling::goExtendedHome() {
    Serial.println(F("Moviendo a posición EXTENDED HOME..."));
    moveServo(0, 0, 0); 
    Serial.println(F("Robot en EXTENDED HOME."));
}

bool ServoControlling::moveJ(V3 target) {
    float q1, q2, q3;
    if (_kinematic->pos2Angle(target.x(), target.y(), target.z(), q1, q2, q3)) {
        moveServo(q1, q2, q3);
        return true;
    } else {
        Serial.println(F("Error: Coordenada inalcanzable. moveJ abortado."));
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
            moveServo(q1, q2, q3);
        } else {
            Serial.println(F("Trayectoria lineal interrumpida: punto inalcanzable."));
            return false;
        }
    }
    return true;
}