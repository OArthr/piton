import pygame, sys

from Player import Player

clock = pygame.time.Clock()

from pygame.locals import *
pygame.init()

WINDOW_SIZE = (1500,900)
screen = pygame.display.set_mode(WINDOW_SIZE)

pl_images = [pygame.image.load("p-sprites/p-idle1.png"),
             pygame.image.load("p-sprites/p-move1.png")]
for i in range(2):
    pl_images[i]=pygame.transform.scale(pl_images[i],[150,150])

moving,flipped = False,False


pl = Player(0,0,5,pl_images)

while True:
    screen.fill((0,0,0,0))
    pl.move(screen)

    for e in pygame.event.get():
        if e.type == QUIT:
            pygame.quit()
            sys.exit()

        if e.type == KEYDOWN:
            if e.key == K_w:
                pl.diry=-1
            if e.key == K_s:
                pl.diry=1
            if e.key == K_d:
                pl.dirx=1
                if flipped:
                    pl_images[1]=pygame.transform.flip(pl_images[1],True,False)
                    flipped = False
            if e.key == K_a:
                pl.dirx=-1
                if not flipped:
                    pl_images[1]=pygame.transform.flip(pl_images[1],True,False)
                    flipped = True
        if e.type == KEYUP:
            if e.key == K_w or e.key ==K_s:
                pl.diry=0
            if e.key == K_d or e.key == K_a:
                pl.dirx=0

    pygame.display.update()
    clock.tick(60)