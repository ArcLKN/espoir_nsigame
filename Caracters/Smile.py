import pygame
import sys, os
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class Smile(pygame.sprite.Sprite):
    
    def __init__(self):
        self.name = 'Lame'
        self.image = pygame.image.load(resource_path(f"assets\sprites\Lame\Front1.png"))
        self.imagenbr = 0
        self.actual_image = 0
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = -100

        self.avatar = pygame.image.load(resource_path(r"assets\sprites\Talk_Icon\Lame\1-1-1.png"))
        self.size_x, self.size_y = self.avatar.get_size()
        self.avatar = pygame.transform.smoothscale(self.avatar, (round(self.size_x/1.3),round(self.size_y/1.3)))
        self.avatar_rect = self.avatar.get_rect()
        self.avatar_rect.y = 60
        self.avatar_off = pygame.image.load(resource_path(r"assets\sprites\Talk_Icon\Lame\1-0-1.png"))
        self.avatar_off = pygame.transform.smoothscale(self.avatar_off, (round(self.size_x / 1.3), round(self.size_y / 1.3)))
        self.title = pygame.image.load(resource_path(r"assets\sprites\Talk_Icon\Lame\title_lame.png"))
        self.size_x, self.size_y = self.title.get_size()
        self.title = pygame.transform.smoothscale(self.title, (round(self.size_x/1.3),round(self.size_y/1.3)))
        self.title_rect = self.title.get_rect()
        self.title_rect.y = 470
        self.title_rect.x = 40

    def downanimate(self):
        self.imagenbr = 2
        if self.actual_image == self.imagenbr:
            self.actual_image = 0
            self.image = pygame.image.load(resource_path(f"assets\sprites\Lame\Front{self.actual_image + 1}.png"))
        else:
            self.image = pygame.image.load(resource_path(f"assets\sprites\Lame\Front{self.actual_image+1}.png"))
            self.actual_image += 1

    def avataranimate(self):
        self.imagenbr = 2
        if self.actual_image == self.imagenbr:
            self.actual_image = 0
            self.avatar = pygame.image.load(resource_path(rf"assets\sprites\Talk_Icon\Lame\1-1-{self.actual_image + 1}.png"))
        else:
            self.avatar = pygame.image.load(resource_path(rf"assets\sprites\Talk_Icon\Lame\1-1-{self.actual_image + 1}.png"))
            self.actual_image += 1
        self.size_x, self.size_y = self.avatar.get_size()
        self.avatar = pygame.transform.smoothscale(self.avatar, (round(self.size_x / 1.3), round(self.size_y / 1.3)))
