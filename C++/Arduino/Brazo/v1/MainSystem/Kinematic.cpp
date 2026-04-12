#include "Kinematic.h"

Kinematic::Kinematic(float _l1, float _l2, float _loffset, float _w1, float _w2) 
    : l1(_l1), l2(_l2), loffset(_loffset), w1(_w1), w2(_w2) {}

    bool Kinematic::pos2Angle(float x, float y, float z, float &th1, float &th2, float &th3) {
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

    th1 = (alpha - beta) * 180.0 / PI;
    th2 = theta2 * -180.0 / PI;
    th3 = atan2(y, x) * 180.0 / PI;      
    return true;
}
    
bool Kinematic::angle2Pos(float theta1, float theta2, float theta3, M4x4 &resMatrix) {
    float t1 = theta1 * PI / 180.0;
    float t2 = theta2 * PI / 180.0;
    float t3 = theta3 * PI / 180.0;

    M4x4 m1 = getDH(t3, PI/2.0, loffset, w1);
    M4x4 m2 = getDH(t1, 0.0, w2, l1);
    M4x4 m3 = getDH(t2, 0.0, 0.0, l2);
    
    resMatrix = m1 * m2 * m3;
    return true;
}

Kinematic::M4x4 Kinematic::getDH(float theta, float alpha, float d, float a) {
    M4x4 MTH;
    float ct = cos(theta); float st = sin(theta);
    float ca = cos(alpha); float sa = sin(alpha);
    MTH << ct, -ca*st,  sa*st, a*ct,
           st,  ca*ct, -sa*ct, a*st,
           0,   sa,     ca,    d,
           0,   0,      0,     1;
    return MTH;
}
