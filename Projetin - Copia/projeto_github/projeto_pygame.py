import pygame, sys
from pygame.locals import *

# Tamanho total do mapa
WINDOW_SIZE = (600,400)

#Tamanho da tela
display = pygame.Surface((300,200)) 
tela = pygame.display.set_mode((WINDOW_SIZE),0,32)

#FPS
clock = pygame.time.Clock()
fps = 60

#Inicia o pygame
pygame.display.set_caption('Projeto Pygame')
pygame.init()

#Inicio do loading de imagens

    # Carrega a imagem do player
player = pygame.image.load('player.png') 
    # setar a cor do player da imagem do player
player.set_colorkey((255,255,255)) 
    # Grama
grass_img = pygame.image.load('grass.png') 
    # Terra
dirt_img = pygame.image.load('dirt.png') 
floor_img = pygame.image.load('floor.png')
floor_img = pygame.transform.scale(floor_img, (16,16))
back_img = pygame.image.load('floorgrass.png')
back_img = pygame.transform.scale(back_img, (600,400))
arvore_img = pygame.image.load('arvore.png')
arvore_img = pygame.transform.scale(arvore_img, (16,16))
#Fim do loading de imagens

#Colisão Player
player_rect = pygame.Rect(50, 50, player.get_width(), player.get_height()) # colisão do player

# Tamanho do bloco(bloco de 1x1px)
TILE_SIZE = grass_img.get_width()
TREE_WIDTH = arvore_img.get_width()
TREE_HEIGHT = arvore_img.get_height()

#Carrega o mapa Inicio
def load_map(path):
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map

game_map = load_map('aaaa copy') # Carrega o mapa
#Carrega o mapa Fim

#Set dos movimentos
move_right = False
move_left = False
move_up = False
move_down = False
reset = False

#Pulo e gravidade
player_y_momentum = 0
air_timer = 0

#Colisão Inicio
    #Volta uma lista com os blocos que colidem
def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list
    #volta a posição do player e se colidiu, se colidiu a colisão é True e o lado do personagem  = lado do tile que colidiu
def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types
#Colisão Fim

#Camera Inicio
scrool = [0,0]
true_scrool = [0,0]
test_rect = pygame.Rect(100,100,100,50)
#camera Fim

# Define the starting position of the player e do Rect de colisão dele
player_start_x = 100
player_start_y = 64
player_rect.x = player_start_x
player_rect.y = player_start_y


while True:
    #display.blit(back_img, (0,0) ) #Setado com a cor de fundo do "Céu"
    display.fill((146,244,255)) #Setado com a cor de fundo do "Céu"
    
    #Camera
        #Seta a camera para seguir o Rect do player, com um efeito de suavização
    true_scrool[0] += (player_rect.x-scrool[0]-152)/20
    true_scrool[1] += (player_rect.y-scrool[1]-106)/20
        #Da uma corrigida na suavização
    scrool = true_scrool.copy()
    scrool[0] = int(scrool[0])
    scrool[1] = int(scrool[1])
   
    #Desenha o mapa e adiciona os blocos a lista de colisão
    y=0
    tile_rects = []
    for row in game_map:
        x=0
        for tile in row:
            if tile == '1':
                display.blit(dirt_img, (x* TILE_SIZE-scrool[0], y* TILE_SIZE-scrool[1]))
            if tile == '2':
                display.blit(grass_img, (x* TILE_SIZE-scrool[0], y* TILE_SIZE-scrool[1]))
            if tile == '3':
                display.blit(floor_img, (x* TILE_SIZE-scrool[0], y* TILE_SIZE-scrool[1]))
            if tile == '4':
                display.blit(arvore_img, (x* TREE_WIDTH-scrool[0], y* TREE_HEIGHT-scrool[1]))
            if tile != '0' and tile != '3':
                tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            x += 1
        y += 1
    
    #Movimento do player (Ainda com gravidade)
    player_movement = [0,0]
    if move_right:
        player_movement[0] += 1
    if move_left:
        player_movement[0] -= 1
    if move_up:
        player_movement[1] -= 1
    if move_down:
        player_movement[1] += 1
        
        #Gravidade e pulo
    #player_movement[1] += player_y_momentum
    #player_y_momentum += 0.2
    #if player_y_momentum > 3:
    #    player_y_momentum = 3

    #Verifica se o player colidiu com algum bloco
    player_rect, colisions = move(player_rect, player_movement, tile_rects)

    #Verifica se o player colidiu com o chão ou com o teto(Serve pra ele n ficar travado pulando em um bloco ou pulando sem chão)
    #if colisions['bottom']:
    #    player_y_momentum = 0
    #    air_timer = 0
        
        
    #else:
    #    air_timer += 1
        
    #if colisions['top']:
    #    player_y_momentum = 0


    #Desenha o player com a posição do player e efeito de camera
    display.blit(player, (player_rect.x-scrool[0], player_rect.y-scrool[1])) 
    

    #Movimentação do player
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                move_left = True
            if event.key == K_RIGHT:
                move_right = True
            if event.key == K_UP:
                move_up = True  
            if event.key == K_DOWN:
                move_down = True
                #O air timer define o tempo que o player leva pra pular novamente, quanto maior mais rapidamente ele pode pular
                # ele é somado a 1 (lnha 152), se colidir com o chão ele é resetado e o player pode pular de novo
            #    if air_timer < 5:  
            #        player_y_momentum = -5
            if event.key == K_z:
                reset = True
        if event.type == KEYUP:
            if event.key == K_LEFT:
                move_left = False
            if event.key == K_RIGHT:
                move_right = False
            if event.key == K_UP:
                move_up = False
                #Reset do player (z)
            if event.key == K_DOWN:
                move_down = False
            if event.key == K_z:
                reset = False
        #Reset do player (z)       
    if player_rect.y > WINDOW_SIZE[1] or reset == True:
        player_rect.x, player_rect.y = 100, 100
        #player_y_momentum = 1
        #air_timer = 0
        reset = False

    surf = pygame.transform.scale(display, WINDOW_SIZE)
    tela.blit(surf, (0,0))
    pygame.display.update()
    clock.tick(fps)