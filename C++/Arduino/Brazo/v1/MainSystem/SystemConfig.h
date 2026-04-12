#ifndef SYSTEM_CONFIG_H
#define SYSTEM_CONFIG_H

#include <Arduino.h>
#include <Keypad.h>
#include <Wire.h>
#include <SPI.h>
#include <ArduinoEigenDense.h>
#include "MenuView.h"

class SystemConfig {
    private:
        byte _dimA, _dimP, _dimL, _dimD;
        byte* _pinAnalogI;
        byte* _pinDigitalIO;
        byte* _pinPulsadores;
        byte* _pinLEDs;
        byte* _pinRows; 
        byte* _pinCols;
        byte* _pinI2C;
        byte* _pinSPI;
        uint32_t _bauds;
        byte* _pinJoy1; // Para {X, Y, SW}
        byte* _pinJoy2; // Para {X, Y, SW}

        char customKeys[4][4] = {
            { '1','2','3','A' },
            { '4','5','6','B' },
            { '7','8','9','C' },
            { '*','0','#','D' } 
        };        
        Keypad _teclado; 

        static volatile uint32_t _statePulsadores;
        static byte* _ptrPulsadores;
        static byte _numPulsadores;
        hw_timer_t* timerDebounce = NULL;

        bool _I2CStatus, _PCA9685Status, _SPIStatus, _SerialStatus, _GPIOStatus;

        unsigned long _joyTimer;
        const int _joyDelay; // Se inicializa en el constructor

    public:
        SystemConfig(byte dimA, byte dimP, byte dimL, byte dimD,
                     byte* pA, byte* pP, byte* pL, byte* pD, 
                     byte* pF, byte* pC, uint32_t b, 
                     byte* pI, byte* pS, byte* j1, byte* j2);


        uint64_t getKeyboardWakeupMask() {
            uint64_t mask = 0;
            for (int i = 0; i < 4; i++) {
                mask |= (1ULL << _pinRows[i]);
            }
            return mask;
        }

        bool start();
        static void IRAM_ATTR debounceISR();

        bool readPulsador(byte index);
        void setLED(byte index, bool state);
        byte getJoystickPin(byte joyNum, byte axis);
        byte getAnalogPin(byte index);
        char getKey();
        
        int joystickAsSelector(int axisValue);
        int joystickAsFasterSelector(int axisValue);
        bool statusChecker();
        Eigen::VectorXi I2CScan();

        uint32_t getP();
        void clearP();

        int getJoystickAxis(byte joystick, char axis);

};

#endif