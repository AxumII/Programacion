#include "Kinematic.h"

Kinematic::Kinematic(float _l1, float _l2, float _l3, 
                     float _w1, float _w2, float _w3, 
                     int _toolType, float _lTool, float _wTool, float _thetaTool, float _phi) 
    : l1(_l1), l2(_l2), l3(_l3),
      w1(_w1), w2(_w2), w3(_w3), toolType(_toolType) 
{
    lTool = _lTool;
    wTool = _wTool;
    theta4 = _thetaTool* 180.0 / PI;
    phi = _phi;
    
    // Configuración de las variables activas según el tipo de tool
    switch (toolType) {
        case -1: // No hay tool, solo hay 3 servos
            lTool = 0.0; 
            wTool = 0.0; 
            theta4 = 0.0;
            phi = 999999;//No se usa
            p2atype = 0;
            break;
         case 0:  // Tool de calibración
            theta4 = 0.0; 
            wTool = 0.0;
            phi = 999999; //No se usa
            p2atype = 0;
            break;
        case 1:  // Gripper rígido
            theta4 = 0.0;
            phi = 999999; //No se usa
            p2atype = 0;
            
            break;
        case 2:  // Gripper articulado con angulo fijo respecto al anterior
            phi = 999999; //No se usa
            p2atype = 0;
            break;
        case 3:  // Gripper articulado con angulo fijo respecto al piso
        p2atype = 1;
            break;
        default:
            lTool = 0.0; 
            wTool = 0.0; 
            theta4 = 0.0;
            phi = 999999;//No se usa
            break;
    }
}


bool Kinematic::pos2Angle(float x, float y, float z, float &th1, float &th2, float &th3, float theta4_in) {
    // Theta 1
    float W = w2 + w3 + wTool;
    float r_xy_sq = (x * x) + (y * y);7    
    // Validacion de la raiz
    if (r_xy_sq < (W * W)) return false; 
    float raiz_w = sqrt(r_xy_sq - (W * W));
    float t1 = atan2(y, x) + atan2(W, -raiz_w);
    
    //Variables generales
    float zRel = z - l1;
    float R = (x * cos(t1)) + (y * sin(t1)) - w1;
    
    // Theta 3
    float L_virt = sqrt((l3 * l3) + (lTool * lTool) + (2.0 * l3 * lTool * cos(theta4_in)));    
    float D = ((R * R) + (zRel * zRel) - (l2 * l2) - (L_virt * L_virt)) / (2.0 * l2 * L_virt);
    // Validacion de la raiz
    if (abs(D) > 1.0) return false;    
    float t3 = atan2(-sqrt(1.0 - (D * D)), D);
    // Theta 2
    float gamma = atan2(zRel, R) - atan2(L_virt * sin(t3), l2 + L_virt * cos(t3));
    float beta = atan2(lTool * sin(theta4_in), l3 + lTool * cos(theta4_in));
    float t2 = gamma - beta;

    th1 = t1 * 180.0 / PI;
    th2 = t2 * 180.0 / PI;
    th3 = t3 * 180.0 / PI;
    return true;
}

bool Kinematic::pos2Angle(float x, float y, float z, float &th1, float &th2, float &th3, float &th4, float phi) {
    //Theta 1
    float W = w2 + w3 + wTool;
    float r_xy_sq = (x * x) + (y * y);
    // Validacion de la raiz
    if (r_xy_sq < (W * W)) return false; 
    float raiz_w = sqrt(r_xy_sq - (W * W));
    float t1 = atan2(y, x) + atan2(W, -raiz_w);
    //Variables generales
    float zRel = z - l1;
    float R = (x * cos(t1)) + (y * sin(t1)) - w1;    
    // Desacoplamiento Cinemático
    float Rj = R - lTool * cos(phi);
    float zj = zRel - lTool * sin(phi); 
    
    float D = ((Rj * Rj) + (zj * zj) - (l2 * l2) - (l3 * l3)) / (2.0 * l2 * l3);
    // Validacion de la raiz
    if (abs(D) > 1.0) return false;
    
    float t3 = atan2(-sqrt(1.0 - (D * D)), D);
    
    // CORREGIDO: t2 es directo, ya no hay eslabón virtual (beta desaparece)
    float t2 = atan2(zj, Rj) - atan2(l3 * sin(t3), l2 + l3 * cos(t3));
    
    // CORREGIDO: Calcular t4 para compensar y mantener phi
    float t4 = phi - (t2 + t3);
    
    // Normalizar t4 entre -PI y PI (buena práctica para servos/steppers)
    t4 = atan2(sin(t4), cos(t4));

    th1 = t1 * 180.0 / PI;
    th2 = t2 * 180.0 / PI;
    th3 = t3 * 180.0 / PI;
    th4 = t4 * 180.0 / PI;     
    return true;
}





    
bool Kinematic::angle2Pos(float theta1, float theta2, float theta3, M4x4 &resMatrix) {
    // 1. Conversión de las articulaciones principales a radianes
    float t1 = theta1 * PI / 180.0;
    float t2 = theta2 * PI / 180.0;
    float t3 = theta3 * PI / 180.0;    
    float t4 = theta4* PI / 180.0; 

    // 2. Construcción de la MTH (Matriz de Transformación Homogénea)
    // El orden de getDH en C++ es: (theta, alpha, d, a)    
    // T_01: Base a Hombro (Giro en la base y rotación del plano Z a vertical)
    M4x4 m1 = getDH(t1, PI/2.0, 0, w1);    
    // T_12: Hombro a Codo (Primer eslabón largo)
    M4x4 m2 = getDH(t2, 0.0, w2, l1);    
    // T_23: Codo a Muñeca (Segundo eslabón largo)
    M4x4 m3 = getDH(t3, 0.0, w3, l2);    
    // T_34: Muñeca a Base de Herramienta (Desfase físico de acople)
    M4x4 m4 = getDH(0.0, 0.0, wTool, l3);    
    // T_45: Efector Final / TCP (Articulación de la herramienta y longitud final)
    M4x4 m5 = getDH(t4, 0.0, 0.0, lTool);    
    // 3. Matriz global (T_05 = T_01 * T_12 * T_23 * T_34 * T_45)
    resMatrix = m1 * m2 * m3 * m4 * m5;
    
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
