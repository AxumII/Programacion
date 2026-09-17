#include "Kinematic.h"

Kinematic::Kinematic(float _l1, float _l2, float _l3, 
                     float _w1, float _w2, float _w3, 
                     float _lTool, float _wTool, float _thetaTool, float _phi) 
    : l1(_l1), l2(_l2), l3(_l3), w1(_w1), w2(_w2), w3(_w3), 
      lTool(_lTool), wTool(_wTool), theta4_internal(_thetaTool), phi(_phi) 
{
}

// Cinemática Inversa 3-DOF
bool Kinematic::pos2Angle(float x, float y, float z, float &th1, float &th2, float &th3, float theta4_in) {
    float W = w2 + w3 + wTool;
    float r_xy_sq = (x * x) + (y * y);    
    if (r_xy_sq < (W * W)) return false;     
    
    float raiz_w = sqrt(r_xy_sq - (W * W));    
    float t1 = atan2(y, x) + atan2(W, raiz_w); 
    
    float zRel = z - l1;
    float R = (x * cos(t1)) + (y * sin(t1)) - w1;
    
    float theta4_rad = theta4_in * PI / 180.0;
    float L_virt = sqrt((l3 * l3) + (lTool * lTool) + (2.0 * l3 * lTool * cos(theta4_rad)));    
    float D = ((R * R) + (zRel * zRel) - (l2 * l2) - (L_virt * L_virt)) / (2.0 * l2 * L_virt);

    if (std::abs(D) > 1.0) return false; 
    
    float gamma = atan2(-sqrt(1.0 - (D * D)), D); 
    float beta = atan2(lTool * sin(theta4_rad), l3 + lTool * cos(theta4_rad));
    
    float t3 = gamma - beta;
    float t2 = atan2(zRel, R) - atan2(L_virt * sin(gamma), l2 + L_virt * cos(gamma));
    
    th1 = t1 * 180.0 / PI; th2 = t2 * 180.0 / PI; th3 = t3 * 180.0 / PI;
    return true;
}

// Cinemática Inversa 4-DOF
bool Kinematic::pos2Angle(float x, float y, float z, float &th1, float &th2, float &th3, float &th4, float phi_val) {
    float W = w2 + w3 + wTool;
    float r_xy_sq = (x * x) + (y * y);
    if (r_xy_sq < (W * W)) return false; 
    float raiz_w = sqrt(r_xy_sq - (W * W));
    float t1 = atan2(y, x) + atan2(W, raiz_w);

    float zRel = z - l1;
    float R = (x * cos(t1)) + (y * sin(t1)) - w1;    
    float phi_rad = phi_val * PI / 180.0;
    float Rj = R - lTool * cos(phi_rad);
    float zj = zRel - lTool * sin(phi_rad); 
    
    float D = ((Rj * Rj) + (zj * zj) - (l2 * l2) - (l3 * l3)) / (2.0 * l2 * l3);
    if (std::abs(D) > 1.0) return false;
    
    float t3 = atan2(-sqrt(1.0 - (D * D)), D);
    float t2 = atan2(zj, Rj) - atan2(l3 * sin(t3), l2 + l3 * cos(t3));
    float t4_rad = phi_rad - (t2 + t3);
    
    th1 = t1 * 180.0 / PI; th2 = t2 * 180.0 / PI; th3 = t3 * 180.0 / PI;
    th4 = atan2(sin(t4_rad), cos(t4_rad)) * 180.0 / PI;     
    return true;
}

// FK (3 parámetros)
bool Kinematic::angle2Pos(float theta1, float theta2, float theta3, M4x4 &resMatrix) {
    return angle2Pos(theta1, theta2, theta3, this->theta4_internal, resMatrix);
}

// FK (4 parámetros - General)
bool Kinematic::angle2Pos(float theta1, float theta2, float theta3, float theta4_val, M4x4 &resMatrix) {
    float t1 = theta1 * PI / 180.0;
    float t2 = theta2 * PI / 180.0;
    float t3 = theta3 * PI / 180.0;    
    float t4 = theta4_val * PI / 180.0; 

    M4x4 m1 = getDH(t1, PI/2.0, l1, w1);    
    M4x4 m2 = getDH(t2, 0.0, w2, l2);   
    M4x4 m3 = getDH(t3, 0.0, w3, l3);   
    M4x4 m4 = getDH(t4, 0.0, wTool, lTool);
    resMatrix = m1 * m2 * m3 * m4;    
    return true;
}

// FK según normativa (Z es aproximación)
bool Kinematic::angle2TCP(float th1, float th2, float th3, float th4, M4x4 &resMatrix) {
    M4x4 T_dh;
    angle2Pos(th1, th2, th3, th4, T_dh);    
    M4x4 R_adj = M4x4::Identity();    
    float angle = 90.0 * PI / 180.0;

    R_adj << cos(angle),  0, sin(angle), 0,
             0,           1, 0,          0,
             -sin(angle), 0, cos(angle), 0,
             0,           0, 0,          1;
    resMatrix = T_dh * R_adj;
    return true;
}

// Transformación inversa: De Matriz TCP a Ángulos
bool Kinematic::TCP2angle(const M4x4 &tcpMatrix, float &th1, float &th2, float &th3, float &th4) {
    // 1. Extraer la posición final del TCP directamente
    float Px = tcpMatrix(0, 3);
    float Py = tcpMatrix(1, 3);
    float Pz = tcpMatrix(2, 3);

    // 2. Extraer el vector de aproximación (Eje Z de la matriz TCP por la normativa)
    float ax = tcpMatrix(0, 2); 
    float ay = tcpMatrix(1, 2); 
    float az = tcpMatrix(2, 2);

    // 3. Calcular T1 preliminar para definir el plano radial (R-Z)
    float W = w2 + w3 + wTool;
    float r_xy_sq = (Px * Px) + (Py * Py);
    if (r_xy_sq < (W * W)) return false; 
    
    float raiz_w = sqrt(r_xy_sq - (W * W));
    float t1_rad = atan2(Py, Px) + atan2(W, raiz_w);

    // 4. Proyectar el vector de la herramienta en el plano R-Z para hallar Phi exacto
    // Esto evita errores de signo si el robot apunta hacia atrás
    float proj_R = ax * cos(t1_rad) + ay * sin(t1_rad);
    float phi_rad = atan2(az, proj_R);
    float phi_deg = phi_rad * 180.0 / PI;

    // 5. Pasar todo a pos2Angle (él mismo descuenta lTool y wTool internamente)
    return pos2Angle(Px, Py, Pz, th1, th2, th3, th4, phi_deg);
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