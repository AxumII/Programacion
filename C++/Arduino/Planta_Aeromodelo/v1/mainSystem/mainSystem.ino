#include <Arduino.h>
#include "systemConfig.h"
#include "plantStatus.h"
#include "syncMenu.h" // NUEVO: Incluimos el menú

// Pines de control del Motor: { PWMA, AIN1, AIN2 }
byte motorPins[] = {25, 26, 27}; 
byte stbyPin = 33;          
byte i2cPins[] = {21, 22};  
byte spiPins[] = {23, 19, 18, 5}; 

byte targetI2CAddress = 0x68; 

// Instancias encadenadas
SystemConfig sistema(spiPins, i2cPins, motorPins, stbyPin, targetI2CAddress);
plantStatus planta(&sistema);
SyncMenu menu(&planta); // NUEVO: Instancia de comunicación pasando la planta

void setup() {
  sistema.start();
  planta.calibrateSensors();
}

void loop() {
  // 1. Leer sensores (I2C)
  planta.updateSensors();
  // 2. Actualizar perfiles de motor (Rampas/Escalones no bloqueantes)
  planta.updateProfile(); 
  // 3. Escuchar si llegaron comandos (Z, S, Hxx) desde Python/Terminal
  menu.processSerialCommands(); 
  // 4. Transmitir los datos binarios exactos a la frecuencia deseada
  // Puedes cambiar 500 a la frecuencia que necesites (ej. 100, 500, 1000)
  menu.transmitData(500); 
}