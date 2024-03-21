void setup() {
  // Inicializar la comunicación serial a una velocidad de 9600 baudios
  Serial.begin(9600);
}

void loop() {
  // Iterar a través de valores de x de 0 a 360 grados en pasos de 10 grados
  for (int x = 0; x <= 360; x += 10) {
    // Calcular el valor de y = sen(x)
    float y = sin(radians(x)); // La función sin() espera que los ángulos estén en radianes
    
    // Enviar el valor de y al puerto serial
    
    
    Serial.println(y);
    
   
    //delay(100);
  }
}
