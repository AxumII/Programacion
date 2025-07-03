% Parámetros
fs = 1000;            % Frecuencia de muestreo (Hz)
fc = 100;             % Frecuencia de corte (Hz)
order = 4;            % Orden del filtro

% Diseño del filtro Butterworth pasabajo
[b, a] = butter(order, fc/(fs/2), 'low');
freqz(b, a, 512, fs); % Mostrar respuesta en frecuencia
title('Respuesta en frecuencia del filtro pasabajo');
 
% Crear la señal de prueba
t = 0:0.2/fs:0.2;                        % Tiempo de 1 segundo
signal_low = sin(2*pi*50*t);        % Componente de baja frecuencia
signal_high = sin(2*pi*3000*t);      % Componente de alta frecuencia
signal = signal_low + signal_high;  % Señal compuesta

% Mostrar la señal original
figure;
plot(t, signal);
title('Señal original (50 Hz + 300 Hz)');
xlabel('Tiempo (s)');
ylabel('Amplitud');


% Aplicar el filtro pasabajo
filtered_signal = filter(b, a, signal);

% Mostrar la señal filtrada
figure;
plot(t, filtered_signal);
title('Señal después del filtro pasabajo');
xlabel('Tiempo (s)');
ylabel('Amplitud');

n = length(signal);
f = linspace(0, fs, n);

% FFT de señales
S_orig = abs(fft(signal));
S_filt = abs(fft(filtered_signal));

% Mostrar espectro
figure;
plot(f, S_orig, 'b', f, S_filt, 'r');
legend('Original', 'Filtrada');
xlim([0 fs/2]);
xlabel('Frecuencia (Hz)');
ylabel('Magnitud');
title('Espectro de frecuencia');
