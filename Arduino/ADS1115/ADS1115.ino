#include <Wire.h>
#include <Adafruit_ADS1015.h>
 
Adafruit_ADS1115 ads;

int16_t adc0, adc1, adc2, adc3;
const float multiplicador = 0.1875F;                                                              // ADS1115  @ +/- 6.144V ganancia = 0.1875mV/paso
  
void setup(void) 
{
  Serial.begin(9600);                                                                             // Iniciamos monitor serial
  //                                                  Descomentar el que interese
  // ads.setGain(GAIN_TWOTHIRDS);                                                                 // 2/3 ganancia  +/- 6.144V  1 bit = 0.1875mV (por omision)
  // ads.setGain(GAIN_ONE);                                                                       // 1x ganancia   +/- 4.096V  1 bit = 0.125mV
  // ads.setGain(GAIN_TWO);                                                                       // 2x Ganancia   +/- 2.048V  1 bit = 0.0625mV
  // ads.setGain(GAIN_FOUR);                                                                      // 4x ganancia   +/- 1.024V  1 bit = 0.03125mV
  // ads.setGain(GAIN_EIGHT);                                                                     // 8x ganancia   +/- 0.512V  1 bit = 0.015625mV
  // ads.setGain(GAIN_SIXTEEN);                                                                   // 16x ganancia  +/- 0.256V  1 bit = 0.0078125mV 
  ads.begin();                                                                                    // Iniciamos el ads1115.
}
 
void loop(void) 
{
  adc0 = ads.readADC_SingleEnded(0);                                                              // Lectura simple del canal AIN0.
  adc1 = ads.readADC_SingleEnded(1);                                                              // Lectura simple del canal AIN1.
  adc2 = ads.readADC_SingleEnded(2);                                                              // Lectura simple del canal AIN2.
  adc3 = ads.readADC_SingleEnded(3);                                                              // Lectura simple del canal AIN3.
  Serial.print("AIN0: "); Serial.print(adc0 * multiplicador);Serial.println (" mV.");             // IMprime en pantalla por el monitor serie el resultado de la lectura de AIN0.
  Serial.print("AIN1: "); Serial.print(adc1 * multiplicador);Serial.println (" mV.");             // IMprime en pantalla por el monitor serie el resultado de la lectura de AIN1.
  Serial.print("AIN2: "); Serial.print(adc2 * multiplicador);Serial.println (" mV.");             // IMprime en pantalla por el monitor serie el resultado de la lectura de AIN2.
  Serial.print("AIN3: "); Serial.print(adc3 * multiplicador);Serial.println (" mV.");             // IMprime en pantalla por el monitor serie el resultado de la lectura de AIN3.
  Serial.print("Contero: "); Serial.println(adc0);                                                // IMprime en pantalla por el monitor serie el resultado de la lectura de AIN0.
  Serial.println(" ");Serial.println(" ");Serial.println(" ");                                    // Separamos la impresion, diferenciando bloques.     
  delay(1000);                                                                                    // Pausa de 1 segundo.
}
