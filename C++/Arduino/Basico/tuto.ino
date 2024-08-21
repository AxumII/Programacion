#include <Arduino.h>
#include <vector>       // Para el uso de vectores (std::vector)
#include <algorithm>    // Para el uso de algoritmos (std::sort, std::accumulate)
#include <memory>       // Para el uso de punteros inteligentes (std::unique_ptr)
#include <string>       // Para el uso de cadenas de texto (std::string)

#define LED_PIN 13

class Basico {
  private:
    // Variables privadas de diferentes tipos
    int intVar;
    double doubleVar;
    float floatVar;
    char charVar;
    std::string stringVar;     // Usando std::string para cadenas
    std::vector<int> vecVar;   // Usando std::vector para almacenar una lista de enteros

    // Variables para el ejemplo sin std
    char charArray[20];
    int intArray[5] = {1, 2, 3, 4, 5};

  public:
    // Constructor de la clase
    Basico(int a, double b, float c, char d, const std::string &e) 
      : intVar(a), doubleVar(b), floatVar(c), charVar(d), stringVar(e) {
        // Inicializa el vector con valores
        vecVar = {1, 2, 3, 4, 5};
        strcpy(charArray, "Hola ");
    }

    // Método 1: Operaciones matemáticas
    void operacionesMatematicas() {
        // Usando std::vector y std::accumulate
        int sumaVector = std::accumulate(vecVar.begin(), vecVar.end(), 0);
        std::sort(vecVar.begin(), vecVar.end(), std::greater<int>());
        
        // Sumar todos los elementos del array sin std
        int sumaArray = 0;
        for (int i = 0; i < 5; i++) {
            sumaArray += intArray[i];
        }
        // Ordenar array manualmente
        for (int i = 0; i < 5; i++) {
            for (int j = i + 1; j < 5; j++) {
                if (intArray[i] < intArray[j]) {
                    int temp = intArray[i];
                    intArray[i] = intArray[j];
                    intArray[j] = temp;
                }
            }
        }

        Serial.println("Suma con std::vector: " + String(sumaVector));
        Serial.print("Vector ordenado: ");
        for (int val : vecVar) {
            Serial.print(val);
            Serial.print(" ");
        }
        Serial.println();

        Serial.println("Suma con array: " + String(sumaArray));
        Serial.print("Array ordenado: ");
        for (int i = 0; i < 5; i++) {
            Serial.print(intArray[i]);
            Serial.print(" ");
        }
        Serial.println();
    }

    // Método 2: Sobrecarga de métodos
    int metodoSobrecarga(int a, int b) {
        return a + b; // Suma de enteros
    }

    float metodoSobrecarga(float a, float b) {
        return a + b; // Suma de flotantes
    }

    // Método 3: Ejemplo de if, else, case
    void ejemploCondicionales(int valor) {
        if (valor < 10) {
            Serial.println("El valor es menor que 10");
        } else if (valor == 10) {
            Serial.println("El valor es igual a 10");
        } else {
            Serial.println("El valor es mayor que 10");
        }

        switch (valor) {
            case 1:
                Serial.println("El valor es 1");
                break;
            case 2:
                Serial.println("El valor es 2");
                break;
            default:
                Serial.println("El valor no es ni 1 ni 2");
                break;
        }
    }

    // Método 4: Punteros inteligentes vs punteros crudos
    void ejemploPunteros() {
        // Usando std::unique_ptr
        std::unique_ptr<int> ptr = std::make_unique<int>(10);
        Serial.println("Valor con std::unique_ptr: " + String(*ptr));

        // Puntero crudo
        int var = 10;
        int* rawPtr = &var;
        Serial.println("Dirección de memoria de var: " + String((int)rawPtr));
        Serial.println("Valor de var usando puntero crudo: " + String(*rawPtr));
    }

    // Método 5: Uso de memoria dinámica
    void usoMemoriaDinamica() {
        // Usando std::unique_ptr
        std::unique_ptr<int[]> arrayDinamico(new int[10]);
        for (int i = 0; i < 10; i++) {
            arrayDinamico[i] = i * 2;
            Serial.print(arrayDinamico[i]);
            Serial.print(" ");
        }
        Serial.println();

        // Usando punteros crudos
        int* arrayCrudo = new int[10];
        for (int i = 0; i < 10; i++) {
            arrayCrudo[i] = i * 2;
            Serial.print(arrayCrudo[i]);
            Serial.print(" ");
        }
        Serial.println();
        delete[] arrayCrudo;  // Liberar memoria manualmente
    }

    // Método 6: Ejemplo de struct
    struct Persona {
        std::string nombre;
        int edad;
    };

    void ejemploStruct() {
        Persona persona;
        persona.nombre = "Juan";
        persona.edad = 30;

        Serial.println("Nombre: " + String(persona.nombre.c_str()));
        Serial.println("Edad: " + String(persona.edad));
    }

    // Método 7a: Ejemplo de manejo de excepciones con std::exception
    void ejemploExcepcionesStd(int divisor) {
        try {
            if (divisor == 0) {
                throw std::runtime_error("Error: División por cero"); // Usa std::runtime_error
            }
            int resultado = 10 / divisor;
            Serial.println("Resultado con std::exception: " + String(resultado));
        } catch (const std::exception& e) {
            Serial.println(e.what()); // Imprime el mensaje de error
        }
    }

    // Método 7b: Ejemplo de manejo de excepciones básicas sin std::exception
    void ejemploExcepcionesBasicas(int divisor) {
        try {
            if (divisor == 0) {
                throw "Error: División por cero (Excepción básica)";  // Lanzar una excepción de tipo const char*
            }
            int resultado = 10 / divisor;
            Serial.println("Resultado sin std::exception: " + String(resultado));
        } catch (const char* e) {
            // Capturar la excepción de tipo const char*
            Serial.println(e);
        }

        try {
            if (divisor == 0) {
                throw 0;  // Lanzar una excepción de tipo entero
            }
            int resultado = 10 / divisor;
            Serial.println("Resultado con excepción de tipo int: " + String(resultado));
        } catch (int e) {
            // Capturar la excepción de tipo entero
            Serial.println("Error: División por cero (Excepción tipo int)");
        }
    }

    // Método 8: Ejemplo adicional - Uso de std::string y char[]
    void ejemploAdicional() {
        // Usando std::string
        std::string mensaje = "Contador: ";
        for (int contador = 0; contador < 5; contador++) {
            Serial.println((mensaje + std::to_string(contador)).c_str());
        }

        // Usando char[]
        for (int contador = 0; contador < 5; contador++) {
            char buffer[20];
            itoa(contador, buffer, 10);
            strcat(charArray, buffer);
            Serial.println(charArray);
            strcpy(charArray, "Hola ");  // Reiniciar la cadena para la siguiente iteración
        }
    }

    // Método 9: Explicación de tipos de datos
    void explicacionTiposDeDatos() {
        // Tipos básicos
        int entero = 10;
        float flotante = 5.5;
        double doblePrecision = 10.123456789;
        char caracter = 'A';
        bool booleano = true;
        
        // Tipos no tan usuales
        unsigned int enteroSinSigno = 250;
        long enteroLargo = 1000000;
        unsigned long enteroLargoSinSigno = 4000000000;
        byte datoByte = 255;
        word datoWord = 65535;
        char cadena[] = "Hola";

        Serial.println("Entero: " + String(entero) + " (Tamaño: " + String(sizeof(entero)) + " bytes)");
        Serial.println("Flotante: " + String(flotante) + " (Tamaño: " + String(sizeof(flotante)) + " bytes)");
        Serial.println("Doble Precisión: " + String(doblePrecision) + " (Tamaño: " + String(sizeof(doblePrecision)) + " bytes)");
        Serial.println("Carácter: " + String(caracter) + " (Tamaño: " + String(sizeof(caracter)) + " bytes)");
        Serial.println("Booleano: " + String(booleano) + " (Tamaño: " + String(sizeof(booleano)) + " bytes)");
        Serial.println("Entero sin signo: " + String(enteroSinSigno) + " (Tamaño: " + String(sizeof(enteroSinSigno)) + " bytes)");
        Serial.println("Entero largo: " + String(enteroLargo) + " (Tamaño: " + String(sizeof(enteroLargo)) + " bytes)");
        Serial.println("Entero largo sin signo: " + String(enteroLargoSinSigno) + " (Tamaño: " + String(sizeof(enteroLargoSinSigno)) + " bytes)");
        Serial.println("Byte: " + String(datoByte) + " (Tamaño: " + String(sizeof(datoByte)) + " bytes)");
        Serial.println("Word: " + String(datoWord) + " (Tamaño: " + String(sizeof(datoWord)) + " bytes)");
        Serial.println("Cadena: " + String(cadena) + " (Tamaño: " + String(sizeof(cadena)) + " bytes)");
    }
};

void setup() {
  // Inicializa la comunicación serial
  Serial.begin(9600);
  
  // Configura el pin del LED como salida
  pinMode(LED_PIN, OUTPUT);

  // Instancia de la clase Basico
  Basico ejemplo(5, 10.5, 3.14, 'A', "Arduino");

  // Llamada a los métodos de la clase Basico
  ejemplo.operacionesMatematicas();
  Serial.println("Suma (int): " + String(ejemplo.metodoSobrecarga(3, 4)));
  Serial.println("Suma (float): " + String(ejemplo.metodoSobrecarga(3.5f, 4.5f)));
  ejemplo.ejemploCondicionales(5);
  ejemplo.ejemploPunteros();
  ejemplo.usoMemoriaDinamica();
  ejemplo.ejemploStruct();
  ejemplo.ejemploExcepcionesStd(0);        // Probar con std::exception
  ejemplo.ejemploExcepcionesBasicas(0);    // Probar con excepciones básicas
  ejemplo.ejemploAdicional();
  ejemplo.explicacionTiposDeDatos();
}

void loop() {
  // Código en el loop si es necesario
}
