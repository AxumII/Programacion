#ifndef MENUCONTROLLER_H
#define MENUCONTROLLER_H 

#include "SystemConfig.h"
#include "ServoControlling.h"

class MenuController {
    private:
        SystemConfig* _sys;
        ServoControlling* _servo;

        // --- VARIABLES DE ESTADO (CURSORES) ---
        int actualStateMain;
        int actualStateMenu;
        int actualStateSystem;
        int actualStateConfig;         
        int actualStateManual;         
        int actualStateTool;           
        int actualStateSetControlMove; 
        int actualStateSetCoordRef;    // <--- NUEVO: Cursor para el submenú de COORD REF
        
        bool updateState;

        const char* textPicker(void (MenuController::*currentState)(char, int), int id);
        // --- VARIABLES DE CONFIGURACIÓN INTERNA ---
        int _coordRefMode = 0;         // <--- NUEVO: 0 = HOME (Default), 1 = TCP

        // --- VARIABLES PARA APOYO DE JOYS ---
        int multiplierIndex = 0; 
        int multipliers[3] = {1, 2, 5};
        bool wasMoving = false;
        bool wasMovingTool = false;
        
        // Puntero a función miembro (Máquina de estados)
        void (MenuController::*ptrState)(char, int);

        // --- VARIABLES APOYO CALIBRACION ---
        int _calibState = 0; // 0: Base, 1: 0°, 2: Ángulo Máximo
        int _calibServo = 0; // 1, 2, 3, (4)

        // --- METODOS DE APOYO PARA EL RENDERIZADO ---
        void renderMenuView(bool activate);
        int getNumButtonsForState(void (MenuController::*currentState)(char, int));
        int getCurrentCursor();

    public:
        // Constructor
        MenuController(SystemConfig* sys, ServoControlling* servo);

        void update(); 

        // --- HANDLERS PRINCIPALES ---
        void handleIdle(char key, int joy);
        void handleMenu(char key, int joy);
        
        // --- HANDLERS DE SUBMENÚS ---
        void handleSystem(char key, int joy);
        void handleConfig(char key, int joy);
        void handleManual(char key, int joy);
        void handleLoad(char key, int joy);
        void handleTool(char key, int joy);

        // --- HANDLERS DE SYSTEM ---
        void handleGoHome(char key, int joy);
        void handleCalibrate(char key, int joy);
        void handleTest(char key, int joy);
        void handleRestrict(char key, int joy);
        void handleAboutSystem(char key, int joy);

        // --- HANDLERS DE CONFIG ---
        void handleSetCoordRef(char key, int joy);
        void handleSetHomeRef(char key, int joy);      
        void handleSetTCPRef(char key, int joy);       
        void handleSetSystemOfUnits(char key, int joy);
        void handleSetMoveInfo(char key, int joy);
        void handleSetSegment(char key, int joy);

        // --- HANDLERS DE MANUAL / CONTROL MOVE ---
        void handleSetControlMove(char key, int joy);
        void handleJoyAngular(char key, int joy);
        void handleJoyPosition(char key, int joy);

        // --- HANDLERS DE TOOL ---
        void handleGrippen(char key, int joy); 
        void handleTracer(char key, int joy);
        void handleCamera(char key, int joy); 
};

#endif