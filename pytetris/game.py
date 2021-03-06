import pygame

from .board import GameBoard
from .config import defaults
from .util import load_music

class Game:
    LEFT_MOUSE_SEQUENCE_INDEX = 0

    def __init__(self, **kwargs):
        options = defaults.copy()
        options.update(kwargs)
        self.is_running = False
        self.is_loaded = True
        self.sound_on = options["sound_on"]
        self.game_over_display_time = options["game_over_display_time"]

        if self.sound_on:
            pygame.mixer.pre_init(
                options["mixer_frequency"],
                options["mixer_size"],
                options["mixer_channels"],
                options["mixer_buffer_size"]
            )
        pygame.init()
        pygame.joystick.init()

        [pygame.joystick.Joystick(x).init() for x in range(pygame.joystick.get_count())]

        if self.sound_on:
            load_music(options["music_file"])
            pygame.mixer.music.set_volume(options["mixer_volume_music"])

        pygame.display.set_caption("Pytris")
        if options["full_screen"]:
            options["display_flags"] = pygame.FULLSCREEN

        self.allow_restarts = options["allow_restarts"]

        self.clock = pygame.time.Clock()

        self.board = GameBoard(**options)

    def __del__(self):
        self.is_loaded = False
        del self.board
        pygame.joystick.quit()
        pygame.quit()

    def run(self):
        self.is_running = True
        self.board.initialize()

        while self.is_running:
            if self.sound_on:
                if not pygame.mixer.music.get_busy():
                        pygame.mixer.music.play()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[self.LEFT_MOUSE_SEQUENCE_INDEX] == 1 :
                        position = pygame.mouse.get_pos()
                        for buttons in self.board.buttons:
                            buttons.check_click(position)
                if event.type == pygame.QUIT:
                    self.is_running = False
                else:
                    self.__handle_game_event(event)

            self.board.update()
            pygame.display.flip()

            if self.board.game_over:
                pygame.time.wait(self.game_over_display_time)
                if not self.allow_restarts:
                    self.is_running == False

    def __handle_game_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.is_running = False
            else:
                self.board.register_game_key_down(event.key)
        if event.type == pygame.JOYAXISMOTION:
            if event.axis == 0:
                if event.value == 0.0:
                    self.board.register_game_key_up(pygame.K_RIGHT)
                    self.board.register_game_key_up(pygame.K_LEFT)
                elif abs(event.value - 1.0) < 0.001:
                    self.board.register_game_key_down(pygame.K_RIGHT)
                elif abs(event.value + 1.0) < 0.001:
                    self.board.register_game_key_down(pygame.K_LEFT)

            if event.axis == 1:
                if event.value == 0.0:
                    self.board.register_game_key_up(pygame.K_UP)
                    self.board.register_game_key_up(pygame.K_DOWN)
                elif abs(event.value - 1.0) < 0.001:
                    self.board.register_game_key_down(pygame.K_DOWN)
                elif abs(event.value + 1.0) < 0.001:
                    self.board.register_game_key_down(pygame.K_UP)

        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == 0 or event.button == 3:
                self.board.register_game_key_down(pygame.K_k)
            elif event.button == 2:
                self.board.register_game_key_down(pygame.K_i)
            elif event.button == 1:
                self.board.register_game_key_down(pygame.K_m)
            elif event.button == 4 or event.button == 5:
                self.board.register_game_key_down(pygame.K_UP)
            elif event.button == 6:
                self.is_running = False
            elif event.button == 7:
                self.board.register_game_key_down(pygame.K_p)

        if event.type == pygame.KEYUP:
            self.board.register_game_key_up(event.key)
