classdef DemodIIR
    properties
        TX      % Vector de la señal recibida
        fs = 500e3  % Frecuencia de muestreo (Hz), fija en 500 kHz por defecto
        tiempo  % Vector de tiempo correspondiente
        fm1 = 110e3 % Frecuencia de modulacion 1 (Hz)
        fm2 = 190e3 % Frecuencia de modulacion 2 (Hz)
    end

    methods
        % Constructor
        function obj = DemodIIR(input)
            if nargin > 0
                if ischar(input) || isstring(input)
                    data = load(input);
                    fn = fieldnames(data);
                    for k = 1:length(fn)
                        v = data.(fn{k});
                        if isvector(v)
                            obj.TX = v(:);
                            break;
                        end
                    end
                else
                    obj.TX = input(:);
                end
                obj.tiempo = (0:length(obj.TX)-1) / obj.fs;
            end
        end

        % Filtro Inicial
        function [filter_signal1, b, a, orden] = firstfilter(obj, typeband, signal, fm, typeiir, data)
            if nargin < 6, data = false; end
            if strcmpi(typeband, 'bandpass')
                [filter_signal1, b, a, orden] = obj.bandpass(fm, signal, typeiir, data);
            elseif strcmpi(typeband, 'highpass')
                [filter_signal1, b, a, orden] = obj.highpass(signal, typeiir, data);
            else
                error('Tipo de filtro no reconocido. Usa ''bandpass'' o ''highpass''.');
            end
        end

        % Oscilador Sintonizable
        function osc_signal = oscilator(obj, fm)
            osc_signal = cos(2*pi*fm*obj.tiempo);
            osc_signal = osc_signal(:);
        end

        % Pasabajos Salida
        function [y, b, a, orden] = lowpass_out(obj, signal, typeiir, data)
            if nargin < 4, data = false; end
            fs = obj.fs;
            fp = 15e3;   fsb = 40e3;
            Rp = 3;      Rs = 15;
            Wp = 2*pi*fp;
            Ws = 2*pi*fsb;

            [orden, Wn] = buttord(Wp, Ws, Rp, Rs, 's');
            [ban, aan] = butter(orden, Wn, 'low', 's');

            if strcmpi(typeiir, 'bilinear')
                [b, a] = bilinear(ban, aan, fs);
                metodo = 'Bilineal';
            elseif strcmpi(typeiir, 'impinvar')
                [b, a] = impinvar(ban, aan, fs);
                metodo = 'Invariancia al Impulso';
            else
                error('El argumento typeiir debe ser ''bilinear'' o ''impinvar''');
            end

            y = filter(b, a, signal);

            if data
                disp(['----- Filtro Pasabajos Butterworth (' metodo ') -----']);
                disp(['Orden: ', num2str(orden)]);
                disp(['Wn (rad/seg): ', num2str(Wn)]);
                disp('Coeficientes b:'); disp(b);
                disp('Coeficientes a:'); disp(a);
                sysd = tf(b, a, 1/fs);
                disp('Función de transferencia digital H(z):');
                sysd

                figure; bode(sysd); grid on;
                title(['Bode digital (H(z)) - ' metodo]);

                figure; freqz(b, a, 2048, fs);
                title(['Respuesta en frecuencia digital - ' metodo]);

                Nfft = 2^nextpow2(length(signal));
                f = fs*(0:Nfft/2-1)/Nfft;
                S_in  = abs(fft(signal, Nfft));     S_in  = S_in(1:Nfft/2);
                S_out = abs(fft(y,      Nfft));     S_out = S_out(1:Nfft/2);

                figure;
                plot(f/1e3, S_in/max(S_in), 'b', 'LineWidth',1.2); hold on;
                plot(f/1e3, S_out/max(S_out), 'r', 'LineWidth',1.2);
                xlabel('Frecuencia [kHz]'); ylabel('Magnitud normalizada');
                legend('Entrada','Salida'); title(['Espectro señal (entrada y salida) - ' metodo]);
                grid on;
            end
        end

        % Remuestreo
        function resample_signal = samplefilter(obj, signal)
            fs_in = obj.fs;
            fs_out = 30e3;
            [P, Q] = rat(fs_out / fs_in, 1e-12);
            resample_signal = resample(signal, P, Q);
        end

        % Filtro Pasabanda
        function [y, b, a, orden] = bandpass(obj, fc, signal, typeiir, data)
            if nargin < 5, data = false; end
            fs = obj.fs;
            fp1 = fc - 15e3;   fp2 = fc + 15e3;
            fs1 = fc - 40e3;   fs2 = fc + 40e3;
            Wp = [2*pi*fp1, 2*pi*fp2];
            Ws = [2*pi*fs1, 2*pi*fs2];
            Rp = 3; Rs = 15;

            [orden, Wn] = buttord(Wp, Ws, Rp, Rs, 's');
            [ban, aan] = butter(orden, Wn, 'bandpass', 's');

            if strcmpi(typeiir, 'bilinear')
                [b, a] = bilinear(ban, aan, fs);
                metodo = 'Bilineal';
            elseif strcmpi(typeiir, 'impinvar')
                [b, a] = impinvar(ban, aan, fs);
                metodo = 'Invariancia al Impulso';
            else
                error('typeiir debe ser ''bilinear'' o ''impinvar''');
            end

            y = filter(b, a, signal);

            if data
                disp(['----- Filtro Pasabanda Butterworth (' metodo ') -----']);
                disp(['Orden: ', num2str(orden)]);
                disp(['Wn (rad/seg): ', num2str(Wn)]);
                disp('Coeficientes b:'); disp(b);
                disp('Coeficientes a:'); disp(a);
                sysd = tf(b, a, 1/fs);
                disp('Función de transferencia digital H(z):');
                sysd

                figure; bode(sysd); grid on;
                title(['Bode digital (H(z)) - ' metodo]);

                figure; freqz(b, a, 2048, fs);
                title(['Respuesta en frecuencia digital - ' metodo]);

                Nfft = 2^nextpow2(length(signal));
                f = fs*(0:Nfft/2-1)/Nfft;
                S_in  = abs(fft(signal, Nfft));     S_in  = S_in(1:Nfft/2);
                S_out = abs(fft(y,      Nfft));     S_out = S_out(1:Nfft/2);

                figure;
                plot(f/1e3, S_in/max(S_in), 'b', 'LineWidth',1.2); hold on;
                plot(f/1e3, S_out/max(S_out), 'r', 'LineWidth',1.2);
                xlabel('Frecuencia [kHz]'); ylabel('Magnitud normalizada');
                legend('Entrada','Salida'); title(['Espectro señal (entrada y salida) - ' metodo]);
                grid on;
            end
        end

        % Filtro Pasaaltos
        function [y, b, a, orden] = highpass(obj, signal, typeiir, data)
            if nargin < 4, data = false; end
            fs = obj.fs;
            fp = 175e3;   fsb = 150e3;
            Rp = 3;       Rs = 15;
            Wp = 2*pi*fp; Ws = 2*pi*fsb;

            [orden, Wn] = buttord(Wp, Ws, Rp, Rs, 's');
            [ban, aan] = butter(orden, Wn, 'high', 's');

            if strcmpi(typeiir, 'bilinear')
                [b, a] = bilinear(ban, aan, fs);
                metodo = 'Bilineal';
            elseif strcmpi(typeiir, 'impinvar')
                [b, a] = impinvar(ban, aan, fs);
                metodo = 'Invariancia al Impulso';
            else
                error('typeiir debe ser ''bilinear'' o ''impinvar''');
            end

            y = filter(b, a, signal);

            if data
                disp(['----- Filtro Pasaaltos Butterworth (' metodo ') -----']);
                disp(['Orden: ', num2str(orden)]);
                disp(['Wn (rad/seg): ', num2str(Wn)]);
                disp('Coeficientes b:'); disp(b);
                disp('Coeficientes a:'); disp(a);
                sysd = tf(b, a, 1/fs);
                disp('Función de transferencia digital H(z):');
                sysd

                figure; bode(sysd); grid on;
                title(['Bode digital (H(z)) - ' metodo]);

                figure; freqz(b, a, 2048, fs);
                title(['Respuesta en frecuencia digital - ' metodo]);

                Nfft = 2^nextpow2(length(signal));
                f = fs*(0:Nfft/2-1)/Nfft;
                S_in  = abs(fft(signal, Nfft));     S_in  = S_in(1:Nfft/2);
                S_out = abs(fft(y,      Nfft));     S_out = S_out(1:Nfft/2);

                figure;
                plot(f/1e3, S_in/max(S_in), 'b', 'LineWidth',1.2); hold on;
                plot(f/1e3, S_out/max(S_out), 'r', 'LineWidth',1.2);
                xlabel('Frecuencia [kHz]'); ylabel('Magnitud normalizada');
                legend('Entrada','Salida'); title(['Espectro señal (entrada y salida) - ' metodo]);
                grid on;
            end
        end

        % Método para reproducir sonido (usa sound de Matlab)
        function play_sound(obj, signal, fs_audio)
            signal = signal / max(abs(signal));
            sound(signal, fs_audio);
        end
    end
end
