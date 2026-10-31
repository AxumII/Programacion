#ifndef SYNCMENU_H
#define SYNCMENU_H

#include <Arduino.h>
#include "plantStatus.h"

// Estructura binaria empaquetada de 39 bytes (muy rápida de transmitir)
struct __attribute__((packed)) SensorDataPacket {
    uint8_t header[2]; // Bytes de sincronización (Ej: 0xAA, 0xBB)
    uint32_t timestamp; // Marca de tiempo en microsegundos
    float pwm;
    float angulo;
    float ax, ay, az;
    float gx, gy, gz;
    uint8_t footer;    // Byte final (Ej: 0xCC)
};

class SyncMenu {
private:
    plantStatus* _planta; 
    uint32_t _lastTxTime;

    void executeCommand(String input); // Función interna auxiliar

public:
    SyncMenu(plantStatus* plantaPtr);
    
    // Método no bloqueante para leer comandos
    void processSerialCommands();
    
    // Método para transmitir el struct en binario a una frecuencia exacta
    void transmitData(uint32_t frequencyHz);
};

#endif