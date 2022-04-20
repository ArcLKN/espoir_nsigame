# coding: utf8
import pygame
import math
import sys, os
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class StartMenu():

    def __init__(self, game):
        super().__init__()
        self.game = game

        self.is_playing = False
        self.is_start_menu = False
        self.is_escape_menu = False
        self.is_option_menu = False
        self.is_shop_menu = False

        self.play_button_rect = None
        self.option_button_rect = None
        self.quit_button_rect = None

        self.sound_cursor = pygame.image.load(resource_path("assets/sound_cursor.jpg"))
        self.sound_cursor_size_x, self.sound_cursor_size_y = self.sound_cursor.get_size()
        self.sound_cursor = pygame.transform.smoothscale(self.sound_cursor,
                                                    (round(self.sound_cursor_size_x / 6), round(self.sound_cursor_size_y / 6)))
        self.sound_cursor_rect = self.sound_cursor.get_rect()
        self.sound_cursor_rect.x = 650
        self.sound_cursor_is_following = False

        self.escape_play_button_rect = None
        self.escape_option_button_rect = None

        def game_stop(self):  # Stop le jeu
            if self.key == pygame.K_ESCAPE:  # Si la touche échap est pressée
                if self.is_escape_menu:  # Si il y a déjà la touche échap
                    self.is_escape_menu = False  # désactive le menu échap
                    self.is_playing = True  # active le jeu
                elif self.is_playing:  # sinon
                    self.is_escape_menu = True
                    self.is_playing = False
            elif self.key == pygame.K_i:
                if not self.is_escape_menu and self.is_playing:
                    self.is_playing = False
            else:
                self.is_playing = False

    def start_menu(self, screen):
        play_button = pygame.image.load(resource_path("assets\play_button.png"))
        size_x,size_y = play_button.get_size()
        play_button = pygame.transform.smoothscale(play_button, [round(size_x/1.5), round(size_y/1.5)])
        self.play_button_rect = play_button.get_rect()
        self.play_button_rect.x = 150
        self.play_button_rect.y = 230

        option_button = pygame.image.load(resource_path("assets\option_button.png"))
        size_x, size_y = option_button.get_size()
        option_button = pygame.transform.smoothscale(option_button, [round(size_x/1.5), round(size_y/1.5)])
        self.option_button_rect = option_button.get_rect()
        self.option_button_rect.x = 150
        self.option_button_rect.y = 360

        quit_button = pygame.image.load(resource_path("assets\quit_button.png"))
        size_x, size_y = quit_button.get_size()
        quit_button = pygame.transform.smoothscale(quit_button, [round(size_x/1.5), round(size_y/1.5)])
        self.quit_button_rect = quit_button.get_rect()
        self.quit_button_rect.x = 150
        self.quit_button_rect.y = 490

        screen.blit(quit_button, self.quit_button_rect)
        screen.blit(play_button, self.play_button_rect)
        screen.blit(option_button, self.option_button_rect)

    def escape_menu(self, screen):  # Menu échap
        play_button = pygame.image.load(resource_path("assets\play_button.png"))
        size_x,size_y = play_button.get_size()
        play_button = pygame.transform.smoothscale(play_button, [round(size_x/2), round(size_y/2)])
        self.play_button_rect = play_button.get_rect()
        self.play_button_rect.x = pygame.display.Info().current_w / 2 - 140
        self.play_button_rect.y = 200

        option_button = pygame.transform.smoothscale(pygame.image.load(resource_path("assets\dark_option_button.png")), [300, 90])
        self.option_button_rect = option_button.get_rect()
        self.option_button_rect.x = math.floor(pygame.display.Info().current_w / 2 - 290 / 2)
        self.option_button_rect.y = math.floor(pygame.display.Info().current_w / 2 - 800 / 2)

        quit_button = pygame.transform.smoothscale(pygame.image.load(resource_path("assets\dark_button.png")), [300, 90])
        self.quit_button_rect = quit_button.get_rect()
        self.quit_button_rect.x = math.floor(pygame.display.Info().current_w / 2 - 290 / 2)
        self.quit_button_rect.y = math.floor(pygame.display.Info().current_w / 2 - 500 / 2)

        screen.blit(play_button, self.play_button_rect)
        screen.blit(option_button, self.option_button_rect)
        screen.blit(quit_button, self.quit_button_rect)

    def option_menu(self,screen, mouse_x):
        if self.is_escape_menu:
            self.is_option_menu = False
        option_menu_bg = pygame.image.load(resource_path("assets/option_menu.png"))
        option_menu_bg_rect = option_menu_bg.get_rect()
        option_menu_bg_rect.x = 450
        option_menu_bg_rect.y = 100
        self.sound_cursor_rect.y = 260
        sound_bar = pygame.image.load(resource_path("assets/sound_bar.jpg"))
        self.sound_bar_rect = sound_bar.get_rect()
        self.sound_bar_rect.x = 475
        self.sound_bar_rect.y = 280

        if self.sound_cursor_is_following:
            if 400 < self.sound_cursor_rect.x < 1000:
                self.sound_cursor_rect.x = mouse_x
        else:
            if self.sound_cursor_rect.x <= 480:
                self.sound_cursor_rect.x = 480
            if self.sound_cursor_rect.x >= 950:
                self.sound_cursor_rect.x = 950


        screen.blit(option_menu_bg,option_menu_bg_rect)
        screen.blit(sound_bar, self.sound_bar_rect)
        screen.blit(self.sound_cursor, self.sound_cursor_rect)

    def shop_menu(self,screen):
        pass
