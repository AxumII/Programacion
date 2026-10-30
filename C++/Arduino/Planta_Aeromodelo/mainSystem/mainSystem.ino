#include <Arduino.h>
#include "systemConfig.h"
#include "plantStatus.h"

// Pines de control del Motor: { PWMA, AIN1, AIN2 }
byte motorPins[] = {25, 26, 27}; 
byte stbyPin = 33;          
byte i2cPins[] = {21, 22};  
byte spiPins[] = {23, 19, 18, 5}; 

byte targetI2CAddress = 0x68; 

// Instancias
SystemConfig sistema(spiPins, i2cPins, motorPins, stbyPin, targetI2CAddress);
plantStatus planta(&sistema);

void setup() {
  sistema.start();

  planta.calibrateSensors();
  
  Serial.println("Sistema Listo.");
  Serial.println("Comandos: Hxx (Horario), Axx (Antihorario), S (Stop), Z (Calibrar Ceros)");
}

void loop() {
  planta.updateSensors();
  
  // Imprime siempre los datos de los sensores
  planta.printData();
  
  // Escucha los comandos H, A, S, Z en cualquier momento
  planta.serialMotorControl();
  
  delay(100); 
}