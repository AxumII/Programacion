#include "MenuController.h"

using V3 = Eigen::Vector3f;

const char* labelsMain[]   = {"SYSTEM", "CONFIG", "MANUAL", "LOAD", "TOOLS"}; // 5 opciones
const char* labelsSystem[] = {"GO HOME", "CALIBRATE", "TEST", "RESTRICT", "ABOUT"}; // 5 opciones
const char* labelsConfig[] = {"COORD REF", "UNITS", "MOVE INFO", "SEGMENT"}; // 4 opciones
const char* labelsManual[] = {"SET TYPE MOVE"}; // 1 opción
const char* labelsTool[]   = {"GRIPPER", "TRACER", "CAMERA"}; // 3 opciones
const char* labelsSetControlMove[] = {"ANGULAR", "POSITION"}; // 2 opciones

struct Transicion {
    char tecla;
    int cursor;
    void (MenuController::*nextState)(char, int);
};

MenuController::MenuController(SystemConfig* sys, MenuView* view, ServoControlling* servo) 
  : _sys(sys), _view(view), _servo(servo) {
    
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
    char key = _sys->getKey();     
    int rawJoyY = _sys->getJoystickAxis(1, 'Y');     
    int joy = _sys->joystickAsSelector(rawJoyY);

    if (ptrState != nullptr) {
        (this->*ptrState)(key, joy);
    }
}

//--------------------------------------- RENDERIZADOR DE MENÚS NORMALES ---------------------------------------

void MenuController::renderMenuView(bool activate) {
    if (activate) {
        
        if (ptrState == &MenuController::handleIdle) {
            _view->loadScreen();
            updateState = false;
            return; 
        }   

        int maxSize = 5;
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
        updateState = false; 
    }        
}

//--------------------------------------- APOYO GRAFICO -----------------------------------

int MenuController::getNumButtonsForState(void (MenuController::*currentState)(char, int)) {
    // Retorna la cantidad de opciones reales
    if (currentState == &MenuController::handleMenu) return 5;
    if (currentState == &MenuController::handleSystem) return 5;
    if (currentState == &MenuController::handleConfig) return 4;
    if (currentState == &MenuController::handleManual) return 1; 
    if (currentState == &MenuController::handleTool) return 3;
    if (currentState == &MenuController::handleSetControlMove) return 2;
    if (currentState == &MenuController::handleCalibrate && _calibState == 0) return 3;
    
    return 0; 
}

int MenuController::getCurrentCursor() {
    if (ptrState == &MenuController::handleMenu) return actualStateMenu;
    if (ptrState == &MenuController::handleSystem) return actualStateSystem;
    if (ptrState == &MenuController::handleConfig) return actualStateConfig;
    if (ptrState == &MenuController::handleManual) return actualStateManual;
    if (ptrState == &MenuController::handleTool) return actualStateTool;
    if (ptrState == &MenuController::handleSetControlMove) return actualStateSetControlMove;
    if (ptrState == &MenuController::handleCalibrate) {
        return _calibServo == 0 ? 0 : (_calibServo - 1); 
    }
    return 0;
}

const char* MenuController::textPicker(void (MenuController::*currentState)(char, int), int id) {
    if (currentState == &MenuController::handleMenu && id < 5)    return labelsMain[id];
    if (currentState == &MenuController::handleSystem && id < 5)  return labelsSystem[id];
    if (currentState == &MenuController::handleConfig && id < 4)  return labelsConfig[id];
    if (currentState == &MenuController::handleManual && id < 1)  return labelsManual[id];
    if (currentState == &MenuController::handleTool && id < 3)    return labelsTool[id];
    if (currentState == &MenuController::handleSetControlMove && id < 2) return labelsSetControlMove[id];
    if (currentState == &MenuController::handleCalibrate) {
        if (id == 0) return "1. BASE";
        if (id == 1) return "2. HOMBRO";
        if (id == 2) return "3. CODO";
    }
    return ""; 
}

// -------------------------------------- REPOSO / MENU --------------------------------------

void MenuController::handleIdle(char key, int joy) {
    if (key == '#' || joy != 0 || key == '*' ) {
        actualStateMain = 1;
        _view->clearForMenu(); 
        updateState = true;
        ptrState = &MenuController::handleMenu;
    }
    renderMenuView(updateState);
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
            break; // IMPORTANTE: Solo rompe el for, no la función
        }
    }
    renderMenuView(updateState);
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
            break; 
        }
    }
    renderMenuView(updateState);
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
            break; 
        }
    }
    renderMenuView(updateState);
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
            break; 
        }
    }
    renderMenuView(updateState);
}

void MenuController::handleLoad(char key, int joy){
    if(key == '#') { 
        actualStateMain = 1; 
        ptrState = &MenuController::handleMenu; 
        updateState = true; 
    }
    renderMenuView(updateState);
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
            break; 
        }
    }
    renderMenuView(updateState);
}

//-------------------------------------- FUNCIONES DE SYSTEM ----------------------------------

void MenuController::handleGoHome(char key, int joy){
    if(key == '#') { 
        ptrState = &MenuController::handleSystem; 
        updateState = true; 
    }    
    _servo->goHome(); 
}

void MenuController::handleCalibrate(char key, int joy) {
    int rawY = _sys->getJoystickAxis(1, 'Y');
    int joyDir = _sys->joystickAsFasterSelector(rawY);
    int step = joyDir * 7.5; 

    if (key == '#' && _calibState == 0) {
        ptrState = &MenuController::handleSystem;
        _calibServo = 0; 
        updateState = true;
        return;
    }

    switch (_calibState) {
        case 0: // --- SELECCIÓN ---
            if (_calibServo == 0) _calibServo = 1; 
            if (joy != 0) {
                _calibServo = _calibServo + joy;
                if (_calibServo > 3) _calibServo = 1;
                if (_calibServo < 1) _calibServo = 3;
                updateState = true;
            }
            if (key >= '1' && key <= '3') {
                _calibServo = key - '0';
                updateState = true;
            }
            if (key == '*') {
                _calibState = 1;
                _servo->moveSingleServo(_calibServo, 0);
                updateState = true;
            }
            break;

        case 1: // --- AJUSTE 0° ---
            if (step != 0) {
                int p1 = _servo->getPulseLimit(_calibServo, 0);
                int p2 = _servo->getPulseLimit(_calibServo, 180);
                int nuevoP1 = constrain(p1 + step, 500, 2500); 
                
                if (nuevoP1 != p1) {
                    _servo->configAttach(nuevoP1, p2, _calibServo, 0, true); 
                    updateState = true;
                }
            }
            if (key == '*') {
                _calibState = 2;
                int p1 = _servo->getPulseLimit(_calibServo, 0);
                int p2 = _servo->getPulseLimit(_calibServo, 180);
                _servo->configAttach(p1, p2, _calibServo, 180, false); 
                updateState = true;
            }
            if (key == '#') { _calibState = 0; updateState = true; } 
            break;

        case 2: // --- AJUSTE 180° ---
            if (step != 0) {
                int p1 = _servo->getPulseLimit(_calibServo, 0);
                int p2 = _servo->getPulseLimit(_calibServo, 180);
                int nuevoP2 = constrain(p2 + step, 500, 2500);
                
                if (nuevoP2 != p2) {
                    _servo->configAttach(p1, nuevoP2, _calibServo, 180, true);
                    updateState = true;
                }
            }
            if (key == '*') {
                _calibState = 0;
                int p1 = _servo->getPulseLimit(_calibServo, 0);
                int p2 = _servo->getPulseLimit(_calibServo, 180);
                _servo->configAttach(p1, p2, _calibServo, 0, false);
                
                _calibServo = 0; 
                updateState = true;
            }
            if (key == '#') { _calibState = 1; updateState = true; }
            break;
    }

    if (updateState) {
        int p1 = (_calibServo != 0) ? _servo->getPulseLimit(_calibServo, 0) : 0;
        int p2 = (_calibServo != 0) ? _servo->getPulseLimit(_calibServo, 180) : 0;
        _view->drawCalibrateMenu(_calibState, _calibServo, p1, p2);
        updateState = false;
    }
}

void MenuController::handleTest(char key, int joy){
    if(key == '#') { ptrState = &MenuController::handleSystem; updateState = true; }
}
void MenuController::handleRestrict(char key, int joy){
    if(key == '#') { ptrState = &MenuController::handleSystem; updateState = true; }
}
void MenuController::handleAboutSystem(char key, int joy){
    if(key == '#') { ptrState = &MenuController::handleSystem; updateState = true; }
}

//-------------------------------------- FUNCIONES DE CONFIG ----------------------------------
void MenuController::handleSetCoordRef(char key, int joy){
    if(key == '#') { ptrState = &MenuController::handleConfig; updateState = true; }
}
void MenuController::handleSetSystemOfUnits(char key, int joy){
    if(key == '#') { ptrState = &MenuController::handleConfig; updateState = true; }
}
void MenuController::handleSetMoveInfo(char key, int joy){
    if(key == '#') { ptrState = &MenuController::handleConfig; updateState = true; }
}
void MenuController::handleSetSegment(char key, int joy){
    if(key == '#') { ptrState = &MenuController::handleConfig; updateState = true; }
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
            _view->clearForMenu(); 
            ptrState = t.nextState;
            
            if (t.nextState == &MenuController::handleJoyAngular || 
                t.nextState == &MenuController::handleJoyPosition) {
                
                _view->loadScreen();                 
                if (t.nextState == &MenuController::handleJoyPosition || t.nextState == &MenuController::handleJoyAngular) {
                    _servo->ReachForAnglesAndStop(90, 90, 90);
                }
                _view->clearForMenu();
            }
            updateState = true;
            return; 
        }
    }
    if (updateState) {
        renderMenuView(updateState);
    }
}
//-------------------------------------- FUNCIONES DE TOOL ------------------------------------
void MenuController::handleGrippen(char key, int joy){
    if(key == '#') { ptrState = &MenuController::handleTool; updateState = true; }
}
void MenuController::handleTracer(char key, int joy){
    if(key == '#') { ptrState = &MenuController::handleTool; updateState = true; }
}
void MenuController::handleCamera(char key, int joy){
    if(key == '#') { ptrState = &MenuController::handleTool; updateState = true; }
}

//-------------------------------------- FUNCIONES DE SETCONTROLMOVE------------------------------------

void MenuController::handleJoyAngular(char key, int joy) {
    // --- 1. SALIDA Y LIMPIEZA ---
    if(key == '#') { 
        _view->clearForMenu(); 
        ptrState = &MenuController::handleSetControlMove; 
        updateState = true; 
        return; 
    }
    
    // --- 2. CAJA DE CAMBIOS CON ANTI-REBOTE (Adiós parpadeo loco) ---
    // Usamos un temporizador para que un "click" humano no cuente como 50 clicks del procesador.
    static unsigned long lastSwPress = 0;
    if ((_sys->getJoySwState(1) || _sys->getJoySwState(2)) && (millis() - lastSwPress > 300)) {
        multiplierIndex = (multiplierIndex + 1) % 3; // Itela: 0 -> 1 -> 2
        lastSwPress = millis();
    }
    
    // Asegúrate de que tu arreglo multipliers esté definido (ej. multipliers[] = {1, 2, 5};)
    int currentMult = multipliers[multiplierIndex];
    float maxBaseStep = 1.0; 

    // --- 3. LECTURA PROPORCIONAL (-1.0 a 1.0) ---
    float pQ1 = _sys->joystickAnalogProportional(_sys->getJoystickAxis(2, 'Y')); 
    float pQ2 = _sys->joystickAnalogProportional(_sys->getJoystickAxis(1, 'Y')); 
    float pQ3 = _sys->joystickAnalogProportional(_sys->getJoystickAxis(1, 'X'));
    float pTool = _sys->joystickAnalogProportional(_sys->getJoystickAxis(2, 'X'));

    bool moveState = (pQ1 != 0.0f || pQ2 != 0.0f || pQ3 != 0.0f);

    // --- 4. CEREBRO FÍSICO (Refresco Dinámico) ---
    if (moveState) {
        static unsigned long lastAngularUpdate = 0;
        
        // Si el multiplicador es alto, damos un poco más de tiempo para que el servo se mueva
        // x1 -> 40ms, x2 -> 60ms, x5 -> 100ms
        int dynamicDelay = 40 + (currentMult * 12); 

        if (millis() - lastAngularUpdate > dynamicDelay) {
            lastAngularUpdate = millis();

            // Calculamos los targets
            float targetQ1 = _servo->getAngle(1) + (pQ1 * maxBaseStep * currentMult);
            float targetQ2 = _servo->getAngle(2) + (pQ2 * maxBaseStep * currentMult);
            float targetQ3 = _servo->getAngle(3) + (pQ3 * maxBaseStep * currentMult);
            
            // Usamos el método de movimiento sin bloqueo
            _servo->ReachForAnglesContinuous(targetQ1, targetQ2, targetQ3);
        }
        wasMoving = true;
    }
    else if (wasMoving) {
        // Stop exacto al soltar el joystick
        float fQ1 = _servo->getAngle(1);
        float fQ2 = _servo->getAngle(2);
        float fQ3 = _servo->getAngle(3);
        _servo->ReachForAnglesAndStop(fQ1, fQ2, fQ3);
        wasMoving = false;
    }

    // --- 5. CONTROL TOOL ---
    if (pTool != 0.0f) {
        static unsigned long lastToolUpdate = 0;
        if (millis() - lastToolUpdate > 50) {
            lastToolUpdate = millis();
            float targetTool = _servo->getAngle(4) + (pTool * maxBaseStep * currentMult);
            // _servo->moveToolContinuous(targetTool);
        }
        wasMovingTool = true;
    } 
    else if (wasMovingTool) {
        // _servo->moveToolAndStop(_servo->getAngle(4));
        wasMovingTool = false;
    }

    // --- 6. CEREBRO VISUAL (Anti-Flicker Maestro) ---
    static bool justEntered = true; 
    static unsigned long lastUIDraw = 0;
    static int lastDrawnMult = -1; // Memoria para saber si cambió la velocidad
    
    // ¿Cuándo redibujar la pantalla? 
    // 1. Si acabamos de entrar.
    // 2. Si pasaron 250ms (solo actualiza números de forma fluida y sin titilar).
    // 3. Si se pulsó el botón y cambió el multiplicador.
    if (justEntered || millis() - lastUIDraw > 250 || currentMult != lastDrawnMult) {
        lastUIDraw = millis();
        lastDrawnMult = currentMult;
        
        V3 pos = _servo->getPos(); 
        float q1 = _servo->getAngle(1);
        float q2 = _servo->getAngle(2);
        float q3 = _servo->getAngle(3);
        float q4 = _servo->getAngle(4); 
        
        _view->drawMoveMenu(0, pos.x(), pos.y(), pos.z(), q1, q2, q3, q4, currentMult, true);
        
        justEntered = false; 
    }
}

void MenuController::handleJoyPosition(char key, int joy) {
    // --- 1. SALIDA Y LIMPIEZA DE PANTALLA ---
    if(key == '#') { 
        _view->clearForMenu(); 
        ptrState = &MenuController::handleSetControlMove; 
        updateState = true; 
        return; 
    }
    
    // --- 2. CAJA DE CAMBIOS CON ANTI-REBOTE ---
    static unsigned long lastSwPress = 0;
    if ((_sys->getJoySwState(1) || _sys->getJoySwState(2)) && (millis() - lastSwPress > 300)) {
        multiplierIndex = (multiplierIndex + 1) % 3; // Ciclo: x1 -> x2 -> x5
        lastSwPress = millis();
        updateState = true; // Forzar redibujo para mostrar el cambio de multiplicador
    }
    int currentMult = multipliers[multiplierIndex];
    float maxBaseStep = 1.0; 
    
    // --- 3. LECTURA PROPORCIONAL DE EJES ---
    float pX = _sys->joystickAnalogProportional(_sys->getJoystickAxis(1, 'Y')); 
    float pY = _sys->joystickAnalogProportional(_sys->getJoystickAxis(1, 'X')); 
    float pZ = _sys->joystickAnalogProportional(_sys->getJoystickAxis(2, 'Y'));
    float pTool = _sys->joystickAnalogProportional(_sys->getJoystickAxis(2, 'X')); 

    bool moveState = (pX != 0.0f || pY != 0.0f || pZ != 0.0f);
    static bool ikPossible = true; // Almacena el estado de la cinemática

    // --- 4. CONTROLADOR ESPACIAL (Cerebro Físico: 50ms) ---
    if (moveState) {
        static unsigned long lastCartesianUpdate = 0;
        if (millis() - lastCartesianUpdate > 50) { 
            lastCartesianUpdate = millis();
            
            V3 currentPos = _servo->getPos();
            
            float stepX = maxBaseStep * currentMult * pX;
            float stepY = maxBaseStep * currentMult * pY;
            float stepZ = maxBaseStep * currentMult * pZ;
            
            V3 targetPos(currentPos.x() + stepX, 
                         currentPos.y() + stepY, 
                         currentPos.z() + stepZ);

            // Intentar mover y capturar si el punto es alcanzable
            ikPossible = _servo->moveJTrigg(targetPos, -1);
            
            // Si hubo movimiento o intento, pedimos actualizar pantalla
            updateState = true; 
        }
        wasMoving = true;
    } 
    else if (wasMoving) {
        // Al soltar el joystick, clavamos la posición actual
        V3 finalPos = _servo->getPos();
        _servo->moveJ(finalPos, -1);
        wasMoving = false;
        updateState = true;
    }

    // --- 5. CONTROLADOR DE LA TOOL ---
    if (pTool != 0.0f) {
        static unsigned long lastToolUpdate = 0;
        if (millis() - lastToolUpdate > 50) {
            lastToolUpdate = millis();
            float maxToolStep = 2.0; 
            float targetTool = _servo->getAngle(4) + (maxToolStep * currentMult * pTool);
            // _servo->moveToolContinuous(targetTool);
            updateState = true;
        }
        wasMovingTool = true;
    } 
    else if (wasMovingTool) {
        wasMovingTool = false;
        updateState = true;
    }
    
    // --- 6. CEREBRO VISUAL (Actualización de pantalla) ---
    // Redibujamos si updateState es true o por tiempo (cada 250ms) para suavidad
    static unsigned long lastUIDraw = 0;
    static bool firstRun = true;

    if (updateState || firstRun || (millis() - lastUIDraw > 250)) {
        lastUIDraw = millis();
        firstRun = false;

        V3 pos = _servo->getPos(); 
        float q1 = _servo->getAngle(1);
        float q2 = _servo->getAngle(2);
        float q3 = _servo->getAngle(3);
        float q4 = _servo->getAngle(4); 
        
        // Llamada a la vista (modo 1 = Position) pasando el estado ikPossible
        _view->drawMoveMenu(1, pos.x(), pos.y(), pos.z(), q1, q2, q3, q4, currentMult, ikPossible);
        
        updateState = false; 
    }
}