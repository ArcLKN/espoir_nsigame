# coding: utf8
from player import Player
from start_menu import StartMenu
from map import Map, Camera
from Narration import Cutscenes
import pygame, random
import sys, os
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


black_color = [0,0,0]
WHITE = [255,255,255]
font = pygame.font.SysFont('Comic Sans MS', 48)

gem_image = pygame.image.load(resource_path("assets/gemme_violette.png"))
gem_size_x, gem_size_y = gem_image.get_size()
gem_image = pygame.transform.smoothscale(gem_image,(round(gem_size_x/5),round(gem_size_y/5)))
gem_rect = gem_image.get_rect()
gem_rect.x = 1450
gem_rect.y = 10

boss_health_bar_image = pygame.image.load(resource_path("assets/boss_health_bar.png"))
boss_health_bar_image_size_x, boss_health_bar_image_size_y = boss_health_bar_image.get_size()
boss_health_bar_image = pygame.transform.smoothscale(boss_health_bar_image,
                                                     (round(boss_health_bar_image_size_x/2),
                                                      round(boss_health_bar_image_size_y/2)))
boss_health_bar_rect = boss_health_bar_image.get_rect()
boss_health_bar_rect.x = 400
boss_health_bar_rect.y = 710

boss_health_original = pygame.image.load(resource_path("assets/boss_health.png"))
boss_health = pygame.image.load(resource_path("assets/boss_health.png"))
boss_health_size_x, boss_health_size_y = boss_health.get_size()
boss_health = pygame.transform.smoothscale(boss_health,
                                                     (round(boss_health_size_x/2),
                                                      round(boss_health_size_y/2)))
boss_health_rect = boss_health.get_rect()
boss_health_rect.x = 434
boss_health_rect.y = 722


class Game():

    def __init__(self,resolution, screen):
        super().__init__()

        self.screen = screen

        self.particules = []
        self.all_hearts = pygame.sprite.Group()
        self.all_empty_hearts = pygame.sprite.Group()
        self.all_players = pygame.sprite.Group()
        self.player = Player(self)
        self.all_players.add(self.player)
        self.start_menu = StartMenu(self)
        self.map = Map(self)
        self.camera = Camera(self,1920,1080)
        self.scene = Cutscenes(self)
        self.all_objects = self.map.all_objects
        self.all_entity = pygame.sprite.Group()
        self.all_tiles = self.map.all_tiles
        self.all_monsters = self.map.all_monsters
        self.all_gems = pygame.sprite.Group()
        self.escape_button_rect = (pygame.transform.scale(pygame.image.load("assets\escape_menu_button.png"), [50,50])).get_rect()
        self.pressed = self.player.pressed

        self.resolution = resolution
        self.offset_x = (resolution[0])-(self.player.size_x/4)
        self.offset_y = (resolution[1]/2)-(self.player.size_y/2)

        self.all_projectiles_m = pygame.sprite.Group()

    def update(self, screen):

        self.map.watching()

        #print(self.player.rect.y, self.player.rect.x)  # Affiche coordonnées joueur

        screen.fill(black_color)

        # Applique les images de tous les groupes sur l'écran en fonction de la caméra
        for e in self.all_tiles:
            if (self.player.rect.x + e.size_x * 13 > e.rect.x > self.player.rect.x - e.size_x * 14) and (self.player.rect.y + e.size_y * 7 > e.rect.y > self.player.rect.y - e.size_y * 8):
                screen.blit(e.image, self.camera.apply(e))
        for e in self.map.all_liquid_tiles:
            if (self.player.rect.x + e.size_x * 13 > e.rect.x > self.player.rect.x - e.size_x * 14) and (self.player.rect.y + e.size_y * 7 > e.rect.y > self.player.rect.y - e.size_y * 8):
                screen.blit(e.image, self.camera.apply(e))
        for e in self.map.all_solid_decorations:
            if (self.player.rect.x + e.size_x * 13 > e.rect.x > self.player.rect.x - e.size_x * 14) and (self.player.rect.y + e.size_y * 7 > e.rect.y > self.player.rect.y - e.size_y * 8):
                screen.blit(e.image, self.camera.apply(e))
        for e in self.map.all_floor_decorations:
            if (self.player.rect.x + 64 * 13 > e.rect.x > self.player.rect.x - 64 * 14) and (self.player.rect.y + 64 * 7 > e.rect.y > self.player.rect.y - 64 * 8):
                screen.blit(e.image, self.camera.apply(e))
        # Appliquer images gemmes
        for e in self.all_gems:
            e.update()
            if (self.player.rect.x + 64 * 13 > e.rect.x > self.player.rect.x - 64 * 14) and (self.player.rect.y + 64 * 7 > e.rect.y > self.player.rect.y - 64 * 8):
                screen.blit(e.image, self.camera.apply(e))

        # Appliquer images projectiles monstres
        for e in self.all_projectiles_m:
            e.move()
            screen.blit(e.image, self.camera.apply(e))

        for e in self.all_entity:
            if (self.player.rect.x + e.size_x * 13 > e.rect.x > self.player.rect.x - e.size_x * 14) and (
                    self.player.rect.y + e.size_y * 7 > e.rect.y > self.player.rect.y - e.size_y * 8):
                screen.blit(e.image, self.camera.apply(e))
        for e in self.all_monsters:  # importer les images des monstres
            if not e.name == "dragon":
                e.update_distance()
                e.move()
            else:
                e.update()
            screen.blit(e.image, self.camera.apply(e))

        # Appliquer les particules
        for particle in self.particules:
            particle[0][0] += particle[1][0] * (random.choice([0,2])-1)
            particle[0][1] += particle[1][1] * (random.choice([0,2])-1)
            particle[2] -= 0.8
            if len(particle)>4:
                particle[3] = self.player.projectile.change_color_particle(particle)
            particle_edit = self.camera.apply(particle, "particule")
            pygame.draw.circle(screen, particle_edit[3], particle_edit[0], particle_edit[2])
            if particle[2] <= 0:
                self.particules.remove(particle)

        # Appliquer images projectiles joueur
        for e in self.player.all_projectiles:
            e.move()
            screen.blit(e.image, self.camera.apply(e))

        # Appliquer images joueur
        for e in self.all_players:
            screen.blit(e.image, self.camera.apply(e))
            # chrono invincibilité
            if e.invincibility_countdown > 0:
                e.invincibility_countdown-=1
            self.camera.update(e)

        # Appliquer les informations sur l'argent du joueur
        #screen.blit(gem_image,gem_rect)
        #textsurface = font.render(str(self.player.money), True, (255, 255, 255))
        #screen.blit(textsurface,(1380-len(str(self.player.money))*10,10))

        # update du joueur
        self.player.update()

        # update des projectiles des monstres
        for projectile in self.all_projectiles_m:
            projectile.update()

        # affichage barre de vie du boss
        if self.map.name == "map5":
            for e in self.all_monsters:
                health_monster = e.health
                max_health_monster = e.max_health
            if len(self.all_monsters) > 0:
                if health_monster > 0:
                    porcentage = health_monster / max_health_monster
                    boss_health = pygame.transform.smoothscale(boss_health_original,
                                                        (round(boss_health_size_x/2*porcentage),
                                                        round(boss_health_size_y/2)))
                    screen.blit(boss_health,boss_health_rect)
                screen.blit(boss_health_bar_image,boss_health_bar_rect)

        # Appliquer les images de la barre de vie
        self.player.update_health_bar()
        self.player.update_max_health_bar()
        self.all_empty_hearts.draw(screen)
        self.all_hearts.draw(screen)