import pygame

from .board import GameBoard
from .util import load_music

class Game:
    def __init__(self, **kwargs):
        self.is_running = False
        self.is_loaded = True
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()

        pygame.display.set_caption("Pytris")
        self.screen_width = kwargs.get("screen_width", 651)
        self.screen_height = kwargs.get("screen_height", 651)
        self.clock = pygame.time.Clock()

    def __del__(self):
        self.is_loaded = False
        pygame.quit()

    def run(self):
        self.is_running = True
        pygame.mixer.music.set_volume(0.3)
        load_music('bg_music.ogg')
        board = GameBoard(self.screen_width, self.screen_height)
        board.initialize(pygame.time.get_ticks())
        while self.is_running:
            if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.play()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed() ==(1,0,0):
                        position = pygame.mouse.get_pos()
                        for buttons in board.buttons:
                            buttons.check_click(position)
                if event.type == pygame.QUIT:
                    self.is_running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.is_running = False
                    else:
                        board.register_game_key_down(event.key)
                if event.type == pygame.KEYUP:
                    board.register_game_key_up(event.key)
            board.update()
            pygame.display.flip()
