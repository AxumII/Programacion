#include "SystemConfig.h"

volatile uint32_t SystemConfig::_statePulsadores = 0;
byte* SystemConfig::_ptrPulsadores = nullptr;
byte SystemConfig::_numPulsadores = 0; 
byte* SystemConfig::_pinJoy1 = nullptr;
byte* SystemConfig::_pinJoy2 = nullptr;

SystemConfig::SystemConfig(byte dimA, byte dimP, byte dimL, byte dimD,
                           byte* pA, byte* pP, byte* pL, byte* pD, 
                           byte* pF, byte* pC, uint32_t b, 
                           byte* pI, byte* pS, byte* j1, byte* j2) 
    : _dimA(dimA), _dimP(dimP), _dimL(dimL), _dimD(dimD),
      _pinAnalogI(pA), _pinPulsadores(pP), _pinLEDs(pL), _pinDigitalIO(pD), 
      _pinRows(pF), _pinCols(pC), _bauds(b), _pinI2C(pI), _pinSPI(pS),
      _teclado(makeKeymap(customKeys), pF, pC, 4, 1),
      _joyTimer(0), _joyDelay(300)
{
    _ptrPulsadores = pP;
    _numPulsadores = dimP;
    _pinJoy1 = j1; 
    _pinJoy2 = j2;
}

bool SystemConfig::start(){
    //GPIO
    for (int i = 0; i < _numPulsadores; i++) pinMode(_ptrPulsadores[i], INPUT_PULLUP);
    for (int i = 0; i < _dimL; i++) pinMode(_pinLEDs[i], OUTPUT);
    for (int i = 0; i < _dimD; i++) {
        if (_pinDigitalIO != nullptr) pinMode(_pinDigitalIO[i], INPUT);
    }
    for (int i = 0; i < _dimA; i++) {
        if (_pinAnalogI != nullptr) pinMode(_pinAnalogI[i], INPUT); // En ESP32 se usa INPUT para analógicos
    }
    if (_pinJoy1 != nullptr) pinMode(_pinJoy1[2], INPUT_PULLUP);
    if (_pinJoy2 != nullptr) pinMode(_pinJoy2[2], INPUT_PULLUP);

    //SPI 
    if (_dimL > 0) digitalWrite(_pinLEDs[0], HIGH);
    SPI.begin(_pinSPI[2], _pinSPI[1], _pinSPI[0], _pinSPI[3]);
    UI = new MenuView(_pinSPI[3], _pinSPI[4], _pinSPI[5]);
    UI->initTFT();      
    UI->loadScreen();
    _SPIStatus = (UI != nullptr);
    if (!_SPIStatus && _dimL > 0) digitalWrite(_pinLEDs[0], LOW);
   

    //Serial 
    Serial.begin(_bauds);
    unsigned long SerialTimer = millis(); // Usando tu nombre de timer
    while (millis() - SerialTimer < (unsigned long)timeout) {
        if (Serial) {
            _SerialStatus = true;
            break;
        }
        yield();
    }

    if (_SerialStatus) {
        Serial.println(F("System: Serial Connected"));
    } else {
        Serial.end();
        if (_dimL > 0) digitalWrite(_pinLEDs[0], LOW);
    }


    //I2C
    Wire.setPins(_pinI2C[0], _pinI2C[1]); 
    Wire.begin(); 
    unsigned long I2CTimer = millis();
    _I2CStatus = false;
    _PCA9685Status = false;
    while (millis() - I2CTimer < timeout){
        Wire.beginTransmission(0x40); 
        if (Wire.endTransmission() == 0) {
            _I2CStatus = true;
            _PCA9685Status  = true;
            break;
        }
        yield();
    }
    if (!_I2CStatus && _dimL > 0) digitalWrite(_pinLEDs[0], LOW);
    //Timer 
    timerDebounce = timerBegin(1000000); 
    timerAttachInterrupt(timerDebounce, SystemConfig::debounceISR);
    timerAlarm(timerDebounce, 50000, true, 0); 

    return _I2CStatus && _PCA9685Status && _SPIStatus && _SerialStatus;
}

Eigen::VectorXi SystemConfig::I2CScan() {
    uint8_t tempDir[127];
    int contador = 0;
    byte error, address;
    for (address = 1; address < 127; address++) {
        Wire.beginTransmission(address);
        error = Wire.endTransmission();
        if (error == 0) {
            tempDir[contador] = address;
            contador++;        
        }
    }
    Eigen::VectorXi resultado(contador);
    for (int i = 0; i < contador; i++) {
        resultado(i) = tempDir[i];
    }
    return resultado;
}

void IRAM_ATTR SystemConfig::debounceISR() {

    for (int i = 0; i < _numPulsadores; i++) {
        if (digitalRead(_ptrPulsadores[i]) == LOW) {
            _statePulsadores |= (1 << i); 
        }
    }
    if (_pinJoy1 != nullptr && digitalRead(_pinJoy1[2]) == LOW) {
        _statePulsadores |= (1 << _numPulsadores);
    }
    if (_pinJoy2 != nullptr && digitalRead(_pinJoy2[2]) == LOW) {
        _statePulsadores |= (1 << (_numPulsadores + 1));
    }
}

uint32_t SystemConfig::getP() { return _statePulsadores; }

void SystemConfig::clearP() { _statePulsadores = 0; }

int SystemConfig::joystickAsSelector(int axisValue) {
    int d = 0;
    if (axisValue > 3000) d = 1;
    else if (axisValue < 1000) d = -1;
    else d = 0;
    if (millis() - _joyTimer > _joyDelay && d != 0) {
        _joyTimer = millis();
        return d;
    }
    return 0;
}

int SystemConfig::joystickAsFasterSelector(int axisValue) {
    int d = 0;

    if (axisValue > 3500) d = 2;  // Movimiento rápido positivo
    else if (axisValue > 2600) d = 1;  // Movimiento lento positivo            
    else if (axisValue < 500)  d = -2; // Movimiento rápido negativo
    else if (axisValue < 1500) d = -1; // Movimiento lento negativo            
    else d = 0; // Si está entre 1500 y 2600, se considera "QUIETO"

    // Si hay movimiento, aplicamos el debounce de tiempo
    if (millis() - _joyTimer > _joyDelay) {
        _joyTimer = millis();
        return d;
    }
    else return 0; // Bloqueado por debounce
}

char SystemConfig::getKey() {
    return _teclado.getKey();
}

void SystemConfig::setLED(byte index, bool state) {
    if (index < _dimL) digitalWrite(_pinLEDs[index], state);
}

bool SystemConfig::readPulsador(byte index) {
    if (index < _dimP) return digitalRead(_pinPulsadores[index]);
    else return LOW;// 
}

byte SystemConfig::getAnalogPin(byte index) {
    if (index < _dimA) return _pinAnalogI[index];
    else return 0; 
}

byte SystemConfig::getJoystickPin(byte joyNum, byte axis) {
    if (joyNum == 1 && _pinJoy1) return _pinJoy1[axis];
    if (joyNum == 2 && _pinJoy2) return _pinJoy2[axis];
    return 255;
}

int SystemConfig::getJoystickAxis(byte joystick, char axis) {
    axis = toupper(axis); 
    if (joystick == 1) {
        // Se resta de 4095 para invertir físicamente la lectura
        if (axis == 'X') return 4095 - analogRead(_pinJoy1[0]);
        if (axis == 'Y') return 4095 - analogRead(_pinJoy1[1]);
    } 
    else if (joystick == 2) {
        if (axis == 'X') return 4095 - analogRead(_pinJoy2[0]);
        if (axis == 'Y') return 4095 - analogRead(_pinJoy2[1]);
    }    
    return 0; 
}


bool SystemConfig::getJoySwState(byte joyNum) {
    bool pressed = false;
    if (joyNum == 1 && (_statePulsadores & (1 << _numPulsadores))) {
        pressed = true;
        _statePulsadores &= ~(1 << _numPulsadores); 
    }
    else if (joyNum == 2 && (_statePulsadores & (1 << (_numPulsadores + 1)))) {
        pressed = true;
        _statePulsadores &= ~(1 << (_numPulsadores + 1)); 
    }
    return pressed;
}

float SystemConfig::joystickAnalogProportional(int axisValue) {
    const int centerLow = 1500;  // Antes 1800
    const int centerHigh = 2500; // Antes 2200
    const int minVal = 0;
    const int maxVal = 4095;

    if (axisValue > centerHigh) {
        float val = (float)(axisValue - centerHigh) / (maxVal - centerHigh);
        return constrain(val, 0.0f, 1.0f); 
    } 
    else if (axisValue < centerLow) {
        float val = (float)(axisValue - centerLow) / centerLow; 
        return constrain(val, -1.0f, 0.0f); 
    }    
    return 0.0f; 
}