#include <Arduino.h>
#include <math.h>
#define USE_PCA9685_SERVO_EXPANDER 
#include <ServoEasing.hpp>

ServoEasing Servo1(PCA9685_DEFAULT_ADDRESS);
ServoEasing Servo2(PCA9685_DEFAULT_ADDRESS);

class angle2xy {
    

    public:
        float l1,l2;
        int maxAngle;
        int speed;

        float finalTheta1, finalTheta2;


    
        bool inverseKinematic(float x, float y) {
        //Constantes
        float magn2 = (x*x) + (y*y);
        float magn = hypot(x, y);
        float alpha = atan2(y, x);

        if (magn > (l1 + l2) || magn < fabsf(l1 - l2)) {
            Serial.println("Error: Punto fuera de alcance");
            return false;
            }
        float D = (magn2 - l1 * l1 - l2 * l2) / (2.0 * l1 * l2);
        float theta2 = atan2(-sqrt(1-(D*D)) , D);
        float beta = atan2(l2 * sin(theta2), l1 + l2 * cos(theta2));
        float theta1 = alpha - beta;

        finalTheta1 = theta1 * 180.0 / PI;
        finalTheta2 = theta2 * -180.0 / PI;
        return true;
        }

        void moveServo(float x, float y){
        if (inverseKinematic(x, y)) {
            Serial.printf("CÁLCULO IK -> Hombro: %.2f | Codo: %.2f\n", finalTheta1, finalTheta2);
            if (finalTheta1 >= 0 && finalTheta1 <= maxAngle && finalTheta2 >= 0 && finalTheta2 <= maxAngle){
            Serial.printf("Moviendo a %.2f y %.2f con frenada Quartic\n", finalTheta1, finalTheta2);
            Servo1.setEaseTo(finalTheta1, speed);
            Servo2.setEaseTo(finalTheta2, speed);
            synchronizeAllServosStartAndWaitForAllServosToStop();
            }else {
                    Serial.println(F("Error: Ángulos calculados fuera de límites de los servos (0-180)"));
            }
        }
        
        }

        void goHome() {
            Serial.println(F("Moviendo a posición HOME..."));
            Servo1.setEaseTo(0, speed);
            Servo2.setEaseTo(0, speed);
            synchronizeAllServosStartAndWaitForAllServosToStop();
            Serial.println(F("Robot en HOME."));
        }

        void config(float p1, float p2) {
            Serial.begin(115200);
            delay(2000);
            Wire.begin();
            Serial.println(F("Iniciando sistema PCA9685..."));

            //Verificación de seguridad del ejemplo
            if (Servo1.initializeAndCheckI2CConnection(&Serial)) {
                Serial.println(F("ERROR: No se encuentra la PCA9685. Revisa cables y alimentación."));
                while (1) { /* Bucle de error */ }
            }

            // Calibración de pulsos (Canal, Ángulo inicial, Min, Max)
            Servo1.attach(0, 0, p1, p2);
            Servo2.attach(1, 0, p1, p2);

            // Configuración de suavizado (Easing)
            Servo1.setEasingType(EASE_QUARTIC_IN_OUT);
            Servo2.setEasingType(EASE_QUARTIC_IN_OUT);

            Serial.println(F("Listo. Ingresa: x,y"));
        }
        
        void execute(){
            Serial.printf("Moviendo a  -> X: %.2f, Y: %.2f\n", inputX, inputY);
            moveServo(inputX, inputY);
            Serial.printf("Esta en  -> X: %.2f, Y: %.2f\n", inputX, inputY);
        }

    }: