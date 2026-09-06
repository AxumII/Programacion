#ifndef SYSTEMCONFIG_H
#define SYSTEMCONFIG_H

#include <Arduino.h>
#include <Wire.h>
#include <SPI.h>
#include <ArduinoEigen.h> 
#include <ESP32Encoder.h> 
#include <Adafruit_ADS1X15.h> // Librería ADC
#include <Preferences.h>      // Memoria NVS

#define PCA9548_ADDR 0x70
#define PCF8575_ADDR 0x20
#define ADS1115_ADDR 0x48

class SystemConfig {
private:
    byte _dimAnalog; byte* _pinAnalog;
    byte _dimPWMLeft; byte* _pinPWMLeft;
    byte _dimPWMRight; byte* _pinPWMRight;
    byte _dimI2C; byte* _pinI2C;
    byte _dimQEncA; byte* _pinQEncA;
    byte _dimQEncB; byte* _pinQEncB;
    uint32_t _bauds;
    byte _dimSPI; byte* _pinSPI;
    byte _dimCS; byte* _pinCS;
    byte _dimDigIn; byte* _pinDigIn;
    byte _dimDigOut; byte* _pinDigOut;

    // Configuraciones externas de Hardware
    const bool* _invMotor = nullptr;
    const bool* _invEncoder = nullptr;
    const float* _ppr = nullptr;

    // Parámetros de PWM
    uint32_t _pwmFreq = 20000;
    byte _pwmRes = 8;

    // Parámetros de Corriente (ADC)
    Adafruit_ADS1115 _ads;
    const float* _offsetsIS = nullptr;
    float _factor31ZY = 20.0;
    float _factorJGY = 13.6;

    // Parámetros Batería
    int _pinVFuente = -1;
    float _fFuente = 7.66;

    // Encoders y NVS
    ESP32Encoder _encoders[4];
    byte _numEncoders = 0;
    Preferences _preferencias;
    long _offsets_enc[4] = {0, 0, 0, 0};
    long _lastSavedEncoders[4] = {0, 0, 0, 0}; 

    // Variables de estado
    uint16_t timeout = 5000;
    uint16_t pcf8575_state = 0xFFFF;
    bool _SerialStatus = false;
    bool _SPIStatus = false;
    bool _PCA9548Status = false;
    bool _PCF8575Status = false;
    bool _ADSStatus = false;
    bool _I2CStatus = false;

    hw_timer_t * timerDebounce = NULL;


public:
    SystemConfig(
        byte dimAnalog, byte* pAnalog,
        byte dimPWMLeft, byte* pPWMLeft,
        byte dimPWMRight, byte* pPWMRight,
        byte dimI2C, byte* pI2C,
        byte dimQEncA, byte* pQEncA,
        byte dimQEncB, byte* pQEncB,
        uint32_t bauds = 115200,
        byte dimSPI = 0, byte* pSPI = nullptr,
        byte dimCS = 0, byte* pCS = nullptr,
        byte dimDigIn = 0, byte* pDigIn = nullptr,
        byte dimDigOut = 0, byte* pDigOut = nullptr
    );
    
    bool start();
    Eigen::VectorXi I2CScan();
    bool setI2CChannel(uint8_t channel);
    bool writeExpanderAll(uint16_t states);
    bool writeExpanderPin(uint8_t pin, bool state);
    bool readExpanderAll(uint16_t &states);
    bool readExpanderPin(uint8_t pin, bool &state);
    
    void applyMotor(int id, float porcentaje, char dir);

    // Inyección de parámetros
    void setInvMotor(const bool* invMotorConfig) { _invMotor = invMotorConfig; }
    void setEncoderParams(const bool* invEncConfig, const float* pprConfig) { 
        _invEncoder = invEncConfig; 
        _ppr = pprConfig; 
    }
    void setPWMParams(uint32_t freq, byte res) { _pwmFreq = freq; _pwmRes = res; }
    void setADCParams(const float* offsetsIS, float factor31, float factorJgy) {
        _offsetsIS = offsetsIS; _factor31ZY = factor31; _factorJGY = factorJgy;
    }
    void setPowerParams(int pin, float factor) { _pinVFuente = pin; _fFuente = factor; }

    // Lecturas de Hardware
    int64_t getEncoderTicks(int id);
    float getAngle(int id);
    float getCurrent(int id);
    float getSourceVoltage();
    
    // Calibración
    void zeroEncoder(int id);
    
    // Método para autoguardado
    void savePositionsPeriodically(unsigned long interval_ms);

    // Guardado y Carga de Ganancias PID en NVS
    void saveGains(int id, float kp, float ki, float fup, float fdown);
    void loadGains(int id, float &kp, float &ki, float &fup, float &fdown);

    static void ARDUINO_ISR_ATTR debounceISR();
};

#endif