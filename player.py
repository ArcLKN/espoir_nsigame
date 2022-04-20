# coding: utf8
import pygame, math
from projectile import Projectile
import sys, os
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# gérer les collisions entre un sprite et un groupe
def collide_with(sprite, group, direction):
    if direction == "x":
        colisions = pygame.sprite.spritecollide(sprite, group, False)
        if colisions:
            for object in colisions:
                if object == sprite:
                    colisions.remove(object)
            if colisions:
                if sprite.vx > 0:
                    sprite.rect.x = colisions[0].rect.left - sprite.rect.width
                if sprite.vx < 0:
                    sprite.rect.x = colisions[0].rect.right
                sprite.vx = 0
    if direction == "y":
        colisions = pygame.sprite.spritecollide(sprite, group, False)
        if colisions:
            for object in colisions:
                if object == sprite:
                    colisions.remove(object)
            if colisions:
                if sprite.vy > 0:
                    sprite.rect.y = colisions[0].rect.top - sprite.rect.height
                if sprite.vy < 0:
                    sprite.rect.y = colisions[0].rect.bottom
                sprite.vy = 0

# gérer les coeurs (franchement cpa très utile mais bon)
class Health(pygame.sprite.Sprite):

    def __init__(self):
        super(Health, self).__init__()
        self.image = pygame.image.load(resource_path("assets/coeur.png"))
        self.image = pygame.transform.smoothscale(self.image,(40,40))
        self.rect = self.image.get_rect()
        self.rect.y = 30

# aussi gérer les coeurs (de moins en moins utile)
class MaxHealth(pygame.sprite.Sprite):

    def __init__(self):
        super(MaxHealth, self).__init__()
        self.image = pygame.image.load(resource_path("assets/empty_coeur.png"))
        self.image = pygame.transform.smoothscale(self.image,(40,40))
        self.rect = self.image.get_rect()
        self.image.set_alpha(100)
        self.rect.y = 30

class Player(pygame.sprite.Sprite):

    def __init__(self,game):
        super().__init__()
        self.game = game
        self.image = pygame.image.load(resource_path("assets\player.png"))
        self.size_x,self.size_y = self.image.get_size()
        self.rect = self.image.get_rect()
        self.image = pygame.transform.smoothscale(self.image,(int(self.size_x/1920*1536),int(self.size_x/1920*1536)))
        self.size_x,self.size_y = self.image.get_size()
        self.rect.x = pygame.display.Info().current_w / 2 - self.size_x / 2 + 1000
        self.rect.y = pygame.display.Info().current_h / 2 - self.size_y / 2 + 1000

        self.avatar = pygame.image.load(resource_path(r"assets\sprites\Talk_Icon\Player\0-1.png"))
        self.size_x, self.size_y = self.avatar.get_size()
        self.avatar = pygame.transform.smoothscale(self.avatar, (round(self.size_x/1.3),round(self.size_y/1.3)))
        self.avatar_rect = self.avatar.get_rect()
        self.avatar_rect.y = 85  # 60
        self.avatar_rect.x = 1000  # 1000
        self.avatar_off = pygame.image.load(resource_path(r"assets\sprites\Talk_Icon\Player\0-0.png"))
        self.avatar_off = pygame.transform.smoothscale(self.avatar_off, (round(self.size_x / 1.3), round(self.size_y / 1.3)))
        self.title = pygame.image.load(resource_path(r"assets\sprites\Talk_Icon\Player\title_player.png"))
        self.size_x, self.size_y = self.title.get_size()
        self.title = pygame.transform.smoothscale(self.title, (round(self.size_x/1.3),round(self.size_y/1.3)))
        self.title_rect = self.title.get_rect()
        self.title_rect.y = 470
        self.title_rect.x = 1000

        self.player_global_size = 3.7  # nombre par lequel la taille du joueur est divisé. Valeur initiale = 3.7

        self.fireball_sound = pygame.mixer.Sound(resource_path(r'assets\Sound\fireA.wav'))
        self.fireball_sound.set_volume(0.2)  # Valeur initiale = 0.2

        self.way = '+'
        self.rotation = int(0)

        self.max_health = 10  # Santé maximum du joueur. Valeur initiale = 10
        self.health = 10  # Santé actuelle du joueur. Valeur initiale = 10
        self.invincibility_time = 10  # Temps d'invincibilité après dégat. Valeur initiale = 10
        self.invincibility_countdown = 0

        self.pressed = {}
        self.all_projectiles = pygame.sprite.Group()

        self.money = 0  # Argent du joueur. Valeur initiale = 0

        self.fly_liquids = False

        self.velocity = 10  # Vitesse du joueur. Valeur initiale = 10
        self.vx = 0
        self.vy = 0

        self.speed_projectile_x = 0
        self.speed_projectile_y = 0

        self.projectile = Projectile(self)

    def rotate(self):
        if self.way == '+':
            self.rotation = self.rotation + 1
        elif self.way == '-':
            self.rotation = self.rotation - 1
        if self.rotation >= 5:
            self.way = '-'
        elif self.rotation <= -5:
            self.way = '+'
        self.image = pygame.transform.rotate(self.image,(self.rotation))
        for e in self.game.all_player:
            e.image = self.image

    def move_right(self):
        self.rect.x += self.velocity
        if pygame.sprite.spritecollideany(self, self.game.all_entity):
            self.rect.x -= self.velocity
    def move_left(self):
        if not pygame.sprite.spritecollideany(self, self.game.all_entity):
            self.rect.x -= self.velocity
    def move_up(self):
        self.rotate()
        self.rect.y -= self.velocity
        if pygame.sprite.spritecollideany(self, self.game.all_entity):
            self.rect.y += self.velocity
    def move_down(self):
        self.rect.y += self.velocity
        self.rotate()
        if pygame.sprite.spritecollideany(self, self.game.all_entity):
            self.rect.y -= self.velocity

    def get_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.vx = self.velocity
            self.image = pygame.image.load(resource_path("assets\sprites\Player\cartoonright1.png"))
            self.image = pygame.transform.smoothscale(self.image,
                                                      (int(self.size_x / self.player_global_size), int(self.size_x / self.player_global_size)))
        elif keys[pygame.K_LEFT]:
            self.vx = -self.velocity
            self.image = pygame.image.load(resource_path("assets\sprites\Player\cartoonleft1.png"))
            self.image = pygame.transform.smoothscale(self.image,
                                                      (int(self.size_x / self.player_global_size), int(self.size_x / self.player_global_size)))
        if keys[pygame.K_UP]:
            self.vy = -self.velocity
            self.image = pygame.image.load(resource_path("assets\sprites\Player\cartoonback1.png"))
            self.image = pygame.transform.smoothscale(self.image,
                                                      (int(self.size_x / self.player_global_size), int(self.size_x / self.player_global_size)))
            self.rotate()
        elif keys[pygame.K_DOWN]:
            self.vy = self.velocity
            self.image = pygame.image.load("assets\sprites\Player\cartoonface1.png")
            self.image = pygame.transform.smoothscale(self.image,
                                                (int(self.size_x / self.player_global_size), int(self.size_x / self.player_global_size)))
            self.rotate()
        if self.vy != 0 and self.vx != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071


    def update(self):
        self.get_keys()
        self.rect.x += self.vx
        collide_with(self,self.game.all_entity,'x')
        collide_with(self,self.game.map.all_liquid_tiles,'x')
        self.rect.y += self.vy
        collide_with(self,self.game.all_entity,'y')
        collide_with(self, self.game.map.all_liquid_tiles, 'y')
        self.vx, self.vy = 0,0

    def launch_projectile(self, mouse_x, mouse_y):
        pygame.mixer.Channel(3).play(pygame.mixer.Sound(self.fireball_sound))
        self.projectile.change_bullet("player")
        radians = math.atan2(mouse_y - 430, mouse_x - 780)
        projectile = Projectile(self)
        projectile.rect.x += 10
        projectile.vx = self.projectile.velocity * math.cos(radians) * 0.7071
        projectile.vy = self.projectile.velocity * math.sin(radians) * 0.7071
        self.all_projectiles.add(projectile)

    def damage(self, amount):
        if self.invincibility_countdown == 0:
            self.invincibility_countdown = self.invincibility_time
            self.health -= amount
            if self.health <= 0:
                self.game.all_projectiles_m.empty()
                pygame.mixer.Channel(5).play(pygame.mixer.Sound(resource_path(r'assets\Sound\player_death.wav')))
                # Rand stats
                if self.game.scene.number_story <=1:
                    self.game.map.name = "map0"
                    self.game.map.update = False
                    self.game.map.update_map()
                    self.rect.x = 1400
                    self.rect.y = 3400
                else:
                    self.rect.y = 2450
                    self.rect.x = 2000
                    self.game.map.name = "map2"
                    self.game.map.update = False
                    self.game.map.update_map()
                self.health = self.max_health

    def rotate(self):
        if self.way == '+':
            self.rotation = self.rotation + 1
        elif self.way == '-':
            self.rotation = self.rotation - 1
        if self.rotation >= 5:
            self.way = '-'
        elif self.rotation <= -5:
            self.way = '+'
        self.image = pygame.transform.rotate(self.image,self.rotation)

    def update_health_bar(self):
        if len(self.game.all_hearts) < self.health:
            coeur = Health()
            coeur.rect.x = 100 + (50 * len(self.game.all_hearts))
            self.game.all_hearts.add(coeur)
        elif len(self.game.all_hearts) > self.health:
            self.game.all_hearts.empty()

    def update_max_health_bar(self):
        if len(self.game.all_empty_hearts) < self.max_health:
            empty_coeur = MaxHealth()
            empty_coeur.rect.x = 100 + (50 * len(self.game.all_empty_hearts))
            self.game.all_empty_hearts.add(empty_coeur)