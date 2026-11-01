#include <Arduino.h>
#include "systemConfig.h"
#include "plantStatus.h"
#include "plantController.h" 
#include "syncMenu.h" 

byte motorPins[] = {25, 26, 27}; 
byte stbyPin = 33;          
byte i2cPins[] = {21, 22};  
byte spiPins[] = {23, 19, 18, 5}; 
byte targetI2CAddress = 0x68; 

SystemConfig sistema(spiPins, i2cPins, motorPins, stbyPin, targetI2CAddress);
plantStatus planta(&sistema);
plantController controlador(&planta); // Instancia del controlador
SyncMenu menu(&planta, &controlador); // Punteros encadenados

void setup() {
  sistema.start();
  planta.calibrateSensors();
  
  // Ganancias iniciales: K, Ti, Td
  controlador.setPID(2.5, 0.5, 0.01);
}

void loop() {
  planta.updateSensors();
  planta.updateProfile(); 
  
  controlador.update(); // Inyecta la corrección del PID
  
  menu.processSerialCommands(); 
  menu.transmitData(500); 
}