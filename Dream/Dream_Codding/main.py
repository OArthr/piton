import pygame, sys
from pygame.locals import *

# Tamanho total do mapa
WINDOW_SIZE = (1280, 720)

# Tamanho da tela
display = pygame.Surface((300, 200))
tela = pygame.display.set_mode((WINDOW_SIZE), 0, 32)

# FPS
clock = pygame.time.Clock()
fps = 60

# Inicia o pygame
pygame.display.set_caption('Projeto Pygame')
pygame.init()

# Carregamento de imagens do cenário

grass_img = pygame.image.load('Dream/Dream_Codding/IMGs/grass.png')
dirt_img = pygame.image.load('Dream/Dream_Codding/IMGs/dirt.png')
dirt_img = pygame.transform.scale(dirt_img, (16, 16))
floor_img = pygame.image.load('Dream/Dream_Codding/IMGs/floor.png')
floor_img = pygame.transform.scale(floor_img, (16, 16))
back_img = pygame.image.load('Dream/Dream_Codding/IMGs/floorgrass.png')
back_img = pygame.transform.scale(back_img, (600, 400))
arvore_img = pygame.image.load('Dream/Dream_Codding/IMGs/arvore.png')
arvore_img = pygame.transform.scale(arvore_img, (16, 16))
arvore2_img = pygame.image.load('Dream/Dream_Codding/IMGs/arvore2.png')
arvore2_img = pygame.transform.scale(arvore2_img, (16, 16))

# Colisão Player

player_rect = pygame.Rect(50,50, 16, 16)  # Reduzir o tamanho do retângulo do player

# Tamanho do bloco(bloco de 1x1px)
TILE_SIZE = grass_img.get_width()
TREE_WIDTH = arvore_img.get_width()
TREE_HEIGHT = arvore_img.get_height()

# Carrega o mapa
def load_map(path):
    with open(path + '.txt', 'r') as f:
        data = f.read().split('\n')
    game_map = [list(row) for row in data]
    return game_map

# Carregar animações
animation_frames = {}

def load_animation(path, frame_durations):
    global animation_frames
    animation_frame_data = []
    n = 0
    for frame in frame_durations:
        animation_frame_id = path.split('/')[-1] + '_' + str(n)
        img_loc = f'{path}/{animation_frame_id}.png'
        animation_image = pygame.image.load(img_loc).convert_alpha()
        # Redimensionar a imagem do personagem
        animation_image = pygame.transform.scale(animation_image, (35, 23))
        animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data

def change_action(action_var, frame, new_value):
    if action_var != new_value:
        action_var = new_value
        frame = 0
    return action_var, frame

# Carregar animações de correr e ociosidade
animation_database = {
    'run': load_animation('Dream/Dream_Codding/player_animations/run', [7, 7, 7, 7, 7, 7]),
    'idle': load_animation('Dream/Dream_Codding/player_animations/idle', [7, 7, 7, 7, 40])
}

player_action = 'idle'
player_frame = 0
player_flip = False

# Carrega o mapa
game_map = load_map('Dream/Dream_Codding/Mapa/aaaa copy')

# Variáveis de movimento
move_right = False
move_left = False
move_up = False
move_down = False
reset = False

# Funções de colisão
def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

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

# Ajuste: definir a posição inicial do player dentro do mapa
player_start_x = 80  # Ajuste conforme o tamanho do mapa
player_start_y = 55  # Ajuste conforme o tamanho do mapa
player_rect.x = player_start_x
player_rect.y = player_start_y

# Variáveis de rolagem da câmera
true_scroll = [0, 0]

while True:
    display.fill((37,19,26))  # Cor de fundo do céu
    
    # Ajuste: Cálculo da rolagem da câmera com base na posição do jogador
    true_scroll[0] += (player_rect.x - true_scroll[0] - 152) / 20
    true_scroll[1] += (player_rect.y - true_scroll[1] - 106) / 10
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    # Desenha o mapa
    y = 0
    tile_rects = []
    for row in game_map:
        x = 0
        for tile in row:
            if tile == '1':
                display.blit(dirt_img, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
            if tile == '2':
                display.blit(grass_img, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
            if tile == '3':
                display.blit(floor_img, (x * TILE_SIZE - scroll[0], y * TILE_SIZE - scroll[1]))
            if tile == '4':
                display.blit(arvore_img, (x * TREE_WIDTH - scroll[0], y * TREE_HEIGHT - scroll[1]))
            if tile == '5':
                display.blit(arvore2_img, (x * TREE_WIDTH - scroll[0], y * TREE_HEIGHT - scroll[1]))
            if tile != '0' and tile != '3':
                tile_rects.append(pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                
            x += 1
        y += 1

    # Movimento do player
    player_movement = [0, 0]
    if move_right:
        player_movement[0] += 2
    if move_left:
        player_movement[0] -= 2
    if move_up:
        player_movement[1] -= 2
    if move_down:
        player_movement[1] += 2

    if player_movement[0] > 0:
        player_action, player_frame = change_action(player_action, player_frame, 'run')
        player_flip = False
    elif player_movement[0] < 0:
        player_action, player_frame = change_action(player_action, player_frame, 'run')
        player_flip = True
    else:
        player_action, player_frame = change_action(player_action, player_frame, 'idle')

    # Atualiza posição e verifica colisão
    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    # Desenhar o player
    player_frame += 1
    if player_frame >= len(animation_database[player_action]):
        player_frame = 0
    player_img_id = animation_database[player_action][player_frame]
    player_img = animation_frames[player_img_id]
    display.blit(pygame.transform.flip(player_img, player_flip, False), 
                 (player_rect.x-7 - scroll[0], player_rect.y-7 - scroll[1]))

    # Eventos de input do jogador
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
            if event.key == K_z:
                reset = True
        if event.type == KEYUP:
            if event.key == K_LEFT:
                move_left = False
            if event.key == K_RIGHT:
                move_right = False
            if event.key == K_UP:
                move_up = False
            if event.key == K_DOWN:
                move_down = False
            if event.key == K_z:
                reset = False

    # Redefine a posição do player se sair da tela ou for resetado
    if player_rect.y > WINDOW_SIZE[1] or reset:
        player_rect.x, player_rect.y = player_start_x, player_start_y
        reset = False

    # Atualizar a tela
    surf = pygame.transform.scale(display, WINDOW_SIZE)
    tela.blit(surf, (0, 0))
    pygame.display.update()
    clock.tick(fps)