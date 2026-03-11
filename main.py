import pygame
from random import randint

pygame.init()
pygame.font.init()
pygame.mixer.init()

# Configuração da janela
janela = pygame.display.set_mode([960,540])
pygame.display.set_caption('First Game')

# Música e sons 
musica_menu = "Sons_game/musica_menu.mp3"
musica_jogo = "Sons_game/musica_jogo.mp3"

# Sons de disparo 
som_tiro_player = pygame.mixer.Sound("Sons_game/player_laser.mp3")
som_tiro_player.set_volume(0.1)  

som_tiro_inimigo = pygame.mixer.Sound("Sons_game/inimigo_laser.mp3")
som_tiro_inimigo.set_volume(0.01)  

# Imagens
imagem_menu = pygame.image.load('C:/Users/João/Documents/meu_jogo/imagens_game/194dc263-8a6a-4b15-88e4-f8ae2ff09550.png')
imagem_jogo = pygame.image.load('C:/Users/João/Documents/meu_jogo/imagens_game/pngtree-cosmic-nebula-in-deep-space-image_21185010.webp')
nave_player = pygame.image.load('imagens_game/sprite_nave_pequena.png')
nave_inimiga = pygame.image.load('imagens_game/nave_inimiga_pequena.png')

# Variáveis globais
pos_y_player = 400
pos_x_player = 420
velocidade_nave = 1

pos_x_inimiga = 450
pos_y_inimiga = 70
velocidade_inimiga_x = 0.2
velocidade_inimiga_y = 0.2

tiros_inimigos = []
velocidade_tiro = 0.2
contador_tiro = 0

tiros_player = []
velocidade_tiro_player = -4

# -------- MENU --------
def desenha_menu():
    pygame.mixer.music.load(musica_menu)
    pygame.mixer.music.set_volume(0.1)  
    pygame.mixer.music.play(-1)

    fonte = pygame.font.SysFont("Arial", 30)
    menu = True
    while menu:
        janela.blit(imagem_menu, (0,0))

        titulo = fonte.render("DEMO SPACE GAME", True, (255,255,255))
        instrucoes = fonte.render("Setas = mover | CTRL = atirar", True, (255,255,255))
        iniciar = fonte.render("Pressione ENTER para começar", True, (255,255,0))
        sair = fonte.render("Pressione ESC para sair", True, (255,0,0))

        janela.blit(titulo, (300, 150))
        janela.blit(instrucoes, (250, 220))
        janela.blit(iniciar, (250, 280))
        janela.blit(sair, (250, 320))

        pygame.display.update()

        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                return False
            if events.type == pygame.KEYDOWN:
                if events.key == pygame.K_RETURN:
                    return True
                if events.key == pygame.K_ESCAPE:
                    return False

# -------- JOGO --------
def desenha_jogo():
    global pos_x_player, pos_y_player, pos_x_inimiga, pos_y_inimiga
    global velocidade_inimiga_x, velocidade_inimiga_y
    global tiros_inimigos, contador_tiro, tiros_player

    pygame.mixer.music.load(musica_jogo)
    pygame.mixer.music.set_volume(0.1)  
    pygame.mixer.music.play(-1)

    loop = True
    while loop:
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                loop = False
            if events.type == pygame.KEYDOWN:
                if events.key == pygame.K_ESCAPE:
                    return "menu"
                if events.key == pygame.K_LCTRL or events.key == pygame.K_RCTRL:
                    tiros_player.append([pos_x_player + 20, pos_y_player])
                    som_tiro_player.play(loops=0, maxtime=200)  # toca só uma vez

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_UP]: pos_y_player -= velocidade_nave
        if teclas[pygame.K_DOWN]: pos_y_player += velocidade_nave
        if teclas[pygame.K_LEFT]: pos_x_player -= velocidade_nave
        if teclas[pygame.K_RIGHT]: pos_x_player += velocidade_nave

        pos_x_inimiga += velocidade_inimiga_x
        pos_y_inimiga += velocidade_inimiga_y
        if pos_y_inimiga <= 50 or pos_y_inimiga >= 200:
            velocidade_inimiga_y *= -1
        if pos_x_inimiga <= 100 or pos_x_inimiga >= 800:
            velocidade_inimiga_x *= -1

        contador_tiro += 1
        if contador_tiro > 600:
            tiros_inimigos.append([pos_x_inimiga + 20, pos_y_inimiga + 40])
            som_tiro_inimigo.play(loops=0, maxtime=200)
            contador_tiro = 0

        for tiro in tiros_inimigos:
            tiro[1] += velocidade_tiro
        tiros_inimigos = [tiro for tiro in tiros_inimigos if tiro[1] < 540]

        for tiro in tiros_player:
            tiro[1] += velocidade_tiro_player
        tiros_player = [tiro for tiro in tiros_player if tiro[1] > 0]

        if pos_y_player <= -10: pos_y_player = -10
        if pos_y_player >= 440: pos_y_player = 440
        if pos_x_player <= -40: pos_x_player = -40
        if pos_x_player >= 900: pos_x_player = 900

        janela.blit(imagem_jogo,(0, 0))
        janela.blit(nave_player,(pos_x_player, pos_y_player))
        janela.blit(nave_inimiga,(pos_x_inimiga, pos_y_inimiga))

        for tiro in tiros_inimigos:
            pygame.draw.rect(janela, (255, 0, 0), (tiro[0], tiro[1], 5, 10))
        for tiro in tiros_player:
            pygame.draw.rect(janela, (0, 255, 0), (tiro[0], tiro[1], 5, 10))

        pygame.display.update()

# -------- EXECUÇÃO --------
if desenha_menu():
    resultado = desenha_jogo()
    if resultado == "menu":
        if desenha_menu():
            desenha_jogo()
