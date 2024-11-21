import pygame, sys
from settings import *
from level import Level

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption('Dream') 
        # pygame_icon = pygame.image.load('Dream/Dream_Codding/grafico/Icon.png.png')
        # pygame.display.set_icon(pygame_icon)
        self.clock = pygame.time.Clock()
        self.level = Level()

    def run(self):
        respostas = {
            1: 'B',
            2: 'FVFV',
            3: 'C',
            4: 'O((N+M)LOGN)'
        }

        font = pygame.font.SysFont('System', 32)
        scoreFont = pygame.font.SysFont('System', 64)
        text = ''
        textbox = pygame.Rect(SCREEN_WIDTH // 2 - 100, 600, 200, 50)
        corAtivo = pygame.Color('red')
        corPassivo = pygame.Color('gray10')
        cor = corPassivo

        ativo = False
        score = 0

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if textbox.collidepoint(event.pos):
                        ativo = True
                    else:
                        ativo = False

                if event.type == pygame.KEYDOWN:
                    if ativo:
                        if event.key == pygame.K_BACKSPACE:
                            text = text[0:-1]
                        elif event.key == pygame.K_RETURN:
                            score = 0
                            splitText = text.upper().split(',')
                            while len(splitText) < 4:
                                splitText.append('')
                            for i in respostas.keys():
                                if splitText[i - 1] == respostas[i]:
                                    score += 1
                            print(score)
                        else:
                            text += event.unicode

            if ativo:
                cor = corAtivo
            else:
                cor = corPassivo

            dt = self.clock.tick() / 1000.0
            self.level.run(dt, ativo)

            textSurf = font.render(text, False, (0, 0, 0))
            scoreSurf = scoreFont.render(f"{score}/4", False, 'darkblue')
            textbox.x = self.screen.get_width() // 2 - textbox.w // 2
            textbox.y = self.screen.get_height() - 100
            pygame.draw.rect(self.screen, cor, textbox, 3)
            self.screen.blit(textSurf, (textbox.x + 5, textbox.y + 5))
            self.screen.blit(scoreSurf, (100, 100))

            textbox.w = max(200, textSurf.get_width() + 10)

            pygame.display.update()

# Verifica se está no main
if __name__ == '__main__':
    game = Game()
    game.run()
