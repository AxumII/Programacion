#ifndef SYSTEMCONFIG_H
#define SYSTEMCONFIG_H

#include <Arduino.h>
#include <SPI.h>
#include <SD.h>
#include <Wire.h>
#include "driver/mcpwm.h"

class SystemConfig {
private:
    byte* _pinSPI;
    byte* _pinI2C;
    byte* _pinPWM;
    byte _pinSTBY;
    byte _i2cAddress;
    
    bool _SDStatus;
    bool _I2CStatus;
    bool _SerialStatus;
    
    unsigned long _bauds;
    unsigned int timeout;

public:
    SystemConfig(byte* spiPins, byte* i2cPins, byte* pwmPins, byte stbyPin, byte i2cAddress);
    bool start();
};

#endif