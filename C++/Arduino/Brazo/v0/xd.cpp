#include <Arduino.h>
#include <stdio.h>
#include <math.h>
#include <Keypad.h>

//Globales static

//Inputs Analógicos
const byte pinAnalog[6] = {}; // Pines analógicos para joysticks y sensores extra

//Inputs Digitales
const uint8_t pinPulsadores[] = {}; 
const int numPulsadores = sizeof(pinPulsadores) / sizeof(pinPulsadores[0]);
//Timer
volatile uint32_t botonesDetectados = 0;
hw_timer_t *timerDebounce = NULL;

void IRAM_ATTR debounceISR() {
    for (int i = 0; i < numPulsadores; i++) {
        if (digitalRead(pinPulsadores[i]) == LOW) {
            botonesDetectados |= (1 << i);
        }
    }
}


class Controlador{
    private:
        // --- TECLADO MATRICIAL ---
        static const byte ROWS = 4; 
        static const byte COLS = 4; 
        char customKeys[ROWS][COLS] = {
            { '1','2','3','A' }, // D1 cambiado a un solo char 'A' para compatibilidad
            { '4','5','6','B' }, // D2 -> 'B'
            { '7','8','9','C' }, // ms -> 'C'
            { '*','0','#','D' }  // ok, back, shift cambiados a char simples
        };
        byte rowPins[ROWS] = {15, 2, 0, 16}; // Ejemplo de pines
        byte colPins[COLS] = {17, 18, 19, 21}; // Ejemplo de pines
        Keypad customKeypad;


        // --- JOYSTICKS ---
        // Pines: X, Y, SW
        const byte joystick1Pins[3] = {34, 35, 32}; // Pines analógicos típicos de ESP32
        const byte joystick2Pins[3] = {36, 39, 33}; 
        
        // Variables de estado Joystick 1
        int x1,y1,x2, y2;
        bool sw1,sw2;
        int x1_digital, y1_digital,x2_digital, y2_digital;

        // --- PULSADORES ---
        const byte pines[3] = {4, 5, 13}; // Pines de los pulsadores
        
    public:
        Controlador() : customKeypad(makeKeymap(customKeys), rowPins, colPins, ROWS, COLS) {
            x1 = y1 = x2 = y2 = 0;
            sw1 = sw2 = false;
            x1_digital = y1_digital = x2_digital = y2_digital = 0;
        }
        
        void begin() {
            // Setup de joysticks
            pinMode(joystick1Pins[2], INPUT_PULLUP);
            pinMode(joystick2Pins[2], INPUT_PULLUP);
            
            // Setup de botones e interrupciones
            for (int i = 0; i < 3; i++) {
                pinMode(pinPulsadores[i], INPUT_PULLUP);
                attachInterrupt(digitalPinToInterrupt(pinPulsadores[i]), debounceISR, FALLING);
            }

            // Setup del Timer para debounce (Solo ESP32)
            timerDebounce = timerBegin(0, 80, true);
            timerAttachInterrupt(timerDebounce, &debounceISR, true);
            timerAlarmWrite(timerDebounce, 50000, false);
        }

        void JoystickAsDigitalCursor() {
            x1 = analogRead(joystick1Pins[0]);
            y1 = analogRead(joystick1Pins[1]);
            x2 = analogRead(joystick2Pins[0]);
            y2 = analogRead(joystick2Pins[1]);
            
            sw1 = digitalRead(joystick1Pins[2]);
            sw2 = digitalRead(joystick2Pins[2]);

            // Mapeo digital (Asumiendo que ADC va de 0 a 4095 en ESP32, o 0-1023 en Arduino)
            // Valores ajustados para ESP32 (Centro ~2048)
            x1_digital = (x1 < 1500) ? -1 : ((x1 > 2500) ? 1 : 0);
            y1_digital = (y1 < 1500) ? -1 : ((y1 > 2500) ? 1 : 0);
            x2_digital = (x2 < 1500) ? -1 : ((x2 > 2500) ? 1 : 0);
            y2_digital = (y2 < 1500) ? -1 : ((y2 > 2500) ? 1 : 0);
        }

        void getKeypadInput() {
            char customKey = customKeypad.getKey();
            if (customKey) {
                Serial.println(customKey);
            }
        }

void setup() {
    Serial.begin(115200); // 115200 es el estándar común actual (144000 no es estándar)
    miControlador.begin();
    Serial.println("Sistema iniciado.");
}

void loop() {
    // 1. Leer entradas normales
    miControlador.leerTeclado();
    miControlador.leerJoysticks();

    // 2. Procesar botones detectados por interrupción
    if (botonesDetectados != 0) {
        for (int i = 0; i < numPulsadores; i++) {
            if (botonesDetectados & (1 << i)) {
                Serial.printf("Pulsador %d presionado!\n", pinPulsadores[i]);
                botonesDetectados &= ~(1 << i); // Limpiar flag
            }
        }
    }

    delay(10); // Pequeña pausa para estabilidad
}        






















}