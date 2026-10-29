#include "systemConfig.h"

SystemConfig::SystemConfig(byte* spiPins, byte* i2cPins, byte* pwmPins, byte stbyPin, byte i2cAddress) {
    _pinSPI = spiPins;
    _pinI2C = i2cPins;
    _pinPWM = pwmPins;
    _pinSTBY = stbyPin;
    _i2cAddress = i2cAddress;
    
    _bauds = 115200;
    timeout = 5000;
    
    _SDStatus = false;
    _I2CStatus = false;
    _SerialStatus = false;
}

bool SystemConfig::start() {
    // 1. Serial 
    Serial.begin(_bauds);
    unsigned long SerialTimer = millis(); 
    while (millis() - SerialTimer < timeout) {
        if (Serial) {
            _SerialStatus = true;
            break;
        }
        yield();
    }

    // 2. GPIO (STBY del TB6612)
    if (_pinSTBY != 255) {
        pinMode(_pinSTBY, OUTPUT);
        digitalWrite(_pinSTBY, HIGH); // Habilitar el puente H
    }

    // 3. I2C (Escaneo del dispositivo)
    Wire.begin(_pinI2C[0], _pinI2C[1]);
    Wire.beginTransmission(_i2cAddress);
    byte error = Wire.endTransmission();
    
    if (error == 0) {
        _I2CStatus = true;
        if (_SerialStatus) Serial.println("Éxito: Dispositivo I2C encontrado.");
    } else {
        _I2CStatus = false;
        if (_SerialStatus) Serial.println("Error: Dispositivo I2C NO encontrado.");
    }

    // 4. SPI y SD
    // _pinSPI[0]=MOSI, _pinSPI[1]=MISO, _pinSPI[2]=SCK, _pinSPI[3]=CS
    SPI.begin(_pinSPI[2], _pinSPI[1], _pinSPI[0], _pinSPI[3]);
    
    if (!SD.begin(_pinSPI[3], SPI)) {
        _SDStatus = false;
        if (_SerialStatus) Serial.println("Error: Fallo al montar la tarjeta SD.");
    } else {
        _SDStatus = true;
        if (_SerialStatus) Serial.println("Éxito: Tarjeta SD inicializada.");
    }

    // 5. MCPWM (Para motor DC con TB6612)
    // Asigna los dos pines a los canales A y B del Generador 0 en la Unidad 0
    mcpwm_gpio_init(MCPWM_UNIT_0, MCPWM0A, _pinPWM[0]);
    mcpwm_gpio_init(MCPWM_UNIT_0, MCPWM0B, _pinPWM[1]);

    mcpwm_config_t pwm_config;
    pwm_config.frequency = 10000;    // Frecuencia del PWM en Hz (10kHz)
    pwm_config.cmpr_a = 0;           // Duty cycle inicial 0%
    pwm_config.cmpr_b = 0;           // Duty cycle inicial 0%
    pwm_config.counter_mode = MCPWM_UP_COUNTER;
    pwm_config.duty_mode = MCPWM_DUTY_MODE_0;
    
    mcpwm_init(MCPWM_UNIT_0, MCPWM_TIMER_0, &pwm_config);

    // Retorna true solo si los componentes críticos iniciaron correctamente
    return (_SDStatus && _I2CStatus);
}