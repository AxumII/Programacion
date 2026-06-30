#define USE_PCA9685_SERVO_EXPANDER

#include <Arduino.h>
#include "SystemConfig.h"
#include "Kinematic.h"
#include "ServoControlling.h"
#include <ServoEasing.hpp>
#include "MenuView.h"
#include "MenuController.h"

// Pines
byte aPines[] = {255};
byte dPines[] = {254};
byte pPines[] = {19, 15};
byte lPines[] = {253,252};
byte rows[]   = {13, 14, 27, 16};
byte cols[]   = {17};
byte i2cPins[] = {21, 22}; // SDA(21), SCL(22)
byte spiPins[] = {23, 255, 18, 5, 2, 4};// SPI para ST7789: MOSI(11), MISO(N/A), SCK(12), CS(10), DC(14), RST(9)
byte joystick1Pins[] = {32, 33, 25}; // X, Y, SW
byte joystick2Pins[] = {34, 35, 26}; // X, Y, SW


//Instancias
SystemConfig sistema(2, 2, 2, 1, aPines, pPines, lPines, dPines, rows, cols, 115200, i2cPins, spiPins, joystick1Pins, joystick2Pins);

ServoEasing Servo1(0x40, &Wire); 
ServoEasing Servo2(0x40, &Wire);
ServoEasing Servo3(0x40, &Wire);
ServoEasing Servo4(0x40, &Wire);

Kinematic* cinBrazo = nullptr;
ServoControlling* controladorServos = nullptr;
MenuController* menu = nullptr;


int typeDimensionsConfig = 3;

void setup(){
    // IMPORTANTE: Nota cómo cada case ahora tiene llaves { }
    switch (typeDimensionsConfig){
        case 0: { // 3 articulaciones, antebrazo corto, con tool de calibracion
            float l1 = 40.04, l2 = 100.8, l3 = 55;
            float w1 = 15.1, w2 = 1, w3 = -14;
            float lTool = 14, wTool = -6.5;
            // Se usa "new" para guardar el objeto en el puntero global
            cinBrazo = new Kinematic(l1, l2, l3, w1, w2, w3, lTool, wTool, 0.0, 0.0);
            break;
        }
        case 1: { // 3 articulaciones, antebrazo largo con tool de calibracion
            float l1 = 40.04, l2 = 100.8, l3 = 85;
            float w1 = 15.1, w2 = 1, w3 = -14;
            float lTool = 14, wTool = -6.5;
            cinBrazo = new Kinematic(l1, l2, l3, w1, w2, w3, lTool, wTool, 0.0, 0.0);
            break;
        }
        case 2: { // 3 articulaciones, antebrazo corto, con grippen
            float l1 = 40.04, l2 = 100.8, l3 = 55;
            float w1 = 15.1, w2 = 1, w3 = -14;
            float lTool = 90.4, wTool = -6.5;
            cinBrazo = new Kinematic(l1, l2, l3, w1, w2, w3, lTool, wTool, 0.0, 0.0);
            break;
        }
        case 3: { // 4 articulaciones, antebrazo corto, con tool de calibracion
            float l1 = 40.04, l2 = 100.8, l3 = 70;
            float w1 = 15.1, w2 = 1, w3 = -14;
            float lTool = 69, wTool = 20.5;
            cinBrazo = new Kinematic(l1, l2, l3, w1, w2, w3, lTool, wTool, 0.0, 0.0);
            break;
        }
        case 4: { // 4 articulaciones, antebrazo corto, con grippen
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
    
    // Asignación de dependencias
    controladorServos = new ServoControlling(cinBrazo);
    menu = new MenuController(&sistema, controladorServos);
    
    sistema.start();
    
    controladorServos->settings(612, 2305, 693, 2369, 652, 2266, 500, 2900, 180, 180, 135, 92, 20, 'Q'); 
}

void loop(){
    menu->update();
}