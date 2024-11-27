import pygame
import sys
from button import Button
from settings import *
from level import Level

pygame.init()

class Game:
    def __init__(self):
        # Configurações de tela
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Dream")
        self.clock = pygame.time.Clock()
        self.level = Level()

        # Estados do jogo
        self.state = "menu"  # Pode ser "menu", "tutorial", ou "jogo"

        # Fonte e plano de fundo do menu
        self.font_path = "Dream/Dream_Codding/assets/font.ttf"
        self.background = pygame.image.load("Dream/Dream_Codding/bg1.png").convert()
        self.background_scaled = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Músicas
        self.menu_tutorial_music = "Dream/Dream_Codding/Audio/Anemoia - Chimeric.mp3"  # Música para menu e tutorial
        self.game_music = "Dream/Dream_Codding/Audio/Bggm.mp3"  # Música para o jogo
        self.current_music = None  # Controle da música atual
        self.play_music(self.menu_tutorial_music)

        # Caixa de texto para respostas
        self.text = ''
        self.textbox_height = 50  # Altura fixa da caixa de texto
        self.textbox_width = 200  # Largura inicial
        self.max_textbox_width = 450  # Largura máxima da caixa de texto
        self.textbox = pygame.Rect(SCREEN_WIDTH // 2 - self.textbox_width // 2, SCREEN_HEIGHT - 100, self.textbox_width, self.textbox_height)
        self.corAtivo = pygame.Color('green')  # Cor verde quando ativo
        self.corPassivo = pygame.Color('gray10')  # Cor original
        self.cor = self.corPassivo
        self.ativo = False
        self.score = 0
        self.score_max = 4  # Máxima pontuação
        self.pontuacao_acertada = False  # Flag para piscar em verde ao acertar
        self.pontuacao_acertada_time = 0  # Temporizador para o efeito de piscar

        # Respostas corretas
        self.respostas = {
            1: 'B',
            2: 'FVFV',
            3: 'C',
            4: 'O((N+M)LOGN)'
        }

    def play_music(self, music_path):
        """Troca a música de fundo se necessário."""
        if self.current_music != music_path:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(-1)  # Loop infinito
            self.current_music = music_path

    def get_font(self, size):
        """Carrega a fonte personalizada no tamanho especificado."""
        return pygame.font.Font(self.font_path, size)

    def scale_background(self):
        """Redimensiona o plano de fundo para o tamanho atual da janela."""
        self.background_scaled = pygame.transform.scale(self.background, (self.screen.get_width(), self.screen.get_height()))

    def draw_textbox(self):
        """Desenha a caixa de texto com bordas arredondadas e sombra. A caixa de texto se adapta ao tamanho do texto digitado."""
        
        # Atualizar o tamanho da caixa de texto com base no comprimento do texto digitado
        text_length = len(self.text)
        self.textbox.width = min(self.max_textbox_width, max(200, 21 * text_length))  # Ajuste de largura (21 pixels por caractere, com limites)

        shadow_rect = self.textbox.inflate(10, 10)  # Efeito de sombra
        pygame.draw.rect(self.screen, "gray", shadow_rect, border_radius=15)  # Sombra preta
        pygame.draw.rect(self.screen, self.cor, self.textbox, 3, border_radius=15)  # Caixa com borda arredondada

        # Definir a cor da letra
        text_color = ("gray15")  # Cor para o texto

        # Diminuir o tamanho da fonte para 12
        text_surf = self.get_font(20).render(self.text, False, text_color)
        self.screen.blit(text_surf, (self.textbox.x + 5, self.textbox.y + 5))  # Texto dentro da caixa

    def draw_score(self):
        """Exibe a pontuação com efeito de piscar em verde ao acertar."""
        # Determinar a cor da pontuação
        if self.pontuacao_acertada:
            if pygame.time.get_ticks() - self.pontuacao_acertada_time < 500:  # Piscar por 500ms
                score_color = (0, 255, 0)  # Verde
            else:
                self.pontuacao_acertada = False  # Terminar o efeito de piscar
                score_color = (255, 255, 255)  # Branco padrão
        else:
            score_color = (255, 255, 255)  # Branco padrão

        # Renderizar a pontuação
        score_text = self.get_font(20).render(f"Pontuação: {self.score}/{self.score_max}", True, score_color)
        score_rect = score_text.get_rect(topleft=(10, 10))
        self.screen.blit(score_text, score_rect)

    def draw_menu(self):
        """Exibe o menu principal com botões."""
        self.play_music(self.menu_tutorial_music)  # Trocar para música do menu e tutorial
        while self.state == "menu":
            self.scale_background()
            self.screen.blit(self.background_scaled, (0, 0))
            menu_mouse_pos = pygame.mouse.get_pos()

            # Texto do menu
            menu_text = self.get_font(100).render("DREAMCODE", True, "#b68f40")
            menu_rect = menu_text.get_rect(center=(self.screen.get_width() // 2, 100))
            self.screen.blit(menu_text, menu_rect)

            # Botões
            play_button = Button(
                image=pygame.image.load("Dream/Dream_Codding/assets/Play Rect.png"),
                pos=(self.screen.get_width() // 2, 250),
                text_input="PLAY",
                font=self.get_font(55),
                base_color="#d7fcd4",
                hovering_color="White",
            )
            options_button = Button(
                image=pygame.image.load("Dream/Dream_Codding/assets/Options Rect.png"),
                pos=(self.screen.get_width() // 2, 400),
                text_input="TUTORIAL",
                font=self.get_font(55),
                base_color="#d7fcd4",
                hovering_color="White",
            )
            quit_button = Button(
                image=pygame.image.load("Dream/Dream_Codding/assets/Quit Rect.png"),
                pos=(self.screen.get_width() // 2, 550),
                text_input="QUIT",
                font=self.get_font(55),
                base_color="#d7fcd4",
                hovering_color="White",
            )

            # Atualizar cores e exibir botões
            for button in [play_button, options_button, quit_button]:
                button.changeColor(menu_mouse_pos)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.checkForInput(menu_mouse_pos):
                        self.state = "inicio"
                        return pygame.time.get_ticks()
                    if options_button.checkForInput(menu_mouse_pos):
                        self.state = "tutorial"
                        return
                    if quit_button.checkForInput(menu_mouse_pos):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()

    def draw_tutorial(self):
        """Exibe a tela de tutorial com texto informativo."""
        self.play_music(self.menu_tutorial_music)  # Trocar para música do menu e tutorial
        while self.state == "tutorial":
            self.screen.fill("black")
            tutorial_lines = [
                "Bem-vindo ao dream_Code!",
                "Um jogo educativo de programação e algoritimos.",
                "Use W, A, S, D para mover e SHIFT para correr.",
                "Explore o mapa e encontre os NPCs com as perguntas.",
                "Caso não saiba a resposta, procure dicas pelo cenário.",
                "As respostas devem ser escritas na caixa de resposta ",
                "na parte inferior da tela.",
                "No formato de uma lista (EX.: a,b,c,d).",
                "As respostas de cada pergunta ",
                "devem ser separadas por uma virgula",
                "e na ordem das questões.",
                "Cada resposta correta aumenta sua pontuação,",
                "mas uma resposta errada zera a pontuação.",
                "Pressione qualquer tecla para voltar ao menu.",
            ]
            line_spacing = 40
            start_y = self.screen.get_height() // 2 - (len(tutorial_lines) * line_spacing) // 2

            for i, line in enumerate(tutorial_lines):
                line_surf = self.get_font(22).render(line, True, 'darkgreen')
                line_rect = line_surf.get_rect(center=(self.screen.get_width() // 2, start_y + i * line_spacing))
                self.screen.blit(line_surf, line_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.state = "menu"
                    return

            pygame.display.update()


    def draw_cinematic(self,start_time):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if self.state == "inicio":
                        self.score = 0
                        self.text = ''
                        self.ativo = False
                        self.state = "jogo"
                        return
                    else:
                        self.state = "menu"
        if self.state == "inicio":
            if pygame.time.get_ticks() - start_time < 4000:
                imagem = pygame.image.load("Dream/Dream_Codding/cinematic/1.png")
                self.screen.blit(imagem,(0,0))
            elif pygame.time.get_ticks() -start_time< 10000:
                imagem = pygame.image.load("Dream/Dream_Codding/cinematic/2.png")
                self.screen.blit(imagem,(0,0))
            elif pygame.time.get_ticks() -start_time< 17000:
                imagem = pygame.image.load("Dream/Dream_Codding/cinematic/3.png")
                self.screen.blit(imagem,(0,0))
            elif pygame.time.get_ticks() -start_time< 20000:
                imagem = pygame.image.load("Dream/Dream_Codding/cinematic/4.png")
                self.screen.blit(imagem,(0,0))
            else:
                self.score = 0
                self.text = ''
                self.ativo = False
                self.state = "jogo"
        else:
            imagem = pygame.image.load("Dream/Dream_Codding/cinematic/5.png")
            self.screen.blit(imagem,(0,0))
        
        pygame.display.update()




    def run_game_logic(self):
        """Executa a lógica principal do jogo."""
        self.play_music(self.game_music)  # Trocar para música do jogo

        while self.state == "jogo":
            dt = self.clock.tick(60) / 1000.0
            self.level.run(dt, self.ativo)

            # Desenhar a caixa de texto com efeito
            self.draw_textbox()
            

            # Exibir pontuação
            self.draw_score()

            if self.score == 4:
                if pygame.time.get_ticks() - self.pontuacao_acertada_time>= 3000:
                    self.state = "fim"

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.textbox.collidepoint(event.pos):
                        self.ativo = True  # Ativar a caixa de texto
                        self.cor = self.corAtivo  # Mudar para verde
                    else:
                        self.ativo = False  # Desativar a caixa de texto
                        self.cor = self.corPassivo  # Voltar para a cor original
                if event.type == pygame.KEYDOWN:
                    if self.ativo:
                        if event.key == pygame.K_BACKSPACE:
                            self.text = self.text[:-1]  # Remover o último caractere
                        elif event.key == pygame.K_RETURN:
                            # Calcular pontuação com base nas respostas
                            splitText = self.text.upper().split(',')
                            while len(splitText) < 4:
                                splitText.append('')
                            correct_answers = 0
                            for i in self.respostas.keys():
                                if splitText[i - 1] == self.respostas[i]:
                                    correct_answers += 1

                            self.score = correct_answers  # Atualiza a pontuação baseada nas respostas corretas

                            # Ativar efeito de piscar em verde ao acertar
                            if self.score > 0:
                                self.pontuacao_acertada = True
                                self.pontuacao_acertada_time = pygame.time.get_ticks()

                            print(self.score)
                        elif self.textbox.width != self.max_textbox_width:
                            self.text += event.unicode  # Adicionar caracteres à caixa de texto
                        
                            
            pygame.display.update()

    def run(self):
        """Gerencia os diferentes estados do jogo."""
        start_time = 0
        while True:
            if self.state == "menu":
                start_time = self.draw_menu()
            elif self.state == "tutorial":
                self.draw_tutorial()
            elif self.state == "inicio" or self.state == "fim":
                self.draw_cinematic(start_time)
            elif self.state == "jogo":
                self.run_game_logic()


# Executar o jogo
if __name__ == '__main__':
    game = Game()
    game.run()
