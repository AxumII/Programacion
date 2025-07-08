% exeDemodAnalog.m
% Ejecutable principal: demodula y grafica TODOS los espectros etapa‑por‑etapa

close all; clc;

demod = DemodAnalog('PruebaDemodulador.mat');

% Canal 1 : 110 kHz (con gráficos)
%[salida110, mezcla110] = demodula110(demod,true);

% Canal 2 : 190 kHz (descomenta si quieres los dos canales)
[salida190, mezcla190] = demodula190(demod,true);


%% --------------- FUNCIONES LOCALES ---------------

function plotSpec(sig, fs, ttl, col)
%  Pequeña utilidad para no repetir código
    N   = 2^nextpow2(length(sig));
    f   = fs*(0:N/2-1)/N;
    S   = abs(fft(sig, N));  S = S(1:N/2);
    figure; plot(f/1e3, S/max(S), col,'LineWidth',1.2);
    xlabel('Frecuencia [kHz]'); ylabel('Magnitud normalizada');
    title(ttl);  grid on;
end


function [s2_resampled, mezcla] = demodula110(obj, data)
    if nargin < 2, data = false; end
    fs = obj.fs;         % 500 kHz
    fm = obj.fm1;        % 110 kHz

    % ------------------ Espectro entrada ------------------
    if data, plotSpec(obj.TX,fs,'Canal 1: Espectro señal de entrada','k'); end

    % 1) Filtro Pasabanda analógico
    [s1, ~, ~, ~] = obj.firstfilter('bandpass', obj.TX, fm, data);
    if data, plotSpec(s1,fs,'Canal 1: Después del pasabanda','b'); end

    % 2) Oscilador
    osc = obj.oscilator(fm);
    if data, plotSpec(osc,fs,'Canal 1: Espectro oscilador','g'); end

    % 3) Mezcla
    mezcla = s1 .* osc;
    if data, plotSpec(mezcla,fs,'Canal 1: Señal mezclada','m'); end

    % 4) Pasabajos analógico
    [s2, ~, ~, ~] = obj.lowpass_out(mezcla, data);
    if data, plotSpec(s2,fs,'Canal 1: Después del pasabajos','r'); end

    % 5) Remuestreo a 30 kHz
    s2_resampled = obj.samplefilter(s2);
    if data, plotSpec(s2_resampled,30e3,'Canal 1: Señal resampleada 30 kHz','c'); end

    % 6) Reproducir audio
    obj.play_sound(s2_resampled,30e3);
end


function [s2_resampled, mezcla] = demodula190(obj, data)
    if nargin < 2, data = false; end
    fs = obj.fs;
    fm = obj.fm2;        % 190 kHz

    if data, plotSpec(obj.TX,fs,'Canal 2: Espectro señal de entrada','k'); end

    % 1) Filtro Pasaaltos analógico
    [s1, ~, ~, ~] = obj.firstfilter('highpass', obj.TX, [], data);
    if data, plotSpec(s1,fs,'Canal 2: Después del pasaaltos','b'); end

    % 2) Oscilador
    osc = obj.oscilator(fm);
    if data, plotSpec(osc,fs,'Canal 2: Espectro oscilador','g'); end

    % 3) Mezcla
    mezcla = s1 .* osc;
    if data, plotSpec(mezcla,fs,'Canal 2: Señal mezclada','m'); end

    % 4) Pasabajos analógico
    [s2, ~, ~, ~] = obj.lowpass_out(mezcla, data);
    if data, plotSpec(s2,fs,'Canal 2: Después del pasabajos','r'); end

    % 5) Remuestreo a 30 kHz
    s2_resampled = obj.samplefilter(s2);
    if data, plotSpec(s2_resampled,30e3,'Canal 2: Señal resampleada 30 kHz','c'); end

    obj.play_sound(s2_resampled,30e3);
end
