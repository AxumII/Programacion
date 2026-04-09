#include "system_config.h"

SystemConfig::SystemConfig(byte dimA, byte dimP, byte dimL, 
                           byte* pA, byte* pB, byte* pL, 
                           byte* pF, byte* pC, 
                           uint32_t b, byte* pI, byte* pS) 
    : _dimA(dimA), _dimP(dimP), _dimL(dimL), 
      _pinAnalogI(pA), _pinButton(pB)), _pinLEDs(pL), 
      _pinRows(pF), _pinCols(pC), 
      _bauds(b), _pinI2C(pI), _pinSPI(pS),
      _teclado(makeKeymap(customKeys), pF, pC, 4, 4) {
}

void SystemConfig::start() {
    Serial.begin(_bauds);
    
    // I2C (SDA, SCL)
    Wire.begin(_pinI2C[0], _pinI2C[1]); 

    // SPI (MOSI, MISO, SCK) - El orden depende de tu librería de pantalla
    SPI.begin(_pinSPI[2], _pinSPI[1], _pinSPI[0]);

    for (int i = 0; i < _dimP; i++) {
        pinMode(_pinButton[i], INPUT_PULLUP);
    }
    for (int i = 0; i < _dimL; i++) {
        pinMode(_pinLEDs[i], OUTPUT);
    }
    for (int i = 0; i < _dimA; i++) {
        pinMode(_pinAnalogI[i], INPUT);
    }
    for (int i = 0; i < _dimD; i++) {
        pinMode(_pinDigitalIO[i], INPUT); // O OUTPUT según tu necesidad
    }

    Serial.println("SystemConfig: Hardware OK.");
}

char SystemConfig::leerTeclado() {
    return _teclado.getKey();
}