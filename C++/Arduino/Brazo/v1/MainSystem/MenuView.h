#ifndef MENU_VIEW_H
#define MENU_VIEW_H

#include <Arduino.h>
#include <Adafruit_GFX.h>
#include <Adafruit_ST7789.h>
#include <SPI.h>

class MenuView {
    private:
        Adafruit_ST7789* _tft; 
        
        // ---> NUEVO: Declarar las variables aquí
        int posXMenuButton;
        int hMenuButton;
        int wMenuButton;
        int posXCenterUpper;
        int posYCenterUpper;
        int hCenterUpper;
        int wCenterUpper;

    public:
        MenuView(byte cs, byte dc, byte rst);
        void initTFT();
        void loadScreen();   
        void clearForMenu(); 
        void clear(uint16_t color);
        void drawMenuButton(int id, bool picked, const char* text);
        void drawCalibrateMenu( int calibState, int calibServo, int p1,int p2);
};

#endif