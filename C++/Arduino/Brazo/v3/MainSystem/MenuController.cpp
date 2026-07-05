#include "MenuController.h"

using V3 = Eigen::Vector3f;

const char* labelsMain[]   = {"SYSTEM", "CONFIG", "MANUAL", "LOAD", "TOOLS"}; // 5 opciones
const char* labelsSystem[] = {"GO HOME", "CALIBRATE", "TEST", "RESTRICT", "ABOUT"}; // 5 opciones
const char* labelsConfig[] = {"COORD REF", "UNITS", "MOVE INFO", "SEGMENT"}; // 4 opciones
const char* labelsManual[] = {"SET TYPE MOVE"}; // 1 opción
const char* labelsTool[]   = {"GRIPPER", "TRACER", "CAMERA"}; // 3 opciones
const char* labelsSetControlMove[] = {"ANGULAR", "POSITION"}; // 2 opciones
const char* labelsCoordRef[] = {"HOME", "TCP"}; // 2 opciones

struct Transicion {
    char tecla;
    int cursor;
    void (MenuController::*nextState)(char, int);
};

MenuController::MenuController(SystemConfig* sys, ServoControlling* servo) 
  : _sys(sys), _servo(servo) {
    
    ptrState = &MenuController::handleIdle; 
    
    actualStateMain = 0;
    actualStateMenu = 0;
    actualStateSystem = 0;
    actualStateConfig = 0;         
    actualStateManual = 0;         
    actualStateTool = 0;           
    actualStateSetControlMove = 0; 
    actualStateSetCoordRef = 0; 
    updateState = true;
}

void MenuController::update() {
    char key = _sys->getKey();     
    int rawJoyY = _sys->getJoystickAxis(1, 'Y');     
    int joy = _sys->joystickAsSelector(rawJoyY);

    if (key != '\0') {
        switch(key) {
            case 'A': 
                // Botón A -> Libre para el futuro 
                key = '#';// Botón C -> Funciona como Atrás / Salir
                break; 
            case 'B': 
                 // Botón B -> Libre para el futuro
                break;
            case 'C':
                // Botón A -> Libre para el futuro 
                break;
            case 'D':
                key = '*'; // Botón D -> Funciona como OK / Seleccionar
                break;
        }
    }

    if (ptrState != nullptr) {
        (this->*ptrState)(key, joy);
    }
}

//--------------------------------------- RENDERIZADOR DE MENÚS NORMALES ---------------------------------------
void MenuController::renderMenuView(bool activate) {
    if (activate) {
        
        if (ptrState == &MenuController::handleIdle) {
            UI->loadScreen();
            updateState = false;
            return; 
        }   

        int maxSize = 5;
        int numButtons = getNumButtonsForState(ptrState); 
        if (numButtons == 0) {
            return; 
        }

        for (int i = 0; i < maxSize; i++) {
            const char* label = textPicker(ptrState, i);        
            if (label[0] == '\0') {
                UI->drawMenuButton(i, false, ""); 
            } else {
                bool isSelected = (getCurrentCursor() == i); 
                UI->drawMenuButton(i, isSelected, label);
            }
        }
        updateState = false; 
    }        
}

//--------------------------------------- APOYO GRAFICO -----------------------------------

int MenuController::getNumButtonsForState(void (MenuController::*currentState)(char, int)) {
    if (currentState == &MenuController::handleMenu) return 5;
    if (currentState == &MenuController::handleSystem) return 5;
    if (currentState == &MenuController::handleConfig) return 4;
    if (currentState == &MenuController::handleManual) return 1; 
    if (currentState == &MenuController::handleTool) return 3;
    if (currentState == &MenuController::handleSetControlMove) return 2;
    if (currentState == &MenuController::handleCalibrate && _calibState == 0) return 3;
    if (currentState == &MenuController::handleSetCoordRef) return _servo->isServo4 ? 2 : 1; 
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
    if (ptrState == &MenuController::handleSetCoordRef) return actualStateSetCoordRef;
    return 0;
}

const char* MenuController::textPicker(void (MenuController::*currentState)(char, int), int id) {
    if (currentState == &MenuController::handleMenu && id < 5)    return labelsMain[id];
    if (currentState == &MenuController::handleSystem && id < 5)  return labelsSystem[id];
    if (currentState == &MenuController::handleConfig && id < 4)  return labelsConfig[id];
    if (currentState == &MenuController::handleManual && id < 1)  return labelsManual[id];
    if (currentState == &MenuController::handleTool && id < 3)    return labelsTool[id];
    if (currentState == &MenuController::handleSetControlMove && id < 2) return labelsSetControlMove[id];
    if (currentState == &MenuController::handleSetCoordRef) return labelsCoordRef[id];
    if (currentState == &MenuController::handleCalibrate) {
        if (id == 0) return "1. BASE";
        if (id == 1) return "2. SHOULDER";
        if (id == 2) return "3. ELBOW";
        if (id == 3 && _servo->isServo4) return "4. WRIST";
    }
    return ""; 
}

// -------------------------------------- LOGICA UI GENERAL --------------------------------------
// -------------------------------------- REPOSO / MENU --------------------------------------

void MenuController::handleIdle(char key, int joy) {
    if (key == '#' || joy != 0 || key == '*' ) {
        actualStateMain = 1;
        UI->clearForMenu(); 
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
void MenuController::handleGoHome(char key, int joy) {
    // 1. Salida
    if (key == '#') { 
        ptrState = &MenuController::handleSystem; 
        updateState = true; 
        UI->clearForMenu();
        return; 
    } 
    if (updateState) {
        UI->loadScreen();
        UI->drawGoHome( _servo->goHome());          
        updateState = false; 
    }          
}
//_servo->goHome();
void MenuController::handleCalibrate(char key, int joy) {
    // 1. Configuración de parámetros de entrada y paso
    int rawY = _sys->getJoystickAxis(1, 'Y');
    int joyDir = _sys->joystickAsFasterSelector(rawY);
    int step = joyDir * 7.5; // Velocidad de ajuste de los pulsos

    // 2. Determinar límites dinámicos
    int maxServos = _servo->isServo4 ? 4 : 3;
    // Obtenemos el ángulo máximo real del servo actual (ej. 90, 180, etc.)
    int maxAng = (_calibServo != 0) ? _servo->getMaxAngle(_calibServo) : 180;

    // 3. Salida del menú (Solo en el estado de selección)
    if (key == '#' && _calibState == 0) {
        ptrState = &MenuController::handleSystem;
        _calibServo = 0; 
        updateState = true;
        UI->clearForMenu(); // Limpiamos para volver al menú anterior
        return;
    }

    switch (_calibState) {
        case 0: // --- ESTADO 0: SELECCIÓN DE SERVO ---
            if (_calibServo == 0) _calibServo = 1; 
            
            if (joy != 0) {
                _calibServo = _calibServo + joy;
                if (_calibServo > maxServos) _calibServo = 1;
                if (_calibServo < 1) _calibServo = maxServos;
                updateState = true;
            }

            if (key == '*') { 
                _calibState = 1; 
                updateState = true; 
                
                // Mover los demás servos a posición neutral (90°, 90°, 90°, 0°)
                _servo->moveToNeutralForCalibration(_calibServo);
                
                // Posicionar el servo actual en 0° para empezar a calibrar el límite inferior
                int p1 = _servo->getPulseLimit(_calibServo, 0);
                int p2 = _servo->getPulseLimit(_calibServo, maxAng);
                _servo->configAttach(p1, p2, _calibServo, 0, false); 
            }
            break;

        case 1: // --- ESTADO 1: AJUSTE LÍMITE INFERIOR (0°) ---
            if (step != 0) {
                int p1 = _servo->getPulseLimit(_calibServo, 0);
                int p2 = _servo->getPulseLimit(_calibServo, maxAng);
                int nuevoP1 = constrain(p1 + step, 500, 2500); 
                
                if (nuevoP1 != p1) {
                    // liveUpdate = true para que el servo se mueva mientras ajustas
                    _servo->configAttach(nuevoP1, p2, _calibServo, 0, true); 
                    updateState = true;
                }
            }

            if (key == '*') {
                _calibState = 2; 
                int p1 = _servo->getPulseLimit(_calibServo, 0);
                int p2 = _servo->getPulseLimit(_calibServo, maxAng);
                _servo->configAttach(p1, p2, _calibServo, maxAng, false); 
                updateState = true;
            }

            if (key == '#') { 
                _calibState = 0; 
                updateState = true; 
            } 
            break;

        case 2: // --- ESTADO 2: AJUSTE LÍMITE SUPERIOR (MAX°) ---
            if (step != 0) {
                int p1 = _servo->getPulseLimit(_calibServo, 0);
                int p2 = _servo->getPulseLimit(_calibServo, maxAng);
                int nuevoP2 = constrain(p2 + step, 500, 2500); 
                
                if (nuevoP2 != p2) {
                    _servo->configAttach(p1, nuevoP2, _calibServo, maxAng, true); 
                    updateState = true;
                }
            }

            if (key == '*') {
                _calibState = 0; 
                updateState = true;
            }

            if (key == '#') { 
                _calibState = 1; // Volver al ajuste de 0°
                int p1 = _servo->getPulseLimit(_calibServo, 0);
                int p2 = _servo->getPulseLimit(_calibServo, maxAng);
                _servo->configAttach(p1, p2, _calibServo, 0, false); 
                updateState = true; 
            }
            break;
    }

    // 4. LÓGICA DE DIBUJO (Reemplazo de interfaz)
    if (updateState) {
        if (_calibState == 0) {
            UI->clearForMenu(); 
            const char* servoLabels[] = {"SERVO 1", "SERVO 2", "SERVO 3", "SERVO 4"};
            for (int i = 1; i <= maxServos; i++) {
                UI->drawMenuButton(i, (i == _calibServo), servoLabels[i-1]);
            }
        } 
        else {
            int p1 = _servo->getPulseLimit(_calibServo, 0);
            int p2 = _servo->getPulseLimit(_calibServo, maxAng);
            UI->drawCalibrateMenu(_calibState, _calibServo, p1, p2); 
        }
        updateState = false;
    }
}

void MenuController::handleTest(char key, int joy){
    if(key == '#') { ptrState = &MenuController::handleSystem; updateState = true; }
}

void MenuController::handleRestrict(char key, int joy){
    if(key == '#') { ptrState = &MenuController::handleSystem; updateState = true; }
}

void MenuController::handleAboutSystem(char key, int joy) {
    // Variables estáticas para guardar el estado del escaneo 
    // y mantener el texto en memoria mientras estemos en este menú
    static bool i2cScanned = false;
    static char i2cStr[40] = "";

    // --- 1. LÓGICA DE SALIDA ---
    if (key == '#') { 
        ptrState = &MenuController::handleSystem; 
        updateState = true; 
        _sys->setLED(0, false); 
        _sys->setLED(1, false); 
        UI->clearForMenu();
        i2cScanned = false; 
        return; 
    }

    // --- 2. LECTURA DE SENSORES EN TIEMPO REAL ---
    int jx1 = _sys->getJoystickAxis(1, 'X');
    int jy1 = _sys->getJoystickAxis(1, 'Y');
    int jx2 = _sys->getJoystickAxis(2, 'X');
    int jy2 = _sys->getJoystickAxis(2, 'Y');
    bool sw1 = _sys->getJoySwState(1);
    bool sw2 = _sys->getJoySwState(2);
    bool btn2 = _sys->readPulsador(1); 

    // --- 3. FORZAR LEDS ENCENDIDOS ---
    _sys->setLED(0, true);
    _sys->setLED(1, true);

    // --- 4. PREPARACIÓN INICIAL DE LA PANTALLA ---
    if (updateState) {
        UI->clearForMenu(); 
        updateState = false;
    }

    // --- 5. ESCANEO I2C (Se ejecuta SOLO UNA VEZ por visita) ---
    if (!i2cScanned) {
        Eigen::VectorXi addrs = _sys->I2CScan();
        i2cStr[0] = '\0'; // Vaciamos la cadena de texto

        if (addrs.size() == 0) {
            strcpy(i2cStr, "NONE FOUND");
        } else {
            char hexBuf[8];
            // Límite de 5 direcciones para que no se desborde el texto de la pantalla
            int limit = (addrs.size() > 5) ? 5 : addrs.size();
            for (int i = 0; i < limit; i++) {
                sprintf(hexBuf, "0x%02X ", addrs[i]);
                strcat(i2cStr, hexBuf);
            }
        }
        i2cScanned = true; // Bloqueamos el escaneo para los siguientes ciclos del loop
    }

    // --- 6. ACTUALIZACIÓN DE LA VISTA CONTINUA ---
    UI->drawAboutSystemMenu(
        sw1, sw2, jx1, jy1, jx2, jy2, 
        key, btn2, true, true, 
        _sys->_SerialStatus, _sys->_I2CStatus, _sys->_PCA9685Status, 
        i2cStr 
    );
}


//-------------------------------------- FUNCIONES DE CONFIG ----------------------------------
void MenuController::handleSetCoordRef(char key, int joy) {
    int numOpciones = _servo->isServo4 ? 2 : 1;

    if (joy != 0) {
        actualStateSetCoordRef = (actualStateSetCoordRef + joy + numOpciones) % numOpciones; 
        updateState = true;
    }
    
    Transicion setcoordref[] = {
        {'#', -1, &MenuController::handleConfig},   
        {'*',  0, &MenuController::handleSetHomeRef}, 
        {'*',  1, &MenuController::handleSetTCPRef}  
    };

    for (auto& t : setcoordref) {
        if (key == t.tecla && (t.cursor == -1 || t.cursor == actualStateSetCoordRef)) {
            if (key == '#') {
                UI->clearForMenu(); 
            }
            ptrState = t.nextState;
            updateState = true;
            return; 
        }
    }
    
  
    if (updateState && ptrState == &MenuController::handleSetCoordRef) { 
        renderMenuView(updateState);
        updateState = false;
    }
}

void MenuController::handleSetSystemOfUnits(char key, int joy) {
    if(key == '#') { ptrState = &MenuController::handleConfig; updateState = true; UI->clearForMenu(); }
}

void MenuController::handleSetMoveInfo(char key, int joy) {
    if(key == '#') { ptrState = &MenuController::handleConfig; updateState = true; UI->clearForMenu(); }
}

void MenuController::handleSetSegment(char key, int joy) {
    if(key == '#') { ptrState = &MenuController::handleConfig; updateState = true; UI->clearForMenu(); }
}

//-------------------------------------- FUNCIONES DE SET COORD ----------------------------------

void MenuController::handleSetHomeRef(char key, int joy) {
    if (updateState) {
        _coordRefMode = 0; 
        UI->drawBottomBanner("SUCCESS: Ref set to HOME", ST77XX_GREEN);
        updateState = false;
    }

    if (key == '#' || key == '*') { 
        UI->clearForMenu(); 
        ptrState = &MenuController::handleConfig; 
        updateState = true; 
        return;
    }
}

void MenuController::handleSetTCPRef(char key, int joy) {
    if (updateState) {
        if (_servo->isServo4) {
            _coordRefMode = 1; 
            UI->drawBottomBanner("SUCCESS: Ref set to TCP", ST77XX_GREEN);
        } else {
            ptrState = &MenuController::handleConfig; 
            updateState = true;
            return; 
        }
        updateState = false;
    }

    if (key == '#' || key == '*') { 
        UI->clearForMenu(); 
        ptrState = &MenuController::handleConfig; 
        updateState = true; 
        return;
    }
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
            UI->clearForMenu(); 
            ptrState = t.nextState;
            
            if (t.nextState == &MenuController::handleJoyAngular || 
                t.nextState == &MenuController::handleJoyPosition) {
                
                UI->loadScreen();                 
                if (t.nextState == &MenuController::handleJoyPosition || t.nextState == &MenuController::handleJoyAngular) {
                    _servo->goHome();
                    
                }
                UI->clear(ST77XX_BLACK);
            }
            updateState = true;
            return; 
        }
    }
    if (updateState) {
        renderMenuView(updateState);
    }
}

//-------------------------------------- FUNCIONES DE SETCONTROLMOVE------------------------------------
void MenuController::handleJoyAngular(char key, int joy) {
    if(key == '#') { 
        UI->clearForMenu(); ptrState = &MenuController::handleSetControlMove; updateState = true; return; 
    }
    
    static unsigned long lastSwPress = 0;
    if ((_sys->getJoySwState(1) || _sys->getJoySwState(2)) && (millis() - lastSwPress > 300)) {
        multiplierIndex = (multiplierIndex + 1) % 3; lastSwPress = millis();
    }
    int currentMult = multipliers[multiplierIndex];

    // Zona muerta ampliada para evitar ruidos eléctricos
    auto getStep = [](int val) -> int {
        if (val > 3800) return 2; else if (val > 3000) return 1;
        else if (val < 200) return -2; else if (val < 1000) return -1;
        return 0;
    };

    int dQ1 = getStep(_sys->getJoystickAxis(2, 'Y')); 
    int dQ2 = getStep(_sys->getJoystickAxis(1, 'Y')); 
    int dQ3 = getStep(_sys->getJoystickAxis(1, 'X'));
    int dQ4 = getStep(_sys->getJoystickAxis(2, 'X'));

    bool isTouchingStick = (dQ1 != 0 || dQ2 != 0 || dQ3 != 0 || (dQ4 != 0 && _servo->isServo4));

    // --- VARIABLES DE SETPOINT VIRTUAL (El secreto para poder devolverse sin trabarse) ---
    static float targetQ1 = 0, targetQ2 = 0, targetQ3 = 0, targetQ4 = 0;
    static bool isMovingInternal = false; 

    if (isTouchingStick) {
        static unsigned long lastStepTime = 0;
        float dt_ms = 60.0f; // Bucle de 60ms para estabilidad
        
        if (millis() - lastStepTime > (unsigned long)dt_ms) {
            lastStepTime = millis();

            // 1. SINCRONIZAR SOLO LA PRIMERA VEZ QUE SE TOCA EL JOYSTICK
            if (!isMovingInternal) {
                targetQ1 = _servo->getAngle(1);
                targetQ2 = _servo->getAngle(2);
                targetQ3 = _servo->getAngle(3);
                targetQ4 = _servo->isServo4 ? _servo->getAngle(4) : 0.0f;
                isMovingInternal = true;
            }

            // 2. TAMAÑO DE PASO QUIRÚRGICO (Para que x1 sea súper lento y preciso)
            float baseStep = 0.15f; 
            float step1 = dQ1 * currentMult * baseStep; 
            float step2 = dQ2 * currentMult * baseStep;
            float step3 = dQ3 * currentMult * baseStep;
            float step4 = _servo->isServo4 ? (dQ4 * currentMult * baseStep) : 0.0f;

            // 3. SUMA MATEMÁTICA SOBRE TARGETS (Evita bloqueos de inercia)
            targetQ1 = constrain(targetQ1 + step1, -90.0f, (float)_servo->getMaxAngle(1) - 90.0f);
            targetQ2 = constrain(targetQ2 + step2, 0.0f, (float)_servo->getMaxAngle(2));
            targetQ3 = constrain(targetQ3 + step3, -(float)_servo->getMaxAngle(3), 0.0f);
            if (_servo->isServo4) {
                targetQ4 = constrain(targetQ4 + step4, -90.0f, (float)_servo->getMaxAngle(4) - 90.0f);
            }

            // 4. USO DE FABS() EN LUGAR DE ABS() PARA NO ROMPER LOS DECIMALES
            float d1 = fabs(targetQ1 - _servo->getAngle(1));
            float d2 = fabs(targetQ2 - _servo->getAngle(2));
            float d3 = fabs(targetQ3 - _servo->getAngle(3));
            float d4 = _servo->isServo4 ? fabs(targetQ4 - _servo->getAngle(4)) : 0.0f;

            float max_dTheta = d1;
            if (d2 > max_dTheta) max_dTheta = d2;
            if (d3 > max_dTheta) max_dTheta = d3;
            if (d4 > max_dTheta) max_dTheta = d4;

            // 5. CÁLCULO DE VELOCIDAD DINÁMICA CON LÍMITES
            int dynamicSpeed = (int)((max_dTheta / (dt_ms / 1000.0f)) * 1.3f); 
            if (dynamicSpeed < 8) dynamicSpeed = 8; // Mínimo para que no haga "stick-slip"
            if (dynamicSpeed > 150) dynamicSpeed = 150; // MÁXIMO de seguridad para evitar vibración en x5

            _servo->ReachForAnglesContinuous(targetQ1, targetQ2, targetQ3, targetQ4, dynamicSpeed);
        }
        wasMoving = true;
    }
    else if (wasMoving) {
        wasMoving = false; 
        isMovingInternal = false; // Reset al soltar el joystick para que pueda volver a sincronizar
    }

    static unsigned long lastUIDraw = 0;
    if (millis() - lastUIDraw > 250) {
        lastUIDraw = millis();
        V3 pos = _servo->getPos(); 
        UI->drawMoveMenu(0, pos.x(), pos.y(), pos.z(), _servo->getAngle(1), _servo->getAngle(2), _servo->getAngle(3), _servo->getAngle(4), currentMult, true, _servo->isServo4);
    }
}

void MenuController::handleJoyPosition(char key, int joy) {
    if(key == '#') { 
        UI->clearForMenu(); ptrState = &MenuController::handleSetControlMove; updateState = true; return; 
    }
    
    static bool controlPhiActive = false; 
    static float internalPhi = 0.0f;
    static float targetX = 0, targetY = 0, targetZ = 0;
    static bool isMovingInternal = false; 

    if (key == 'D') {
        controlPhiActive = !controlPhiActive;
        isMovingInternal = false; 
        Serial.printf("CAMBIO MODO: %s\n", controlPhiActive ? "PHI (Inclinación Auto)" : "Q4 (Manual)");
    }

    static unsigned long lastSwPress = 0;
    if ((_sys->getJoySwState(1) || _sys->getJoySwState(2)) && (millis() - lastSwPress > 300)) {
        multiplierIndex = (multiplierIndex + 1) % 3; lastSwPress = millis();
    }
    int currentMult = multipliers[multiplierIndex];

    // Zona muerta estricta para evitar vibraciones por ruido del joystick
    auto getStep = [](int val) -> int {
        if (val > 3800) return 2; else if (val > 3000) return 1;
        else if (val < 200) return -2; else if (val < 1000) return -1;
        return 0;
    };

    int dX  = getStep(_sys->getJoystickAxis(1, 'Y')); 
    int dY  = getStep(_sys->getJoystickAxis(1, 'X')); 
    int dZ  = getStep(_sys->getJoystickAxis(2, 'Y')); 
    int dQ4 = getStep(_sys->getJoystickAxis(2, 'X'));

    bool isTouchingStick = (dX != 0 || dY != 0 || dZ != 0 || (dQ4 != 0 && _servo->isServo4));
    static bool ikPossible = true;

    if (isTouchingStick) {
        static unsigned long lastStepTime = 0;
        float dt_segundos = 0.06f; // Ciclo de 60ms para estabilidad
        
        if (millis() - lastStepTime > 60) {
            lastStepTime = millis();
            
            if (!isMovingInternal) {
                V3 currentPos = _servo->getPos(); 
                targetX = currentPos.x(); targetY = currentPos.y(); targetZ = currentPos.z();
                if (controlPhiActive) internalPhi = _servo->getAngle(2) + _servo->getAngle(3) + _servo->getAngle(4);
                isMovingInternal = true;
            }

            // Sensibilidad controlada (x1 = 0.5mm por paso)
            float stepSize = currentMult * 0.5f; 
            
            float nextX = targetX + (dX * stepSize);
            float nextY = targetY + (dY * stepSize);
            float nextZ = targetZ + (dZ * stepSize);
            
            float t1, t2, t3, t4;
            bool testIk = false;

            if (_servo->isServo4) {
                if (controlPhiActive) {
                    float nextPhi = internalPhi + (dQ4 * currentMult * 0.5f);
                    nextPhi = constrain(nextPhi, -90.0f, 90.0f);
                    testIk = _servo->_kinematic->pos2Angle(nextX, nextY, nextZ, t1, t2, t3, t4, nextPhi);
                    if (testIk) internalPhi = nextPhi; 
                } 
                else {
                    float nextQ4 = _servo->getAngle(4) + (dQ4 * currentMult * 0.5f);
                    testIk = _servo->_kinematic->pos2Angle(nextX, nextY, nextZ, t1, t2, t3, nextQ4);
                    if (testIk) t4 = nextQ4;
                }
            } else {
                testIk = _servo->_kinematic->pos2Angle(nextX, nextY, nextZ, t1, t2, t3, 0.0f);
                t4 = 0.0f;
            }

            if (testIk) {
                ikPossible = true;
                targetX = nextX; targetY = nextY; targetZ = nextZ;
                
                // Cálculo de velocidad dinámica con margen para fluidez
                float d1 = abs(t1 - _servo->getAngle(1));
                float d2 = abs(t2 - _servo->getAngle(2));
                float d3 = abs(t3 - _servo->getAngle(3));
                float d4 = _servo->isServo4 ? abs(t4 - _servo->getAngle(4)) : 0.0f;

                float max_dTheta = d1;
                if (d2 > max_dTheta) max_dTheta = d2;
                if (d3 > max_dTheta) max_dTheta = d3;
                if (d4 > max_dTheta) max_dTheta = d4;

                int dynamicSpeed = (max_dTheta / dt_segundos) * 1.3f;
                if (dynamicSpeed < 15) dynamicSpeed = 15; // Mínimo para evitar saltos

                _servo->ReachForAnglesContinuous(t1, t2, t3, t4, dynamicSpeed);
            } else {
                ikPossible = false;
            }
        }
        wasMoving = true;
    } 
    else if (wasMoving) {
        wasMoving = false;
        isMovingInternal = false; 
    }

    static unsigned long lastUIDraw = 0;
    if (millis() - lastUIDraw > 250) {
        lastUIDraw = millis();
        V3 pos = _servo->getPos(); 
        UI->drawMoveMenu(1, pos.x(), pos.y(), pos.z(), _servo->getAngle(1), _servo->getAngle(2), _servo->getAngle(3), _servo->getAngle(4), currentMult, ikPossible, _servo->isServo4);
    }
}

// --- HANDLERS DE TOOLS ) ---

void MenuController::handleGrippen(char key, int joy) {
    if (key == '#') {
        ptrState = &MenuController::handleTool;
        updateState = true;
        UI->clearForMenu();
    }
}

void MenuController::handleTracer(char key, int joy) {
    if (key == '#') {
        ptrState = &MenuController::handleTool;
        updateState = true;
        UI->clearForMenu();
    }
}

void MenuController::handleCamera(char key, int joy) {
    if (key == '#') {
        ptrState = &MenuController::handleTool;
        updateState = true;
        UI->clearForMenu();
    }
}