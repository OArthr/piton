
import pygame
from settings import *
from support import *

class Player(pygame.sprite.Sprite):

    def __init__(self, pos, group):
        super().__init__(group)

        self.import_assets()
        self.status = 'down_idle'
        self.frame_index = 0

        self.image = self.animations[self.status][self.frame_index]#inicia o player
        self.rect = self.image.get_rect(center=pos)#rect do player

        #Movimento
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

        #Teclas
    def input(self):
    
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_s]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0
            

        if keys[pygame.K_a]:
            self.direction.x = -1
            self.status = 'left'
        elif keys[pygame.K_d]:
            self.direction.x = 1
            self.status = 'right'
            
        else:
            self.direction.x = 0

    #movimentaçao
    def move(self, dt):
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()#normaliza a velocidade em diagonais

        #posiçao horizontal
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.pos.x
        #posiçao vertical
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = self.pos.y
       
    def import_assets(self):
        self.animations = {'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle': [], 'up': [], 'down': [], 'left': [], 'right': []}

        for animation in self.animations.keys():
            full_path = 'Dream/Dream_Codding/grafico/movimento/'+animation
            self.animations[animation] = import_folder(full_path)

    def animate(self, dt):
        self.frame_index +=4*dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        
        self.image = self.animations[self.status][int(self.frame_index)]


    
        
    def get_status(self):
        if self.direction.magnitude() == 0  :
            self.status = self.status.split('_')[0] + '_idle'

    
    

    #atualizaçao
    def update(self, dt):
        self.input()
        self.get_status()
        self.move(dt)
        self.animate(dt)
            


 