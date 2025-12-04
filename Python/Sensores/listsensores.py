import matplotlib.pyplot as plt
from sensortable import SensorTable  # <--- más claro

DATA = DATA = {
    "temperatura": {
        "title": "Sensores de Temperatura",
        "rows": [
            {
                "Sensor": "RTD (Pt100, etc.)",
                "Precio": "Alto",
                "Rango_típico": "−200 a 600 °C",
                "Linealidad": "Alta",
                "Energía": "Pasivo",
                "Funcionamiento": "Variación de R (ohm) con la temperatura",
                "Precisión": "Alta",
                "Tipo_de_medición": "Absoluta",
                "Tipo": "Transductor",
                "Con_contacto": "Si",
                "Medida": "Resistencia eléctrica (Ω)",
                "Comentarios": "Con contacto, Muy estable, ideal industria/lab, más caro y delicado"
            },
            {
                "Sensor": "Termistor NTC",
                "Precio": "Bajo",
                "Rango_típico": "−50 a 150 °C",
                "Linealidad": "Baja",
                "Energía": "Pasivo",
                "Funcionamiento": "R(Ohm) baja al subir T(C°)",
                "Precisión": "Media",
                "Tipo_de_medición": "Absoluta",
                "Tipo": "Transductor",
                "Con_contacto": "Si",
                "Medida": "Resistencia eléctrica (Ω)",
                "Comentarios": "Con contacto, Muy sensible y barato, pero muy no lineal, inverso "
            },
            {
                "Sensor": "Termistor PTC",
                "Precio": "Bajo",
                "Rango_típico": "−50 a 150 °C",
                "Linealidad": "Baja",
                "Energía": "Pasivo",
                "Funcionamiento": "R(Ohm) sube al subir T(C°)",
                "Precisión": "Media",
                "Tipo_de_medición": "Absoluta",
                "Tipo": "Transductor",
                "Con_contacto": "Si",
                "Medida": "Resistencia eléctrica (Ω)",
                "Comentarios": "Con contacto, Útil para protección térmica o detección de sobretemperatura"
            },
            {
                "Sensor": "Termopar",
                "Precio": "Bajo",
                "Rango_típico": "−200 a 1300 °C",
                "Linealidad": "Media",
                "Energía": "Pasivo",
                "Funcionamiento": "Tensión termoeléctrica entre dos metales distintos",
                "Precisión": "Media",
                "Tipo_de_medición": "Diferencial",
                "Tipo": "Transductor",
                "Con_contacto": "Si",
                "Medida": "Tensión termoeléctrica (V)",
                "Comentarios": "Con contacto, Robusto y amplio rango, necesita compensación de unión fría"
            },
            {
                "Sensor": "Pirómetro IR",
                "Precio": "Alto",
                "Rango_típico": "−50 a 3000 °C",
                "Linealidad": "Media",
                "Energía": "Activo",
                "Funcionamiento": "Mide radiación infrarroja emitida por el objeto",
                "Precisión": "Alta",
                "Tipo_de_medición": "Absoluta aprox.",
                "Tipo": "Indicador/Transductor",
                "Con_contacto": "No",
                "Medida": "Potencia/radiancia infrarroja (W/m²)",
                "Comentarios": "Sin contacto, sensible a suciedad óptica, util en hornos"
            },
            {
                "Sensor": "Sensor IR puntual",
                "Precio": "Medio",
                "Rango_típico": "−20 a 500 °C",
                "Linealidad": "Media",
                "Energía": "Activo",
                "Funcionamiento": "Mide radiación infrarroja emitida por el objeto",
                "Precisión": "Media",
                "Tipo_de_medición": "Absoluta",
                "Tipo": "Transductor",
                "Con_contacto": "No",
                "Medida": "Potencia/radiancia infrarroja (W/m²)",
                "Comentarios": "Sin contacto, Muy usado en termómetros IR de consumo"
            },
            {
                "Sensor": "Temperatura acústica",
                "Precio": "Alto",
                "Rango_típico": "−20 a 200 °C",
                "Linealidad": "Media",
                "Energía": "Activo",
                "Funcionamiento": "Usa velocidad del sonido en un medio para estimar T",
                "Precisión": "Media",
                "Tipo_de_medición": "Absoluta",
                "Tipo": "Transductor",
                "Con_contacto": "No",
                "Medida": "Velocidad del sonido (m/s)",
                "Comentarios": "Sin contacto, util para gases ideales"
            },
            {
                "Sensor": "Piroeléctrico",
                "Precio": "Medio",
                "Rango_típico": "Cambios pequeños de T",
                "Linealidad": "Baja",
                "Energía": "Activo",
                "Funcionamiento": "genera corriente(A) al cambiar T(C°)",
                "Precisión": "Baja",
                "Tipo_de_medición": "Diferencial",
                "Tipo": "Transductor",
                "Con_contacto": "No",
                "Medida": "Corriente / carga eléctrica (A / C)",
                "Comentarios": "Sin contacto, Muy usado en detección de movimiento (PIR)"
            }
        ]
    },

    "presion": {
        "title": "Sensores de Presión",
        "rows": [
            {
                "Sensor": "Tubo de Bourdon",
                "Precio": "Medio",
                "Rango_típico": "0–1000 bar",
                "Linealidad": "Media",
                "Energía": "Pasivo",
                "Funcionamiento": "Tubo curvado se deforma por presión y mueve una aguja",
                "Precisión": "Media",
                "Tipo_de_medición": "Relativa",
                "Tipo": "Indicador",
                "Con_contacto": "Si",
                "Medida": "Presión (Pa)",
                "Comentarios": "Clásico manómetro analógico, muy robusto"
            },
            {
                "Sensor": "Diafragma mecánico",
                "Precio": "Medio",
                "Rango_típico": "0.001-500 bar",
                "Linealidad": "Media",
                "Energía": "Pasivo",
                "Funcionamiento": "Membrana se deforma con la presión",
                "Precisión": "Media",
                "Tipo_de_medición": "Absoluta/relativa",
                "Tipo": "Indicador/Transductor",
                "Con_contacto": "Si",
                "Medida": "Deformación mecánica (strain)",
                "Comentarios": "Base de muchos transmisores industriales"
            },
            {
                "Sensor": "Manómetro en U",
                "Precio": "Bajo",
                "Rango_típico": "1-10 bar",
                "Linealidad": "Alta",
                "Energía": "Pasivo",
                "Funcionamiento": "Diferencia de alturas de fluido en tubo en U",
                "Precisión": "Alta",
                "Tipo_de_medición": "Diferencial",
                "Tipo": "Indicador",
                "Con_contacto": "Si",
                "Medida": "Diferencia de altura de columna (m)",
                "Comentarios": "Barato y rustico"
            },
            {
                "Sensor": "Barómetro",
                "Precio": "Medio",
                "Rango_típico": "800–1100 mbar",
                "Linealidad": "Alta",
                "Energía": "Pasivo",
                "Funcionamiento": "Mide presión atmosférica",
                "Precisión": "Alta",
                "Tipo_de_medición": "Absoluta",
                "Tipo": "Indicador/Transductor",
                "Con_contacto": "Si",
                "Medida": "Presión atmosférica (Pa)",
                "Comentarios": "Meteorología y compensación de altitud"
            },
            {
                "Sensor": "Transducción por fuerza/contacto (galgas)",
                "Precio": "Medio",
                "Rango_típico": "0.001-500 bar",
                "Linealidad": "Alta",
                "Energía": "Pasivo",
                "Funcionamiento": "Es una galga",
                "Precisión": "Alta",
                "Tipo_de_medición": "Diferencial/relativa/absoluta",
                "Tipo": "Transductor",
                "Con_contacto": "Si",
                "Medida": "Deformación mecánica (strain)",
                "Comentarios": "Permite una facil digitalizacion, correcciones faciles"
            }
        ]
    },

    "flujo": {
        "title": "Sensores de Flujo",
        "rows": [
            {
                "Sensor": "Vortex",
                "Precio": "Medio",
                "Rango_típico": "50-5000 L/min",
                "Linealidad": "Media-Alta",
                "Energía": "Activo",
                "Funcionamiento": "Cuenta vortices y trasduce a velocidad del fluido",
                "Precisión": "Media",
                "Tipo_de_medición": "Absoluta",
                "Tipo": "Transductor",
                "Con_contacto": "Si",
                "Medida": "Frecuencia de vórtices (Hz)",
                "Comentarios": "Util en gases, requiere velocidad mínima y vortices"
            },
            {
                "Sensor": "Coriolis",
                "Precio": "Alto",
                "Rango_típico": "1-200 mL/min",
                "Linealidad": "Alta",
                "Energía": "Activo",
                "Funcionamiento": "Mide masa/tiempo(kg/s) desde vibracion(Hz)",
                "Precisión": "Muy alta",
                "Tipo_de_medición": "Absoluta",
                "Tipo": "Transductor",
                "Con_contacto": "Si",
                "Medida": "Desfase / torsión de tubos vibrantes (s / rad)",
                "Comentarios": "Caro, sensible a vibraciones externas"
            },
            {
                "Sensor": "Pitot",
                "Precio": "Bajo",
                "Rango_típico": "1–100000 L/min",
                "Linealidad": "Media",
                "Energía": "Pasivo",
                "Funcionamiento": "Diferencia de presiones a velocidad del fluido",
                "Precisión": "Media",
                "Tipo_de_medición": "Diferencial",
                "Tipo": "Transductor",
                "Con_contacto": "Si",
                "Medida": "Presión dinámica (Pa)",
                "Comentarios": "Simple y barato, sensible a alineación y suciedad"
            },
            {
                "Sensor": "Venturi / Placa / Tobera (ΔP)",
                "Precio": "Medio",
                "Rango_típico": "1–6000 L/min",
                "Linealidad": "Media",
                "Energía": "Pasivo",
                "Funcionamiento": "Restricción de area genera caída de presión proporcional al flujo",
                "Precisión": "Media",
                "Tipo_de_medición": "Diferencial",
                "Tipo": "Transductor",
                "Con_contacto": "Si",
                "Medida": "Caída de presión ΔP (Pa)",
                "Comentarios": "Muy usado en industria, requiere tramo recto y calibración"
            },
            {
                "Sensor": "Ultrasónico (tiempo de tránsito)",
                "Precio": "Alto",
                "Rango_típico": "1–5000 L/min",
                "Linealidad": "Alta",
                "Energía": "Activo",
                "Funcionamiento": "Mide diferencia de tiempo de viaje de pulsos ultrasónicos (Doppler)",
                "Precisión": "Alta",
                "Tipo_de_medición": "Absoluta",
                "Tipo": "Transductor",
                "Con_contacto": "No",
                "Medida": "Tiempo de tránsito ultrasónico (s)",
                "Comentarios": "Sin contacto, sensible a ruidos"
            }
        ]
    },

    "nivel": {
        "title": "Sensores de Nivel",
        "rows": [
            {
                "Sensor": "Ultrasónico",
                "Precio": "Medio-Alto",
                "Rango_típico": "0.05–20 m",
                "Linealidad": "Media",
                "Energía": "Activo",
                "Funcionamiento": "Tiempo de vuelo de pulso ultrasónico hasta superficie",
                "Precisión": "Media",
                "Tipo_de_medición": "Absoluta",
                "Tipo": "Transductor",
                "Con_contacto": "No",
                "Medida": "Tiempo de vuelo (s)",
                "Comentarios": "Sin contacto, afectado por espuma y ecos falsos"
            },
            {
                "Sensor": "Infrarrojo",
                "Precio": "Bajo",
                "Rango_típico": "Puntos de nivel",
                "Linealidad": "NA",
                "Energía": "Activo",
                "Funcionamiento": "Emisión/recepción IR cambia con presencia de líquido",
                "Precisión": "Media",
                "Tipo_de_medición": "Absoluta",
                "Tipo": "Transductor",
                "Con_contacto": "No",
                "Medida": "Intensidad/reflexión de luz IR (W/m²)",
                "Comentarios": "Sin contacto, Interruptor de nivel"
            },
            {
                "Sensor": "Presión hidrostática",
                "Precio": "Medio",
                "Rango_típico": "0-50 m",
                "Linealidad": "Alta",
                "Energía": "Pasivo",
                "Funcionamiento": "Peso de columna de fluido sobre sensor de presión (galga)",
                "Precisión": "Alta",
                "Tipo_de_medición": "Absoluta",
                "Tipo": "Transductor",
                "Con_contacto": "Si",
                "Medida": "Presión (Pa)",
                "Comentarios": "Muy usado en tanques, depende de densidad del fluido"
            },
            {
                "Sensor": "Capacitivo",
                "Precio": "Medio",
                "Rango_típico": "0.01-50 m",
                "Linealidad": "Media",
                "Energía": "Activo",
                "Funcionamiento": "Cambio de capacitancia entre electrodo y pared/sonda",
                "Precisión": "Media",
                "Tipo_de_medición": "Absoluta",
                "Tipo": "Transductor",
                "Con_contacto": "Si",
                "Medida": "Capacitancia (F)",
                "Comentarios": "Sirve para sólidos y líquidos, sensible a suciedad"
            },
            {
                "Sensor": "Resistivo (boya/potenciómetro)",
                "Precio": "Bajo",
                "Rango_típico": "0.01-2 m",
                "Linealidad": "Baja-Media",
                "Energía": "Pasivo",
                "Funcionamiento": "Flotador mueve una resistencia/potenciómetro",
                "Precisión": "Media",
                "Tipo_de_medición": "Absoluta",
                "Tipo": "Transductor/Indicador",
                "Con_contacto": "Si",
                "Medida": "Resistencia eléctrica (Ω)",
                "Comentarios": "Barato, pero con desgaste mecánico"
            }
        ]
    },

    "fuerza": {
        "title": "Sensores de Fuerza",
        "rows": [
            {
                "Sensor": "Galga extensiométrica",
                "Precio": "Medio",
                "Rango_típico": "1-10000 N",
                "Linealidad": "Alta",
                "Energía": "Pasivo",
                "Funcionamiento": "Resistencia cambia con deformación mecánica",
                "Precisión": "Alta",
                "Tipo_de_medición": "Diferencial",
                "Tipo": "Transductor",
                "Con_contacto": "Si",
                "Medida": "Resistencia eléctrica en puente de galgas (Ω)",
                "Comentarios": "Base de celdas de carga, requiere buen acondicionamiento"
            },
            {
                "Sensor": "FSR",
                "Precio": "Bajo",
                "Rango_típico": "20-100 N",
                "Linealidad": "Baja",
                "Energía": "Pasivo",
                "Funcionamiento": "Resistencia cambia con presión aplicada (piezoresistivo)",
                "Precisión": "Baja",
                "Tipo_de_medición": "Relativa",
                "Tipo": "Transductor",
                "Con_contacto": "Si",
                "Medida": "Resistencia eléctrica (Ω)",
                "Comentarios": "Muy barato, no lineal, deriva con el tiempo"
            },

        ]
    },


    "aceleracion_lineal": {
        "title": "Sensores de Aceleración Lineal",
        "rows": [
            {
                "Sensor": "IMU",
                "Precio": "Medio",
                "Rango_típico": "±2–200 g",
                "Linealidad": "Media",
                "Energía": "Activo",
                "Funcionamiento": "Combina acelerómetros y giróscopos",
                "Precisión": "Media-Alta",
                "Tipo_de_medición": "Absoluta (orientación integrada)",
                "Tipo": "Transductor",
                "Con_contacto": "Si",
                "Medida": "Aceleración lineal (m/s²) y velocidad angular (rad/s)",
                "Comentarios": "Ideal para robótica/drones, necesita fusión de sensores"
            },
            {
            "Sensor": "Acelerómetro MEMS capacitivo",
            "Precio": "Bajo",
            "Rango_típico": "±2–200 g",
            "Linealidad": "Alta",
            "Energía": "Activo",
            "Funcionamiento": "Una masa MEMS modifica la capacitancia entre placas al acelerarse, Masa-Resorte",
            "Precisión": "Alta",
            "Tipo_de_medición": "Absoluta",
            "Tipo": "Transductor",
            "Con_contacto": "Si",
            "Medida": "Cambio de capacitancia (F)",
            "Comentarios": "El más común; bueno en baja frecuencia y DC; sensible a temperatura"
        },
        {
            "Sensor": "Acelerómetro piezoeléctrico",
            "Precio": "Medio",
            "Rango_típico": "±500–10000 g",
            "Linealidad": "Alta",
            "Energía": "Activo",
            "Funcionamiento": "Un cristal piezoeléctrico genera carga al ser acelerado y cambiar la oscilacion",
            "Precisión": "Muy alta en dinámico",
            "Tipo_de_medición": "Diferencial (cambios)",
            "Tipo": "Transductor",
            "Con_contacto": "Si",
            "Medida": "Carga eléctrica (C) o tensión (V)",
            "Comentarios": "Excelente para vibraciones; no mide estatico; ideal en máquinas rotativas"
        },
        {
            "Sensor": "Acelerómetro piezoresistivo",
            "Precio": "Medio",
            "Rango_típico": "±50–6000 g",
            "Linealidad": "Alta",
            "Energía": "Activo",
            "Funcionamiento": "Una masa flexiona un elemento con galgas piezoresistivas",
            "Precisión": "Alta",
            "Tipo_de_medición": "Absoluta",
            "Tipo": "Transductor",
            "Con_contacto": "Si",
            "Medida": "Cambio resistivo (Ω)",
            "Comentarios": "Sirve para DC y choques; usado en crash-tests y altas aceleraciones"
        },
        {
            "Sensor": "Acelerómetro basado en galgas",
            "Precio": "Medio",
            "Rango_típico": "±10–2000 g",
            "Linealidad": "Alta",
            "Energía": "Pasivo",
            "Funcionamiento": "Un resorte o viga con galgas mide la deformación causada por aceleración",
            "Precisión": "Alta",
            "Tipo_de_medición": "Absoluta",
            "Tipo": "Transductor",
            "Con_contacto": "Si",
            "Medida": "Strain (µε)",
            "Comentarios": "Muy robusto; ideal en ambientes industriales pesados; buen desempeño en DC"
        }
        ]
    },


    "distancia": {
        "title": "Sensores de Distancia / Desplazamiento Lineal",
        "rows": [
            {
                "Sensor": "LVDT",
                "Precio": "Alto",
                "Rango_típico": "0.5–300 mm",
                "Linealidad": "Alta",
                "Energía": "Activo",
                "Funcionamiento": "Transformador diferencial con núcleo móvil",
                "Precisión": "Muy alta",
                "Tipo_de_medición": "Absoluta",
                "Tipo": "Transductor",
                "Con_contacto": "Si",
                "Medida": "Tensión AC diferencial proporcional al desplazamiento (V)",
                "Comentarios": "Muy preciso y robusto, requiere excitación AC"
            },
            {
                "Sensor": "Ultrasónico (ToF)",
                "Precio": "Bajo-Medio",
                "Rango_típico": "20–5000 mm",
                "Linealidad": "Media",
                "Energía": "Activo",
                "Funcionamiento": "Calcula distancia midiendo tiempo de vuelo de un pulso ultrasónico",
                "Precisión": "Media",
                "Tipo_de_medición": "Absoluta",
                "Tipo": "Transductor",
                "Con_contacto": "No",
                "Medida": "Tiempo de vuelo del sonido (s)",
                "Comentarios": "Sin contacto; sensible a temperatura, ángulo y absorción; muy usado en robótica"
            },
            {
                "Sensor": "Infrarrojo por triangulación",
                "Precio": "Bajo",
                "Rango_típico": "100–800 mm",
                "Linealidad": "Baja-Media",
                "Energía": "Activo",
                "Funcionamiento": "Un LED IR y un fotodiodo determinan distancia por ángulo reflejado",
                "Precisión": "Media",
                "Tipo_de_medición": "Absoluta",
                "Tipo": "Transductor",
                "Con_contacto": "No",
                "Medida": "Intensidad/ángulo de reflexión (W/m² / rad)",
                "Comentarios": "Barato; no lineal; afecta el color del objeto; muy usado en robótica"
            },
            {
                "Sensor": "Infrarrojo ToF (LIDAR corto alcance)",
                "Precio": "Medio",
                "Rango_típico": "5–2000 mm",
                "Linealidad": "Alta",
                "Energía": "Activo",
                "Funcionamiento": "Mide tiempo real de vuelo de un pulso IR modulada (ToF)",
                "Precisión": "Alta",
                "Tipo_de_medición": "Absoluta",
                "Tipo": "Transductor",
                "Con_contacto": "No",
                "Medida": "Tiempo de vuelo de luz IR (s)",
                "Comentarios": "Muy preciso; independiente del color; usado en teléfonos, robots y escáneres 3D"
            }
        ]
    },
    
    "angulo": {
        "title": "Sensores de Ángulo / Posición Angular",
        "rows": [
            {
                "Sensor": "Encoder incremental",
                "Precio": "Bajo-Medio",
                "Rango_típico": "0–360° (1 vuelta)",
                "Linealidad": "Alta",
                "Energía": "Activo",
                "Funcionamiento": "Disco ranurado y fotodiodo generan pulsos al girar",
                "Precisión": "Alta (según PPR)",
                "Tipo_de_medición": "Relativa (incremental)",
                "Tipo": "Transductor",
                "Con_contacto": "No",
                "Medida": "Pulsos digitales por revolución (cuentas/rev)",
                "Comentarios": "Necesita referencia de cero (homing); resolución típica 100–10 000 PPR, requiere disco"
            },
            {
                "Sensor": "Encoder absoluto",
                "Precio": "Medio-Alto",
                "Rango_típico": "0–360° (1 vuelta)",
                "Linealidad": "Alta",
                "Energía": "Activo",
                "Funcionamiento": "Disco con patrón codificado genera una palabra digital única para cada ángulo",
                "Precisión": "Muy alta (según bits)",
                "Tipo_de_medición": "Absoluta",
                "Tipo": "Transductor",
                "Con_contacto": "No",
                "Medida": "Código digital de posición angular (bits)",
                "Comentarios": "No necesita ref; resolución típica 8–20 bits (256–1 048 576 posiciones), requiere disco"
            },
            {
                "Sensor": "Encoder de cuadratura",
                "Precio": "Bajo-Medio",
                "Rango_típico": "0–360° (1 vuelta)",
                "Linealidad": "Alta",
                "Energía": "Activo",
                "Funcionamiento": "Dos señales desfasadas permiten determinar sentido y multiplicar resolución",
                "Precisión": "Alta",
                "Tipo_de_medición": "Relativa",
                "Tipo": "Transductor",
                "Con_contacto": "No",
                "Medida": "Pulsos digitales en cuadratura (cuentas/rev ×4)",
                "Comentarios": "Resolución 4× mayor que un incremental estándar; muy usado en CNC y servomotores"
            },
            {
                "Sensor": "Encoder magnético Hall",
                "Precio": "Bajo-Medio",
                "Rango_típico": "0–360° (1 vuelta)",
                "Linealidad": "Media-Alta",
                "Energía": "Activo",
                "Funcionamiento": "Un imán giratorio altera el flujo magnético; sensores Hall miden sus componentes y calculan el ángulo",
                "Precisión": "Alta ",
                "Tipo_de_medición": "Absoluta",
                "Tipo": "Transductor",
                "Con_contacto": "No",
                "Medida": "Campo magnético Bx y By (tesla)",
                "Comentarios": "Robusto, inmune a suciedad; resoluciones típicas 10–14 bits; ideal para motores BLDC, robótica y servos, requeire disco"
            }

        ]
    },

    "velocidad_angular": {
        "title": "Sensores de Velocidad Angular",
        "rows": [
            {
                "Sensor": "Giroscopio MEMS",
                "Precio": "Medio",
                "Rango_típico": "±125–2000 °/s",
                "Linealidad": "Alta",
                "Energía": "Activo",
                "Funcionamiento": "Detecta la fuerza de Coriolis sobre una masa vibrante para inferir velocidad angular",
                "Precisión": "Alta",
                "Tipo_de_medición": "Absoluta",
                "Tipo": "Transductor",
                "Con_contacto": "No",
                "Medida": "Fuerza de Coriolis o variación capacitiva proporcional",
                "Comentarios": "Muy usado en drones y estabilización"
            },
            {
                "Sensor": "IMU",
                "Precio": "Medio",
                "Rango_típico": "±2–200 g, ±250–2000 °/s",
                "Linealidad": "Media",
                "Energía": "Activo",
                "Funcionamiento": "Combina acelerómetros y giróscopos (y a veces compás)",
                "Precisión": "Media-Alta",
                "Tipo_de_medición": "Absoluta (orientación integrada)",
                "Tipo": "Transductor",
                "Con_contacto": "Si",
                "Medida": "Velocidad angular (rad/s) y aceleración lineal (m/s²)",
                "Comentarios": "Ideal para robótica/drones, necesita fusión de sensores"
            }
        ]
    }

}



def tabla():
    tables: dict[str, SensorTable] = {}

    # Crear un SensorTable por cada magnitud física
    for key, cfg in DATA.items():
        tables[key] = SensorTable(
            title=cfg["title"],
            info_rows=cfg["rows"]    # <--- nombre correcto del parámetro
        )

    # Mostrar todas las tablas
    for table in tables.values():
        table.show()

    plt.show()


tabla()