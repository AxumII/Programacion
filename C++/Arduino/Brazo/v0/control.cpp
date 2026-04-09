#include <Arduino.h>
#include <Keypad.h>
#include <Wire.h> 
#include "angle2pos.h"

// ==============================================================================
// PINES DE PANTALLA ST7789 (SPI)
// ==============================================================================
#define TFT_MOSI 11
#define TFT_SCLK 12
#define TFT_CS   10
#define TFT_DC   13
#define TFT_RST  48

// ==============================================================================
// VARIABLES GLOBALES E INTERRUPCIONES (ESP32-S3-N16R8)
// ==============================================================================

// 2 Análogos libres
const byte pinAnalog[2] = {5, 6}; 

// 3 pulsadores 
const byte pinPulsadores[3] = {40, 41, 42}; 
const int numPulsadores = sizeof(pinPulsadores) / sizeof(pinPulsadores[0]);

// EXACTAMENTE 2 Outputs Digitales (LEDs)
const byte pinOutputs[2] = {47, 48}; 

// Timer
volatile uint32_t botonesDetectados = 0;
hw_timer_t *timerDebounce = NULL;

void IRAM_ATTR debounceISR() {
    for (int i = 0; i < numPulsadores; i++) {
        if (digitalRead(pinPulsadores[i]) == LOW) {
            botonesDetectados |= (1 << i);
        }
    }
}

// Input Servo Frecuencia
int fs1 = 537;
int fs2 = 2214;

// ==============================================================================
// CLASE CONTROLADOR
// ==============================================================================
class Controlador{
    private:
        // -- BRAZO --
        angle2xy brazo;

        // --- VARIABLES CONTROL MANUAL ---
        int multiplicador = 1;         
        int sw1_last = HIGH;           
        unsigned long ultimoMovimiento = 0; 
        const int intervaloMov = 100;   
        float currentX;
        float currentY;
        String inputSpeed = "";

        // --- VARIABLES DEL BOTÓN DINÁMICO ---
        const byte pinDinamico = 40;   // Coincide con pinPulsadores[0]
        bool modoDinamico = false;     
        int swDinamico_last = HIGH;    

        // --- TECLADO MATRICIAL ---
        static const byte ROWS = 4; 
        static const byte COLS = 4; 
        char customKeys[ROWS][COLS] = {
            { '1','2','3','A' },
            { '4','5','6','B' },
            { '7','8','9','C' },
            { '*','0','#','D' } 
        };
        // Pines de teclado actualizados
        byte rowPins[ROWS] = {7, 8, 9, 14}; 
        byte colPins[COLS] = {15, 16, 17, 18}; 
        Keypad customKeypad;

        // --- JOYSTICKS ---
        const byte joystick1Pins[3] = {2, 1, 38}; // X, Y, SW
        const byte joystick2Pins[3] = {4, 3, 39}; // X, Y, SW
        
        int x1, y1, x2, y2;
        bool sw1, sw2;
        int x1_digital, y1_digital, x2_digital, y2_digital;

        // --- MENÚ ---
        int cursorMenu = 0; 
        int estadoActual = 0; 
        int y1_digital_last = 0; 
        bool necesitaActualizar = true;

    public:
        Controlador() : 
            customKeypad(makeKeymap(customKeys), rowPins, colPins, ROWS, COLS), 
            brazo(97, 106, 40, 180)
        {
            x1 = y1 = x2 = y2 = 0;
            sw1 = sw2 = false;
            x1_digital = y1_digital = x2_digital = y2_digital = 0;
        }

        // ... [El resto de las funciones (begin, menuInput, etc.) siguen igual] ...
        void begin() {
            // Setup de pines
            pinMode(joystick1Pins[2], INPUT_PULLUP);
            pinMode(joystick2Pins[2], INPUT_PULLUP);
            pinMode(pinDinamico, INPUT_PULLUP);
            
            pinMode(pinOutputs[0], OUTPUT); 
            pinMode(pinOutputs[1], OUTPUT); 

            // Setup de botones e interrupciones
            for (int i = 0; i < numPulsadores; i++) {
                pinMode(pinPulsadores[i], INPUT_PULLUP);
                attachInterrupt(digitalPinToInterrupt(pinPulsadores[i]), debounceISR, FALLING);
            }

            // Setup Timer
            timerDebounce = timerBegin(1000000); 
            timerAttachInterrupt(timerDebounce, &debounceISR);
            timerAlarm(timerDebounce, 50000, true, 0); 

            // Setup del brazo
            brazo.config(fs1, fs2); 
            brazo.goHome();
        }

        int AxisAsLevel(int raw) {
            if (raw > 3500) return 2;  
            if (raw > 2200) return 1;  
            if (raw < 500)  return -2; 
            if (raw < 1800) return -1; 
            return 0;                  
        }

        void menuInput() {
            y1 = analogRead(joystick1Pins[1]);
            y1_digital = (y1 < 1500) ? -1 : ((y1 > 2500) ? 1 : 0);

            char key = customKeypad.getKey();
            menuLogic(key, y1_digital);
        }

        void menuLogic(char key, int y1_dig) {
            
            // ==========================================
            // LÓGICA DE MENÚS GRÁFICOS (Estados 0 al 4)
            // ==========================================
            if (estadoActual < 5) {
                if (y1_dig != y1_digital_last) {        
                    switch (y1_dig) {
                        case -1: cursorMenu = (cursorMenu <= 0) ? obtenerMaxOpciones() : cursorMenu - 1; necesitaActualizar = true; break;
                        case 1:  cursorMenu = (cursorMenu >= obtenerMaxOpciones()) ? 0 : cursorMenu + 1; necesitaActualizar = true; break;
                    }
                    y1_digital_last = y1_dig; 
                }

                if (key) {
                    if (key == '*') {
                        switch (estadoActual) {
                            case 0: 
                                switch (cursorMenu) {
                                    case 0: estadoActual = 1; cursorMenu = 0; break; 
                                    case 1: estadoActual = 2; cursorMenu = 0; break; 
                                    case 2: estadoActual = 3; cursorMenu = 0; loadProgram(); break; 
                                    case 3: estadoActual = 4; cursorMenu = 0; break; 
                                    case 4: estadoActual = 5; cursorMenu = 0; manualControl(); break; 
                                }
                                necesitaActualizar = true;
                                break;
                            case 1: 
                                switch (cursorMenu) {
                                    case 0: home(); break;
                                    case 1: test(); break;
                                    case 2: calibrate(); break;
                                }
                                break;
                        }
                    }
                    else if (key == '#') {
                        if (estadoActual > 0) {
                            estadoActual = 0; 
                            cursorMenu = 0;   
                            necesitaActualizar = true;
                        }
                    }
                }
            } 
            
            // ==========================================
            // LÓGICA DE CONTROL MANUAL (Estado 5)
            // ==========================================
            else if (estadoActual == 5) {
                
                // --- 1. MÁQUINA DE ESTADOS DEL PULSADOR 33 (TOGGLE) ---
                int lecturaDinamico = digitalRead(pinDinamico);
                if (lecturaDinamico == LOW && swDinamico_last == HIGH) {
                    modoDinamico = !modoDinamico; // Cambia el estado (Invertir)
                    digitalWrite(pinOutputs[0], modoDinamico ? HIGH : LOW); // Prender/Apagar LED
                    Serial.printf(">>> MODO DE MOVIMIENTO: %s\n", modoDinamico ? "ACTIVADO" : "PAUSADO");
                    delay(50); // Debounce
                }
                swDinamico_last = lecturaDinamico;

                // --- 2. LÓGICA DE TECLADO PARA VELOCIDAD ---
                if (key) {
                    if (key >= '0' && key <= '9') {
                        inputSpeed += key;
                        Serial.print("Digitando velocidad: ");
                        Serial.println(inputSpeed);
                    } 
                    else if (key == '*') { 
                        if (inputSpeed.length() > 0) {
                            brazo.speed = inputSpeed.toInt(); 
                            Serial.printf(">>> NUEVA VELOCIDAD: %d\n", brazo.speed);
                            inputSpeed = ""; 
                        }
                    } 
                    else if (key == '#') { 
                        if (inputSpeed.length() > 0) {
                            inputSpeed = ""; 
                            Serial.println("Entrada cancelada.");
                        } else {
                            Serial.println("Saliendo de Control Manual...");
                            modoDinamico = false;             // Apagar seguridad
                            digitalWrite(pinOutputs[0], LOW); // Apagar LED
                            brazo.goHome(); 
                            estadoActual = 0; 
                            cursorMenu = 0;   
                            necesitaActualizar = true;
                        }
                    }
                }

                // --- 3. MULTIPLICADOR DE INCREMENTO (Botón Joystick) ---
                int estadoSW1 = digitalRead(joystick1Pins[2]);
                if (estadoSW1 == LOW && sw1_last == HIGH) {
                    switch (multiplicador) {
                        case 1:  multiplicador = 2;  break;
                        case 2:  multiplicador = 5;  break;
                        case 5:  multiplicador = 10; break;
                        case 10: multiplicador = 1;  break;
                        default: multiplicador = 1;  break;
                    }
                    Serial.printf("Multiplicador de incremento: x%d\n", multiplicador);
                    delay(50); 
                }
                sw1_last = estadoSW1;

                // --- 4. MOVER EL BRAZO (Solo si la bandera modoDinamico es True) ---
                if (modoDinamico && (millis() - ultimoMovimiento > intervaloMov)) {
                    
                    int rawX = analogRead(joystick1Pins[0]);
                    int rawY = analogRead(joystick1Pins[1]);
                    
                    float incX = 0, incY = 0;

                    switch (AxisAsLevel(rawX)) {
                        case 2:  incX = 2.0;  break;
                        case 1:  incX = 1.0;  break;
                        case -1: incX = -1.0; break;
                        case -2: incX = -2.0; break;
                    }

                    switch (AxisAsLevel(rawY)) {
                        case 2:  incY = 2.0;  break;
                        case 1:  incY = 1.0;  break;
                        case -1: incY = -1.0; break;
                        case -2: incY = -2.0; break;
                    }

                    if (incX != 0 || incY != 0) {
                        currentX += (incX * multiplicador);
                        currentY += (incY * multiplicador);
                        brazo.moveServo(currentX, currentY);
                    }
                    
                    ultimoMovimiento = millis();
                }
            }

            // ==========================================
            // DIBUJADO DE LA INTERFAZ
            // ==========================================
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
                }
                necesitaActualizar = false;
            }
        }
            
        int obtenerMaxOpciones() {
            switch (estadoActual) {
                case 0: return 4; 
                case 1: return 2; 
                default: return 0; 
            }
        }

        // --- ACCIONES ---
        void home() {
            Serial.println("Ejecutando: Motores a HOME..."); 
            brazo.goHome();
            
            // Reinicio de seguridad
            currentX = brazo.l1; 
            currentY = brazo.l2; 
            multiplicador = 1;              
            modoDinamico = false;
            digitalWrite(pinOutputs[0], LOW); // Apaga LED por seguridad
            Serial.println("Variables manuales reiniciadas.");
        }
        
        void test() { Serial.println("Ejecutando: Test ejecutado!"); }
        void calibrate() { Serial.println("Ejecutando: Calibración iniciada..."); }
        void loadProgram() { Serial.println("Ejecutando: Cargando programa..."); }
        
        void manualControl() {
            Serial.println("\n>>> MODO MANUAL ACTIVADO <<<"); 
            Serial.println("- PULSA el Pin 33 para encender/apagar el movimiento (LED indicador)");
            Serial.println("- Escribe velocidad (0-9) y presiona '*' para fijarla");
            Serial.println("- Presiona Joy1_SW para cambiar multiplicador (x1, x2, x5, x10)");
            Serial.println("- Presiona '#' para borrar texto o salir al menú principal");
            
            // Valores iniciales
            currentX = brazo.l1; 
            currentY = brazo.l2; 
            multiplicador = 1;
            inputSpeed = ""; 
            
            // Forzar inicio apagado por seguridad
            modoDinamico = false;
            swDinamico_last = digitalRead(pinDinamico);
            digitalWrite(pinOutputs[0], LOW); 
        }
};

// ==============================================================================
// INSTANCIA Y BUCLE PRINCIPAL
// ==============================================================================
Controlador miControlador; 

void setup() {
    Serial.begin(115200); 
    Wire.begin(19, 20);
    miControlador.begin();
    Serial.println("Sistema iniciado.");
    Serial.println("Sistema iniciado: 2 LEDs, 3 Pulsadores, 2 Analógicos libres e I2C en pines 19/20.");
}

void loop() {
    miControlador.menuInput();
    
    // Limpiamos los flags del timer por si acaso
    if (botonesDetectados != 0) {
        botonesDetectados = 0; 
    }
    
    delay(10);
}