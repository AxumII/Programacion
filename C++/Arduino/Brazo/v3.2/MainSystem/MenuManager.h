#ifndef MENUMANAGER_H 
#define MENUMANAGER_H 

#include <Arduino.h>
#include "SystemConfig.h"
#include "ServoControlling.h"

class MenuManager {
    private:
        SystemConfig* _sys;
        ServoControlling* _servo;

    public:
        MenuManager(SystemConfig* sys, ServoControlling* servo);

        void update(); 
        void procesarComandosSeriales();

        // Rutinas Automáticas
        void rutinaPickAndPlace();
        bool esperarPasoRutina(unsigned long tiempoEspera_ms);
};

#endif