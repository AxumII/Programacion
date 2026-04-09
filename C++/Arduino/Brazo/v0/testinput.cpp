#include <Arduino.h>
#include <Keypad.h>

// ==========================================
// 1. DEFINICIÓN DE PINES (Tus mismos pines)
// ==========================================

// Teclado
const byte ROWS = 4; 
const byte COLS = 4; 
char keys[ROWS][COLS] = {
  { '1','2','3','A' }, 
  { '4','5','6','B' }, 
  { '7','8','9','C' }, 
  { '*','0','#','D' }  
};
byte rowPins[ROWS] = {15, 2, 4, 16}; 
byte colPins[COLS] = {17, 27, 14, 12}; 
Keypad teclado = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS);

// Joysticks
const byte joy1X = 32, joy1Y = 33, joy1SW = 25; 
const byte joy2X = 35, joy2Y = 34, joy2SW = 26; 

// Pulsadores Extra
const byte pinPulsadores[3] = {5, 18, 19}; 

// Pin Analógico Extra
const byte pinAnalogExtra = 13;

// Variables para evitar leer el mismo botón mil veces (Antirrebote simple)
int lastJoy1SW = HIGH;
int lastJoy2SW = HIGH;
int lastPulsadorState[3] = {HIGH, HIGH, HIGH};

// Temporizador para no saturar el Monitor Serie
unsigned long ultimoTiempoImpresion = 0;

// ==========================================
// 2. SETUP
// ==========================================
void setup() {
    Serial.begin(115200);
    delay(1000); // Dar tiempo a que abra el monitor serie
    Serial.println("\n==================================");
    Serial.println("  INICIANDO TEST DE HARDWARE...");
    Serial.println("==================================\n");

    // Configurar botones de joysticks con Pull-Up
    pinMode(joy1SW, INPUT_PULLUP);
    pinMode(joy2SW, INPUT_PULLUP);

    // Configurar pulsadores extra con Pull-Up
    for (int i = 0; i < 3; i++) {
        pinMode(pinPulsadores[i], INPUT_PULLUP);
    }
}

// ==========================================
// 3. LOOP (Lectura constante)
// ==========================================
void loop() {
    
    // --- 1. TEST DE TECLADO ---
    char tecla = teclado.getKey();
    if (tecla) {
        Serial.print("[TECLADO] Tecla presionada: ");
        Serial.println(tecla);
    }

    // --- 2. TEST DE BOTONES DE JOYSTICK ---
    int estadoJ1 = digitalRead(joy1SW);
    if (estadoJ1 == LOW && lastJoy1SW == HIGH) {
        Serial.println("[JOYSTICK 1] Boton Central Presionado!");
        delay(50); // Pequeño debounce
    }
    lastJoy1SW = estadoJ1;

    int estadoJ2 = digitalRead(joy2SW);
    if (estadoJ2 == LOW && lastJoy2SW == HIGH) {
        Serial.println("[JOYSTICK 2] Boton Central Presionado!");
        delay(50); 
    }
    lastJoy2SW = estadoJ2;

    // --- 3. TEST DE PULSADORES EXTRA ---
    for (int i = 0; i < 3; i++) {
        int estadoBtn = digitalRead(pinPulsadores[i]);
        if (estadoBtn == LOW && lastPulsadorState[i] == HIGH) {
            Serial.printf("[BOTONES] Pulsador en pin %d presionado!\n", pinPulsadores[i]);
            delay(50);
        }
        lastPulsadorState[i] = estadoBtn;
    }

    // --- 4. TEST DE ENTRADAS ANALÓGICAS (Se imprime cada medio segundo) ---
    if (millis() - ultimoTiempoImpresion > 500) {
        int vJ1X = analogRead(joy1X);
        int vJ1Y = analogRead(joy1Y);
        int vJ2X = analogRead(joy2X);
        int vJ2Y = analogRead(joy2Y);
        int vExt = analogRead(pinAnalogExtra);

        Serial.printf("[ANALOG] Joy1(X:%4d, Y:%4d) | Joy2(X:%4d, Y:%4d) | Pin13:%4d\n", vJ1X, vJ1Y, vJ2X, vJ2Y, vExt);
        
        ultimoTiempoImpresion = millis();
    }
}