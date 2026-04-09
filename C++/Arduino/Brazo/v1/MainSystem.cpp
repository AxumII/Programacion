#include <Arduino.h>
#include "SystemConfig.h"
#include "Angle2Pos.h"
// Datos de ejemplo para ESP32
byte aPines[] = {34, 35};
byte pPines[] = {4, 5, 18};
byte lPines[] = {2, 15};
byte rows[]   = {13, 12, 14, 27};
byte cols[]   = {26, 25, 33, 32};
byte i2cPins[] = {21, 22};
byte spiPins[] = {23, 19, 18}; // MOSI, MISO, SCK

// Creamos la instancia
SystemConfig sistema(2, 3, 2, aPines, pPines, lPines, rows, cols, 115200, i2cPins, spiPins);

void setup() {
    sistema.start();
}

void loop() {
    char tecla = sistema.leerTeclado();
    if (tecla == 'A') {
        arm.moveServo(100, 100, 50);
    }
}