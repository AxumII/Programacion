#ifndef MENU_VIEW_H
#define MENU_VIEW_H

#include <Arduino.h>
#include <Adafruit_GFX.h>
#include <Adafruit_ST7789.h>
#include <SPI.h>

class MenuView {
    private:
        Adafruit_ST7789* _tft; 
        int posXMenuButton;
        int hMenuButton;
        int wMenuButton;
    public:
        MenuView(byte cs, byte dc, byte rst);
        void initTFT();
        void loadScreen();   
        void clearForMenu(); 
        void clearYellow();
        void clear(uint16_t color);
        void drawMenuButton(int id, bool picked, const char* text);
        void drawCalibrateMenu( int calibState, int calibServo, int p1,int p2);
        void drawMoveMenu(int mode, float x, float y, float z, float q1, float q2, float q3, float q4, int speedMult, bool isPossible, bool isServo4);
        void drawAboutSystemMenu(bool sw1, bool sw2, int jx1, int jy1, int jx2, int jy2, 
                                   char key, bool button2, bool led1, bool led2, 
                                   bool serialOk, bool i2cOk, bool pcaOk, const char* i2cAddrs);
        void drawGoHome(bool isHomeReached);
        void drawBottomBanner(const char* text, uint16_t color);
};
extern MenuView* UI;
#endif
