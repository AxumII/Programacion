#ifndef SYSTEM_CONFIG_H
#define SYSTEM_CONFIG_H

#include <Arduino.h>
#include <Keypad.h>
#include <Wire.h>
#include <SPI.h>

class SystemConfig {
    private:
        byte _dimA, _dimP, _dimL;
        
        byte* _pinAnalogI;
        byte* _pinPulsadores;
        byte* _pinLEDs;
        byte* _pinRows; // Tenía un error de punto y coma
        byte* _pinCols;
        byte* _pinI2C;
        byte* _pinSPI;

        char customKeys[4][4] = {
            { '1','2','3','A' },
            { '4','5','6','B' },
            { '7','8','9','C' },
            { '*','0','#','D' } 
        };
        
        Keypad _teclado; // Faltaba declarar el objeto aquí
        uint32_t _bauds;

    public:
        SystemConfig(byte dimA, byte dimP, byte dimL, 
                     byte* pA, byte* pP, byte* pL, 
                     byte* pF, byte* pC, 
                     uint32_t b, byte* pI, byte* pS);

        void start();
        char leerTeclado();
};

#endif