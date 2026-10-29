#include <Arduino.h>
#include "systemConfig.h"

// Pines
byte pwmPines[] = {19, 15}; // Pines para el driver TB6612 (ej. PWMA / PWMB o IN1 / IN2)
byte stbyPin = 14;          // Pin opcional para STBY (255 si no se usa)
byte i2cPins[] = {21, 22};  // SDA(21), SCL(22)
// SPI para SD: MOSI(23), MISO(19), SCK(18), CS(5). DC y RST se omiten para SD.
byte spiPins[] = {23, 19, 18, 5}; 

byte targetI2CAddress = 0x3C; // Dirección I2C del dispositivo a verificar

// Instancia
SystemConfig sistema(spiPins, i2cPins, pwmPines, stbyPin, targetI2CAddress);

void setup() {
  sistema.start();
}

void loop() {
  // Código principal
}