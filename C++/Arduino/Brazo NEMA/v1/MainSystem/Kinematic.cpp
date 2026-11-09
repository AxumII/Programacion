#include "Kinematic.h"

Kinematic::Kinematic(float _l1, float _l2, float _l3, 
                     float _w1, float _w2, float _w3, 
                     float _l4, float _w4) 
    : l1(_l1), l2(_l2), l3(_l3), w1(_w1), w2(_w2), w3(_w3), 
      l4(_l4), w4(_w4)
{
}

// Cinemática Inversa 4-DOF con Muñeca con angulo fijo
bool Kinematic::pos2Angle(float x, float y, float z, float &th1, float &th2, float &th3, float theta4_in, bool elbowUp) {
    float W = w2 + w3 + w4;
    float r_xy_sq = (x * x) + (y * y);    
    if (r_xy_sq < (W * W)) return false;     
    
    float raiz_w = sqrt(r_xy_sq - (W * W));    
    float t1 = atan2(y, x) + atan2(W, raiz_w); 
    
    float zRel = z - l1;
    float R = (x * cos(t1)) + (y * sin(t1)) - w1;
    
    float theta4_rad = theta4_in * PI / 180.0;
    float L_virt = sqrt((l3 * l3) + (l4 * l4) + (2.0 * l3 * l4 * cos(theta4_rad)));    
    float D = ((R * R) + (zRel * zRel) - (l2 * l2) - (L_virt * L_virt)) / (2.0 * l2 * L_virt);

    if (std::abs(D) > 1.0) return false; 
    
    // Determinamos el signo dependiendo de la preferencia de codo
    float elbowSign = elbowUp ? -1.0 : 1.0;
    
    float gamma = atan2(elbowSign * sqrt(1.0 - (D * D)), D); 
    float beta = atan2(l4 * sin(theta4_rad), l3 + l4 * cos(theta4_rad));
    
    float t3 = gamma - beta;
    float t2 = atan2(zRel, R) - atan2(L_virt * sin(gamma), l2 + L_virt * cos(gamma));
    
    th1 = t1 * 180.0 / PI; th2 = t2 * 180.0 / PI; th3 = t3 * 180.0 / PI;
    return true;
}

// Cinemática Inversa 4-DOF con muñeca con angulo relativo al suelo
bool Kinematic::pos2Angle(float x, float y, float z, float &th1, float &th2, float &th3, float &th4, float phi_val, bool elbowUp) {
    float W = w2 + w3 + w4;
    float r_xy_sq = (x * x) + (y * y);
    if (r_xy_sq < (W * W)) return false; 
    float raiz_w = sqrt(r_xy_sq - (W * W));
    float t1 = atan2(y, x) + atan2(W, raiz_w);

    float zRel = z - l1;
    float R = (x * cos(t1)) + (y * sin(t1)) - w1;    
    float phi_rad = phi_val * PI / 180.0;
    float Rj = R - l4 * cos(phi_rad);
    float zj = zRel - l4 * sin(phi_rad); 
    
    float D = ((Rj * Rj) + (zj * zj) - (l2 * l2) - (l3 * l3)) / (2.0 * l2 * l3);
    if (std::abs(D) > 1.0) return false;
    
    // Determinamos el signo dependiendo de la preferencia de codo
    float elbowSign = elbowUp ? -1.0 : 1.0;
    
    float t3 = atan2(elbowSign * sqrt(1.0 - (D * D)), D);
    float t2 = atan2(zj, Rj) - atan2(l3 * sin(t3), l2 + l3 * cos(t3));
    float t4_rad = phi_rad - (t2 + t3);
    
    th1 = t1 * 180.0 / PI; th2 = t2 * 180.0 / PI; th3 = t3 * 180.0 / PI;
    th4 = atan2(sin(t4_rad), cos(t4_rad)) * 180.0 / PI;     
    return true;
}
// Cinematica Directa (4 parámetros)
bool Kinematic::angle2Pos(float theta1, float theta2, float theta3, float theta4_val, M4x4 &resMatrix) {
    float t1 = theta1 * PI / 180.0;
    float t2 = theta2 * PI / 180.0;
    float t3 = theta3 * PI / 180.0;    
    float t4 = theta4_val * PI / 180.0; 

    M4x4 m1 = getDH(t1, PI/2.0, l1, w1);    
    M4x4 m2 = getDH(t2, 0.0, w2, l2);   
    M4x4 m3 = getDH(t3, 0.0, w3, l3);   
    M4x4 m4 = getDH(t4, 0.0, w4, l4);
    resMatrix = m1 * m2 * m3 * m4;    
    return true;
}


// Jacobiano Analítico 3x4 (Control de Posición XYZ)
Eigen::MatrixXf Kinematic::Jacobian3x4(float th1, float th2, float th3, float th4) {
    // Pasar a radianes para los cálculos matemáticos
    float t1 = th1 * PI / 180.0;
    float t2 = th2 * PI / 180.0;
    float t3 = th3 * PI / 180.0;
    float t4 = th4 * PI / 180.0;
    
    // Precalcular senos y cosenos para ahorrar CPU
    float s1 = sin(t1), c1 = cos(t1);
    float s2 = sin(t2), c2 = cos(t2);
    float s23 = sin(t2 + t3), c23 = cos(t2 + t3);
    float s234 = sin(t2 + t3 + t4), c234 = cos(t2 + t3 + t4);
    
    // Variables cinemáticas agrupadas (basado en tus ecuaciones de pos2Angle)
    float W = w2 + w3 + w4;
    float R = l2 * c2 + l3 * c23 + l4 * c234; // Proyección en el plano radial
    
    // Posiciones Cartesianas Actuales
    float X = (R + w1) * c1 - W * s1;
    float Y = (R + w1) * s1 + W * c1;
    
    // Derivadas de la proyección Radial (R) respecto a los ángulos
    float dR_dt2 = -l2 * s2 - l3 * s23 - l4 * s234;
    float dR_dt3 = -l3 * s23 - l4 * s234;
    float dR_dt4 = -l4 * s234;
    
    // Construcción de la matriz 3x4
    Eigen::MatrixXf J(3, 4);
    
    // Fila 0: dX/dt
    J(0, 0) = -Y;
    J(0, 1) = dR_dt2 * c1;
    J(0, 2) = dR_dt3 * c1;
    J(0, 3) = dR_dt4 * c1;
    
    // Fila 1: dY/dt
    J(1, 0) = X;
    J(1, 1) = dR_dt2 * s1;
    J(1, 2) = dR_dt3 * s1;
    J(1, 3) = dR_dt4 * s1;
    
    // Fila 2: dZ/dt
    J(2, 0) = 0.0;
    J(2, 1) = l2 * c2 + l3 * c23 + l4 * c234;
    J(2, 2) = l3 * c23 + l4 * c234;
    J(2, 3) = l4 * c234;    
    return J;
}

// Jacobiano Analítico 4x4 (Control de Posición XYZ + Orientación Muñeca Phi)
Eigen::MatrixXf Kinematic::Jacobian4x4(float th1, float th2, float th3, float th4) {
    Eigen::MatrixXf J3x4 = Jacobian3x4(th1, th2, th3, th4);
    Eigen::MatrixXf J4x4(4, 4);
    J4x4.block<3,4>(0,0) = J3x4;    
    // Fila 3: d(phi)/dt. Como phi_rad = t2 + t3 + t4
    // Derivada de phi respecto a t1 es 0. Respecto a t2, t3, t4 es 1.
    J4x4(3, 0) = 0.0;
    J4x4(3, 1) = 1.0;
    J4x4(3, 2) = 1.0;
    J4x4(3, 3) = 1.0;
    
    return J4x4;
}


// Implementación de la Pseudo Inversa usando SVD (Eigen)
Eigen::MatrixXf Kinematic::pseudoInverse(const Eigen::MatrixXf& M) {
    // Calculamos la descomposición en valores singulares (SVD)
    Eigen::JacobiSVD<Eigen::MatrixXf> svd(M, Eigen::ComputeThinU | Eigen::ComputeThinV);
    
    Eigen::VectorXf singularValues = svd.singularValues();
    Eigen::MatrixXf S_inv = Eigen::MatrixXf::Zero(M.cols(), M.rows());
    
    // Tolerancia para evitar divisiones por cero en singularidades
    float tolerance = 1e-4f; 
    
    for (int i = 0; i < singularValues.size(); ++i) {
        if (singularValues(i) > tolerance) {
            S_inv(i, i) = 1.0f / singularValues(i);
        }
    }
    
    // Formula de la pseudoinversa: V * S_inv * U^T
    return svd.matrixV() * S_inv * svd.matrixU().transpose();
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