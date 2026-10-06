import pygame
import sys
import random

# Inicializa o Pygame
pygame.init()

# Configurações da tela
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Confeitaria Maluca: Monte seu Bolo!")

# Cores Temáticas (Doces e Tons Pastéis)
ROSA_PASTEL = (255, 228, 225)
ROSA_CHOQUE = (255, 105, 180)
MARROM_CHOCOLATE = (101, 67, 33)
VERMELHO_MORANGO = (220, 20, 60)
VERMELHO_CEREJA = (139, 0, 0)
VERDE_ESTRAGADO = (34, 139, 34)
BRANCO_CREME = (255, 253, 208)

# Configurações do Bolo (Jogador)
LARGURA_BOLO, ALTURA_BOLO = 100, 40
velocidade_jogador = 10
bolo_x = LARGURA // 2 - LARGURA_BOLO // 2
bolo_y = ALTURA - 70

# Pontuação e Vidas
pontos = 0
vidas = 3
fonte = pygame.font.Font(None, 40)
fonte_fim = pygame.font.Font(None, 60)

# Lista para gerenciar os ingredientes que caem
# Cada item será um dicionário: {"rect": pygame.Rect, "tipo": "morango"/"cereja"/"bomba", "velocidade": int}
ingredientes = []

def criar_ingrediente():
    x = random.randint(20, LARGURA - 40)
    y = -40
    sorteio = random.random()
    
    if sorteio < 0.6:
        tipo = "morango"
        tamanho = 20
        velocidade = random.randint(4, 7)
    elif sorteio < 0.8:
        tipo = "cereja"
        tamanho = 15
        velocidade = random.randint(6, 9)
    else:
        tipo = "bomba"
        tamanho = 25
        velocidade = random.randint(5, 8)
        
    rect = pygame.Rect(x, y, tamanho, tamanho)
    return {"rect": rect, "tipo": tipo, "velocidade": velocidade}

# Frequência de surgimento dos ingredientes
tempo_ultimo_ingrediente = 0
intervalo_surgimento = 1000 # milissegundos (1 segundo)

relogio = pygame.time.Clock()
jogo_ativo = True

# Loop Principal
while True:
    # 1. Tratamento de Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if evento.type == pygame.KEYDOWN and not jogo_ativo:
            if evento.key == pygame.K_SPACE:
                # Reinicia o jogo
                pontos = 0
                vidas = 3
                ingredientes.clear()
                bolo_x = LARGURA // 2 - LARGURA_BOLO // 2
                jogo_ativo = True

    if jogo_ativo:
        # 2. Controles do Jogador (Setas para Esquerda e Direita)
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and bolo_x > 0:
            bolo_x -= velocidade_jogador
        if teclas[pygame.K_RIGHT] and bolo_x < LARGURA - LARGURA_BOLO:
            bolo_x += velocidade_jogador

        # Criar retângulo atualizado do bolo do jogador
        jogador_rect = pygame.Rect(bolo_x, bolo_y, LARGURA_BOLO, ALTURA_BOLO)

        # 3. Geração de Novos Ingredientes por tempo
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - tempo_ultimo_ingrediente > intervalo_surgimento:
            ingredientes.append(criar_ingrediente())
            tempo_ultimo_ingrediente = tempo_atual

        # 4. Atualização e Movimentação dos Ingredientes
        for ingrediente in ingredientes[:]:
            ingrediente["rect"].y += ingrediente["velocidade"]

            # Verifica colisão com o bolo do jogador
            if ingrediente["rect"].colliderect(jogador_rect):
                if ingrediente["tipo"] == "morango":
                    pontos += 10
                elif ingrediente["tipo"] == "cereja":
                    pontos += 25
                elif ingrediente["tipo"] == "bomba":
                    vidas -= 1
                    if vidas <= 0:
                        jogo_ativo = False
                ingredientes.remove(ingrediente)
                continue

            # Remove se passar do chão e tira vida se for fruta boa perdida
            if ingrediente["rect"].top > ALTURA:
                if ingrediente["tipo"] != "bomba":
                    # Opcional: penalidade por deixar a fruta cair
                    pass
                ingredientes.remove(ingrediente)

    # 5. Desenho da Tela e Elementos
    tela.fill(ROSA_PASTEL) # Fundo rosa bebê bem fofo

    if jogo_ativo:
        # Desenha o prato do bolo (base cinza clara)
        pygame.draw.box = pygame.Rect(bolo_x - 10, bolo_y + ALTURA_BOLO, LARGURA_BOLO + 20, 10)
        pygame.draw.rect(tela, (220, 220, 220), pygame.draw.box, border_radius=5)

        # Desenha o Bolo (Camadas de Chocolate e Creme Rosa)
        pygame.draw.rect(tela, MARROM_CHOCOLATE, jogador_rect, border_radius=8) # Base de chocolate
        # Cobertura de creme por cima do bolo
        pygame.draw.rect(tela, BRANCO_CREME, (bolo_x, bolo_y, LARGURA_BOLO, 12), border_top_left_radius=8, border_top_right_radius=8)

        # Desenha os Ingredientes Caindo
        for ingrediente in ingredientes:
            r = ingrediente["rect"]
            if ingrediente["tipo"] == "morango":
                pygame.draw.ellipse(tela, VERMELHO_MORANGO, r)
                # Detalhe da folhinha verde do morango
                pygame.draw.rect(tela, VERDE_ESTRAGADO, (r.x + r.width//2 - 2, r.y - 2, 5, 4))
            elif ingrediente["tipo"] == "cereja":
                pygame.draw.ellipse(tela, VERMELHO_CEREJA, r)
            elif ingrediente["tipo"] == "bomba":
                pygame.draw.ellipse(tela, VERDE_ESTRAGADO, r) # Ingrediente estragado/mofado

        # Placar na tela
        texto_pontos = fonte.render(f"Pontos: {pontos}", True, MARROM_CHOCOLATE)
        texto_vidas = fonte.render(f"Vidas: {'❤️ ' * vidas}", True, VERMELHO_MORANGO)
        tela.blit(texto_pontos, (20, 20))
        tela.blit(texto_vidas, (LARGURA - 180, 20))

    else:
        # Tela de Game Over
        texto_fim = fonte_fim.render("FIM DE JOGO!", True, VERMELHO_MORANGO)
        texto_score = fonte.render(f"Seu bolo fez {pontos} pontos!", True, MARROM_CHOCOLATE)
        texto_restart = fonte.render("Pressione ESPAÇO para assar outro bolo", True, ROSA_CHOQUE)
        
        tela.blit(texto_fim, (LARGURA//2 - texto_fim.get_width()//2, ALTURA//2 - 80))
        tela.blit(texto_score, (LARGURA//2 - texto_score.get_width()//2, ALTURA//2 - 20))
        tela.blit(texto_restart, (LARGURA//2 - texto_restart.get_width()//2, ALTURA//2 + 40))

    # Atualiza gráficos e crava a 60 FPS
    pygame.display.flip()
    relogio.tick(60)
