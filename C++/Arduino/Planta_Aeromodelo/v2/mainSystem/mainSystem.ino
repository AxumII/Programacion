#include <Arduino.h>
#include "systemConfig.h"
#include "plantStatus.h"
#include "plantController.h" // NUEVO
#include "syncMenu.h" 

byte motorPins[] = {25, 26, 27}; 
byte stbyPin = 33;          
byte i2cPins[] = {21, 22};  
byte spiPins[] = {23, 19, 18, 5}; 
byte targetI2CAddress = 0x68; 

// Instancias conectadas en cascada
SystemConfig sistema(spiPins, i2cPins, motorPins, stbyPin, targetI2CAddress);
plantStatus planta(&sistema);
plantController controlador(&planta); // El controlador manipula la planta
SyncMenu menu(&planta, &controlador); // El menú manda sobre la planta y el controlador

void setup() {
  sistema.start();
  planta.calibrateSensors();
  
  // Configuración PID inicial: K = 2.5, Ti = 0.5, Td = 0.01 (Ajustar según pruebas reales)
  controlador.setPID(2.5, 0.5, 0.01);
}

void loop() {
  // 1. Leer sensores físicos a máxima velocidad
  planta.updateSensors();
  
  // 2. Procesar perfiles en lazo abierto (Escalones puros/Rampas)
  planta.updateProfile(); 
  
  // 3. Procesar el lazo cerrado (El PID inyectará aquí las variaciones de PWM)
  controlador.update();
  
  // 4. Escuchar comandos desde Python
  menu.processSerialCommands(); 
  
  // 5. Enviar telemetría binaria (ej. 500 Hz)
  menu.transmitData(500); 
}