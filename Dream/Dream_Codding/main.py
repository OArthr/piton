import pygame, sys
from settings import *
from level import Level

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption('Dream')
        self.clock = pygame.time.Clock()
        self.level = Level()

        # Estados do jogo
        self.state = "menu"  # Pode ser "menu", "tutorial" ou "jogo"

        # Fontes e textos pré-renderizados
        self.title_font = pygame.font.SysFont('System', 64)
        self.text_font = pygame.font.SysFont('System', 32)
        self.title_surf = self.title_font.render("Dream", True, 'white')
        self.start_surf = self.text_font.render("Pressione qualquer tecla para começar", True, 'white')

        # Dados de interação
        self.text = ''
        self.textbox = pygame.Rect(SCREEN_WIDTH // 2 - 100, 600, 200, 50)
        self.corAtivo = pygame.Color('red')
        self.corPassivo = pygame.Color('gray10')
        self.cor = self.corPassivo
        self.ativo = False
        self.score = 0

        # Respostas corretas
        self.respostas = {
            1: 'B',
            2: 'FVFV',
            3: 'C',
            4: 'O((N+M)LOGN)'
        }

    def draw_menu(self):
        self.screen.fill((30, 30, 30))
        title_rect = self.title_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(self.title_surf, title_rect)

        start_rect = self.start_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(self.start_surf, start_rect)

    def draw_tutorial(self):
        self.screen.fill((20, 20, 60))
        
        # Lista de linhas do tutorial
        tutorial_lines = [
            "Use W, A, S, D para mover e SHIFT para correr.",
            "Pressione ENTER para interagir com objetos.",
            "Evite obstáculos e colete itens para ganhar pontos.",
            "Pressione qualquer tecla para continuar."
        ]
        
        # Espaçamento entre linhas
        line_spacing = 40
        start_y = SCREEN_HEIGHT // 2 - (len(tutorial_lines) * line_spacing) // 2

        # Renderizar cada linha e desenhá-la na tela
        for i, line in enumerate(tutorial_lines):
            line_surf = self.text_font.render(line, True, 'white')
            line_rect = line_surf.get_rect(center=(SCREEN_WIDTH // 2, start_y + i * line_spacing))
            self.screen.blit(line_surf, line_rect)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if self.state == "menu":
                    self.state = "tutorial"
                elif self.state == "tutorial":
                    self.state = "jogo"

            if self.state == "jogo":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.textbox.collidepoint(event.pos):
                        self.ativo = True
                    else:
                        self.ativo = False

                if event.type == pygame.KEYDOWN and self.ativo:
                    if event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    elif event.key == pygame.K_RETURN:
                        self.score = 0
                        splitText = self.text.upper().split(',')
                        while len(splitText) < 4:
                            splitText.append('')
                        for i in self.respostas.keys():
                            if splitText[i - 1] == self.respostas[i]:
                                self.score += 1
                        print(self.score)
                    else:
                        self.text += event.unicode

    def run_game_logic(self):
        if self.ativo:
            self.cor = self.corAtivo
        else:
            self.cor = self.corPassivo

        dt = self.clock.tick(60) / 1000.0  # Limitar FPS para 60
        self.level.run(dt, self.ativo)

        textSurf = self.text_font.render(self.text, False, (0, 0, 0))
        scoreSurf = self.text_font.render(f"{self.score}/4", False, 'darkblue')
        self.textbox.x = self.screen.get_width() // 2 - self.textbox.w // 2
        self.textbox.y = self.screen.get_height() - 100
        pygame.draw.rect(self.screen, self.cor, self.textbox, 3)
        self.screen.blit(textSurf, (self.textbox.x + 5, self.textbox.y + 5))
        self.screen.blit(scoreSurf, (100, 100))

        self.textbox.w = max(200, textSurf.get_width() + 10)

    def run(self):
        while True:
            self.handle_events()

            if self.state == "menu":
                self.draw_menu()
            elif self.state == "tutorial":
                self.draw_tutorial()
            elif self.state == "jogo":
                self.run_game_logic()

            pygame.display.flip()  # Usar flip para melhorar desempenho

# Verifica se está no main
if __name__ == '__main__':
    game = Game()
    game.run()
