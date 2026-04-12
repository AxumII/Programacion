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

MenuView::MenuView(byte cs, byte dc, byte rst) {
    _tft = new Adafruit_ST7789(cs, dc, rst);
    posXMenuButton = 40;
    hMenuButton = 30;
    wMenuButton = 180;
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




