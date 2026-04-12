#include "MenuController.h"
const char* labelsMain[]   = {"SYSTEM", "CONFIG", "MANUAL", "LOAD", "TOOLS"}; // 5 opciones
const char* labelsSystem[] = {"HOME", "CALIBRATE", "TEST", "RESTRICT", "ABOUT"}; // 5 opciones
const char* labelsConfig[] = {"COORD REF", "UNITS", "MOVE INFO", "SEGMENT"}; // 4 opciones
const char* labelsManual[] = {"SET TYPE MOVE"}; // 1 opción
const char* labelsTool[]   = {"GRIPPER", "TRACER", "CAMERA"}; // 3 opciones
const char* labelsSetControlMove[] = {"ANGULAR", "POSITION"}; // 2 opciones

struct Transicion {
    char tecla;
    int cursor;
    void (MenuController::*nextState)(char, int);
};

MenuController::MenuController(SystemConfig* sys, MenuView* view) : _sys(sys), _view(view) {
    
    ptrState = &MenuController::handleIdle; 
    
    actualStateMain = 0;
    actualStateMenu = 0;
    actualStateSystem = 0;
    actualStateConfig = 0;         
    actualStateManual = 0;         
    actualStateTool = 0;           
    actualStateSetControlMove = 0; 
    updateState = true;
}


void MenuController::update() {
    // 1. Leer el teclado
    char key = _sys->getKey(); 
    
    // 2. Leer el joystick usando tu nueva función (Joystick 1, Eje Y)
    int rawJoyY = _sys->getJoystickAxis(1, 'Y'); 
    
    // 3. Procesar el movimiento con el anti-rebote
    int joy = _sys->joystickAsSelector(rawJoyY);
    
    // Imprimir para depuración (opcional, pero recomendado)
    if (key || joy != 0) {
        Serial.print("Tecla: "); Serial.print(key ? key : '-');
        Serial.print(" | Joy Y: "); Serial.print(rawJoyY);
        Serial.print(" -> Dir: "); Serial.print(joy);
        Serial.print(" | Main: "); Serial.print(actualStateMain);
        Serial.print(" | Sub: "); Serial.println(actualStateMenu);
    }

    // 4. Ejecutar la máquina de estados
    if (ptrState != nullptr) {
        (this->*ptrState)(key, joy);
    }
    if (updateState) {
        renderCurrentView(); // Nueva función privada para decidir qué dibujar
        updateState = false; 
    }
}

//--------------------------------------- RENDERIZADOR ---------------------------------------

void MenuController::renderCurrentView() {
    int maxSize = 5;
    if (ptrState == &MenuController::handleIdle) {
        _view->loadScreen();
        return; 
    }
    

    int numButtons = getNumButtonsForState(ptrState); 

    for (int i = 0; i < maxSize; i++) {
        const char* label = textPicker(ptrState, i);        
        if (label[0] == '\0') {
            _view->drawMenuButton(i, false, ""); 
        } else {
            bool isSelected = (getCurrentCursor() == i); 
            _view->drawMenuButton(i, isSelected, label);
        }
    }
}
//--------------------------------------- APOYO GRAFICO -----------------------------------

int MenuController::getNumButtonsForState(void (MenuController::*currentState)(char, int)) {
    // Retorna la cantidad de opciones que tiene cada menú para que el 'for' no dibuje de más
    if (currentState == &MenuController::handleMenu) return 5;
    if (currentState == &MenuController::handleSystem) return 5;
    if (currentState == &MenuController::handleConfig) return 4;
    if (currentState == &MenuController::handleManual) return 5;
    if (currentState == &MenuController::handleTool) return 4;
    if (currentState == &MenuController::handleSetControlMove) return 3;
    
    return 0; // Si es un estado final (como handleGoHome), no dibuja menú
}

int MenuController::getCurrentCursor() {
    // Devuelve la variable de cursor correcta dependiendo de dónde estemos
    if (ptrState == &MenuController::handleMenu) return actualStateMenu;
    if (ptrState == &MenuController::handleSystem) return actualStateSystem;
    if (ptrState == &MenuController::handleConfig) return actualStateConfig;
    if (ptrState == &MenuController::handleManual) return actualStateManual;
    if (ptrState == &MenuController::handleTool) return actualStateTool;
    if (ptrState == &MenuController::handleSetControlMove) return actualStateSetControlMove;
    
    return 0;
}

const char* MenuController::textPicker(void (MenuController::*currentState)(char, int), int id) {
    // Añadimos && id < cantidad para que NUNCA lea memoria prohibida
    if (currentState == &MenuController::handleMenu && id < 5)    return labelsMain[id];
    if (currentState == &MenuController::handleSystem && id < 5)  return labelsSystem[id];
    if (currentState == &MenuController::handleConfig && id < 4)  return labelsConfig[id];
    if (currentState == &MenuController::handleManual && id < 1)  return labelsManual[id];
    if (currentState == &MenuController::handleTool && id < 3)    return labelsTool[id];
    if (currentState == &MenuController::handleSetControlMove && id < 2) return labelsSetControlMove[id];
    
    return ""; 
}
// -------------------------------------- REPOSO / MENU --------------------------------------

void MenuController::handleIdle(char key, int joy) {
    if (key == '#' || joy != 0 || key == '*' ) {
        _view->clearForMenu();
        actualStateMain = 1;
        updateState = true;
        ptrState = &MenuController::handleMenu;
    }
}

void MenuController::handleMenu(char key, int joy) {
    if (joy != 0) {
        actualStateMenu = (actualStateMenu + joy + 5) % 5; 
        updateState = true;
    }

    Transicion menu[] = {
        {'#', -1, &MenuController::handleIdle},      
        {'*',  0, &MenuController::handleSystem},    
        {'*',  1, &MenuController::handleConfig},    
        {'*',  2, &MenuController::handleManual},
        {'*',  3, &MenuController::handleLoad},
        {'*',  4, &MenuController::handleTool}
    };

    for (auto& t : menu) {
        if (key == t.tecla && (t.cursor == -1 || t.cursor == actualStateMenu)) {
            ptrState = t.nextState;
            updateState = true;
            return; 
        }
    }
}

//-------------------------------- SUBMENÚS ---------------------------------------------------

void MenuController::handleSystem(char key, int joy){
    if (joy != 0) {
        actualStateSystem = (actualStateSystem + joy + 5) % 5; 
        updateState = true;
    }
    
    Transicion system[] = {
        {'#', -1, &MenuController::handleMenu},    
        {'*',  0, &MenuController::handleGoHome},    
        {'*',  1, &MenuController::handleCalibrate},
        {'*',  2, &MenuController::handleTest},
        {'*',  3, &MenuController::handleRestrict},
        {'*',  4, &MenuController::handleAboutSystem}
    };

    for (auto& t : system) {
        if (key == t.tecla && (t.cursor == -1 || t.cursor == actualStateSystem)) {
            ptrState = t.nextState;
            updateState = true;
            return; 
        }
    }
}

void MenuController::handleConfig(char key, int joy){
    if (joy != 0) {
        actualStateConfig = (actualStateConfig + joy + 4) % 4; 
        updateState = true;
    }
    
    Transicion config[] = {
        {'#', -1, &MenuController::handleMenu}, 
        {'*',  0, &MenuController::handleSetCoordRef},    
        {'*',  1, &MenuController::handleSetSystemOfUnits},    
        {'*',  2, &MenuController::handleSetMoveInfo},
        {'*',  3, &MenuController::handleSetSegment}        
    };

    for (auto& t : config) {
        if (key == t.tecla && (t.cursor == -1 || t.cursor == actualStateConfig)) {
            ptrState = t.nextState;
            updateState = true;
            return; 
        }
    }
}

void MenuController::handleManual(char key, int joy){
    if (joy != 0) {
        actualStateManual = (actualStateManual + joy + 1) % 1; 
        updateState = true;
    }
    
    Transicion manual[] = {
        {'#', -1, &MenuController::handleMenu},    
        {'*',  0, &MenuController::handleSetControlMove}  
    };

    for (auto& t : manual) {
        if (key == t.tecla && (t.cursor == -1 || t.cursor == actualStateManual)) {
            ptrState = t.nextState;
            updateState = true;
            return; 
        }
    }
}

void MenuController::handleLoad(char key, int joy){
    if(key == '#') { actualStateMain = 1; ptrState = &MenuController::handleMenu; updateState = true; }
    //Por ahora vacio ya que no voy a implementar esto por ahora
}

void MenuController::handleTool(char key, int joy){
    if (joy != 0) {
        actualStateTool = (actualStateTool + joy + 3) % 3; 
        updateState = true;
    }
    
    Transicion tool[] = {
        {'#', -1, &MenuController::handleMenu},    
        {'*',  0, &MenuController::handleGrippen},    
        {'*',  1, &MenuController::handleTracer},
        {'*',  2, &MenuController::handleCamera}     
    };

    for (auto& t : tool) {
        if (key == t.tecla && (t.cursor == -1 || t.cursor == actualStateTool)) {
            ptrState = t.nextState;
            updateState = true;
            return; 
        }
    }
}

//-------------------------------------- FUNCIONES DE SYSTEM ----------------------------------

void MenuController::handleGoHome(char key, int joy){
    if(key == '#') { ptrState = &MenuController::handleSystem; updateState = true; }
    //Por ahora vacia
}
void MenuController::handleCalibrate(char key, int joy){
    if(key == '#') { ptrState = &MenuController::handleSystem; updateState = true; }
    //Por ahora vacia
}
void MenuController::handleTest(char key, int joy){
    if(key == '#') { ptrState = &MenuController::handleSystem; updateState = true; }
    //Por ahora vacia
}
void MenuController::handleRestrict(char key, int joy){
    if(key == '#') { ptrState = &MenuController::handleSystem; updateState = true; }
    //Por ahora vacia
}
void MenuController::handleAboutSystem(char key, int joy){
    if(key == '#') { ptrState = &MenuController::handleSystem; updateState = true; }
    //Por ahora vacia
}

//-------------------------------------- FUNCIONES DE CONFIG ----------------------------------
void MenuController::handleSetCoordRef(char key, int joy){
    if(key == '#') { ptrState = &MenuController::handleConfig; updateState = true; }
    //Por ahora vacia
}
void MenuController::handleSetSystemOfUnits(char key, int joy){
    if(key == '#') { ptrState = &MenuController::handleConfig; updateState = true; }
    //Por ahora vacia
}
void MenuController::handleSetMoveInfo(char key, int joy){
    if(key == '#') { ptrState = &MenuController::handleConfig; updateState = true; }
    //Por ahora vacia
}
void MenuController::handleSetSegment(char key, int joy){
    if(key == '#') { ptrState = &MenuController::handleConfig; updateState = true; }
    //Por ahora vacia
}

//-------------------------------------- FUNCIONES DE MANUAL ----------------------------------
void MenuController::handleSetControlMove(char key, int joy){
    if (joy != 0) {
        actualStateSetControlMove = (actualStateSetControlMove + joy + 2) % 2;
        updateState = true;
    }
    
    Transicion controlMove[] = {
        {'#', -1, &MenuController::handleManual},    
        {'*',  0, &MenuController::handleJoyAngular},
        {'*',  1, &MenuController::handleJoyPosition}    
    };

    for (auto& t : controlMove) {
        if (key == t.tecla && (t.cursor == -1 || t.cursor == actualStateSetControlMove)) {
            ptrState = t.nextState;
            updateState = true;
            return; 
        }
    }
}

//-------------------------------------- FUNCIONES DE TOOL ------------------------------------
void MenuController::handleGrippen(char key, int joy){
    if(key == '#') { ptrState = &MenuController::handleTool; updateState = true; }
    //Por ahora vacia
}
void MenuController::handleTracer(char key, int joy){
    if(key == '#') { ptrState = &MenuController::handleTool; updateState = true; }
    //Por ahora vacia
}
void MenuController::handleCamera(char key, int joy){
    if(key == '#') { ptrState = &MenuController::handleTool; updateState = true; }
    //Por ahora vacia
}

//-------------------------------------- FUNCIONES DE SETCONTROLMOVE------------------------------------
void MenuController::handleJoyAngular(char key, int joy){
    if(key == '#') { ptrState = &MenuController::handleSetControlMove; updateState = true; }
    //Por ahora vacia
}
void MenuController::handleJoyPosition(char key, int joy){
    if(key == '#') { ptrState = &MenuController::handleSetControlMove; updateState = true; }
    //Por ahora vacia
}

