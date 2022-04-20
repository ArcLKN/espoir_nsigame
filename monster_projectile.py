import pygame, random, math
import sys, os
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class MProjectile(pygame.sprite.Sprite):

    def __init__(self, monster):
        super().__init__()
        self.monster = monster
        self.name = str()
        self.image = pygame.transform.smoothscale(pygame.image.load(resource_path("assets/projectilem.png")), (40, 40))
        self.original_image = self.image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.velocity = 0
        self.velocity_x = self.velocity_y = 0

        self.attack = 1
        self.max_projectile = 20

        self.spawn_time = pygame.time.get_ticks()
        self.bullet_lifetime = 1000

        self.turn = 0

        self.fly_liquids = False

        self.blow_sound = pygame.mixer.Sound(resource_path(r'assets\Sound\blow3.ogg'))
        self.blow_sound.set_volume(0.2)

    def remove(self):
        self.monster.game.all_projectiles_m.remove(self)

    def update(self):
        if self.monster.name == "nuzlock":
            if self.name == "little_thunder_ball" and self.turn >= 15:
                return
            for player in self.monster.map.game.all_players:
                radians = math.atan2(player.rect.centery - self.rect.y, player.rect.centerx - self.rect.x)
            self.velocity_x = self.velocity * math.cos(radians)
            self.velocity_y = self.velocity * math.sin(radians)
            self.image = pygame.transform.rotate(self.original_image,(1+self.turn))
            self.turn+=1

    def move(self):
        if pygame.time.get_ticks() - self.spawn_time > self.bullet_lifetime:
            self.kill()
            for i in range(10):
                self.monster.map.game.particules.append(
                [[self.rect.x + random.randint(0, 30), self.rect.y + random.randint(0, 30)]
                    , [random.randint(0, 20) / 10 - 1, -2], random.randint(4, 18),
                 (255, 255, 255,)])
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        if pygame.sprite.spritecollideany(self, self.monster.map.game.all_entity):
            if not self.name == "wall_of_fire":
                pygame.mixer.Channel(5).play(self.blow_sound)
            for i in range(10):
                self.monster.map.game.particules.append(
                    [[self.rect.x + random.randint(0, 30), self.rect.y + random.randint(0, 30)]
                        , [random.randint(0, 20) / 10 - 1, -2], random.randint(4, 18),
                     (255, 255, 255,)])
            self.remove()

        for player in pygame.sprite.spritecollide(self, self.monster.map.game.all_players, False):
            pygame.mixer.Channel(5).play(self.blow_sound)
            for i in range(10):
                self.monster.map.game.particules.append(
                    [[self.rect.x + random.randint(0, 30), self.rect.y + random.randint(0, 30)]
                        , [random.randint(0, 20) / 10 - 1, -2], random.randint(4, 18),
                     (255, 255, 255,)])
            player.damage(self.attack)
            self.remove()
            break