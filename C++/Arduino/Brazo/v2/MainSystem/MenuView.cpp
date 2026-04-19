#include "MenuView.h"
#include "Axum.h"

MenuView* UI = nullptr;
extern const uint16_t Axum[] PROGMEM; 

#define COLOR_NARANJA 0xf284 
#define COLOR_AZUL 0x18D9       
#define COLOR_AZUL_CLARO 0xA519  
#define COLOR_NEGRO 0x0000
#define COLOR_AMARILLO     0xFFE0


#define COLOR_BG COLOR_NARANJA
#define COLOR_CONTOURMENU1 COLOR_AZUL
#define COLOR_CONTOURMENU2 COLOR_AZUL_CLARO
#define COLOR_T COLOR_NEGRO
#define COLOR_FILL_MENU COLOR_AZUL_CLARO


MenuView::MenuView(byte cs, byte dc, byte rst) {
    _tft = new Adafruit_ST7789(&SPI, cs, dc, rst);
    //MenuButton
    posXMenuButton = 40;
    hMenuButton = 30;
    wMenuButton = 180;
}

void MenuView::initTFT() {
    _tft->init(240, 280); 
    _tft->setRotation(2);
}

void MenuView::loadScreen() {
    _tft->fillScreen(COLOR_NARANJA);
    _tft->drawRGBBitmap(0, 0, Axum, 240, 280);
}

void MenuView::clearForMenu() {
    _tft->fillScreen(COLOR_BG); 
}

void MenuView::clearYellow() {
    _tft->fillScreen(COLOR_AMARILLO );
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
            _tft->setCursor(posXMenuButton, 200); 
            _tft->print("PULSE 1, 2 o 3");
            break;

        case 1: 
        case 2: // El diseño es similar para 0° y 180°
            // --- FONDO AMARILLO ---
            _tft->fillScreen(COLOR_AMARILLO); 

            // --- RECUADRO 1: TÍTULO DEL SERVO (NEGRO) ---
            _tft->fillRoundRect(10, 30, 220, 55, 12, COLOR_NEGRO);
            _tft->drawRoundRect(10, 30, 220, 55, 12, ST77XX_WHITE);
            _tft->setTextColor(ST77XX_WHITE);
            _tft->setTextSize(2); 
            _tft->setCursor(30, 50);
            if(calibState == 1) sprintf(msg, "SERVO %d: 0 GRAD", calibServo);
            else                sprintf(msg, "SERVO %d: MAX GRAD", calibServo);
            _tft->print(msg);

            // --- RECUADRO 2: VALOR NUMÉRICO (AZUL CLARO) ---
            _tft->fillRoundRect(10, 100, 220, 55, 12, COLOR_FILL_MENU);
            _tft->drawRoundRect(10, 100, 220, 55, 12, infoColor);
            _tft->setTextColor(COLOR_T);
            _tft->setTextSize(3);
            _tft->setCursor(45, 115);
            _tft->print("P: "); 
            _tft->print(calibState == 1 ? p1 : p2); 
            _tft->print(" us");

            // --- RECUADRO 3: INSTRUCCIONES (AZUL CLARO) ---
            // Se redujo la altura (de 70 a 55) al tener menos texto
            _tft->fillRoundRect(10, 170, 220, 55, 12, COLOR_FILL_MENU);
            _tft->drawRoundRect(10, 170, 220, 55, 12, infoColor);
            _tft->setTextColor(COLOR_T);
            _tft->setTextSize(1);
            
            // Instrucción 1
            _tft->setCursor(25, 185);
            _tft->print("Use Joystick to adjust level");
            
            // Instrucción 2
            _tft->setCursor(25, 205);
            _tft->print("Remove joint to calibrate");
            
            break;
    }
}

void MenuView::drawMoveMenu(int mode, float x, float y, float z, float q1, float q2, float q3, float q4, int speedMult, bool isPossible, bool isServo4) {
    char buf[20];
    
    // --- 1. ENCABEZADO DINÁMICO ---
    _tft->setTextColor(ST77XX_WHITE, COLOR_NEGRO);
    _tft->setTextSize(2); 
    _tft->setCursor(30, 15);
    
    // El modo indica cómo estamos moviendo el brazo (Joy -> XYZ o Joy -> Q123)
    if (mode == 0) _tft->print("CTRL: ANGULAR");
    else           _tft->print("CTRL: POSICION");
    
    _tft->drawLine(10, 40, 230, 40, COLOR_NARANJA); 

    // --- 2. BLOQUE DE DATOS (JOINTS Y CARTESIANAS) ---
    _tft->setTextSize(2); 
    
    // [Recuadro Izquierdo: ESTADO DE SERVOS]
    _tft->drawRoundRect(8, 55, 110, 150, 6, COLOR_NARANJA);
    _tft->setTextColor(ST77XX_CYAN);
    _tft->setCursor(25, 65); _tft->print("JOINTS");
    
    _tft->setTextColor(ST77XX_WHITE, COLOR_NEGRO);
    sprintf(buf, "Q1:%4.0f", q1); _tft->setCursor(15, 90);  _tft->print(buf);
    sprintf(buf, "Q2:%4.0f", q2); _tft->setCursor(15, 120); _tft->print(buf);
    sprintf(buf, "Q3:%4.0f", q3); _tft->setCursor(15, 150); _tft->print(buf);
    
    // Lógica isServo4: ¿Es un ángulo manual o es Phi?
    if (isServo4) {
        sprintf(buf, "Q4:%4.0f", q4); // Theta de la herramienta/servo
    } else {
        sprintf(buf, "PH:%4.0f", q4); // Phi (Orientación calculada)
    }
    _tft->setCursor(15, 180); _tft->print(buf);

    // [Recuadro Derecho: COORDENADAS ESPACIALES]
    _tft->drawRoundRect(122, 55, 110, 150, 6, COLOR_NARANJA);
    _tft->setTextColor(0xFDA0); // Naranja claro
    _tft->setCursor(138, 65); _tft->print("CARTES");

    _tft->setTextColor(ST77XX_WHITE, COLOR_NEGRO);
    sprintf(buf, "X:%5.1f", x); _tft->setCursor(128, 95);  _tft->print(buf);
    sprintf(buf, "Y:%5.1f", y); _tft->setCursor(128, 130); _tft->print(buf);
    sprintf(buf, "Z:%5.1f", z); _tft->setCursor(128, 165); _tft->print(buf);

    // --- 3. AVISO DE CINEMÁTICA (READY / BLOCK) ---
    _tft->setTextSize(2);
    _tft->setCursor(45, 215);
    if (isPossible) {
        _tft->setTextColor(ST77XX_GREEN, ST77XX_BLACK);
        _tft->print("STATUS: OK");
    } else {
        _tft->setTextColor(ST77XX_RED, ST77XX_BLACK);
        _tft->print("STATUS: ERR");
    }

    // --- 4. BARRA DE CONTROL INFERIOR ---
    _tft->drawRoundRect(10, 240, 220, 35, 4, COLOR_NARANJA);
    _tft->setTextColor(ST77XX_WHITE, COLOR_NEGRO);
    
    // Multiplicador
    _tft->setCursor(25, 250);
    sprintf(buf, "x%d", speedMult); _tft->print(buf);
    
    // Referencia de modo (TCP si nos movemos en el espacio, HOME si estamos en origen)
    _tft->setCursor(120, 250);
    if (mode == 1) _tft->print("REF: TCP");
    else           _tft->print("REF: HOME");
}

void MenuView::drawAboutSystemMenu(bool sw1, bool sw2, int jx1, int jy1, int jx2, int jy2, 
                                   char key, bool button2, bool led1, bool led2, 
                                   bool serialOk, bool i2cOk, bool pcaOk, const char* i2cAddrs) 
{
    char buf[40];
    // --- TÍTULO ---
    _tft->setTextColor(ST77XX_WHITE, COLOR_BG); 
    _tft->setTextSize(2);
    _tft->setCursor(20, 10);
    _tft->print("SYSTEM DIAGNOSTICS");

    // ==========================================
    // SECCIÓN 1: JOYSTICKS (Mitad Izquierda y Derecha)
    // ==========================================
    // Cajas contenedoras (Dibujar solo los bordes o un fondo si es la primera vez)
    _tft->fillRoundRect(5, 40, 110, 60, 6, COLOR_NEGRO);
    _tft->drawRoundRect(5, 40, 110, 60, 6, COLOR_AZUL_CLARO);
    _tft->fillRoundRect(125, 40, 110, 60, 6, COLOR_NEGRO);
    _tft->drawRoundRect(125, 40, 110, 60, 6, COLOR_AZUL_CLARO);

    _tft->setTextColor(ST77XX_WHITE, COLOR_NEGRO);
    _tft->setTextSize(1);
    
    // Joystick 1
    _tft->setCursor(15, 45); _tft->print("JOYSTICK 1");
    sprintf(buf, "X: %-4d Y: %-4d", jx1, jy1); // %-4d evita rastros de números viejos
    _tft->setCursor(15, 60); _tft->print(buf);
    sprintf(buf, "SW: %-3s", sw1 ? "ON" : "OFF");
    _tft->setCursor(15, 75); _tft->print(buf);

    // Joystick 2
    _tft->setCursor(135, 45); _tft->print("JOYSTICK 2");
    sprintf(buf, "X: %-4d Y: %-4d", jx2, jy2);
    _tft->setCursor(135, 60); _tft->print(buf);
    sprintf(buf, "SW: %-3s", sw2 ? "ON" : "OFF");
    _tft->setCursor(135, 75); _tft->print(buf);

    // ==========================================
    // SECCIÓN 2: BOTÓN, TECLADO Y LEDS
    // ==========================================
    _tft->fillRoundRect(5, 105, 110, 50, 6, COLOR_NEGRO);
    _tft->drawRoundRect(5, 105, 110, 50, 6, COLOR_AZUL_CLARO);
    _tft->fillRoundRect(125, 105, 110, 50, 6, COLOR_NEGRO);
    _tft->drawRoundRect(125, 105, 110, 50, 6, COLOR_AZUL_CLARO);

    _tft->setTextColor(ST77XX_WHITE, COLOR_NEGRO);
    // Panel Izquierdo (Btn y Key)
    sprintf(buf, "BTN 2 : %-3s", button2 ? "ON" : "OFF");
    _tft->setCursor(15, 115); _tft->print(buf);
    sprintf(buf, "TECLA : %c  ", key ? key : '-');
    _tft->setCursor(15, 135); _tft->print(buf);

    // Panel Derecho (LEDs)
    sprintf(buf, "LED 1 : %-3s", led1 ? "ON" : "OFF");
    _tft->setCursor(135, 115); _tft->print(buf);
    sprintf(buf, "LED 2 : %-3s", led2 ? "ON" : "OFF");
    _tft->setCursor(135, 135); _tft->print(buf);

    // ==========================================
    // SECCIÓN 3: ESTADO DE COMUNICACIONES
    // ==========================================
    _tft->fillRoundRect(5, 160, 230, 45, 6, COLOR_NEGRO);
    _tft->drawRoundRect(5, 160, 230, 45, 6, COLOR_AZUL_CLARO);
    
    _tft->setCursor(15, 170);
    _tft->setTextColor(ST77XX_WHITE, COLOR_NEGRO); _tft->print("SER: ");
    _tft->setTextColor(serialOk ? ST77XX_GREEN : ST77XX_RED, COLOR_NEGRO);
    _tft->print(serialOk ? "OK   " : "FAIL ");

    _tft->setTextColor(ST77XX_WHITE, COLOR_NEGRO); _tft->print(" I2C: ");
    _tft->setTextColor(i2cOk ? ST77XX_GREEN : ST77XX_RED, COLOR_NEGRO);
    _tft->print(i2cOk ? "OK   " : "FAIL ");

    _tft->setTextColor(ST77XX_WHITE, COLOR_NEGRO); _tft->setCursor(15, 185); _tft->print("PCA: ");
    _tft->setTextColor(pcaOk ? ST77XX_GREEN : ST77XX_RED, COLOR_NEGRO);
    _tft->print(pcaOk ? "OK   " : "FAIL ");

    // ==========================================
    // SECCIÓN 4: ESCÁNER I2C (Direcciones)
    // ==========================================
    _tft->fillRoundRect(5, 210, 230, 60, 6, COLOR_NEGRO);
    _tft->drawRoundRect(5, 210, 230, 60, 6, COLOR_AZUL_CLARO);
    
    _tft->setTextColor(ST77XX_WHITE, COLOR_NEGRO);
    _tft->setCursor(15, 220); 
    _tft->print("I2C ADDRS FOUND:");

    _tft->setTextColor(0xFDA0, COLOR_NEGRO); // Naranja claro para los hex
    _tft->setCursor(15, 240);
    // Formateamos para que limpie la línea si hay menos direcciones que antes
    sprintf(buf, "%-33s", i2cAddrs); 
    _tft->print(buf);
}

void MenuView::drawGoHome(bool isHomeReached) {
    _tft->fillScreen(COLOR_NEGRO);
    int w = 180;
    int h = 80;
    int x = (240 - w) / 2;
    int y = (280 - h) / 2;

    _tft->fillRoundRect(x, y, w, h, 10, COLOR_NEGRO);
    _tft->setTextSize(1);

    if (isHomeReached) {
        _tft->drawRoundRect(x, y, w, h, 10, ST77XX_GREEN); 
        _tft->setTextColor(ST77XX_WHITE);
        _tft->setCursor(x + 20, y + 40);
        _tft->print("Robot reached HOME");
    } else {
        _tft->drawRoundRect(x, y, w, h, 10, ST77XX_RED); 
        _tft->setTextColor(ST77XX_RED);
        _tft->setCursor(x + 20, y + 40);
        _tft->print("HOME Failed (Limits)");
    }
}
void MenuView::drawBottomBanner(const char* text, uint16_t color) {
    _tft->fillRoundRect(15, 220, 210, 35, 6, COLOR_NEGRO);
    _tft->drawRoundRect(15, 220, 210, 35, 6, color);
    _tft->setTextColor(color);
    _tft->setTextSize(1);    
    int xPos = (240 - (strlen(text) * 6)) / 2;     
    _tft->setCursor(xPos, 233);
    _tft->print(text);
}