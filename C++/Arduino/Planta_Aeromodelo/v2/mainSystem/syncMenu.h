#ifndef SYNCMENU_H
#define SYNCMENU_H

#include <Arduino.h>
#include "plantStatus.h"
#include "plantController.h" // NUEVO

struct __attribute__((packed)) SensorDataPacket {
    uint8_t header[2]; 
    uint32_t timestamp; 
    float pwm;
    float angulo;
    float ax, ay, az;
    float gx, gy, gz;
    uint8_t footer;    
};

class SyncMenu {
private:
    plantStatus* _planta; 
    plantController* _controlador; // NUEVO Puntero
    uint32_t _lastTxTime;

    void executeCommand(String input); 

public:
    // NUEVO Constructor recibe ambos punteros
    SyncMenu(plantStatus* plantaPtr, plantController* ctrlPtr); 
    void processSerialCommands();
    void transmitData(uint32_t frequencyHz);
};

#endif