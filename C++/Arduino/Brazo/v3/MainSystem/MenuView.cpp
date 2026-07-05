#include "MenuView.h"
#include "Axum.h"

MenuView* UI = nullptr;
extern const uint16_t Axum[] PROGMEM; 

// ====================================================================
// CORRECCIÓN DE COLOR (Formato BGR)
// Los canales Rojo y Azul han sido intercambiados matemáticamente 
// para que se vean correctos en tu panel ST7789.
// ====================================================================
#define COLOR_NARANJA      0x229E // Corregido para BGR
#define COLOR_AZUL         0xC8C3 // Corregido para BGR
#define COLOR_AZUL_CLARO   0xCD14 // Corregido para BGR
#define COLOR_AMARILLO     0x07FF // Corregido para BGR
#define COLOR_NEGRO        0x0000

// Colores estándar también convertidos a BGR para evitar errores
#define COLOR_BLANCO       0xFFFF
#define COLOR_ROJO         0x001F // Red convertido a BGR
#define COLOR_VERDE        0x07E0 // Green se mantiene igual
#define COLOR_CYAN         0xFFE0 // Cyan convertido a BGR

#define COLOR_BG           COLOR_NARANJA
#define COLOR_CONTOURMENU1 COLOR_AZUL
#define COLOR_CONTOURMENU2 COLOR_AZUL_CLARO
#define COLOR_T            COLOR_NEGRO
#define COLOR_FILL_MENU    COLOR_AZUL_CLARO

MenuView::MenuView(byte cs, byte dc, byte rst) {
    _tft = new Adafruit_ST7789(&SPI, cs, dc, rst);
    // MenuButton (Ajustado para el centro horizontal de 320px)
    posXMenuButton = 70;  
    hMenuButton = 25;
    wMenuButton = 180;
}

void MenuView::initTFT() {
    _tft->init(240, 320); // Resolución real del panel de 2.8"
    _tft->setRotation(1); // 1 = Orientación Horizontal (Landscape 320x240)

}

void MenuView::loadScreen() {
    _tft->fillScreen(COLOR_NARANJA);    
    _tft->drawRGBBitmap(40, -20, Axum, 240, 280); 
}

void MenuView::clearForMenu() {
    _tft->fillScreen(COLOR_BG); 
}

void MenuView::clearYellow() {
    _tft->fillScreen(COLOR_AMARILLO);
}

void MenuView::clear(uint16_t color) {
    _tft->fillScreen(color);
}

void MenuView::drawMenuButton(int id, bool picked, const char* text){
    int posY = 20 + (id * 40); 
    uint16_t color = picked ?  COLOR_CONTOURMENU1 :  COLOR_CONTOURMENU2;

    if (text[0] == '\0') {
        _tft->fillRect(posXMenuButton - 2, posY - 2, wMenuButton + 4, hMenuButton + 4, COLOR_BG);
        return; 
    }
    uint16_t fillColor   = picked ? COLOR_FILL_MENU : COLOR_BLANCO;
    uint16_t borderColor = COLOR_AZUL; 
    uint16_t textColor   = picked ? COLOR_BLANCO : COLOR_T;

    _tft->fillRoundRect(posXMenuButton - 2, posY - 2, wMenuButton + 4, hMenuButton + 4, 12, COLOR_BG);
    _tft->fillRoundRect(posXMenuButton, posY, wMenuButton, hMenuButton, 10, fillColor);
    _tft->drawRoundRect(posXMenuButton, posY, wMenuButton, hMenuButton, 10, borderColor);

    int textWidth  = strlen(text) * 12; 
    int textHeight = 16;
    int cursorX = posXMenuButton + (wMenuButton - textWidth) / 2;
    int cursorY = posY + (hMenuButton - textHeight) / 2;
    _tft->setCursor(cursorX, cursorY);     
    _tft->setTextColor(textColor);
    _tft->setTextSize(2);
    _tft->print(text); 
    if (picked) {
        _tft->drawRoundRect(posXMenuButton - 1, posY - 1, wMenuButton + 2, hMenuButton + 2, 11, COLOR_AZUL);
    }
}

void MenuView::drawCalibrateMenu(int calibState, int calibServo, int p1, int p2) {
    char msg[30];
    uint16_t infoColor = COLOR_AZUL;

    switch(calibState) {
        case 0: // --- SELECCIÓN DE MOTOR ---
            clearForMenu(); 
            drawMenuButton(0, (calibServo == 1), "1. BASE");
            drawMenuButton(1, (calibServo == 2), "2. HOMBRO");
            drawMenuButton(2, (calibServo == 3), "3. CODO");

            _tft->setTextColor(COLOR_T);
            _tft->setTextSize(2);
            _tft->setCursor(80, 190); // Centrado en Horizontal
            _tft->print("PULSE 1, 2 o 3");
            break;

        case 1: 
        case 2: // --- PANTALLA DE CALIBRACIÓN (Ajustada a 320x240) ---
            _tft->fillScreen(COLOR_AMARILLO); 

            // RECUADRO 1: TÍTULO DEL SERVO
            _tft->fillRoundRect(10, 20, 300, 50, 12, COLOR_NEGRO);
            _tft->drawRoundRect(10, 20, 300, 50, 12, COLOR_BLANCO);
            _tft->setTextColor(COLOR_BLANCO);
            _tft->setTextSize(2); 
            _tft->setCursor(65, 35);
            if(calibState == 1) sprintf(msg, "SERVO %d: 0 GRAD", calibServo);
            else                sprintf(msg, "SERVO %d: MAX GRAD", calibServo);
            _tft->print(msg);

            // RECUADRO 2: VALOR NUMÉRICO
            _tft->fillRoundRect(10, 80, 300, 60, 12, COLOR_FILL_MENU);
            _tft->drawRoundRect(10, 80, 300, 60, 12, infoColor);
            _tft->setTextColor(COLOR_T);
            _tft->setTextSize(3);
            _tft->setCursor(85, 100);
            _tft->print("P: "); 
            _tft->print(calibState == 1 ? p1 : p2); 
            _tft->print(" us");

            // RECUADRO 3: INSTRUCCIONES
            _tft->fillRoundRect(10, 150, 300, 60, 12, COLOR_FILL_MENU);
            _tft->drawRoundRect(10, 150, 300, 60, 12, infoColor);
            _tft->setTextColor(COLOR_T);
            _tft->setTextSize(1);
            _tft->setCursor(65, 165);
            _tft->print("Use Joystick to adjust level");
            _tft->setCursor(65, 185);
            _tft->print("Remove joint to calibrate");
            break;
    }
}

void MenuView::drawMoveMenu(int mode, float x, float y, float z, float q1, float q2, float q3, float q4, int speedMult, bool isPossible, bool isServo4) {
    char buf[20];
    
    // --- 1. ENCABEZADO ---
    _tft->setTextColor(COLOR_BLANCO, COLOR_NEGRO);
    _tft->setTextSize(2); 
    _tft->setCursor(80, 10);
    
    if (mode == 0) _tft->print("CTRL: ANGULAR");
    else           _tft->print("CTRL: POSICION");
    
    _tft->drawLine(10, 30, 310, 30, COLOR_NARANJA); 

    // --- 2. BLOQUE DE DATOS (Ajustado horizontalmente a 320x240) ---
    _tft->setTextSize(2); 
    
    // [Recuadro Izquierdo: JOINTS]
    _tft->drawRoundRect(10, 40, 145, 140, 6, COLOR_NARANJA);
    _tft->setTextColor(COLOR_CYAN);
    _tft->setCursor(45, 50); _tft->print("JOINTS");
    
    _tft->setTextColor(COLOR_BLANCO, COLOR_NEGRO);
    sprintf(buf, "Q1:%4.0f", q1); _tft->setCursor(20, 75);  _tft->print(buf);
    sprintf(buf, "Q2:%4.0f", q2); _tft->setCursor(20, 100); _tft->print(buf);
    sprintf(buf, "Q3:%4.0f", q3); _tft->setCursor(20, 125); _tft->print(buf);
    
    if (isServo4) sprintf(buf, "Q4:%4.0f", q4);
    else          sprintf(buf, "PH:%4.0f", q4); 
    _tft->setCursor(20, 150); _tft->print(buf);

    // [Recuadro Derecho: CARTESIANAS]
    _tft->drawRoundRect(165, 40, 145, 140, 6, COLOR_NARANJA);
    _tft->setTextColor(0xFDA0); 
    _tft->setCursor(200, 50); _tft->print("CARTES");

    _tft->setTextColor(COLOR_BLANCO, COLOR_NEGRO);
    sprintf(buf, "X:%5.1f", x); _tft->setCursor(180, 75);  _tft->print(buf);
    sprintf(buf, "Y:%5.1f", y); _tft->setCursor(180, 105); _tft->print(buf);
    sprintf(buf, "Z:%5.1f", z); _tft->setCursor(180, 135); _tft->print(buf);

    // --- 3. AVISO DE CINEMÁTICA ---
    _tft->setTextSize(2);
    _tft->setCursor(100, 185);
    if (isPossible) {
        _tft->setTextColor(COLOR_VERDE, COLOR_NEGRO);
        _tft->print("STATUS: OK");
    } else {
        _tft->setTextColor(COLOR_ROJO, COLOR_NEGRO);
        _tft->print("STATUS: ERR");
    }

    // --- 4. BARRA DE CONTROL INFERIOR ---
    _tft->drawRoundRect(10, 205, 300, 30, 4, COLOR_NARANJA);
    _tft->setTextColor(COLOR_BLANCO, COLOR_NEGRO);
    
    _tft->setCursor(25, 212);
    sprintf(buf, "x%d", speedMult); _tft->print(buf);
    
    _tft->setCursor(200, 212);
    if (mode == 1) _tft->print("REF: TCP");
    else           _tft->print("REF: HOME");
}

void MenuView::drawAboutSystemMenu(bool sw1, bool sw2, int jx1, int jy1, int jx2, int jy2, 
                                   char key, bool button2, bool led1, bool led2, 
                                   bool serialOk, bool i2cOk, bool pcaOk, const char* i2cAddrs) 
{
    char buf[40];
    // --- TÍTULO ---
    _tft->setTextColor(COLOR_BLANCO, COLOR_BG); 
    _tft->setTextSize(2);
    _tft->setCursor(55, 10);
    _tft->print("SYSTEM DIAGNOSTICS");

    // ==========================================
    // SECCIÓN 1: JOYSTICKS (Reorganizado lado a lado para paisaje)
    // ==========================================
    _tft->fillRoundRect(5, 35, 150, 60, 6, COLOR_NEGRO);
    _tft->drawRoundRect(5, 35, 150, 60, 6, COLOR_AZUL_CLARO);
    _tft->fillRoundRect(165, 35, 150, 60, 6, COLOR_NEGRO);
    _tft->drawRoundRect(165, 35, 150, 60, 6, COLOR_AZUL_CLARO);

    _tft->setTextColor(COLOR_BLANCO, COLOR_NEGRO);
    _tft->setTextSize(1);
    
    // Joystick 1
    _tft->setCursor(15, 45); _tft->print("JOYSTICK 1");
    sprintf(buf, "X: %-4d Y: %-4d", jx1, jy1); 
    _tft->setCursor(15, 60); _tft->print(buf);
    sprintf(buf, "SW: %-3s", sw1 ? "ON" : "OFF");
    _tft->setCursor(15, 75); _tft->print(buf);

    // Joystick 2
    _tft->setCursor(175, 45); _tft->print("JOYSTICK 2");
    sprintf(buf, "X: %-4d Y: %-4d", jx2, jy2);
    _tft->setCursor(175, 60); _tft->print(buf);
    sprintf(buf, "SW: %-3s", sw2 ? "ON" : "OFF");
    _tft->setCursor(175, 75); _tft->print(buf);

    // ==========================================
    // SECCIÓN 2: BOTÓN, TECLADO Y LEDS
    // ==========================================
    _tft->fillRoundRect(5, 100, 150, 45, 6, COLOR_NEGRO);
    _tft->drawRoundRect(5, 100, 150, 45, 6, COLOR_AZUL_CLARO);
    _tft->fillRoundRect(165, 100, 150, 45, 6, COLOR_NEGRO);
    _tft->drawRoundRect(165, 100, 150, 45, 6, COLOR_AZUL_CLARO);

    _tft->setTextColor(COLOR_BLANCO, COLOR_NEGRO);
    // Panel Izquierdo
    sprintf(buf, "BTN 2 : %-3s", button2 ? "ON" : "OFF");
    _tft->setCursor(15, 110); _tft->print(buf);
    sprintf(buf, "TECLA : %c  ", key ? key : '-');
    _tft->setCursor(15, 125); _tft->print(buf);

    // Panel Derecho
    sprintf(buf, "LED 1 : %-3s", led1 ? "ON" : "OFF");
    _tft->setCursor(175, 110); _tft->print(buf);
    sprintf(buf, "LED 2 : %-3s", led2 ? "ON" : "OFF");
    _tft->setCursor(175, 125); _tft->print(buf);

    // ==========================================
    // SECCIÓN 3: COMUNICACIONES (Alineado en una sola fila)
    // ==========================================
    _tft->fillRoundRect(5, 150, 310, 35, 6, COLOR_NEGRO);
    _tft->drawRoundRect(5, 150, 310, 35, 6, COLOR_AZUL_CLARO);
    
    _tft->setCursor(15, 162);
    _tft->setTextColor(COLOR_BLANCO, COLOR_NEGRO); _tft->print("SER: ");
    _tft->setTextColor(serialOk ? COLOR_VERDE : COLOR_ROJO, COLOR_NEGRO);
    _tft->print(serialOk ? "OK   " : "FAIL ");

    _tft->setTextColor(COLOR_BLANCO, COLOR_NEGRO); _tft->print(" I2C: ");
    _tft->setTextColor(i2cOk ? COLOR_VERDE : COLOR_ROJO, COLOR_NEGRO);
    _tft->print(i2cOk ? "OK   " : "FAIL ");

    _tft->setTextColor(COLOR_BLANCO, COLOR_NEGRO); _tft->print(" PCA: ");
    _tft->setTextColor(pcaOk ? COLOR_VERDE : COLOR_ROJO, COLOR_NEGRO);
    _tft->print(pcaOk ? "OK   " : "FAIL ");

    // ==========================================
    // SECCIÓN 4: ESCÁNER I2C
    // ==========================================
    _tft->fillRoundRect(5, 190, 310, 45, 6, COLOR_NEGRO);
    _tft->drawRoundRect(5, 190, 310, 45, 6, COLOR_AZUL_CLARO);
    
    _tft->setTextColor(COLOR_BLANCO, COLOR_NEGRO);
    _tft->setCursor(15, 200); 
    _tft->print("I2C ADDRS FOUND:");

    _tft->setTextColor(0xFDA0, COLOR_NEGRO); 
    _tft->setCursor(15, 215);
    sprintf(buf, "%-40s", i2cAddrs); 
    _tft->print(buf);
}

void MenuView::drawGoHome(bool isHomeReached) {
    _tft->fillScreen(COLOR_NEGRO);
    int w = 220;
    int h = 80;
    // Centrado absoluto para 320x240
    int x = (320 - w) / 2;
    int y = (240 - h) / 2;

    _tft->fillRoundRect(x, y, w, h, 10, COLOR_NEGRO);
    _tft->setTextSize(1);

    if (isHomeReached) {
        _tft->drawRoundRect(x, y, w, h, 10, COLOR_VERDE); 
        _tft->setTextColor(COLOR_BLANCO);
        _tft->setCursor(x + 50, y + 35);
        _tft->print("Robot reached HOME");
    } else {
        _tft->drawRoundRect(x, y, w, h, 10, COLOR_ROJO); 
        _tft->setTextColor(COLOR_ROJO);
        _tft->setCursor(x + 50, y + 35);
        _tft->print("HOME Failed (Limits)");
    }
}

void MenuView::drawBottomBanner(const char* text, uint16_t color) {
    _tft->fillRoundRect(10, 200, 300, 35, 6, COLOR_NEGRO);
    _tft->drawRoundRect(10, 200, 300, 35, 6, color);
    _tft->setTextColor(color);
    _tft->setTextSize(1);    
    // Centrado respecto al nuevo ancho (320)
    int xPos = (320 - (strlen(text) * 6)) / 2;     
    _tft->setCursor(xPos, 212);
    _tft->print(text);
}