#include <Arduino.h>
#include <stdio.h>
#include <math.h>
#include <Keypad.h>

//Globales static
           

//Inputs Analógicos
const byte pinAnalog[1] = {13}; // Pines analógicos para sensores extra

// Inputs Digitales (Pulsadores)
const uint8_t pinPulsadores[3] = {5, 18, 19}; 
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
// ==============================================================================
// CLASE CONTROLADOR
// ==============================================================================
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
        byte rowPins[ROWS] = {15, 2, 4, 16}; // Ejemplo de pines
        byte colPins[COLS] = {17, 27, 14, 12}; // Ejemplo de pines
        Keypad customKeypad;


        // --- JOYSTICKS ---
        // Pines: X, Y, SW
        const byte joystick1Pins[3] = {32, 33, 25}; // Pines analógicos típicos de ESP32
        const byte joystick2Pins[3] = {35, 34, 26}; 
        
        int x1,y1,x2, y2;
        bool sw1,sw2;
        int x1_digital, y1_digital,x2_digital, y2_digital;

        // --- PULSADORES ADICIONALES---
        const uint8_t pinPulsadores[3] = {5,18,19}; 

        // --- MENÚ ---
        int cursorMenu = 0; 
        int estadoActual = 0; 
        int y1_digital_last = 0; 
        bool necesitaActualizar = true;


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

        void joystickAsDigitalCursor() {
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

        void menuInput() {
            y1 = analogRead(joystick1Pins[1]);
            y1_digital = (y1 < 1500) ? -1 : ((y1 > 2500) ? 1 : 0);

            // 2. Leer Teclado (Una sola vez)
            char key = customKeypad.getKey();

            // 3. Mandar los datos a la lógica del menú
            menuLogic(key, y1_digital);
        }

        void menuLogic(char key, int y1_dig) {
        // 1. NAVEGACIÓN GLOBAL (El joystick mueve el cursor si hay cambio)
        if (y1_dig != y1_digital_last) {        
            switch (y1_dig) {
                case -1: // Arriba
                    cursorMenu = (cursorMenu <= 0) ? obtenerMaxOpciones() : cursorMenu - 1; 
                    necesitaActualizar = true;
                    break;
                case 1:  // Abajo
                    cursorMenu = (cursorMenu >= obtenerMaxOpciones()) ? 0 : cursorMenu + 1; 
                    necesitaActualizar = true;
                    break;
            }
            y1_digital_last = y1_dig; 
        }

        // 2. MÁQUINA DE ESTADOS (Manejo de selecciones con '*')
        if (key == '*') {
            switch (estadoActual) {
                case 0: // ESTADO 0: MENU PRINCIPAL
                    switch (cursorMenu) {
                        case 0: estadoActual = 1; cursorMenu = 0; break; // Ir a System
                        case 1: estadoActual = 2; cursorMenu = 0; break; // Ir a Show
                        case 2: estadoActual = 3; cursorMenu = 0; loadProgram(); break; // Ir a Load
                        case 3: estadoActual = 4; cursorMenu = 0; break; // Ir a Program
                        case 4: estadoActual = 5; cursorMenu = 0; manualControl(); break; // Ir a Manual
                    }
                    necesitaActualizar = true;
                    break;

                case 1: // ESTADO 1: SUBMENU SYSTEM
                    switch (cursorMenu) {
                        case 0: home(); break;
                        case 1: test(); break;
                        case 2: calibrate(); break;
                    }
                    // Aquí no cambiamos de estado para quedarnos en el submenú tras ejecutar
                    break;
            }
        }

        // 3. BOTÓN DE RETROCESO (Ejemplo usando la tecla '#')
        if (key == '#') {
            switch (estadoActual) {
                case 1: // Si estamos en System...
                case 2: // o en Show...
                case 3: // o en Load...
                case 4: // o en Program...
                case 5: // o en Manual...
                    estadoActual = 0; // Volvemos al menú principal
                    cursorMenu = 0;   // Reseteamos el cursor
                    necesitaActualizar = true;
                    break;
            }
        }

        // 4. DIBUJADO DE LA INTERFAZ
        if (necesitaActualizar) {
            switch (estadoActual) {
                case 0:
                    Serial.println("\n--- MENU PRINCIPAL ---");
                    Serial.print(cursorMenu == 0 ? " > " : "   "); Serial.println("System");
                    Serial.print(cursorMenu == 1 ? " > " : "   "); Serial.println("Show");
                    Serial.print(cursorMenu == 2 ? " > " : "   "); Serial.println("Load");
                    Serial.print(cursorMenu == 3 ? " > " : "   "); Serial.println("Program");
                    Serial.print(cursorMenu == 4 ? " > " : "   "); Serial.println("Manual");
                    break;
                case 1:
                    Serial.println("\n--- SUBMENU SYSTEM ---");
                    Serial.print(cursorMenu == 0 ? " > " : "   "); Serial.println("Home");
                    Serial.print(cursorMenu == 1 ? " > " : "   "); Serial.println("Test");
                    Serial.print(cursorMenu == 2 ? " > " : "   "); Serial.println("Calibrate");
                    Serial.println("   (Presiona # para volver)");
                    break;
                case 2:
                    Serial.println("\n--- SHOW ---");
                    Serial.println("   (Presiona # para volver)");
                    break;
                // Puedes agregar los cases para los otros menús gráficos aquí...
            }
            necesitaActualizar = false;
        }
        }
            
        int obtenerMaxOpciones() {
            switch (estadoActual) {
                case 0: return 4; // Menú principal tiene 5 opciones (0 a 4)
                case 1: return 2; // System tiene 3 opciones (0 a 2)
                default: return 0; // Menús sin opciones
            }
        }

        // --- ACCIONES ---
        void home() { Serial.println("Ejecutando: Motores a 0..."); }
        void test() { Serial.println("Ejecutando: Test ejecutado!"); }
        void calibrate() { Serial.println("Ejecutando: Calibración iniciada..."); }
        void loadProgram() { Serial.println("Ejecutando: Cargando programa..."); }
        void manualControl() { Serial.println("Ejecutando: Control manual activado..."); }
};

// ==============================================================================
// INSTANCIA Y BUCLE PRINCIPAL
// ==============================================================================
Controlador miControlador; // <-- ESTO FALTABA

void setup() {
    Serial.begin(115200); // 115200 es el estándar común actual (144000 no es estándar)
    miControlador.begin();
    Serial.println("Sistema iniciado.");
}

void loop() {
    // Una sola función se encarga de leer hardware y procesar la lógica visual
    miControlador.menuInput();
    
    // Procesar pulsadores extra por interrupción
    if (botonesDetectados != 0) {
        botonesDetectados = 0; // Limpiar flag tras usarlos
    }
    
    delay(10);
}  






















}