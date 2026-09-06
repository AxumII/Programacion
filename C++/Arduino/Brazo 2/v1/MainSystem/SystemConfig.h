#ifndef SYSTEM_CONFIG_H
#define SYSTEM_CONFIG_H

#include <Arduino.h>
#include <Wire.h>
#include <SPI.h>
#include <ArduinoEigenDense.h>

// Librerías de hardware movidas al sistema
#include <ESP32Encoder.h>
#include <Adafruit_ADS1X15.h>
#include <Preferences.h>

class SystemConfig {
private:
    byte* _pinAnalogI; byte* _pinDigitalIO; byte* _pinDigitalOut;
    byte* _pinPWMLeft; byte* _pinPWMRight;
    byte* _pinI2C; byte* _pinSPI;
    byte* _pinQEncA; byte* _pinQEncB;

    const bool* _invMotor;
    const bool* _invEnc;

    int _dimA, _dimDI, _dimDO, _dimPWM, _dimI2C, _dimSPI, _dimEnc;

    const uint8_t PCA9548_ADDR = 0x70; 
    const uint8_t PCF8575_ADDR = 0x20; 
    const uint8_t ADS1115_ADDR = 0x48; 
    uint16_t pcf8575_state = 0xFFFF;

    bool _SerialStatus = false; bool _I2CStatus = false; bool _SPIStatus = false;
    bool _PCA9548Status = false; bool _PCF8575Status = false; bool _ADSStatus = false;
    hw_timer_t* timerControl = NULL;

public:
    // Objetos instanciados en el sistema
    ESP32Encoder encoders[4];
    Adafruit_ADS1115 ads;
    Preferences preferencias;
    long offsets_enc[4];

    SystemConfig();

    bool bindPins(byte* pAI, int dA, byte* pDI, int dDI, byte* pDO, int dDO,
                  byte* pPWML, byte* pPWMR, int dPWM, byte* pI2C, int dI2C,
                  byte* pSPI, int dSPI, byte* pQA, byte* pQB, int dEnc);

    // Método para inyectar configuraciones lógicas
    void setInversions(const bool* invMotor, const bool* invEnc);

    bool start();

    // Método que oculta el hardware físico al aplicar PWM
    void applyMotor(int id, int pwm_val, char dir);

    // Utils
    Eigen::VectorXi I2CScan();
    bool setI2CChannel(uint8_t channel);
    bool writeExpanderAll(uint16_t states);
    bool writeExpanderPin(uint8_t pin, bool state);
    bool readExpanderAll(uint16_t &states);
    bool readExpanderPin(uint8_t pin, bool &state);
    static void IRAM_ATTR controlISR(); 
};

#endif