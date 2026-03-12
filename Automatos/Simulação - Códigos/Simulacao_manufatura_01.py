# Autor: Lucas Guilherme
# Data: 2024-06-10

'''Simulação de uma célula de manufatura com duas máquinas, um robô pick-and-place e um buffer.'''

# Importações das bibliotecas necessárias
import time, random
from enum import Enum, auto

# Constantes da simulação
CAPACIDADE_BUFFER = 2

# Estados usando Enum para ficar legível
class EstadoMaquina(Enum):
    OCIOSA = auto()       # Pronta para começar
    PROCESSANDO = auto()  # Trabalhando
    PECA_PRONTA = auto()  # Esperando retirada

class EstadoRobo(Enum):
    LIVRE = auto()
    CARREGANDO = auto()

class Maquina:
    def __init__(self, id_maquina):
        self.id = id_maquina                # Identificador da máquina que pode ser 1 ou 2
        self.estado = EstadoMaquina.OCIOSA  # Estado inicial da maquína
        self.tempo_restante = 0             # Tempo restante para finalizar o processamento

    def atualizar(self):
        """Lógica interna da máquina: Processar e finalizar."""
        if self.estado == EstadoMaquina.OCIOSA:
            # Inicia trabalho (assumindo matéria-prima infinita)
            self.tempo_restante = random.randint(2, 6) # Tempo aleatório dentro do intervalo [2 a 6] ciclos
            self.estado = EstadoMaquina.PROCESSANDO
            print(f"[Maquina {self.id}]\nIniciou processamento.")
        
        elif self.estado == EstadoMaquina.PROCESSANDO:
            if self.tempo_restante > 0:
                self.tempo_restante -= 1
            else:
                self.estado = EstadoMaquina.PECA_PRONTA
                print(f"[Maquina {self.id}] Terminou!\nAguardando retirada...")
        
        elif self.estado == EstadoMaquina.PECA_PRONTA:
            # Fica travada aguardando o robô
            print(f"[Maquina {self.id}] Peça pronta!\nAguardando o robô...")
            pass

class Buffer:
    def __init__(self, capacidade):
        self.qtd_pecas = 0
        self.capacidade_max = capacidade

    def consumir(self):
        """Simula agente externo removendo peças."""
        if self.qtd_pecas > 0:
            # 40% de chance de remover uma peça para simular variabilidade
            if random.random() < 0.40:
                self.qtd_pecas -= 1
                print("[EXTERNO] \nUma peça foi removida do Buffer.")

class Robo:
    def __init__(self):
        self.estado = EstadoRobo.LIVRE
        self.peca_origem = 0 # 0 = nenhuma, 1 = M1, 2 = M2

    def atuar(self, m1, m2, buffer):
        """Lógica de decisão do Robô (Pick and Place)."""
        # 1. Se estiver LIVRE: Procura peças nas máquinas (Pick)
        if self.estado == EstadoRobo.LIVRE:
            # Prioridade para M1, depois M2
            if m1.estado == EstadoMaquina.PECA_PRONTA:
                self.estado = EstadoRobo.CARREGANDO
                self.peca_origem = 1
                m1.estado = EstadoMaquina.OCIOSA # Libera a máquina
                print("[ROBO] Pegou a peça da Máquina 1.")
            
            elif m2.estado == EstadoMaquina.PECA_PRONTA:
                self.estado = EstadoRobo.CARREGANDO
                self.peca_origem = 2
                m2.estado = EstadoMaquina.OCIOSA # Libera a máquina
                print("[ROBO] Pegou a peça da Máquina 2.")
            
            else:
                print("[ROBO] Aguardando peças...")

        # 2. Se estiver CARREGANDO: Tenta depositar no Buffer (Place)
        elif self.estado == EstadoRobo.CARREGANDO:
            if buffer.qtd_pecas < buffer.capacidade_max:
                buffer.qtd_pecas += 1
                self.estado = EstadoRobo.LIVRE
                print(f"[ROBO] Depositou peça (origem M{self.peca_origem}) no Buffer.")
            else:
                # Buffer cheio! Bloqueio físico.
                print("[ALERTA] Buffer CHEIO! Robô aguardando liberação de espaço.")

# Mostrar o resultado na tela da simulação
def imprimir_status(m1, m2, robo, buffer):
    """Exibe o painel de status formatado."""
    # Helpers para formatar string dos estados
    s_m1 = "PRONTA" if m1.estado == EstadoMaquina.PECA_PRONTA else ("Processando" if m1.estado == EstadoMaquina.PROCESSANDO else "Ociosa")
    s_m2 = "PRONTA" if m2.estado == EstadoMaquina.PECA_PRONTA else ("Processando" if m2.estado == EstadoMaquina.PROCESSANDO else "Ociosa")
    s_robo = "LIVRE" if robo.estado == EstadoRobo.LIVRE else "CARREGANDO"

    print("\n\t   STATUS ATUAL:\n")
    print(f"   | M1: {s_m1:<22}")
    print(f"   | M2: {s_m2:<22}")
    print(f"   | Robô: {s_robo:<22}")
    print(f"   | Buffer: [{buffer.qtd_pecas} / {buffer.capacidade_max}]")
    print("\n")

# --- BLOCO PRINCIPAL (MAIN) ---

def main():
    # Instanciação dos objetos
    m1 = Maquina(1)
    m2 = Maquina(2)
    robo = Robo()
    buffer = Buffer(CAPACIDADE_BUFFER)

    print("=== INICIANDO SIMULAÇÃO DA CÉLULA DE MANUFATURA (PYTHON) ===")
    print("Pressione Ctrl+C para parar.\n")

    try:
        while True:
            print("-" * 48)
            
            # 1. Atualizar Máquinas
            m1.atualizar()
            m2.atualizar()

            # 2. Ação do Robô
            robo.atuar(m1, m2, buffer)

            # 3. Simulação externa (esvaziar buffer)
            buffer.consumir()

            # 4. Mostrar Dashboard
            imprimir_status(m1, m2, robo, buffer)

            # Aguarda 4 segundos
            time.sleep(4)

    except KeyboardInterrupt:
        print("\n\nSimulação interrompida pelo usuário.")

if __name__ == "__main__":
    main()