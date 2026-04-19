#include <iostream>
#include <iomanip>
#include "Kinematic.h"

void printResults(const std::string& caseName, float tx, float ty, float tz, float t1, float t2, float t3, float t4, const Kinematic::Matrix4f& mat) {
    std::cout << "=== " << caseName << " ===" << std::endl;
    std::cout << "1. IK Angulos Calculados: T1:" << std::fixed << std::setprecision(2) << t1 << ", T2:" << t2 << ", T3:" << t3 << ", T4:" << t4 << std::endl;
    std::cout << "2. Posicion Resultante: X:" << mat(0,3) << " Y:" << mat(1,3) << " Z:" << mat(2,3) << std::endl;
    std::cout << "   Error vs Objetivo -> DX:" << (mat(0,3)-tx) << " DY:" << (mat(1,3)-ty) << " DZ:" << (mat(2,3)-tz) << std::endl;
    std::cout << "--------------------------------------------------------" << std::endl << std::endl;
}

int main() {
    float l1 = 40.04, l2 = 100.8, l3 = 55.0;
    float w1 = 0.1, w2 = 1.0, w3 = -14.0;
    float lTool = 25.0;
    float wTool = -6.5;
    Kinematic robot(l1, l2, l3, w1, w2, w3, lTool, wTool);

    float t1, t2, t3, t4;
    float targetX = 130.0, targetY = 20.0, targetZ = 60.0;
    Kinematic::Matrix4f mat;

    std::cout << "OBJETIVO ORIGINAL -> X:" << targetX << " Y:" << targetY << " Z:" << targetZ << "\n" << std::endl;

    // CASO 1: IK 3-DOF
    if (robot.pos2Angle(targetX, targetY, targetZ, t1, t2, t3, 0.0)) {
        robot.angle2Pos(t1, t2, t3, 0.0, mat);
        printResults("PRUEBA 3-DOF", targetX, targetY, targetZ, t1, t2, t3, 0.0, mat);
    }

    // CASO 2: IK 4-DOF
    float desiredPhi = 30.0;
    if (robot.pos2Angle(targetX, targetY, targetZ, t1, t2, t3, t4, desiredPhi)) {
        robot.angle2Pos(t1, t2, t3, t4, mat);
        printResults("PRUEBA 4-DOF", targetX, targetY, targetZ, t1, t2, t3, t4, mat);
    }

    // CASO 3: SISTEMA TCP (Normativa)
    Kinematic::Matrix4f matTCP, checkMat;
    // Generamos una matriz objetivo desde ángulos de prueba
    robot.angle2TCP(10.0, 30.0, -60.0, 20.0, matTCP);

    if (robot.TCP2angle(matTCP, t1, t2, t3, t4)) {
        robot.angle2TCP(t1, t2, t3, t4, checkMat);
        printResults("RECONSTRUCCION DESDE MATRIZ TCP", 
                      matTCP(0,3), matTCP(1,3), matTCP(2,3), 
                      t1, t2, t3, t4, checkMat);
    }

    return 0;
}
/*
g++ -I "C:/Librerias c++/eigen-5.0.0" "C:/GitHub/Programacion/C++/Arduino/Brazo/v2/Kinematic Analysis/main.cpp" "C:/GitHub/Programacion/C++/Arduino/Brazo/v2/Kinematic Analysis/Kinematic.cpp" -o "C:/GitHub/Programacion/C++/Arduino/Brazo/v2/Kinematic Analysis/output/main.exe"; if ($?) { & "C:/GitHub/Programacion/C++/Arduino/Brazo/v2/Kinematic Analysis/output/main.exe" }

*/