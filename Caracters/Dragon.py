import pygame
import sys, os
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class Dragon(pygame.sprite.Sprite):
    
    def __init__(self):
        self.name = 'Dragon'
        self.image = pygame.image.load(resource_path(f"assets/sprites/Ennemy/dragon1.png"))
        self.imagenbr = 0
        self.actual_image = 0
        self.rect = self.image.get_rect()
        self.rect.x = 500
        self.rect.y = -100

        self.avatar = pygame.image.load(resource_path(r"assets\sprites\dragon_head.png"))
        self.size_x, self.size_y = self.avatar.get_size()
        self.resize = 1
        self.avatar = pygame.transform.smoothscale(self.avatar, (round(self.size_x/self.resize),round(self.size_y/self.resize)))
        self.avatar_rect = self.avatar.get_rect()
        self.avatar_rect.y = 160
        self.avatar_rect.x = 20
        self.avatar_off = pygame.image.load(resource_path(r"assets\sprites\dragon_head_off.png"))
        self.avatar_off = pygame.transform.smoothscale(self.avatar_off, (round(self.size_x / self.resize), round(self.size_y / self.resize)))
        self.title = pygame.image.load(resource_path(r"assets\sprites\title_dragon.png"))
        self.size_x, self.size_y = self.title.get_size()
        self.title = pygame.transform.smoothscale(self.title, (round(self.size_x/1.3),round(self.size_y/1.3)))
        self.title_rect = self.title.get_rect()
        self.title_rect.y = 470
        self.title_rect.x = 40
