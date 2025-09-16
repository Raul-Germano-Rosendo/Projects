import pygame
import random
import time
import sys

# Inicializar pygame
pygame.init()

# Configurações
LARGURA, ALTURA = 1200, 620
TAMANHO_QUADRADO = 36
ESPACAMENTO = 10
COR_FUNDO = (240, 240, 240)
COR_TEXTO = (0, 0, 0)

# Cores
CORES = {
    'normal': (200, 200, 200),
    'esquerda': (144, 238, 144),  # Verde claro
    'direita': (255, 182, 193),   # Rosa claro
    'medio': (255, 165, 0),       # Laranja
    'encontrado': (138, 43, 226), # Roxo
    'alvo': (255, 0, 0),          # Vermelho
    'texto': (0, 0, 0),
    'destaque': (30, 144, 255)    # Azul
}

# Criar janela
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("🔍 Busca Binária Visual com Quadrados Coloridos")

def desenhar_quadrados(lista, esquerda, meio, direita, alvo, passo, encontrado=None):
    """Desenha os quadrados coloridos na tela"""
    tela.fill(COR_FUNDO)
    
    # Calcular posição inicial para centralizar
    total_largura = len(lista) * (TAMANHO_QUADRADO + ESPACAMENTO) - ESPACAMENTO
    x_inicio = (LARGURA - total_largura) // 2
    y_pos = 200
    
    # Desenhar título e informações
    fonte = pygame.font.SysFont('Arial', 24)
    titulo = fonte.render("BUSCA BINÁRIA VISUAL - QUADRADOS COLORIDOS", True, COR_TEXTO)
    tela.blit(titulo, (LARGURA//2 - titulo.get_width()//2, 30))
    
    info = fonte.render(f"Alvo: {alvo} | Passo: {passo}", True, CORES['alvo'])
    tela.blit(info, (LARGURA//2 - info.get_width()//2, 70))
    
    intervalo = fonte.render(f"Intervalo: [{esquerda}, {direita}] | Médio: {meio} = {lista[meio]}", True, CORES['texto'])
    tela.blit(intervalo, (LARGURA//2 - intervalo.get_width()//2, 100))
    
    # Desenhar todos os quadrados
    for i, valor in enumerate(lista):
        x = x_inicio + i * (TAMANHO_QUADRADO + ESPACAMENTO)
        
        # Definir cor do quadrado
        if encontrado == i:
            cor = CORES['encontrado']
        elif i == meio:
            cor = CORES['medio']
        elif i == esquerda:
            cor = CORES['esquerda']
        elif i == direita:
            cor = CORES['direita']
        elif esquerda <= i <= direita:
            cor = CORES['normal']
        else:
            cor = (180, 180, 180)  # Cinza para fora do intervalo
        
        # Desenhar quadrado
        pygame.draw.rect(tela, cor, (x, y_pos, TAMANHO_QUADRADO, TAMANHO_QUADRADO))
        pygame.draw.rect(tela, (0, 0, 0), (x, y_pos, TAMANHO_QUADRADO, TAMANHO_QUADRADO), 2)
        
        # Desenhar valor
        fonte_valor = pygame.font.SysFont('Arial', 20)
        texto_valor = fonte_valor.render(str(valor), True, COR_TEXTO)
        tela.blit(texto_valor, (x + TAMANHO_QUADRADO//2 - texto_valor.get_width()//2, 
                               y_pos + TAMANHO_QUADRADO//2 - texto_valor.get_height()//2))
        
        # Desenhar índice
        fonte_indice = pygame.font.SysFont('Arial', 16)
        texto_indice = fonte_indice.render(str(i), True, CORES['destaque'])
        tela.blit(texto_indice, (x + TAMANHO_QUADRADO//2 - texto_indice.get_width()//2, y_pos + TAMANHO_QUADRADO + 5))
    
    # Legenda
    y_legenda = y_pos + TAMANHO_QUADRADO + 50
    legenda_titulo = fonte.render("LEGENDA:", True, COR_TEXTO)
    tela.blit(legenda_titulo, (50, y_legenda))
    
    # Itens da legenda
    itens_legenda = [
        ("Verde", CORES['esquerda'], "Limite esquerdo"),
        ("Rosa", CORES['direita'], "Limite direito"),
        ("Laranja", CORES['medio'], "Ponto médio"),
        ("Roxo", CORES['encontrado'], "Alvo encontrado"),
        ("Cinza", CORES['normal'], "Intervalo atual"),
        ("Cinza escuro", (180, 180, 180), "Fora do intervalo")
    ]
    
    for i, (nome, cor, descricao) in enumerate(itens_legenda):
        y_item = y_legenda + 40 + i * 30
        pygame.draw.rect(tela, cor, (50, y_item, 20, 20))
        pygame.draw.rect(tela, (0, 0, 0), (50, y_item, 20, 20), 1)
        texto_legenda = pygame.font.SysFont('Arial', 18).render(f"{nome}: {descricao}", True, COR_TEXTO)
        tela.blit(texto_legenda, (80, y_item))
    
    pygame.display.flip()

def busca_binaria_pygame(lista, alvo):
    """Executa busca binária com visualização pygame"""
    esquerda, direita = 0, len(lista) - 1
    passo = 0
    executando = True
    
    while executando and esquerda <= direita:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    executando = False
        
        if not executando:
            break
            
        passo += 1
        meio = (esquerda + direita) // 2
        
        # Mostrar visualização
        desenhar_quadrados(lista, esquerda, meio, direita, alvo, passo)
        time.sleep(1.5)
        
        if lista[meio] == alvo:
            # Alvo encontrado!
            desenhar_quadrados(lista, esquerda, meio, direita, alvo, passo, encontrado=meio)
            
            # Mostrar mensagem de sucesso
            fonte = pygame.font.SysFont('Arial', 32)
            mensagem = fonte.render(f"🎯 ALVO ENCONTRADO! Posição: {meio}", True, CORES['encontrado'])
            tela.blit(mensagem, (LARGURA//2 - mensagem.get_width()//2, 450))
            pygame.display.flip()
            
            time.sleep(3)
            break
            
        elif lista[meio] < alvo:
            esquerda = meio + 1
        else:
            direita = meio - 1
    
    # Manter janela aberta
    esperando_saida = True
    while esperando_saida:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT or (evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE):
                esperando_saida = False
    
    pygame.quit()

# Criar lista e executar
if __name__ == "__main__":
    # Criar lista ordenada
    tamanho = 15
    lista = sorted(random.sample(range(1, 100), tamanho))
    alvo = random.choice(lista)
    
    print(f"Lista: {lista}")
    print(f"Alvo: {alvo}")
    
    busca_binaria_pygame(lista, alvo)