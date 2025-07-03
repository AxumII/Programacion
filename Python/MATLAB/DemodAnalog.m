classdef DemodAnalog
    properties
        TX
        fs = 500e3                 % Frecuencia de muestreo (Hz)
        tiempo                     % Vector de tiempo (s)
        fm1 = 110e3                % Frecuencia de modulación 1
        fm2 = 190e3                % Frecuencia de modulación 2
    end

    methods
        %% -------- Constructor --------
        function obj = DemodAnalog(input)
            if nargin > 0
                if ischar(input) || isstring(input)
                    data = load(input);
                    fn = fieldnames(data);
                    for k = 1:numel(fn)
                        v = data.(fn{k});
                        if isvector(v), obj.TX = v(:); break; end
                    end
                else
                    obj.TX = input(:);
                end
                obj.tiempo = (0:length(obj.TX)-1).' / obj.fs;
            end
        end

        %% ------ Filtro inicial -------
        function [y,b,a,orden] = firstfilter(obj,typeband,signal,fm,data)
            if nargin < 5, data = false; end
            switch lower(typeband)
                case 'bandpass', [y,b,a,orden] = obj.bandpass(fm,signal,data);
                case 'highpass', [y,b,a,orden] = obj.highpass(signal,data);
                otherwise, error('Use ''bandpass'' o ''highpass''.');
            end
        end

        %% -------- Oscilador ---------
        function osc_signal = oscilator(obj,fm)
            osc_signal = cos(2*pi*fm*obj.tiempo);
        end

        %% ---- Pasabajos analógico ---
        function [y,b,a,orden] = lowpass_out(obj,signal,data)
            if nargin < 3, data = false; end
            fp = 15e3; fsb = 40e3; Rp = 3; Rs = 15;
            [orden,Wn] = buttord(2*pi*fp,2*pi*fsb,Rp,Rs,'s');
            [b,a]      = butter(orden,Wn,'low','s');
            sysS       = tf(b,a);                     % H(s)
            y          = lsim(sysS,signal,obj.tiempo);% filtra analógico

            if data
                disp('--- Pasabajos Butterworth ANALÓGICO ---');
                fprintf('Orden = %d\n',orden);
                disp('Función de transferencia H(s):');  sysS   % <-- se muestra aquí
                figure, bode(sysS); grid on; title('Bode H(s) - Pasabajos');
            end
        end

        %% ---------- Remuestreo ----------
        function resample_signal = samplefilter(obj,signal)
            [P,Q] = rat(30e3/obj.fs,1e-12);
            resample_signal = resample(signal,P,Q);
        end

        %% --- Pasabanda analógico -----
        function [y,b,a,orden] = bandpass(obj,fc,signal,data)
            if nargin < 4, data = false; end
            fp = [fc-15e3, fc+15e3]; fsb = [fc-40e3, fc+40e3];
            [orden,Wn] = buttord(2*pi*fp,2*pi*fsb,3,15,'s');
            [b,a]      = butter(orden,Wn,'bandpass','s');
            sysS       = tf(b,a);
            y          = lsim(sysS,signal,obj.tiempo);

            if data
                disp('--- Pasabanda Butterworth ANALÓGICO ---');
                fprintf('Orden = %d\n',orden);
                disp('Función de transferencia H(s):');  sysS   % <-- se muestra aquí
                figure, bode(sysS); grid on; title('Bode H(s) - Pasabanda');
            end
        end

        %% --- Pasaaltos analógico -----
        function [y,b,a,orden] = highpass(obj,signal,data)
            if nargin < 3, data = false; end
            [orden,Wn] = buttord(2*pi*175e3,2*pi*150e3,3,15,'s');
            [b,a]      = butter(orden,Wn,'high','s');
            sysS       = tf(b,a);
            y          = lsim(sysS,signal,obj.tiempo);

            if data
                disp('--- Pasaaltos Butterworth ANALÓGICO ---');
                fprintf('Orden = %d\n',orden);
                disp('Función de transferencia H(s):');  sysS   % <-- se muestra aquí
                figure, bode(sysS); grid on; title('Bode H(s) - Pasaaltos');
            end
        end

        %% ---- Reproducir sonido -----
        function play_sound(~,signal,fs_audio)
            sound(signal/max(abs(signal)),fs_audio);
        end
    end
end
