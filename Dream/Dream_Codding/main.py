import pygame, sys
from settings import *
from level import Level

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Dream') 
        pygame_icon = pygame.image.load('Dream/Dream_Codding/grafico/Icon.png.png')
        pygame.display.set_icon(pygame_icon)
        self.clock = pygame.time.Clock()
        self.level = Level()


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            
            dt = self.clock.tick() / 1000.0
            self.level.run(dt)
            pygame.display.update()

#Verifica se está no main
if __name__ == '__main__':
    game = Game()
    game.run()