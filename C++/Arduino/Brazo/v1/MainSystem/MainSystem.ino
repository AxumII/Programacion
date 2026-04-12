#define USE_PCA9685_SERVO_EXPANDER

#include <Arduino.h>
#include "SystemConfig.h"
#include "Kinematic.h"
#include "ServoControlling.h"
#include <ServoEasing.hpp>
#include "MenuView.h"
#include "MenuController.h"

// Datos de ejemplo para ESP32
byte aPines[] = {8, 9};
byte dPines[] = {254};
byte pPines[] = {3, 47};
byte lPines[] = {45, 46};
byte rows[]   = {15, 16, 17, 18};
byte cols[]   = {39, 40, 41, 42};
byte i2cPins[] = {1, 2};
byte spiPins[] = {11, 255, 12, 10, 13, 14}; // SPI para ST7789: MOSI(11), MISO(N/A), SCK(12), CS(10), DC(13), RST(14)
byte joystick1Pins[] = {5, 4, 21}; // X, Y, SW
byte joystick2Pins[] = {7, 6, 38}; // X, Y
// Creamos la instancia

SystemConfig sistema(2, 2, 2, 1, aPines, pPines, lPines, dPines, rows, cols, 115200, i2cPins, spiPins, joystick1Pins, joystick2Pins);
Kinematic cerebro(97.0, 106.0, 0, 0, 0);
ServoControlling brazo(&cerebro);
MenuView pantalla(spiPins[3], spiPins[4], spiPins[5]);
MenuController menu(&sistema, &pantalla);

ServoEasing Servo1(0x40, &Wire); 
ServoEasing Servo2(0x40, &Wire);
ServoEasing Servo3(0x40, &Wire);


void setup() {
    sistema.start();
    brazo.settings(500, 2500, 500, 2500, 500, 2500, 90, 120, 90, 30, 'Q');
    
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