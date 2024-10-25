import pygame
from settings import *
from player import Player 
from sprites import Generic, Objetos
from pytmx.util_pygame import load_pygame

class Level:

    def __init__(self):
        
        #Pega a superficie
        self.display_surface = pygame.display.get_surface()    
        self.all_sprites = CameraGroup()
        self.colisions_sprites = pygame.sprite.Group()

        self.setup()

    def setup(self):
        #Mapa
        tmx_data = load_pygame('Dream/Dream_Codding/Mapa/basico.tmx')

        #pegando as tiles da camada
        '''#No loop basta colocar o nome da camada(do tiled) por layer(uma ou mais de uma)
        for layer in ['Camada']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                #Aqui basta modificar a posição em que vai ser renderizada a imagem      AQUI (estão no arquivo settings.py)
                Generic((x * TILE_SIZE,y * TILE_SIZE), surf , self.all_sprites , LAYERS['layer'])'''

        for layer in ['Terreno']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x * TILE_SIZE,y * TILE_SIZE), surf , self.all_sprites , LAYERS['ground'])

        for layer in ['Agua']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x * TILE_SIZE,y * TILE_SIZE), surf , self.all_sprites , LAYERS['agua'])
        
        for layer in ['casa_chão']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x * TILE_SIZE,y * TILE_SIZE), surf , self.all_sprites , LAYERS['casa_chão'])
        for layer in ['Cerca']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x * TILE_SIZE,y * TILE_SIZE), surf , [self.all_sprites, self.colisions_sprites] , LAYERS['main'])
        for layer in ['Parede']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x * TILE_SIZE,y * TILE_SIZE), surf , self.all_sprites , LAYERS['main'])
        for layer in ['porta']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x * TILE_SIZE,y * TILE_SIZE), surf , self.all_sprites , LAYERS['main'])
        #Obejtos
        for obj in tmx_data.get_layer_by_name('Objetos'):
            Objetos((obj.x , obj.y), obj.image , [self.all_sprites, self.colisions_sprites])

        #Colisões
        for x, y, surf in tmx_data.get_layer_by_name('Colisões').tiles():
            Generic((x * TILE_SIZE,y * TILE_SIZE), pygame.Surface((TILE_SIZE, TILE_SIZE)) , self.colisions_sprites)

        #Inicio
        for obj in tmx_data.get_layer_by_name('Player'):
            if obj.name == 'Inicio':
                self.player = Player((obj.x , obj.y), self.all_sprites, self.colisions_sprites)



        # Generic(
        #     pos = (0, 0), 
        #     surf = pygame.image.load('Dream/Dream_Codding/grafico/grafico/ground.png').convert_alpha(), 
        #     groups = self.all_sprites,
        #     z = LAYERS['ground'])

    def run(self, dt):
        self.display_surface.fill('black')
        self.all_sprites.custom_draw(self.player)
        self.all_sprites.update(dt)

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2
            
        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)