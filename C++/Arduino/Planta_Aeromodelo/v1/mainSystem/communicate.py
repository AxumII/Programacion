import serial
import struct
import csv
import time
from datetime import datetime
import threading
import sys

# ==========================================
# CONFIGURACIÓN DEL PUERTO SERIAL
# ==========================================
PUERTO = 'COM3'      # <- CAMBIA ESTO POR TU PUERTO
BAUD_RATE = 921600   # Debe coincidir con systemConfig

# ==========================================
# HILO 1: TRANSMISIÓN DE COMANDOS (SyncMenu)
# ==========================================
def enviar_comandos(esp32_serial):
    print("\n" + "="*40)
    print(" MENÚ DE CONTROL (SyncMenu)")
    print("="*40)
    print(" Escribe un comando y presiona Enter:")
    print("  Hxx -> Giro Horario al xx% (Ej: H50)")
    print("  Axx -> Giro Antihorario al xx% (Ej: A30)")
    print("  S   -> Stop Suave (Coast)")
    print("  E   -> Paro de Emergencia (Freno)")
    print("  Z   -> Calibrar Ceros de Sensores")
    print("="*40 + "\n")
    
    while True:
        try:
            comando = input()
            if comando:
                # Enviar el comando con salto de línea (\n) tal como lo espera el ESP32
                comando_bytes = (comando + '\n').encode('ascii')
                esp32_serial.write(comando_bytes)
                
                # Borramos la línea actual y mostramos la confirmación para mantener limpia la consola
                sys.stdout.write(f"\033[A\r> Comando ejecutado: {comando.upper()} " + " "*20 + "\n")
                sys.stdout.flush()
        except EOFError:
            break
        except serial.SerialException:
            break # Si se desconecta el cable, salir del hilo

# ==========================================
# HILO PRINCIPAL: RECEPCIÓN Y DATALOGGER
# ==========================================
fecha_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
nombre_archivo = f"registro_datos_{fecha_hora}.csv"

cabeceras_csv = [
    "Timestamp_us", "PWM_Porcentaje", "Angulo_Grados", 
    "Acc_X", "Acc_Y", "Acc_Z", 
    "Gyr_X", "Gyr_Y", "Gyr_Z"
]

try:
    # Iniciar conexión serial
    esp32 = serial.Serial(PUERTO, BAUD_RATE)
    time.sleep(0.5) # Pequeña pausa para estabilizar la conexión
    print(f"Conectado a {PUERTO} a {BAUD_RATE} baudios.")
    
    # Iniciar el hilo para leer el teclado
    hilo_teclado = threading.Thread(target=enviar_comandos, args=(esp32,), daemon=True)
    hilo_teclado.start()

    # Abrir el archivo CSV
    with open(nombre_archivo, mode='w', newline='') as archivo_csv:
        escritor = csv.writer(archivo_csv)
        escritor.writerow(cabeceras_csv) 
        
        print(f"Guardando telemetría en: {nombre_archivo}")
        print("Presiona Ctrl+C para detener todo y guardar el archivo de forma segura.\n")
        
        paquetes_recibidos = 0
        tiempo_inicio = time.time()
        
        while True:
            # 1. Buscar los bytes de sincronización (0xAA y 0xBB)
            if esp32.read(1) == b'\xAA' and esp32.read(1) == b'\xBB':
                
                # 2. Leer los 37 bytes restantes del struct
                raw_data = esp32.read(37)
                
                if len(raw_data) == 37:
                    # 3. Desempaquetar los datos binarios
                    datos = struct.unpack('<I8fB', raw_data)
                    
                    timestamp = datos[0]
                    pwm = datos[1]
                    angulo = datos[2]
                    ax, ay, az = datos[3], datos[4], datos[5]
                    gx, gy, gz = datos[6], datos[7], datos[8]
                    footer = datos[9]
                    
                    # 4. Validar el byte de cierre (0xCC)
                    if footer == 0xCC:
                        escritor.writerow([timestamp, pwm, angulo, ax, ay, az, gx, gy, gz])
                        paquetes_recibidos += 1
                        
                        # 5. Imprimir estado sin saltos de línea (\r) para no ensuciar el menú de comandos
                        if paquetes_recibidos % 200 == 0:
                            sys.stdout.write(f"\r [Grabando...] Angulo: {angulo:6.2f}° | PWM: {pwm:5.1f}% | Muestras: {paquetes_recibidos}")
                            sys.stdout.flush()
                    else:
                        sys.stdout.write("\n[Advertencia] Trama corrupta omitida.\n")
                        
except KeyboardInterrupt:
    print("\n\nGrabación detenida por el usuario.")
    
except serial.SerialException as e:
    print(f"\nError de puerto serial: {e}")
    print("Revisa que el cable esté conectado y el Arduino IDE cerrado.")
    
finally:
    if 'esp32' in locals() and esp32.is_open:
        esp32.close()
        
    tiempo_total = time.time() - tiempo_inicio if 'tiempo_inicio' in locals() else 0
    frecuencia_aprox = paquetes_recibidos / tiempo_total if tiempo_total > 0 else 0
    print("\n" + "=" * 40)
    print(" RESUMEN DE CAPTURA")
    print("=" * 40)
    print(f" Archivo guardado: {nombre_archivo}")
    print(f" Total de muestras: {paquetes_recibidos}")
    print(f" Frecuencia promedio: {frecuencia_aprox:.2f} Hz")
    print("=" * 40)