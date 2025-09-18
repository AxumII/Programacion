/*
  ============================================================================
  TUTORIAL RÁPIDO DE C PARA PIC (XC8)
  Temas: variables, strings, operadores, if, switch, while, for, funciones,
         parámetros, punteros y structs.
  Autor: Tú :)
  Compilador: MPLAB XC8
  ============================================================================
*/

#ifdef __XC8
  #include <xc.h>         // Cabecera del compilador XC8 (registros, __delay_ms, etc.)
  // --- Config bits: (EJEMPLO) Descomenta y ajusta a TU dispositivo ---
  // #pragma config FOSC = INTRC_NOCLKOUT, WDTE = OFF, PWRTE = ON, MCLRE = ON
  // #pragma config CP = OFF, CPD = OFF, BOREN = ON, IESO = OFF, FCMEN = OFF, LVP = OFF
  // #define _XTAL_FREQ 8000000UL  // Necesario si usas __delay_ms/__delay_us
#endif

#include <stdint.h>   // enteros con tamaño fijo: uint8_t, uint16_t, etc.
#include <stdbool.h>  // tipo bool, true/false
#include <string.h>   // manejo de strings: strcpy, strlen, strcat, etc.

/* ============================================================================
   1) VARIABLES (GLOBALES, ESTÁTICAS, VOLÁTILES)
   ----------------------------------------------------------------------------
   - 'volatile' se usa cuando un valor puede cambiar fuera del flujo normal
     del C (p.ej. ISR, hardware). Evita optimizaciones peligrosas.
   ============================================================================ */
volatile uint8_t flag_tick = 0;     // Podría cambiar en una interrupción
uint16_t contador_global = 0;       // Variable global normal
static uint8_t privado = 42;        // 'static' con ámbito interno a este .c

/* ============================================================================
   2) STRINGS EN C
   ----------------------------------------------------------------------------
   - Un "string" en C es un array de char terminado en '\0'.
   - Evita desbordes de buffer: respeta tamaños.
   ============================================================================ */
char mensaje[32] = "Hola PIC";
const char firma[] = " - XC8";  // Constante en flash/ROM en la mayoría de PIC

/* ============================================================================
   3) OPERADORES (ARITMÉTICOS, LÓGICOS, RELACIONALES, A NIVEL DE BIT)
   ----------------------------------------------------------------------------
   - Aritméticos: + - * / %
   - Lógicos: && || !
   - Relacionales: == != < > <= >=
   - Bit: & | ^ ~ << >>
   ============================================================================ */
uint8_t ejemplo_operadores(uint8_t a, uint8_t b) {
    uint8_t r = 0;
    // Aritméticos
    uint8_t suma = a + b;
    uint8_t resta = a - b;
    uint8_t prod = a * b;
    uint8_t mod  = (b != 0) ? (a % b) : 0;

    // Relacionales / Lógicos
    bool iguales = (a == b);           // true si a y b son iguales
    bool condicion = (a > 10) && (b < 5);

    // Bits (imaginemos que 'a' representa un registro de puertos)
    r  = a | (1u << 0);   // Set bit 0
    r &= ~(1u << 1);      // Clear bit 1
    r ^= (1u << 2);       // Toggle bit 2
    r  = (r << 1);        // Desplaza a la izquierda (multiplica por 2)

    // Evitar warnings por variables no usadas (solo didáctico)
    (void)suma; (void)resta; (void)prod; (void)mod; (void)iguales; (void)condicion;
    return r;
}

/* ============================================================================
   4) FUNCIONES, PARÁMETROS (VALOR vs REFERENCIA/PUNTERO)
   ----------------------------------------------------------------------------
   - Por valor: recibe una copia; no modifica el original.
   - Por puntero (referencia): permite modificar la variable original.
   ============================================================================ */
uint16_t sumar(uint16_t x, uint16_t y) {     // por valor
    return (uint16_t)(x + y);
}

void intercambiar(int *a, int *b) {          // por puntero (modifica originales)
    int tmp = *a;
    *a = *b;
    *b = tmp;
}

/* -----------------------------------------------------------------------------
   Funciones para strings (ejemplo simple, sin printf):
   ----------------------------------------------------------------------------- */
void concat_mensaje(char *dest, size_t dest_len, const char *a, const char *b) {
    // Concatenar con seguridad: primero a, luego b, cuidando el '\0'
    if (!dest || !a || !b || dest_len == 0) return;
    dest[0] = '\0';
    strncat(dest, a, dest_len - 1);
    strncat(dest, b, dest_len - strlen(dest) - 1);
}

/* ============================================================================
   5) STRUCTS (agrupan datos relacionados) y punteros a struct
   ============================================================================ */
typedef struct {
    char     nombre[8];
    uint16_t valor_raw;
    float    escala;      // ¡en 8 bits float puede ser costoso! úsalo con criterio
} Sensor;

void sensor_init(Sensor *s, const char *nombre, float escala) {
    if (!s) return;
    strncpy(s->nombre, nombre, sizeof(s->nombre)-1);
    s->nombre[sizeof(s->nombre)-1] = '\0';
    s->valor_raw = 0;
    s->escala    = escala;
}

float sensor_leer_valor(const Sensor *s) {
    // Convierte raw a unidades físicas (ejemplo)
    return (float)s->valor_raw * s->escala;
}

/* ============================================================================
   6) PUNTEROS (a variables, a arrays y a funciones)
   ----------------------------------------------------------------------------
   - Un puntero guarda una dirección de memoria.
   - *p  : desreferencia (accede al contenido)
   - &x  : dirección de x
   - p++ : aritmética de punteros (avanza al siguiente elemento del tipo apuntado)
   ============================================================================ */
int doble_por_puntero(const int *p) {          // solo lectura
    return p ? (*p * 2) : 0;
}

void llenar_consecutivo(uint8_t *arr, size_t n) {
    if (!arr) return;
    for (size_t i = 0; i < n; ++i) arr[i] = (uint8_t)i;
}

/* ============================================================================
   7) PEQUEÑO ESTADO DE EJEMPLO (switch) y prácticas con if/while/for
   ----------------------------------------------------------------------------
   - Simulamos 3 modos de LED: APAGADO, FIJO, PARPADEO.
   - 'switch' es muy útil para máquinas de estados.
   ============================================================================ */
typedef enum { LED_OFF = 0, LED_ON = 1, LED_BLINK = 2 } LedMode;
static LedMode modo_led = LED_BLINK;

// Simulación de hardware: reemplaza estas funciones por accesos reales a puertos.
static inline void hw_led_set(bool on) {
    // EJEMPLO para 18F: TRISBbits.TRISB0 = 0; LATBbits.LATB0 = on; 
    // EJEMPLO para 16F: TRISBbits.TRISB0 = 0; PORTBbits.RB0  = on;
    (void)on; // <-- quita esto cuando escribas a tu registro real
}
static inline bool hw_boton_leer(void) {
    // EJEMPLO: return PORTBbits.RB1;
    return false; // <-- reemplaza por lectura real
}

/* Un "tick" que se llamaría, p.ej., desde una ISR de Timer (cada 1 ms) */
void systick_isr_simulada(void) {
    flag_tick = 1;  // avisamos al bucle principal que hay un "tick"
}

/* ============================================================================
   8) PROGRAMA PRINCIPAL
   ============================================================================ */
int main(void) {
    /* -------------------- Inicialización básica -------------------- */
    // Configura reloj, pines, interrupciones, UART, ADC, etc. según tu PIC.
    // TRISBbits.TRISB0 = 0;                    // LED como salida
    // TRISBbits.TRISB1 = 1;                    // Botón como entrada
    hw_led_set(false);

    /* -------------------- Variables locales -------------------- */
    uint8_t  registro = 0b00000000;       // para practicar operadores de bit
    int      a = 3, b = 7;
    int      arr_int[4] = {10, 20, 30, 40};
    int     *pA = &a;                      // puntero a int

    Sensor s1;
    sensor_init(&s1, "TEMP", 0.1f);

    // Strings
    char buffer[64];
    concat_mensaje(buffer, sizeof(buffer), mensaje, firma);   // "Hola PIC - XC8"

    /* -------------------- Operadores ejemplo -------------------- */
    registro = ejemplo_operadores(registro, 5);  // práctica de bits

    /* -------------------- Parámetros y punteros -------------------- */
    intercambiar(&a, &b);              // ahora a=7, b=3
    int doble = doble_por_puntero(pA); // doble de 'a' (7*2=14)
    (void)doble;

    /* -------------------- Arrays y punteros -------------------- */
    uint8_t tabla[16];
    llenar_consecutivo(tabla, sizeof(tabla)); // 0..15

    /* -------------------- Control de flujo: if / switch / while / for -------------------- */
    // if/else: cambio de modo con el botón (antirrebote simplificado)
    if (hw_boton_leer()) {
        // Cicla: OFF -> ON -> BLINK -> OFF ...
        modo_led = (LedMode)((modo_led + 1) % 3);
    }

    // Bucle principal (while(1))
    while (1) {
        // Espera cooperativa a un "tick" (p.ej. 1 ms). En la vida real esto vendría de un Timer ISR.
        if (!flag_tick) {
            continue;             // vuelve a checar (no bloqueante)
        }
        flag_tick = 0;            // consumimos el tick

        switch (modo_led) {
            case LED_OFF:
                hw_led_set(false);
                break;

            case LED_ON:
                hw_led_set(true);
                break;

            case LED_BLINK: {
                static uint16_t t = 0;
                t++;
                if (t % 500 == 0) {   // cada ~500 ticks: toggle
                    // Toggle por software usando una variable-bufer "registro"
                    registro ^= (1u << 0);     // invertir bit 0
                    bool estado = (registro & (1u << 0)) != 0;
                    hw_led_set(estado);
                }
            } break;
        }

        // for: ejemplo de procesamiento periódico de un array
        for (size_t i = 0; i < sizeof(tabla); ++i) {
            tabla[i] = (uint8_t)((tabla[i] + 1u) & 0x0F); // contador 0..15
        }

        // Actualiza un "sensor" ficticio
        s1.valor_raw++;
        float valor = sensor_leer_valor(&s1);
        (void)valor; // aquí podrías enviarlo por UART/mostrarlo/etc.

        /* Si tienes XC8 y definiste _XTAL_FREQ, podrías temporizar:
           __delay_ms(1);
        */
    }

    // Nunca llega aquí en un firmware típico
    // return 0;
}
