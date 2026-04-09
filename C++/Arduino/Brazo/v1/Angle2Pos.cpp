#include "Angle2Pos.h"
#include <ServoEasing.hpp> // Asegúrate de tener esta librería

Angle2Pos::Angle2Pos(float _l1, float _l2, float _loffset, int _maxAngle, int _speed) 
    : l1(_l1), l2(_l2), loffset(_loffset), maxAngle(_maxAngle), speed(_speed) {}

bool Angle2Pos::inverseKinematic(float x, float y, float z) {
    float h = z - loffset;
    float w = hypot(x, y);
    float r = hypot(w, h);

    if (r > (l1 + l2) || r < fabsf(l1 - l2)) {
        Serial.println("Error: Punto fuera de alcance");
        return false;
    }

    float D = (r*r - l1*l1 - l2*l2) / (2.0 * l1 * l2);
    float theta2 = atan2(-sqrt(1 - D*D), D);
    float beta = atan2(l2 * sin(theta2), l1 + l2 * cos(theta2));
    float alpha = atan2(h, w);
    float theta1 = alpha - beta;
    float theta3 = atan2(y, x);

    finalTheta1 = theta1 * 180.0 / PI;
    finalTheta2 = theta2 * -180.0 / PI;
    finalTheta3 = theta3 * 180.0 / PI;        
    return true;
}


void Angle2Pos::moveServo(float x, float y, float z){
    if (inverseKinematic(x, y, z)) {
        Serial.printf("CÁLCULO IK -> Hombro: %.2f | Codo: %.2f | Base: %.2f\n", finalTheta1, finalTheta2, finalTheta3);
        if (finalTheta1 >= 0 && finalTheta1 <= maxAngle && 
            finalTheta2 >= 0 && finalTheta2 <= maxAngle &&
            finalTheta3 >= 0 && finalTheta3 <= maxAngle) {
            Serial.printf("Moviendo a %.2f, %.2f y %.2f con frenada Quartic\n", finalTheta1, finalTheta2, finalTheta3);
            Servo1.setEaseTo(finalTheta1, speed);
            Servo2.setEaseTo(finalTheta2, speed);
            Servo3.setEaseTo(finalTheta3, speed); 
            synchronizeAllServosStartAndWaitForAllServosToStop();
        } else {
            Serial.println(F("Error: Ángulos calculados fuera de límites de los servos (0-180)"));
        }

    }
}
void Angle2Pos::goHome() {
    Serial.println(F("Moviendo a posición HOME..."));
    Servo1.setEaseTo(90, speed);
    Servo2.setEaseTo(90, speed);
    Servo3.setEaseTo(90, speed); 
    synchronizeAllServosStartAndWaitForAllServosToStop();
    Serial.println(F("Robot en HOME."));
}
void Angle2Pos::settings(Adafruit_PWMServoDriver* pcaPtr) {
    _pca = pcaPtr;
    Servo1.attach(0, _pca);
    Servo2.attach(1, _pca);
    Servo3.attach(2, _pca); 
}