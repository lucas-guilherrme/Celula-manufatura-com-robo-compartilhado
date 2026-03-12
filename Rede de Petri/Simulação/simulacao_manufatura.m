% Autor: Lucas Guilherme
% Email: lucas.guilherme.silva@ee.ufcg.edu.br
% Data: 03/2026

% =================================================================
% Simulação de Eventos Discretos: Sistema de Manufatura (3 Células)
% =================================================================

clear; clc; close all;

% =================================================================
% Parâmetros do Sistema
% =================================================================
num_celulas = 3;
capacidade_esteira = 2;
ciclos_simulacao = 20;

% =================================================================
% Inicialização dos Estados (0 = Livre/IDLE, 1 = Ocupado/Processando)
% =================================================================
m1_status = zeros(1, num_celulas);
m2_status = zeros(1, num_celulas);
robo_status = zeros(1, num_celulas);
buffer_pecas = zeros(1, num_celulas);

% =================================================================
% Matrizes para armazenar o histórico e plotar gráficos depois
% =================================================================
historico_buffer = zeros(num_celulas, ciclos_simulacao);

disp('--- Iniciando Simulação do Sistema de Manufatura ---');

for t = 1:ciclos_simulacao
    fprintf('\n[Ciclo %d]\n', t);
    
    for c = 1:num_celulas
        % 1. Máquinas tentam processar peças (probabilidade aleatória de terminar)
        if m1_status(c) == 0 && rand() > 0.3
            m1_status(c) = 1; % M1 tem peça pronta
        end
        if m2_status(c) == 0 && rand() > 0.3
            m2_status(c) = 1; % M2 tem peça pronta
        end
        
        % 2. Lógica de Coleta do Robô (Exclusão Mútua)
        if robo_status(c) == 0 % Se o robô está livre (1'IDLE)
            if m1_status(c) == 1
                robo_status(c) = 1; % Robô coleta de M1
                m1_status(c) = 0;   % M1 volta para IDLE
                origem = 'M1';
            elseif m2_status(c) == 1
                robo_status(c) = 1; % Robô coleta de M2
                m2_status(c) = 0;   % M2 volta para IDLE
                origem = 'M2';
            end
        end
        
        % 3. Lógica de Depósito e Controle de Overflow
        if robo_status(c) == 1
            if buffer_pecas(c) < capacidade_esteira
                buffer_pecas(c) = buffer_pecas(c) + 1; % Deposita peça
                robo_status(c) = 0; % Robô volta para IDLE
                fprintf('Célula %d: Robô depositou peça da %s. Buffer: %d/%d\n', c, origem, buffer_pecas(c), capacidade_esteira);
            else
                fprintf('Célula %d: [ALERTA] Buffer cheio! Robô em DEADLOCK aguardando vaga.\n', c);
            end
        end
        
        % 4. Consumo da Esteira (simulando a retirada de peças do sistema)
        if buffer_pecas(c) > 0 && rand() > 0.5
            buffer_pecas(c) = buffer_pecas(c) - 1;
            fprintf('Célula %d: Peça retirada da esteira. Vaga liberada!\n', c);
        end
        
        % Salva estado para o gráfico
        historico_buffer(c, t) = buffer_pecas(c);
    end
end
% =================================================================
% Plotagem dos Resultados
% =================================================================
figure;
hold on; grid on;
plot(1:ciclos_simulacao, historico_buffer(1, :), 'LineWidth', 2);
plot(1:ciclos_simulacao, historico_buffer(2, :), 'LineWidth', 2);
plot(1:ciclos_simulacao, historico_buffer(3, :), 'LineWidth', 2);
title('Ocupação do Buffer (Esteira) ao longo do tempo');
xlabel('Ciclos de Clock');
ylabel('Número de Peças');
legend('Célula 1', 'Célula 2', 'Célula 3');
ylim([0 capacidade_esteira + 1]);
hold off;

disp('--- Finalizando a Simulação do Sistema de Manufatura ---');