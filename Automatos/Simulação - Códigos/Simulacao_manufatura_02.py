# Autor: Lucas Guilherme da Silva
# Data: 2024-06-20

# Importações das bibliotecas necessárias
import tkinter as tk
import random, math
from enum import Enum, auto

# Configurações da tela para simulação
LARGURA_TELA = 900  # 
ALTURA_TELA = 500
COR_FUNDO = "#2c3e50"         # Fundo Azul Escuro Industrial

# Cores
COR_M_OCIOSA = "#bdc3c7"      # Cinza
COR_M_PROCESSANDO = "#f1c40f" # Amarelo
COR_M_PRONTA = "#2ecc71"      # Verde
COR_ROBO_LIVRE = "#3498db"    # Azul
COR_ROBO_OCUPADO = "#e74c3c"  # Vermelho
COR_BUFFER = "#95a5a6"        # Cinza Médio
COR_PECA = "#9b59b6"          # Roxo (Produto Acabado)
COR_MATERIA = "#e67e22"       # Laranja (Matéria Prima)

class EstadoMaquina(Enum):
    OCIOSA = auto()
    PROCESSANDO = auto()
    PECA_PRONTA = auto()

class EstadoRobo(Enum):
    LIVRE = auto()
    CARREGANDO = auto()

class Maquina:
    def __init__(self, id_m, x, y):
        self.id = id_m
        self.estado = EstadoMaquina.OCIOSA
        self.tempo_restante = 0
        self.x = x 
        self.y = y 

    def processar(self):
        if self.estado == EstadoMaquina.OCIOSA:
            if random.randint(0, 100) < 5: 
                self.tempo_restante = random.randint(50, 150)
                self.estado = EstadoMaquina.PROCESSANDO
        
        elif self.estado == EstadoMaquina.PROCESSANDO:
            if self.tempo_restante > 0:
                self.tempo_restante -= 1
            else:
                self.estado = EstadoMaquina.PECA_PRONTA

class Buffer:
    def __init__(self, capacidade, x, y):
        self.qtd = 0
        self.cap_max = capacidade
        self.x = x
        self.y = y

    def tentar_esvaziar(self):
        # Simula agente externo retirando peça
        if self.qtd > 0 and random.randint(0, 100) < 2:
            self.qtd -= 1
            return True # Retorna True para avisar a GUI que saiu uma peça
        return False

class Robo:
    def __init__(self, x, y):
        self.estado = EstadoRobo.LIVRE # 0 = nenhuma, 1 = M1, 2 = M2
        self.peca_origem = 0           
        self.x = x
        self.y = y
        self.target_x = x
        self.target_y = y
        self.velocidade = 6 

    def mover_para(self, x, y):
        self.target_x = x
        self.target_y = y

    def atualizar_posicao(self):
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        dist = math.sqrt(dx**2 + dy**2)

        if dist < self.velocidade:
            self.x = self.target_x
            self.y = self.target_y
            return True 
        else:
            self.x += (dx / dist) * self.velocidade
            self.y += (dy / dist) * self.velocidade
            return False 

class SimulacaoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulação Célula de Manufatura - Visual Otimizado")
        
        # Canvas
        self.canvas = tk.Canvas(root, width=LARGURA_TELA, height=ALTURA_TELA, bg=COR_FUNDO)
        self.canvas.pack()

        # Componentes
        self.m1 = Maquina(1, 150, 150) 
        self.m2 = Maquina(2, 150, 350) 
        self.buffer = Buffer(2, 650, 250)
        self.robo = Robo(400, 250) 
        
        self.home_pos = (400, 250)
        self.destino_atual = "HOME" 

        # Variável para animação de saída do produto
        self.pecas_saindo = [] # Lista de dicionários {'x': int, 'y': int}

        # Loop
        self.atualizar()

    def desenhar(self):
        self.canvas.delete("all") 

        # --- Desenhar Conexões ---
        self.canvas.create_line(self.m1.x, self.m1.y, self.robo.x, self.robo.y, fill="#7f8c8d", dash=(4, 2))
        self.canvas.create_line(self.m2.x, self.m2.y, self.robo.x, self.robo.y, fill="#7f8c8d", dash=(4, 2))
        self.canvas.create_line(self.buffer.x, self.buffer.y, self.robo.x, self.robo.y, fill="#7f8c8d", dash=(4, 2))

        # --- Desenhar Máquinas e Matéria Prima ---
        for m in [self.m1, self.m2]:
            
            # 2. VISUALIZAÇÃO: Silo de Matéria Prima (Esquerda da máquina)
            # Desenha uma caixa de entrada
            self.canvas.create_rectangle(m.x-90, m.y-20, m.x-50, m.y+20, outline="#95a5a6", width=2)
            self.canvas.create_text(m.x-70, m.y-35, text="Insumo", fill="#bdc3c7", font=("Arial", 8))
            
            # Se a máquina NÃO está processando, mostra materia prima esperando
            if m.estado != EstadoMaquina.PROCESSANDO:
                self.canvas.create_oval(m.x-80, m.y-10, m.x-60, m.y+10, fill=COR_MATERIA, outline="black")
            else:
                # Se está processando, desenha linha conectando o insumo à máquina
                self.canvas.create_line(m.x-50, m.y, m.x-40, m.y, fill=COR_MATERIA, width=3)

            # Lógica de cor da Máquina
            cor = COR_M_OCIOSA
            texto_estado = "OCIOSA"
            if m.estado == EstadoMaquina.PROCESSANDO:
                cor = COR_M_PROCESSANDO
                texto_estado = "PROC..."
            elif m.estado == EstadoMaquina.PECA_PRONTA:
                cor = COR_M_PRONTA
                texto_estado = "PRONTA"
            
            # Corpo da máquina
            self.canvas.create_rectangle(m.x-40, m.y-40, m.x+40, m.y+40, fill=cor, outline="white", width=2)
            self.canvas.create_text(m.x, m.y-50, text=f"M{m.id}", font=("Arial", 12, "bold"), fill="white")
            self.canvas.create_text(m.x, m.y+55, text=texto_estado, font=("Arial", 10, "bold"), fill="white")
            
            # Se processando, desenha a matéria prima DENTRO da máquina
            if m.estado == EstadoMaquina.PROCESSANDO:
                 self.canvas.create_oval(m.x-10, m.y-10, m.x+10, m.y+10, fill=COR_MATERIA)

            # Se pronta, desenha a PEÇA ROXA na saída
            if m.estado == EstadoMaquina.PECA_PRONTA:
                self.canvas.create_oval(m.x+20, m.y+20, m.x+35, m.y+35, fill=COR_PECA, outline="white")

        # --- Desenhar Buffer ---
        cor_buff = COR_BUFFER
        if self.buffer.qtd == self.buffer.cap_max:
            cor_buff = "#c0392b" # Vermelho escuro se cheio
        
        # Estrutura do buffer
        self.canvas.create_rectangle(self.buffer.x-40, self.buffer.y-60, self.buffer.x+60, self.buffer.y+60, fill="#ecf0f1", outline=cor_buff, width=3)
        self.canvas.create_text(self.buffer.x, self.buffer.y-75, text=f"BUFFER ({self.buffer.qtd}/{self.buffer.cap_max})", font=("Arial", 12, "bold"), fill="white")
        
        # Peças no buffer
        for i in range(self.buffer.qtd):
            offset_y = 35 * i
            self.canvas.create_oval(self.buffer.x-15, (self.buffer.y-30) + offset_y, self.buffer.x+15, (self.buffer.y) + offset_y, fill=COR_PECA, outline="black")

        # --- 3. VISUALIZAÇÃO: Peças Saindo (Expedição) ---
        # Animação das peças que foram removidas
        nova_lista_saindo = []
        for peca in self.pecas_saindo:
            # Desenha a peça movendo para a direita
            self.canvas.create_oval(peca['x']-10, peca['y']-10, peca['x']+10, peca['y']+10, fill=COR_PECA, outline="white")
            self.canvas.create_text(peca['x'], peca['y']-20, text="Saindo...", font=("Arial", 8), fill="white")
            
            # Atualiza posição para o próximo frame
            peca['x'] += 5 # Velocidade da esteira de saída
            
            # Se ainda estiver na tela, mantém na lista
            if peca['x'] < LARGURA_TELA + 20:
                nova_lista_saindo.append(peca)
        
        self.pecas_saindo = nova_lista_saindo


        # --- Desenhar Robô ---
        cor_robo = COR_ROBO_LIVRE if self.robo.estado == EstadoRobo.LIVRE else COR_ROBO_OCUPADO
        self.canvas.create_oval(self.robo.x-25, self.robo.y-25, self.robo.x+25, self.robo.y+25, fill=cor_robo, outline="white", width=2)
        self.canvas.create_text(self.robo.x, self.robo.y-35, text="Robô", font=("Arial", 10, "bold"), fill="white")
        
        if self.robo.estado == EstadoRobo.CARREGANDO:
            self.canvas.create_oval(self.robo.x-8, self.robo.y-8, self.robo.x+8, self.robo.y+8, fill=COR_PECA, outline="white")

        # --- Legenda ---
        legenda = "Laranja=Matéria Prima | Roxo=Produto Final | Azul=Robô Livre | Vermelho=Ocupado"
        self.canvas.create_text(LARGURA_TELA/2, ALTURA_TELA-20, text=legenda, font=("Arial", 10), fill="#bdc3c7")

    def logica_sistema(self):
        # 1. Atualizar máquinas
        self.m1.processar()
        self.m2.processar()

        # 2. Consumo externo do Buffer (Alterado para gerar animação)
        saiu_peca = self.buffer.tentar_esvaziar()
        if saiu_peca:
            # Cria uma "peça virtual" na saída do buffer para animar
            self.pecas_saindo.append({'x': self.buffer.x + 60, 'y': self.buffer.y})

        # 3. Lógica do Robô
        chegou = self.robo.atualizar_posicao()

        if chegou:
            if self.robo.estado == EstadoRobo.LIVRE:
                if self.destino_atual == "M1_PICK":
                    self.robo.estado = EstadoRobo.CARREGANDO
                    self.m1.estado = EstadoMaquina.OCIOSA
                    self.destino_atual = "BUFFER_PLACE"
                    self.robo.mover_para(self.buffer.x, self.buffer.y)
                
                elif self.destino_atual == "M2_PICK":
                    self.robo.estado = EstadoRobo.CARREGANDO
                    self.m2.estado = EstadoMaquina.OCIOSA
                    self.destino_atual = "BUFFER_PLACE"
                    self.robo.mover_para(self.buffer.x, self.buffer.y)

                else:
                    if self.m1.estado == EstadoMaquina.PECA_PRONTA:
                        self.destino_atual = "M1_PICK"
                        self.robo.mover_para(self.m1.x, self.m1.y)
                    elif self.m2.estado == EstadoMaquina.PECA_PRONTA:
                        self.destino_atual = "M2_PICK"
                        self.robo.mover_para(self.m2.x, self.m2.y)
                    else:
                        self.destino_atual = "HOME"
                        self.robo.mover_para(self.home_pos[0], self.home_pos[1])

            elif self.robo.estado == EstadoRobo.CARREGANDO:
                if self.destino_atual == "BUFFER_PLACE":
                    if self.buffer.qtd < self.buffer.cap_max:
                        self.buffer.qtd += 1
                        self.robo.estado = EstadoRobo.LIVRE
                        self.destino_atual = "HOME"
                    else:
                        pass 

    def atualizar(self):
        self.logica_sistema()
        self.desenhar()
        self.root.after(30, self.atualizar)

if __name__ == "__main__":
    root = tk.Tk()
    app = SimulacaoGUI(root)
    root.mainloop()