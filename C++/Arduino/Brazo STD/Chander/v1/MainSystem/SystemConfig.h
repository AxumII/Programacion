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

        // Cambiamos a 4 filas por 1 columna
        char customKeys[4][1] = {
            {'A'}, // Botón 1 -> Arriba
            {'B'}, // Botón 2 -> Abajo
            {'C'}, // Botón 3 -> Seleccionar / OK
            {'D'}  // Botón 4 -> Atrás / Salir
        };        
        Keypad _teclado;

        static volatile uint32_t _statePulsadores;
        static byte* _ptrPulsadores;
        static byte _numPulsadores;
        static byte* _pinJoy1; 
        static byte* _pinJoy2; 
        hw_timer_t* timerDebounce = NULL;

        unsigned long _joyTimer;
        const int _joyDelay;
        int timeout = 1000;
    public:
        bool _SPIStatus = false;
        bool _SerialStatus = false;
        bool _I2CStatus = false;
        bool _PCA9685Status = false;
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
        Eigen::VectorXi I2CScan();
        static void IRAM_ATTR debounceISR();

        bool readPulsador(byte index);
        void setLED(byte index, bool state);

        byte getJoystickPin(byte joyNum, byte axis);
        byte getAnalogPin(byte index);
        char getKey();
        int getJoystickAxis(byte joystick, char axis);
        bool getJoySwState(byte joyNum);
        float joystickAnalogProportional(int axisValue);
        
        int joystickAsSelector(int axisValue);
        int joystickAsFasterSelector(int axisValue);

        uint32_t getP();
        void clearP();            
};

#endif


