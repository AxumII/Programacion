# Reemplaza la función enviar_comandos en tu communicate.py con esta:
def enviar_comandos(esp32_serial):
    print("\n" + "="*40)
    print(" MENÚ DE CONTROL Y PID (SyncMenu)")
    print("="*40)
    print(" Escribe un comando y presiona Enter:")
    print("  Pxx,yy -> PID: Ir a xx° con yy% PWM máx (Ej: P90,50 o P45)")
    print("  Hxx    -> MANUAL: Giro Horario xx% (Ej: H50)")
    print("  Axx    -> MANUAL: Giro Antihorario xx%")
    print("  S      -> Stop Suave (Apaga PID y motor)")
    print("  E      -> Paro de Emergencia (Freno)")
    print("  Z      -> Calibrar Ceros de Sensores")
    print("="*40 + "\n")
    
    while True:
        try:
            comando = input()
            if comando:
                comando_bytes = (comando + '\n').encode('ascii')
                esp32_serial.write(comando_bytes)
                sys.stdout.write(f"\033[A\r> Comando ejecutado: {comando.upper()} " + " "*20 + "\n")
                sys.stdout.flush()
        except EOFError:
            break
        except serial.SerialException:
            break