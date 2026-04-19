#define USE_PCA9685_SERVO_EXPANDER

#include <Arduino.h>
#include "SystemConfig.h"
#include "Kinematic.h"
#include "ServoControlling.h"
#include <ServoEasing.hpp>
#include "MenuView.h"
#include "MenuController.h"

// Datos de ejemplo para ESP32
byte aPines[] = {8};
byte dPines[] = {254};
byte pPines[] = {3, 47};
byte lPines[] = {45, 46};
byte rows[]   = {15, 16, 17, 18};
byte cols[]   = {39, 40, 41, 42};
byte i2cPins[] = {1, 2};
byte spiPins[] = {11, 255, 12, 10, 14, 9};// SPI para ST7789: MOSI(11), MISO(N/A), SCK(12), CS(10), DC(14), RST(9)
byte joystick1Pins[] = {4, 5, 21}; // X, Y, SW
byte joystick2Pins[] = {6, 7, 38}; // X, Y, SW
// Creamos la instancia

float l1 = 40.04; // Longitud del primer eslabón
float l2 = 100.8; // Longitud del segundo eslabón
float l3 = 55;    // Longitud del tercer eslabón (si es
float w1 = 0.1;     // Ancho del primer eslabón
float w2 = 1;     // Ancho del segundo eslabón      
float w3 = -14;     // Ancho del tercer eslabón (si es necesario)
int toolType = 0; // Tipo de herramienta (1: pinza, 2: soldador, etc.)
/*
float lTool = 114.8;  // Longitud de la herramienta
float wTool = -6.5;  // Ancho de la herramienta
float thetaTool = 0; // Ángulo de la herramienta respecto al último eslabón

*/

float lTool = 14;  // Longitud de la herramienta
float wTool = 0;  // Ancho de la herramienta
float thetaTool = 0; // Ángulo de la herramienta respecto al último eslabón



SystemConfig sistema(2, 2, 2, 1, aPines, pPines, lPines, dPines, rows, cols, 115200, i2cPins, spiPins, joystick1Pins, joystick2Pins);
Kinematic calculosBrazo(l1, l2, l3, w1, w2, w3, toolType, lTool, wTool, thetaTool);
//Kinematic calculosBrazo(l1, l2, l3, w1, w2, w3, toolType);
ServoControlling controladorServos(&calculosBrazo);
MenuView pantalla(spiPins[3], spiPins[4], spiPins[5]);
MenuController menu(&sistema, &pantalla, &controladorServos);

ServoEasing Servo1(0x40, &Wire); 
ServoEasing Servo2(0x40, &Wire);
ServoEasing Servo3(0x40, &Wire);


void setup() {
    SPI.begin(spiPins[2], spiPins[1], spiPins[0], spiPins[3]);
    sistema.start();
    pantalla.initTFT();
    controladorServos.settings(500, 2500, 620, 2280, 570, 2266, 180, 180, 180, 30, 'Q');    
    Serial.println("Sistema Iniciado - Esperando comandos...");
    

}

void loop() {
    /*char tecla = sistema.getKey();
    if (tecla == '*') {
        brazo.goHome();
        delay(2000);
        Eigen::Vector3f puntoDestino(12.0, 5.0, 8.0);
        brazo.moveJ(puntoDestino);
        delay(2000);
        brazo.goHome();
    }*/
    menu.update();
}