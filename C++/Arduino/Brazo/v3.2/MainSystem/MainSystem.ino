#define USE_PCA9685_SERVO_EXPANDER

#include <Arduino.h>
#include "SystemConfig.h"
#include "Kinematic.h"
#include "ServoControlling.h"
#include <ServoEasing.hpp>
#include "MenuManager.h"

// Solo conservamos los pines estrictamente necesarios (I2C)
byte i2cPins[] = {21, 22}; // SDA(21), SCL(22)

// Instanciamos el sistema apagando todo lo demás (0 y nullptr)
SystemConfig sistema(0, 0, 0, 0, nullptr, nullptr, nullptr, nullptr, nullptr, nullptr, 115200, i2cPins, nullptr, nullptr, nullptr);

ServoEasing Servo1(0x40, &Wire); 
ServoEasing Servo2(0x40, &Wire);
ServoEasing Servo3(0x40, &Wire);
ServoEasing Servo4(0x40, &Wire);
ServoEasing Servo5(0x40, &Wire);

Kinematic* cinBrazo = nullptr;
ServoControlling* controladorServos = nullptr;
MenuManager* menu = nullptr;

int typeDimensionsConfig = 4;

void setup(){
    switch (typeDimensionsConfig){
        case 0: { 
            float l1 = 40.04, l2 = 100.8, l3 = 55;
            float w1 = 15.1, w2 = 1, w3 = -14;
            float lTool = 14, wTool = -6.5;
            cinBrazo = new Kinematic(l1, l2, l3, w1, w2, w3, lTool, wTool, 0.0, 0.0);
            break;
        }
        case 1: { 
            float l1 = 40.04, l2 = 100.8, l3 = 85;
            float w1 = 15.1, w2 = 1, w3 = -14;
            float lTool = 14, wTool = -6.5;
            cinBrazo = new Kinematic(l1, l2, l3, w1, w2, w3, lTool, wTool, 0.0, 0.0);
            break;
        }
        case 2: { 
            float l1 = 40.04, l2 = 100.8, l3 = 55;
            float w1 = 15.1, w2 = 1, w3 = -14;
            float lTool = 90.4, wTool = -6.5;
            cinBrazo = new Kinematic(l1, l2, l3, w1, w2, w3, lTool, wTool, 0.0, 0.0);
            break;
        }
        case 3: { 
            float l1 = 40.04, l2 = 100.8, l3 = 70;
            float w1 = 15.1, w2 = 1, w3 = -14;
            float lTool = 69, wTool = 20.5;
            cinBrazo = new Kinematic(l1, l2, l3, w1, w2, w3, lTool, wTool, 0.0, 0.0);
            break;
        }
        case 4: { 
            float l1 = 40.04, l2 = 100.8, l3 = 70;
            float w1 = 15.1, w2 = 1, w3 = -14;
            float lTool = 90.4 + 55, wTool = 20.5;
            cinBrazo = new Kinematic(l1, l2, l3, w1, w2, w3, lTool, wTool, 0.0, 0.0);
            break;
        }
        default: {
            float l1 = 40.04, l2 = 100.8, l3 = 55;
            float w1 = 15.1, w2 = 1, w3 = -14;
            float lTool = 14, wTool = -6.5;
            cinBrazo = new Kinematic(l1, l2, l3, w1, w2, w3, lTool, wTool, 0.0, 0.0);
            break;
        }
    }
    
    controladorServos = new ServoControlling(cinBrazo);
    menu = new MenuManager(&sistema, controladorServos); 
    
    sistema.start();
    
    controladorServos->settings(612, 2305, 693, 2369, 652, 2266, 500, 2900, 180, 180, 135, 92, 20, 'Q'); 
    controladorServos->setupGripper(500, 1500, 180);
}

void loop(){
    menu->update();
}