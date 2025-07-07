% exeDemodAnalog.m
% Ejecutable principal para demodulación

% Crear el objeto y cargar la señal
demod = DemodIIR('PruebaDemodulador.mat');

% Demodulación con bilinear
[salida110_bilineal, mezcla110_bilineal] = demodula110(demod, 'bilinear', true);
%[salida190_bilineal, mezcla190_bilineal] = demodula190(demod, 'bilinear', true);

% Demodulación con invariancia de impulso
%[salida110_impinvar, mezcla110_impinvar] = demodula110(demod, 'impinvar', true);
[salida190_impinvar, mezcla190_impinvar] = demodula190(demod, 'impinvar', true);

% === FUNCIONES LOCALES ABAJO ===
function [s2_resampled, mezcla] = demodula110(obj, typeiir, data)
    if nargin < 3, data = false; end
    fm = obj.fm1; % 110 kHz
    [s1, ~, ~, ~] = obj.firstfilter('bandpass', obj.TX, fm, typeiir, data);
    osc = obj.oscilator(fm);
    mezcla = s1 .* osc;
    [s2, ~, ~, ~] = obj.lowpass_out(mezcla, typeiir, data);
    s2_resampled = obj.samplefilter(s2);
    obj.play_sound(s2_resampled, 30e3);
end

function [s2_resampled, mezcla] = demodula190(obj, typeiir, data)
    if nargin < 3, data = false; end
    fm = obj.fm2; % 190 kHz
    [s1, ~, ~, ~] = obj.firstfilter('highpass', obj.TX, [], typeiir, data);
    osc = obj.oscilator(fm);
    mezcla = s1 .* osc;
    [s2, ~, ~, ~] = obj.lowpass_out(mezcla, typeiir, data);
    s2_resampled = obj.samplefilter(s2);
    obj.play_sound(s2_resampled, 30e3);
end
