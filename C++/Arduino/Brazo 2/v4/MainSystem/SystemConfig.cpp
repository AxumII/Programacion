#include "SystemConfig.h"

void ARDUINO_ISR_ATTR SystemConfig::debounceISR() {}

SystemConfig::SystemConfig(
    byte dimAnalog, byte* pAnalog,
    byte dimPWMLeft, byte* pPWMLeft,
    byte dimPWMRight, byte* pPWMRight,
    byte dimI2C, byte* pI2C,
    byte dimQEncA, byte* pQEncA,
    byte dimQEncB, byte* pQEncB,
    uint32_t bauds,
    byte dimSPI, byte* pSPI,
    byte dimCS, byte* pCS,
    byte dimDigIn, byte* pDigIn,
    byte dimDigOut, byte* pDigOut
) 
    : _dimAnalog(dimAnalog), _pinAnalog(pAnalog),
      _dimPWMLeft(dimPWMLeft), _pinPWMLeft(pPWMLeft),
      _dimPWMRight(dimPWMRight), _pinPWMRight(pPWMRight),
      _dimI2C(dimI2C), _pinI2C(pI2C),
      _dimQEncA(dimQEncA), _pinQEncA(pQEncA),
      _dimQEncB(dimQEncB), _pinQEncB(pQEncB),
      _bauds(bauds),
      _dimSPI(dimSPI), _pinSPI(pSPI),
      _dimCS(dimCS), _pinCS(pCS),
      _dimDigIn(dimDigIn), _pinDigIn(pDigIn),
      _dimDigOut(dimDigOut), _pinDigOut(pDigOut)
{
    _numEncoders = (_dimQEncA < 4) ? _dimQEncA : 4;
}

bool SystemConfig::start(){
    Serial.begin(_bauds);
    Serial.setTimeout(10);
    _preferencias.begin("robot", false);
    
    unsigned long SerialTimer = millis(); 
    while (millis() - SerialTimer < (unsigned long)timeout) {
        if (Serial) { _SerialStatus = true; break; }
        yield();
    }
    
    if (_SerialStatus) {
        Serial.println(F("[+] System: Serial Connected"));
    } else {
        Serial.end();
    }

    if (_dimI2C >= 2 && _pinI2C != nullptr) {
    Wire.begin(_pinI2C[0], _pinI2C[1]); // SDA, SCL
    
    _ads.begin(); // Inicializa la librería


    Wire.beginTransmission(0x48); // Dirección por defecto del ADS1115
    byte error = Wire.endTransmission();

    if (error == 0) {
        if(_SerialStatus) Serial.println(F("[+] ADS1115 (ADC) Detectado y Conectado OK."));
        _ADSStatus = true;
    } else {
        if(_SerialStatus) Serial.println(F("[-] ERROR: ADS1115 (ADC) No responde (Fallo de conexión)."));
        _ADSStatus = false;
        }
    }
    // --- Encoders (Hardware PCNT) ---
    for (int i = 0; i < _numEncoders; i++) {
        if (_pinQEncA != nullptr && _pinQEncB != nullptr) {
            _encoders[i].attachFullQuad(_pinQEncA[i], _pinQEncB[i]);
            
            // ¡NUEVO! Recuperar posición de memoria
            long savedPos = _preferencias.getLong(("E_" + String(i)).c_str(), 0);
            _encoders[i].setCount(savedPos);
            _lastSavedEncoders[i] = savedPos; // Guardar el tracking
            }
        }
    if(_SerialStatus) Serial.println(F("[+] Encoders configurados y recuperados de NVS."));

    // --- Configuración GPIO y PWM ---
    for (int i = 0; i < _dimAnalog; i++) { if (_pinAnalog != nullptr) pinMode(_pinAnalog[i], INPUT); }
    for (int i = 0; i < _dimDigIn; i++)  { if (_pinDigIn != nullptr) pinMode(_pinDigIn[i], INPUT_PULLUP); }
    for (int i = 0; i < _dimDigOut; i++) { if (_pinDigOut != nullptr) pinMode(_pinDigOut[i], OUTPUT); }
    
    for (int i = 0; i < _dimPWMLeft; i++) {
        if (_pinPWMLeft != nullptr) { 
            pinMode(_pinPWMLeft[i], OUTPUT); 
            ledcAttach(_pinPWMLeft[i], _pwmFreq, _pwmRes);
            ledcWrite(_pinPWMLeft[i], 0);
        }
    }
    for (int i = 0; i < _dimPWMRight; i++) {
        if (_pinPWMRight != nullptr) { 
            pinMode(_pinPWMRight[i], OUTPUT); 
            ledcAttach(_pinPWMRight[i], _pwmFreq, _pwmRes);
            ledcWrite(_pinPWMRight[i], 0);
        }
    }
    if(_SerialStatus) Serial.println(F("[+] Pines PWM y GPIO configurados."));

    return true; 
}
// =================================================================
// MÉTODOS DE LECTURA DE ENCODERS
// =================================================================

int64_t SystemConfig::getEncoderTicks(int id) {
    if (id < 0 || id >= _numEncoders) return 0;
    return _encoders[id].getCount();
}

float SystemConfig::getAngle(int id) {
    if (id < 0 || id >= _numEncoders) return 0.0f;
    
    int64_t ticks = _encoders[id].getCount();
    float ppr_val = (_ppr && _ppr[id] > 0) ? _ppr[id] : 1.0f;
    
    float angle_rad = ((float)ticks / ppr_val) * 2.0f * PI;
    
    if (_invEncoder && _invEncoder[id]) {
        angle_rad = -angle_rad;
    }    
    return angle_rad;
}

void SystemConfig::zeroEncoder(int id) {
    if (id < 0 || id >= _numEncoders) return;
    
    // Resetear el conteo del hardware
    _encoders[id].setCount(0);
    
    // Guardar el cero en la memoria permanente NVS
    _preferencias.putLong(("O_" + String(id)).c_str(), 0);
    _preferencias.putLong(("E_" + String(id)).c_str(), 0);
    
    _lastSavedEncoders[id] = 0;
}


void SystemConfig::savePositionsPeriodically(unsigned long interval_ms) {
    static unsigned long lastSaveTime = 0;
    if (millis() - lastSaveTime >= interval_ms) {
        lastSaveTime = millis();
        for (int i = 0; i < _numEncoders; i++) {
            long currentCount = (long)_encoders[i].getCount();
            if (currentCount != _lastSavedEncoders[i]) { // Cuidamos la vida útil verificando cambios
                _preferencias.putLong(("E_" + String(i)).c_str(), currentCount);
                _lastSavedEncoders[i] = currentCount;
            }
        }
    }
}

// =================================================================
// MÉTODOS I2C
// =================================================================

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

bool SystemConfig::setI2CChannel(uint8_t channel) {
    if (!_PCA9548Status || channel > 7) return false;
    Wire.beginTransmission(PCA9548_ADDR);
    Wire.write(1 << channel);
    return (Wire.endTransmission() == 0);
}

bool SystemConfig::writeExpanderAll(uint16_t states) {
    if (!_PCF8575Status) return false;
    pcf8575_state = states;
    Wire.beginTransmission(PCF8575_ADDR);
    Wire.write(lowByte(pcf8575_state));
    Wire.write(highByte(pcf8575_state));
    return (Wire.endTransmission() == 0);
}

bool SystemConfig::writeExpanderPin(uint8_t pin, bool state) {
    if (pin > 15) return false;
    if (state) {
        pcf8575_state |= (1 << pin);
    } else {
        pcf8575_state &= ~(1 << pin);
    }
    return writeExpanderAll(pcf8575_state);
}

bool SystemConfig::readExpanderAll(uint16_t &states) {
    if (!_PCF8575Status) return false;
    Wire.requestFrom((uint8_t)PCF8575_ADDR, (uint8_t)2);
    if (Wire.available() == 2) {
        uint8_t low = Wire.read();
        uint8_t high = Wire.read();
        states = (high << 8) | low;
        return true;
    }
    return false;
}

bool SystemConfig::readExpanderPin(uint8_t pin, bool &state) {
    if (pin > 15) return false;
    uint16_t allStates;
    if (readExpanderAll(allStates)) {
        state = (allStates & (1 << pin)) != 0;
        return true;
    }
    return false;
}

float SystemConfig::getCurrent(int id) {
    // Si el ADC no fue detectado al inicio, no intentamos leer I2C.
    if (!_ADSStatus) return 0.00; 
    
    // Mapeo inverso de ADC debido al cruce de pines de Base y Hombro
    int physical_adc = id;
    if (id == 0) physical_adc = 1;      // Lógico 0 (Base) lee el canal físico A1
    else if (id == 1) physical_adc = 0; // Lógico 1 (Hombro) lee el canal físico A0

    if (!_offsetsIS || _offsetsIS[physical_adc] <= 0.0) return 0.00;
    
    float vMedido = _ads.computeVolts(_ads.readADC_SingleEnded(physical_adc));
    float vSinRuido = vMedido - _offsetsIS[physical_adc];
    
    if (vSinRuido < 0.03) return 0.00;

    // El factor 31ZY ahora se aplica al canal físico 0
    float factor = (physical_adc == 0) ? _factor31ZY : _factorJGY;
    float corriente = vSinRuido * factor;

    return (corriente < 0.05) ? 0.00 : corriente;
}

// =================================================================
// MOTORES
// =================================================================

void SystemConfig::applyMotor(int id, float porcentaje, char dir) {
    if (id < 0 || id >= _dimPWMLeft || id >= _dimPWMRight) return;

    porcentaje = constrain(porcentaje, 0.0f, 100.0f);
    int maxPWM = (1 << _pwmRes) - 1; 
    int valPWM = (int)((porcentaje / 100.0f) * maxPWM);

    int pin_izq = (_invMotor && _invMotor[id]) ? _pinPWMRight[id] : _pinPWMLeft[id];
    int pin_der = (_invMotor && _invMotor[id]) ? _pinPWMLeft[id] : _pinPWMRight[id];

    if (porcentaje == 0.0f || dir == 'S') {
        ledcWrite(pin_izq, 0);
        ledcWrite(pin_der, 0);
        
        long currentCount = (long)_encoders[id].getCount();
        if (currentCount != _lastSavedEncoders[id]) {
            _preferencias.putLong(("E_" + String(id)).c_str(), currentCount);
            _lastSavedEncoders[id] = currentCount;
        }
    } else if (dir == 'H' || dir == 'R') {
        ledcWrite(pin_izq, 0);
        ledcWrite(pin_der, valPWM);
    } else if (dir == 'A' || dir == 'L') {
        ledcWrite(pin_der, 0);
        ledcWrite(pin_izq, valPWM);
    }
}
// =================================================================
// FUENTE
// =================================================================


float SystemConfig::getSourceVoltage() {
    if (_pinVFuente < 0) return 0.0f;
    return ((analogRead(_pinVFuente) / 4095.0) * 3.3f) * _fFuente;
}


// =================================================================
// GANANCIAS
// =================================================================
void SystemConfig::saveGains(int id, float kp, float ki, float fup, float fdown) {
    String base = "G" + String(id) + "_";
    _preferencias.putFloat((base + "P").c_str(), kp);
    _preferencias.putFloat((base + "I").c_str(), ki);
    _preferencias.putFloat((base + "U").c_str(), fup);
    _preferencias.putFloat((base + "D").c_str(), fdown);
}

void SystemConfig::loadGains(int id, float &kp, float &ki, float &fup, float &fdown) {
    String base = "G" + String(id) + "_";
    kp = _preferencias.getFloat((base + "P").c_str(), kp);
    ki = _preferencias.getFloat((base + "I").c_str(), ki);
    fup = _preferencias.getFloat((base + "U").c_str(), fup);
    fdown = _preferencias.getFloat((base + "D").c_str(), fdown);
}



