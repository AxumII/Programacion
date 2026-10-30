#include "plantStatus.h"

plantStatus::plantStatus(SystemConfig* sysPtr){
    _sys = sysPtr; 

    // Parámetros PWM iniciales
    PWM_BITS = 8;
    PWM_MAX = (1 << PWM_BITS) - 1;
    currentFreq = 20000;
    
    offset_angulo = 0; offset_ax = 0; offset_ay = 0; offset_az = 0;
    offset_gx = 0; offset_gy = 0; offset_gz = 0;
}

// ---------- Motor control ----------

void plantStatus::motorCoast() {
    digitalWrite(_sys->motorPins[1], LOW);
    digitalWrite(_sys->motorPins[2], LOW);
    ledcWrite(_sys->motorPins[0], 0);
}

void plantStatus::motorBrake() {
    digitalWrite(_sys->motorPins[1], HIGH);
    digitalWrite(_sys->motorPins[2], HIGH);
    ledcWrite(_sys->motorPins[0], PWM_MAX);
}

void plantStatus::motorSet(int speedPercent) {
    speedPercent = constrain(speedPercent, -100, 100);

    if (speedPercent == 0) {
        motorCoast(); // Puedes cambiar a motorBrake() si prefieres frenado en seco
        return;
    }

    digitalWrite(_sys->motorPins[1], speedPercent > 0 ? HIGH : LOW);
    digitalWrite(_sys->motorPins[2], speedPercent > 0 ? LOW : HIGH);
    ledcWrite(_sys->motorPins[0], map(abs(speedPercent), 0, 100, 0, PWM_MAX));
}

// ---------- Serial terminal control ----------

void plantStatus::serialMotorControl() {
    if (Serial.available() > 0) {
        String input = Serial.readStringUntil('\n');
        input.trim();
        
        if (input.length() > 0) {
            char cmd = input.charAt(0);
            
            // Z para Calibrar
            if (cmd == 'Z' || cmd == 'z') {
                calibrateSensors();
            }
            // S para Stop
            else if (cmd == 'S' || cmd == 's') {
                motorSet(0);
                Serial.println("Comando Serial: Motor DETENIDO");
            }
            // H para Horario, A para Antihorario
            else if (cmd == 'H' || cmd == 'h' || cmd == 'A' || cmd == 'a') {
                if (input.length() > 1) {
                    int pwr = input.substring(1).toInt();
                    
                    // Ajustar el signo de la velocidad dependiendo del sentido
                    int speed = pwr;
                    if (cmd == 'A' || cmd == 'a') {
                        speed = -pwr; 
                    }
                    
                    motorSet(speed);
                    
                    Serial.print("Comando Serial: Direccion = ");
                    Serial.print(cmd);
                    Serial.print(" | Potencia = ");
                    Serial.println(pwr);
                }
            }
        }
    }
}

// ---------- Sensor Reading y Calibration ----------

void plantStatus::calibrateSensors() {
    Serial.println("Iniciando calibracion de sensores. Mantenga el sistema quieto...");
    
    offset_angulo = 0; offset_ax = 0; offset_ay = 0; offset_az = 0;
    offset_gx = 0; offset_gy = 0; offset_gz = 0;

    int num_samples = 100;
    for (int i = 0; i < num_samples; i++) {
        // Lectura cruda temporal (sin usar las funciones que restan el offset)
        Wire.beginTransmission(0x36); 
        Wire.write(0x0E);             
        Wire.endTransmission(false);
        Wire.requestFrom((uint16_t)0x36, (uint8_t)2, true);
        if (Wire.available() == 2) {
            uint16_t rawAngle = Wire.read() << 8;
            rawAngle |= Wire.read();
            offset_angulo += (rawAngle * 360.0f) / 4096.0f;
        }

        sensors_event_t accel, gyro, temp;
        _sys->mpu_temp->getEvent(&temp);
        _sys->mpu_accel->getEvent(&accel);
        _sys->mpu_gyro->getEvent(&gyro);
        
        offset_ax += accel.acceleration.x; 
        offset_ay += accel.acceleration.y; 
        offset_az += accel.acceleration.z;
        offset_gx += gyro.gyro.x; 
        offset_gy += gyro.gyro.y; 
        offset_gz += gyro.gyro.z;
        
        delay(10);
    }

    offset_angulo /= num_samples; offset_ax /= num_samples;
    offset_ay /= num_samples; offset_az /= num_samples;
    offset_gx /= num_samples; offset_gy /= num_samples;
    offset_gz /= num_samples;
    
    Serial.println("Calibracion exitosa.");
}

void plantStatus::readAS5600() {
    Wire.beginTransmission(0x36); 
    Wire.write(0x0E);             
    Wire.endTransmission(false);
    Wire.requestFrom((uint16_t)0x36, (uint8_t)2, true);
    
    if (Wire.available() == 2) {
        uint16_t rawAngle = Wire.read() << 8;
        rawAngle |= Wire.read();
        angulo_as5600 = ((rawAngle * 360.0f) / 4096.0f) - offset_angulo;
    }
}

void plantStatus::readMPU6050() {
    sensors_event_t accel, gyro, temp;
    _sys->mpu_temp->getEvent(&temp);
    _sys->mpu_accel->getEvent(&accel);
    _sys->mpu_gyro->getEvent(&gyro);

    ax = accel.acceleration.x - offset_ax;
    ay = accel.acceleration.y - offset_ay;
    az = accel.acceleration.z - offset_az;
    gx = gyro.gyro.x - offset_gx;
    gy = gyro.gyro.y - offset_gy;
    gz = gyro.gyro.z - offset_gz;
}

void plantStatus::updateSensors() {
    readAS5600(); readMPU6050();
}

void plantStatus::printData() {
    Serial.print("Angulo: "); Serial.print(angulo_as5600);
    Serial.print("° | Acc[X:"); Serial.print(ax); Serial.print(" Y:"); Serial.print(ay); Serial.print(" Z:"); Serial.print(az);
    Serial.print("] | Gyr[X:"); Serial.print(gx); Serial.print(" Y:"); Serial.print(gy); Serial.print(" Z:"); Serial.print(gz);
    Serial.println("]");
}