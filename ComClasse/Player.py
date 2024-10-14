import pygame, sys

class Player:
    def __init__(self,posx,posy,speed,images):
        self.moving = False
        self.images = images
        self.speed = speed
        self.dirx = 0
        self.diry = 0
        self.pos = [posx,posy]

    def move(self,screen):
        self.pos[0] += self.speed * self.dirx
        self.pos[1] += self.speed * self.diry
        if self.dirx!=0 or self.diry!=0:
            self.moving = True
        else:
            self.moving = False
        screen.blit(self.images[0] if not self.moving else self.images[1], self.pos)