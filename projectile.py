import pygame, random
import sys, os
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class Projectile(pygame.sprite.Sprite):

    def __init__(self, player):
        super().__init__()
        self.player = player
        self.original_image = pygame.image.load(resource_path(r"assets\projectile.png")).convert_alpha()
        self.image = pygame.image.load(resource_path(r"assets\projectile.png")).convert_alpha()
        self.image = pygame.transform.smoothscale(self.image,(40,40))
        self.rect = self.image.get_rect()
        self.size = self.image.get_size()
        self.rect.x = self.player.rect.x
        self.rect.y = self.player.rect.y
        self.velocity = 20
        self.vx = self.vy = 0

        self.attack = 10  # Valeur initiale = 10
        self.max_projectile = 20
        self.cast = 1

        self.color_projectile = [0,255,10]

        self.spawn_time = pygame.time.get_ticks()
        self.bullet_lifetime = 1000

        self.hit_sound = pygame.mixer.Sound(resource_path(r'assets\Sound\blow3.ogg'))
        self.hit_sound.set_volume(0.2)

    def remove(self):
        self.player.all_projectiles.remove(self)

    def move(self):
        if pygame.time.get_ticks() - self.spawn_time > self.bullet_lifetime:
            self.kill()
            for i in range(10):
                self.player.game.particules.append(
                [[self.rect.x + random.randint(0, 30), self.rect.y + random.randint(0, 30)]
                    , [random.randint(0, 20) / 10 - 1, -2], random.randint(4, 18),
                 (255, 255, 255,)])
        for i in range(3):
            self.player.game.particules.append([
                [self.rect.x + random.randint(0, 30), self.rect.y + random.randint(0, 30)],
                [random.randint(0, 20) / 10 - 1, -2],
                random.randint(4, 12),
                self.color_projectile,
                True
            ])
        self.rect.x += self.vx
        self.rect.y += self.vy

        if pygame.sprite.spritecollideany(self,self.player.game.all_entity):
            pygame.mixer.Channel(7).play(self.hit_sound)
            for i in range(10):
                self.player.game.particules.append(
                    [[self.rect.x + random.randint(0, 30), self.rect.y + random.randint(0, 30)]
                        , [random.randint(0, 20) / 10 - 1, -2], random.randint(4, 18),
                     (255, 255, 255,)])
            self.remove()

        for monster in pygame.sprite.spritecollide(self,self.player.game.map.all_monsters,False):
            pygame.mixer.Channel(7).play(self.hit_sound)
            for i in range(10):
                self.player.game.particules.append([[self.rect.x+random.randint(0,30), self.rect.y+random.randint(0,30)]
                                                       , [random.randint(0, 20) / 10 - 1, -2], random.randint(4, 18),
                                                    (255,255,255,)])
            self.remove()
            monster.damage(self.attack)
            break

    def change_bullet(self,caster):
        if caster == "player":
            self.velocity = 20
            self.attack = 10
            self.max_projectile = 20
            self.cast = 2
        elif caster == "monster":
            self.velocity = 10
            self.attack = 5
            self.max_projectile = 5
            self.cast = 4

    def change_color_particle(self,particle):
        new_color = []
        for color in particle[3]:
            if color > 200:
                color -= random.randint(0, 15)
                new_color.append(color)
            else:
                color += random.randint(0, 15)
                new_color.append(color)
        return new_color