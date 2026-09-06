#include "SystemConfig.h"

SystemConfig::SystemConfig() {
    _pinAnalogI = nullptr; _pinDigitalIO = nullptr; _pinDigitalOut = nullptr;
    _pinPWMLeft = nullptr; _pinPWMRight = nullptr; _pinI2C = nullptr;
    _pinSPI = nullptr; _pinQEncA = nullptr; _pinQEncB = nullptr;
    _dimA = 0; _dimDI = 0; _dimDO = 0; _dimPWM = 0; _dimI2C = 0; _dimSPI = 0; _dimEnc = 0;    
    for(int i=0; i<4; i++) offsets_enc[i] = 0;
}

bool SystemConfig::bindPins(byte* pAI, int dA, byte* pDI, int dDI, byte* pDO, int dDO,
                            byte* pPWML, byte* pPWMR, int dPWM, byte* pI2C, int dI2C,
                            byte* pSPI, int dSPI, byte* pQA, byte* pQB, int dEnc) {
    
    _pinAnalogI = pAI;       _dimA = dA;
    _pinDigitalIO = pDI;     _dimDI = dDI;
    _pinDigitalOut = pDO;    _dimDO = dDO;
    
    _pinPWMLeft = pPWML;     
    _pinPWMRight = pPWMR;    
    _dimPWM = dPWM;
    
    _pinI2C = pI2C;          _dimI2C = dI2C;
    _pinSPI = pSPI;          _dimSPI = dSPI;
    
    _pinQEncA = pQA;         
    _pinQEncB = pQB;         
    _dimEnc = dEnc;
    
    return true;
}

void SystemConfig::setInversions(const bool* invMotor, const bool* invEnc) {
    _invMotor = invMotor;
    _invEnc = invEnc;
}

bool SystemConfig::start() {
    // --- Serial ---
    Serial.begin(115200);
    unsigned long serialTimer = millis();
    while (!Serial && millis() - serialTimer < 2000) { yield(); }
    _SerialStatus = true;
    Serial.println("\n--- Iniciando Sistema ---");

    // --- GPIO ---
    Serial.println("[*] Configurando GPIO...");
    for (int i = 0; i < _dimA; i++) {
        if (_pinAnalogI != nullptr) pinMode(_pinAnalogI[i], INPUT);
    }
    for (int i = 0; i < _dimDI; i++) {
        if (_pinDigitalIO != nullptr) pinMode(_pinDigitalIO[i], INPUT_PULLUP);
    }
    for (int i = 0; i < _dimDO; i++) {
        if (_pinDigitalOut != nullptr) pinMode(_pinDigitalOut[i], OUTPUT);
    }
    for (int i = 0; i < _dimPWM; i++) {
        if (_pinPWMLeft != nullptr) {
            pinMode(_pinPWMLeft[i], OUTPUT);
            digitalWrite(_pinPWMLeft[i], LOW);
        }
        if (_pinPWMRight != nullptr) {
            pinMode(_pinPWMRight[i], OUTPUT);
            digitalWrite(_pinPWMRight[i], LOW);
        }
    }
    for (int i = 0; i < _dimEnc; i++) {
        if (_pinQEncA != nullptr) pinMode(_pinQEncA[i], INPUT_PULLUP);
        if (_pinQEncB != nullptr) pinMode(_pinQEncB[i], INPUT_PULLUP);
    }

    // --- SPI ---
    Serial.println("[*] Configurando SPI...");
    if (_dimSPI >= 4) {
        SPI.begin(_pinSPI[2], _pinSPI[1], _pinSPI[0], _pinSPI[3]);
        _SPIStatus = true;
    } else {
        Serial.println("[-] No se declararon pines SPI suficientes.");
        _SPIStatus = false;
    }

    // --- I2C ---
    // --- I2C ---
    Serial.println("[*] Configurando I2C...");
    if (_dimI2C >= 2) {
        Wire.begin(_pinI2C[0], _pinI2C[1]); // SDA, SCL
        Wire.setClock(100000); // 100 kHz (Más estable para cables o sensores ausentes)
        Wire.setTimeOut(20);   // Timeout corto
        delay(50);
        
        // Comprobación segura y aislada para evitar bloqueos del bus
        Wire.beginTransmission(PCA9548_ADDR);
        _PCA9548Status = (Wire.endTransmission() == 0);
        delay(5); // Respiro de bus

        Wire.beginTransmission(PCF8575_ADDR);
        _PCF8575Status = (Wire.endTransmission() == 0);
        delay(5); // Respiro de bus

        Wire.beginTransmission(ADS1115_ADDR);
        _ADSStatus = (Wire.endTransmission() == 0);
        delay(5);
    }
    
    // --- REPORTE DETALLADO I2C ---
    if (_PCA9548Status) Serial.println("[+] PCA9548A (Multiplexor) OK.");
    else Serial.println("[-] AVISO: PCA9548A (Multiplexor) NO DETECTADO (Desconectado).");

    if (_PCF8575Status) Serial.println("[+] PCF8575 (Expansor I/O) OK.");
    else Serial.println("[-] AVISO: PCF8575 (Expansor I/O) NO DETECTADO (Desconectado).");

    if (_ADSStatus) Serial.println("[+] ADS1115 (ADC) OK.");
    else Serial.println("[-] ERROR: ADS1115 (ADC) NO DETECTADO.");

    // Permitir que el sistema arranque si hay al menos comunicación básica
    if (_PCA9548Status || _PCF8575Status || _ADSStatus) {
        _I2CStatus = true;
        if (_PCF8575Status) writeExpanderAll(0xFFFF);
        if (_PCA9548Status) setI2CChannel(0);         
    } else {
        _I2CStatus = false;
        Serial.println("[-] AVISO: Ningun modulo I2C respondio, continuando de forma segura...");
    }
    
    
    
}

Eigen::VectorXi SystemConfig::I2CScan() {
    uint8_t tempDir[127];
    int contador = 0;
    byte error, address;
    
    Serial.println("\n[Escaneo I2C Iniciado]");
    for (address = 1; address < 127; address++) {
        Wire.beginTransmission(address);
        error = Wire.endTransmission();
        if (error == 0) {
            tempDir[contador] = address;
            Serial.print("Dispositivo en direccion: 0x");
            if (address < 16) Serial.print("0");
            Serial.println(address, HEX);
            contador++;        
        }
    }
    Serial.println("[Escaneo I2C Finalizado]\n");
    
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

void SystemConfig::applyMotor(int id, int pwm_val, char dir) {
    if(id >= _dimPWM) return;
    
    int pin_izq = (_invMotor && _invMotor[id]) ? _pinPWMRight[id] : _pinPWMLeft[id];
    int pin_der = (_invMotor && _invMotor[id]) ? _pinPWMLeft[id] : _pinPWMRight[id];

    if (dir == 'R') {
        analogWrite(pin_der, pwm_val);
        analogWrite(pin_izq, 0);
    } else if (dir == 'L') {
        analogWrite(pin_der, 0);
        analogWrite(pin_izq, pwm_val);
    } else {
        analogWrite(pin_der, 0);
        analogWrite(pin_izq, 0);
    }
}

void IRAM_ATTR SystemConfig::controlISR() {
}