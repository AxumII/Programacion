#include "MenuView.h"
#include "Axum.h"

extern const uint16_t Axum[] PROGMEM; 

#define COLOR_NARANJA 0xf284 
#define COLOR_BG COLOR_NARANJA
#define COLOR_AZUL 0x18D9       
#define COLOR_AZUL_CLARO 0xA519  
#define COLOR_CONTOURMENU1 COLOR_AZUL
#define COLOR_CONTOURMENU2 COLOR_AZUL_CLARO
#define COLOR_T 0x0000
#define COLOR_FILL_MENU COLOR_AZUL_CLARO
#define COLOR_AMARILLO     0xFFE0
MenuView::MenuView(byte cs, byte dc, byte rst) {
    _tft = new Adafruit_ST7789(cs, dc, rst);
    posXMenuButton = 40;
    hMenuButton = 30;
    wMenuButton = 180;
    posXCenterUpper = 20;
    posYCenterUpper = 40;
    hCenterUpper = 160;
    wCenterUpper = 60;

 }

void MenuView::initTFT() {
    _tft->init(240, 280); 
}

void MenuView::loadScreen() {
    _tft->fillScreen(COLOR_NARANJA);
    _tft->drawRGBBitmap(0, 0, Axum, 240, 280);
}

void MenuView::clearForMenu() {
    _tft->fillScreen(COLOR_BG); 
}
void MenuView::clear(uint16_t color) {
    _tft->fillScreen(color);
}

void MenuView::drawMenuButton(int id, bool picked, const char* text){
    
    int posY = 30 + (id * 50); 
    uint16_t color = picked ?  COLOR_CONTOURMENU1 :  COLOR_CONTOURMENU2;

    if (text[0] == '\0') {
        _tft->fillRect(posXMenuButton - 2, posY - 2, wMenuButton + 4, hMenuButton + 4, COLOR_BG);
        return; 
    }
    uint16_t fillColor   = picked ? COLOR_FILL_MENU : ST77XX_WHITE;
    uint16_t borderColor = COLOR_AZUL; 
    uint16_t textColor   = picked ? ST77XX_WHITE : COLOR_T;

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
    // Variables para centrado de texto dinámico
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
            _tft->setCursor(posXMenuButton, 190); 
            _tft->print("PULSE 1, 2 o 3");
            break;

        case 1: // --- AJUSTE DE 0° ---
            clearForMenu(); // Limpia la lista de botones
            
            _tft->fillRoundRect(10, 50, 220, 120, 12, COLOR_FILL_MENU);
            _tft->drawRoundRect(10, 50, 220, 120, 12, infoColor);

            _tft->setTextColor(ST77XX_WHITE);
            _tft->setTextSize(2);
            _tft->setCursor(20, 70);
            sprintf(msg, "SERVO %d a 0 Grad", calibServo);
            _tft->print(msg);

            _tft->setCursor(20, 110);
            _tft->print("P1: "); _tft->print(p1); _tft->print("us");

            _tft->setTextSize(1);
            _tft->setCursor(20, 145);
            _tft->print("Mueva Joystick para nivelar");
            break;

        case 2: // --- AJUSTE DE 180° ---
            
            _tft->fillRoundRect(10, 50, 220, 120, 12, COLOR_FILL_MENU);
            _tft->drawRoundRect(10, 50, 220, 120, 12, infoColor);

            _tft->setTextColor(ST77XX_WHITE);
            _tft->setTextSize(2);
            _tft->setCursor(20, 70);
            sprintf(msg, "SERVO %d a 180 Grad", calibServo);
            _tft->print(msg);

            _tft->setCursor(20, 110);
            _tft->print("P2: "); _tft->print(p2); _tft->print("us");
            break;
    }
}

void MenuView::drawMoveMenu(int mode, float x, float y, float z, float q1, float q2, float q3, float q4, int speedMult, bool isPossible) {
    
    

    // 2. ENCABEZADO DINÁMICO
    _tft->setTextSize(2);
    _tft->setTextColor(ST77XX_YELLOW, ST77XX_BLACK);
    _tft->setCursor(36, 15); 
    
    if (mode == 0) {
        _tft->print(" MODO ANGULAR ");
    } else {
        _tft->print(" MODO POSITION");
    }

    // 3. INDICADOR DE VELOCIDAD (MULTIPLICADOR)
    _tft->setTextColor(ST77XX_GREEN, ST77XX_BLACK);
    _tft->setCursor(24, 40);
    _tft->print("Multiplier: x" + String(speedMult));

    // 4. CONFIGURACIÓN DE COLUMNAS
    int startY = 85;     // Altura inicial de datos
    int gap = 30;        // Espacio vertical entre filas
    int colAngles = 10;  // X columna izquierda (Servos)
    int colCoords = 125; // X columna derecha (Cartesianas)
    char buf[20]; 

    // >> COLUMNA IZQUIERDA: ÁNGULOS DE SERVOS (Q) <<
    _tft->setTextColor(ST77XX_CYAN, ST77XX_BLACK);
    
    sprintf(buf, "Q1:%6.1f", q1);
    _tft->setCursor(colAngles, startY);
    _tft->print(buf);
    
    sprintf(buf, "Q2:%6.1f", q2);
    _tft->setCursor(colAngles, startY + gap);
    _tft->print(buf);
    
    sprintf(buf, "Q3:%6.1f", q3);
    _tft->setCursor(colAngles, startY + gap * 2);
    _tft->print(buf);
    
    sprintf(buf, "TL:%6.1f", q4);
    _tft->setCursor(colAngles, startY + gap * 3);
    _tft->print(buf);

    // >> COLUMNA DERECHA: COORDENADAS (X, Y, Z) <<
    // Estos valores vienen de la cinemática directa (DH)
    _tft->setTextColor(ST77XX_ORANGE, ST77XX_BLACK);
    
    sprintf(buf, "X:%6.1f", x);
    _tft->setCursor(colCoords, startY);
    _tft->print(buf);
    
    sprintf(buf, "Y:%6.1f", y);
    _tft->setCursor(colCoords, startY + gap);
    _tft->print(buf);
    
    sprintf(buf, "Z:%6.1f", z);
    _tft->setCursor(colCoords, startY + gap * 2);
    _tft->print(buf);

    _tft->setCursor(140, 200);
    if (isPossible) {
        _tft->setTextColor(ST77XX_GREEN, ST77XX_BLACK);
        _tft->print("READY ");
    } else {
        _tft->setTextColor(ST77XX_RED, ST77XX_BLACK);
        _tft->print("BLOCK ");
    }

    // 5. PIE DE PÁGINA (Instrucciones)
    _tft->setTextSize(1);
    _tft->setTextColor(0x7BEF, ST77XX_BLACK); // Gris
    _tft->setCursor(51, 220);
    _tft->print("Presione [#] para salir");
}