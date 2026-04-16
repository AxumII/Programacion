#include <iostream>
#include "Kinematic.h"

int main() {
    // Ejemplo de dimensiones: l1, l2, l3, w1, w2, w3, toolType, lTool, wTool, thetaTool
    float l1 = 40.04; // Longitud del primer eslabón
    float l2 = 100.8; // Longitud del segundo eslabón
    float l3 = 55;    // Longitud del tercer eslabón (si es
    float w1 = 0.1;     // Ancho del primer eslabón
    float w2 = 1;     // Ancho del segundo eslabón      
    float w3 = -14;     // Ancho del tercer eslabón (si es necesario)
    float lTool = 0;
    float wTool = 0;
    float thetaTool = 0;
    int toolType = 0; // Tipo de herramienta (1: pinza, 2: soldador, etc.)
    Kinematic robot(l1, l2, l3, w1, w2, w3, toolType, lTool, wTool, thetaTool);

    float t1, t2, t3;
    float targetX = 150.0, targetY = 0.0, targetZ = 0;

    std::cout << "--- Prueba de Cinemática Inversa ---" << std::endl;
    if (robot.pos2Angle(targetX, targetY, targetZ, t1, t2, t3)) {
        std::cout << "Ángulos calculados: " << std::endl;
        std::cout << "Theta 1: " << t1 << " deg" << std::endl;
        std::cout << "Theta 2: " << t2 << " deg" << std::endl;
        std::cout << "Theta 3: " << t3 << " deg" << std::endl;

        std::cout << "\n--- Prueba de Cinemática Directa ---" << std::endl;
        Kinematic::Matrix4f mat;
        robot.angle2Pos(t1, t2, t3, mat);
        //std::cout << "Matriz de Transformación Resultante:\n" << mat << std::endl;
        std::cout << "\nPosición final TCP: " 
                  << "X: " << mat(0,3) << " Y: " << mat(1,3) << " Z: " << mat(2,3) << std::endl;

        std::cout << "\n--- Prueba de Cinemática Directa Home---" << std::endl;
        Kinematic::Matrix4f mat2;
        robot.angle2Pos(0, 0, 0, mat2);
        //std::cout << "Matriz de Transformación Resultante:\n" << mat << std::endl;
        std::cout << "\nPosición final TCP: " 
                  << "X: " << mat2(0,3) << " Y: " << mat2(1,3) << " Z: " << mat2(2,3) << std::endl;

    } else {
        std::cerr << "Punto fuera del alcance del robot." << std::endl;
    }

    return 0;
}

/*
g++ -I "C:/Librerias c++/eigen-5.0.0" "C:/GitHub/Programacion/C++/Arduino/Brazo/v2/Kinematic Analysis/main.cpp" "C:/GitHub/Programacion/C++/Arduino/Brazo/v2/Kinematic Analysis/Kinematic.cpp" -o "C:/GitHub/Programacion/C++/Arduino/Brazo/v2/Kinematic Analysis/output/main.exe"; if ($?) { & "C:/GitHub/Programacion/C++/Arduino/Brazo/v2/Kinematic Analysis/output/main.exe" }

*/