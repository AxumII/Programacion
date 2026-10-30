#include "systemConfig.h"

SystemConfig::SystemConfig(byte* spiPins, byte* i2cPins, byte* mPins, byte stbyPin, byte i2cAddress) {
    _pinSPI = spiPins;
    _pinI2C = i2cPins;
    motorPins = mPins;
    _pinSTBY = stbyPin;
    _i2cAddress = i2cAddress;
    
    _bauds = 115200;
    timeout = 5000;
    
    _SDStatus = false;
    _I2CStatus = false;
    _SerialStatus = false;
}

bool SystemConfig::start() {
    Serial.begin(_bauds);
    unsigned long SerialTimer = millis(); 
    while (millis() - SerialTimer < timeout) {
        if (Serial) { _SerialStatus = true; break; }
        yield();
    }

    // --- Configuración H-Bridge y ledc (Core 3.x) ---
    pinMode(motorPins[1], OUTPUT); // AIN1
    pinMode(motorPins[2], OUTPUT); // AIN2
    
    if (_pinSTBY != 255) {
        pinMode(_pinSTBY, OUTPUT);
        digitalWrite(_pinSTBY, HIGH); // Despertar el driver
    }

    ledcAttach(motorPins[0], 20000, 8); // PWMA a 20kHz, resolución de 8 bits
    digitalWrite(motorPins[1], LOW);
    digitalWrite(motorPins[2], LOW);
    ledcWrite(motorPins[0], 0);

    // --- Inicialización I2C y Sensores ---
    Wire.begin(_pinI2C[0], _pinI2C[1]);

    Wire.beginTransmission(0x36);
    if (Wire.endTransmission() == 0) {
        if (_SerialStatus) Serial.println("AS5600 Encontrado.");
    } else {
        if (_SerialStatus) Serial.println("Error: AS5600 NO encontrado.");
    }

    if (!mpu.begin()) {
        if (_SerialStatus) Serial.println("Fallo al encontrar MPU6050");
        _I2CStatus = false;
    } else {
        if (_SerialStatus) Serial.println("MPU6050 Encontrado e Inicializado!");
        mpu_temp = mpu.getTemperatureSensor();
        mpu_accel = mpu.getAccelerometerSensor();
        mpu_gyro = mpu.getGyroSensor();
        _I2CStatus = true;
    }

    // --- Configuración SPI y SD ---
    SPI.begin(_pinSPI[2], _pinSPI[1], _pinSPI[0], _pinSPI[3]);
    if (!SD.begin(_pinSPI[3], SPI)) {
        _SDStatus = false;
        if (_SerialStatus) Serial.println("Error: Fallo SD.");
    } else {
        _SDStatus = true;
    }

    return (_SDStatus && _I2CStatus);
}