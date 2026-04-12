#ifndef MENUCONTROLLER_H
#define MENUCONTROLLER_H 
#include "SystemConfig.h"

class MenuController {
    private:
        SystemConfig* _sys;
        MenuView* _view;

        // --- VARIABLES DE ESTADO (CURSORES) ---
        int actualStateMain;
        int actualStateMenu;
        int actualStateSystem;
        int actualStateConfig;         // NUEVO
        int actualStateManual;         // NUEVO
        int actualStateTool;           // NUEVO
        int actualStateSetControlMove; // NUEVO
        
        bool updateState;

        // Puntero a función miembro
        void (MenuController::*ptrState)(char, int);

        // --- FUNCIONES DE APOYO PARA EL RENDERIZADO ---
        void renderCurrentView();
        int getNumButtonsForState(void (MenuController::*currentState)(char, int));
        int getCurrentCursor();
        const char* textPicker(void (MenuController::*currentState)(char, int), int id);

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

    public:
        MenuController(SystemConfig* sys, MenuView* view);
        void update(); 
};
#endif