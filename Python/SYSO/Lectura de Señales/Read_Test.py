import serial




baudios = 9600
# Configura el puerto serial
ser = serial.Serial('COM7', baudios)  # Reemplaza 'COM7' con tu puerto serial y ajusta la velocidad (baud rate) según sea necesario

try:
    while True:
        # Lee una línea de datos desde el puerto serial
        line = ser.readline().decode('utf-8').strip()
        
        # Muestra la línea de datos en la consola
        print(line)

except KeyboardInterrupt:
    # Maneja la interrupción del teclado (Ctrl+C)
    print("Lectura del puerto serial detenida.")

finally:
    # Cierra el puerto serial al finalizar
    ser.close()
