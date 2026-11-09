#include "systemConfig.h"


SystemConfig::SystemConfig(byte* i2cPins,byte* CANPins, byte* pQEncA,byte* pQEncB,byte* pPWMLeft,byte* pPWMRight,byte dimAnalogIn, byte* pAnalogIn    byte dimDigIn, byte* pDigIn,
    byte dimDigOut, byte* pDigOut){
            _bauds = 921600;
    timeout = 5000;
    _I2CStatus = false;
    _CANStatus = false;
    _WIFIStatus = false;

}

bool SystemConfig::start(){

#GPIO

#CAN

#MCPWM

#WIFI




}
void SystemConfig::startGPIO(){

}
void SystemConfig::startCAN(){

}
void SystemConfig::startMCPWM(){
       // Inicializar el pin de PWM para MCPWM (Unidad 0, Timer 0, Operador A)
    mcpwm_gpio_init(MCPWM_UNIT_0, MCPWM0A, motorPins[0]);
    
    // Configurar los parámetros del MCPWM
    mcpwm_config_t pwm_config;
    pwm_config.frequency = 20000;    // 20kHz
    pwm_config.cmpr_a = 0.0;         // Duty cycle inicial 0%
    pwm_config.cmpr_b = 0.0;
    pwm_config.counter_mode = MCPWM_UP_COUNTER;
    pwm_config.duty_mode = MCPWM_DUTY_MODE_0;
    
    mcpwm_init(MCPWM_UNIT_0, MCPWM_TIMER_0, &pwm_config);
}

void SystemConfig::startWIFI(){
    
}
