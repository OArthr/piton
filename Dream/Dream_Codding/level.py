import pygame
from settings import *
from player import Player 
from sprites import Generic, Objetos
from pytmx.util_pygame import load_pygame

class Level:

    def __init__(self):
        # Carregar uma imagem
        self.image = pygame.image.load('Dream/Dream_Codding/Mapa/tilesets/DREAMCODE mapa.png').convert_alpha()
        #Pega a superficie
        # Mostrar a imagem na tela
        
        self.display_surface = pygame.display.get_surface()    
        self.all_sprites = CameraGroup()
        self.colisions_sprites = pygame.sprite.Group()
        

        self.setup()

        #musica
        self.music = pygame.mixer.Sound('Dream/Dream_Codding/Audio/this-isnx27t-the-radio-i-listen-before-248595.mp3')
        self.music.play(loops = -1)
        self.music.set_volume(0.1)

            

    def setup(self):
        #Mapa
        tmx_data = load_pygame('Dream/Dream_Codding/Mapa/tilesets/DREAMCODE mapa.tmx')

        #pegando as tiles da camada
        '''#No loop basta colocar o nome da camada(do tiled) por layer(uma ou mais de uma)
        for layer in ['Camada']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                #Aqui basta modificar a posição em que vai ser renderizada a imagem      AQUI (estão no arquivo settings.py)
                Generic((x * TILE_SIZE,y * TILE_SIZE), surf , self.all_sprites , LAYERS['layer'])'''

            # for layer in ['chão']:
            #     for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
            #         Generic((x * TILE_SIZE,y * TILE_SIZE), surf , self.all_sprites , LAYERS['ground'])

        # for layer in ['mar']:
        #     for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
        #         Generic((x * TILE_SIZE,y * TILE_SIZE), surf , self.all_sprites , LAYERS['agua'])
        
        # for layer in ['casa_chão']:
        #     for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
        #         Generic((x * TILE_SIZE,y * TILE_SIZE), surf , self.all_sprites , LAYERS['casa_chão'])
        # for layer in ['Cerca']:
        #     for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
        #         Generic((x * TILE_SIZE,y * TILE_SIZE), surf , [self.all_sprites, self.colisions_sprites] , LAYERS['main'])
        # for layer in ['paredes']:
        #     for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
        #         Generic((x * TILE_SIZE,y * TILE_SIZE), surf , self.all_sprites , LAYERS['main'])
        # for layer in ['porta']:
        #     for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
        #         Generic((x * TILE_SIZE,y * TILE_SIZE), surf , self.all_sprites , LAYERS['main'])
        #Obejtos
        for obj in tmx_data.get_layer_by_name('objetos'):
            obj_image = pygame.transform.scale(obj.image, (int(obj.width), int(obj.height)))
            Objetos((obj.x , obj.y), obj_image , self.all_sprites, z=LAYERS['main'])
        
        for obj in tmx_data.get_layer_by_name('mar'):
             Objetos((obj.x , obj.y), obj.image , self.all_sprites, z=LAYERS['agua'])

        #Colisões
        for x, y, surf in tmx_data.get_layer_by_name('Colisões').tiles():
            Generic((x * TILE_SIZE,y * TILE_SIZE), pygame.Surface((TILE_SIZE, TILE_SIZE)) , self.colisions_sprites)
            
        for obj in tmx_data.get_layer_by_name('obj colisão'):
            obj_image = pygame.transform.scale(obj.image, (int(obj.width), int(obj.height)))
            Objetos((obj.x , obj.y), obj_image ,self.colisions_sprites, z=LAYERS['main'])

        #Inicio
        for obj in tmx_data.get_layer_by_name('Entidades'):
            if obj.name == 'Inicio':
                self.player = Player((obj.x , obj.y), self.all_sprites, self.colisions_sprites)
        
        for obj in tmx_data.get_layer_by_name('Textos'):
             Objetos((obj.x , obj.y), obj.image , self.all_sprites, z=LAYERS['texts'])
            




        # Generic(
        #     pos = (0, 0), 
        #     surf = pygame.image.load('Dream/Dream_Codding/grafico/grafico/ground.png').convert_alpha(), 
        #     groups = self.all_sprites,
        #     z = LAYERS['ground'])

    def run(self, dt,ativo):
        self.display_surface.fill('blue')
        self.all_sprites.custom_draw(self.player)
        self.all_sprites.update(dt,ativo)
        


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

        self.zoom_scale = 3
        self.inter_surf_size = pygame.display.get_surface().get_size()
        self.inter_surf = pygame.Surface(self.inter_surf_size, pygame.SRCALPHA)
        self.inter_surf_size_vect = pygame.math.Vector2(self.inter_surf_size)

    
    def zoom(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q] and self.zoom_scale < 5:
            self.zoom_scale += .1
        if keys[pygame.K_e] and self.zoom_scale > 3:
            self.zoom_scale -= .1

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - SCREEN_WIDTH // 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT // 2
        
        self.zoom()

        self.inter_surf.fill('#3a3f5e')

            
        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.inter_surf.blit(sprite.image, offset_rect)
                
        scaled_surf = pygame.transform.scale(self.inter_surf,self.inter_surf_size_vect * self.zoom_scale)
        scaled_rect = scaled_surf.get_rect(center = (self.display_surface.get_size()[0]//2,self.display_surface.get_size()[1]//2))

        self.display_surface.blit(scaled_surf,scaled_rect)
