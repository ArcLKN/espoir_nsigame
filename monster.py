from random import randint, choice
import pygame, math
from player import Player, collide_with
from monster_projectile import MProjectile
import sys, os
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class Gems(pygame.sprite.Sprite):
    def __init__(self, monster):
        pygame.sprite.Sprite.__init__(self)
        self.monster = monster

        self.image = pygame.image.load(resource_path("assets/gemme_violette.png"))
        self.size_x, self.size_y = self.image.get_size()
        self.image = pygame.transform.smoothscale(self.image, (round(self.size_x/5),round(self.size_y/5)))
        self.rect = self.image.get_rect()
        self.value = 1

        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        if pygame.time.get_ticks() - self.spawn_time > 10000:
            self.monster.map.game.all_gems.remove(self)
        if pygame.sprite.spritecollide(self,self.monster.map.game.all_players, False):
            self.monster.map.game.all_gems.remove(self)
            self.monster.map.game.player.health += 1
            pygame.mixer.Channel(7).play(pygame.mixer.Sound(resource_path(r'assets\Sound\get_a_coin.wav')))


class Monster(pygame.sprite.Sprite):

    def __init__(self,map):
        super().__init__()
        self.player = Player(self)

        self.map = map
        self.game = self.map.game

        self.name = "slime"

        self.image = pygame.image.load(resource_path("assets/sprites/Ennemy/slime1.png")).convert_alpha()
        self.size_x,self.size_y = self.image.get_size()
        self.image = pygame.transform.smoothscale(self.image, (round(self.size_x/3),round(self.size_y/3)))
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.y = 0

        self.name = str()

        self.max_health = 100  # Point de vie maximum du monstre
        self.health = 100  # Point de vie actuel du monstre
        self.velocity = 5  # Vitesse du monstre
        self.vx = self.vy = 0  # vitesse x et y du monstre

        self.distance = 0  # distance entre le monstre et le joueur

        self.drop_of_money = 0

        self.hard_aggro = False
        self.aggro = False

        self.projectile = MProjectile(self)
        self.projectile_cooldown = 75  # Temps entre 2 projectiles 60 = 1s
        self.speed_projectile = 10  # Vitesse du projectile
        self.projectile_life = 1000
        self.countdown = 0

        self.fly_liquids = False  # L'entité peut elle marcher sur les liquides

    def update_distance(self):  # Calcule la distance entre le monstre et le joueur
        for player in self.map.game.all_players:
            self.distance = math.hypot(player.rect.x - self.rect.x, player.rect.y - self.rect.y)
        if self.distance < 600 or self.hard_aggro:
            self.launch_projectile()
        if (self.distance < 550 and self.hard_aggro) or (self.distance > 2000 and self.hard_aggro):
            self.hard_aggro = False

    def move(self):
        if (401 < self.distance < 600) or self.hard_aggro:
            for player in self.map.game.all_players:
                radians = math.atan2(player.rect.y - self.rect.y, player.rect.x - self.rect.x)
            self.vx = math.cos(radians)
            self.vy = math.sin(radians)
            self.rect.x += round(self.vx  * self.velocity)
            collide_with(self,self.map.game.all_entity,"x")
            self.rect.y += round(self.vy * self.velocity)
            collide_with(self, self.map.game.all_entity, "y")
        elif self.distance < 400:
            self.flee()

    def flee(self):
        for player in self.map.game.all_players:
            radians = math.atan2(player.rect.y - self.rect.y, player.rect.x - self.rect.x)
        self.vx -= math.cos(radians) * self.velocity
        self.vy -= math.sin(radians) * self.velocity
        self.rect.x += round(self.vx)
        collide_with(self, self.map.game.all_entity, "x")
        #collide_with(self, self.map.game.all_monsters, "x")
        if not self.fly_liquids:collide_with(self, self.game.map.all_liquid_tiles, 'x')
        self.rect.y += round(self.vy)
        collide_with(self, self.map.game.all_entity, "y")
        #collide_with(self, self.map.game.all_monsters, "y")
        if not self.fly_liquids:collide_with(self, self.game.map.all_liquid_tiles, 'y')
        self.vx = self.vy = 0

    def launch_projectile(self, name=False):
        if self.countdown <= 0:
            for player in self.map.game.all_players:
                radians = math.atan2(player.rect.centery - self.rect.y, player.rect.centerx - self.rect.x)
            speed_x = self.speed_projectile * math.cos(radians)
            speed_y = self.speed_projectile * math.sin(radians)
            angle = (180 / math.pi) * -radians

            projectile = MProjectile(self)
            projectile.velocity_x = speed_x
            projectile.velocity_y = speed_y
            projectile.rect.x = self.rect.x
            projectile.rect.y = self.rect.y
            if self.name == "spider":
                projectile.original_image = pygame.image.load(resource_path("assets/spider_projectile.png"))
                projectile.image = pygame.transform.rotate(projectile.original_image, int(angle+90))
                projectile.size = projectile.image.get_size()
                projectile.image = pygame.transform.smoothscale(projectile.image, (round(projectile.size[0]/2), round(projectile.size[1]/2)))
                # 2eme projectile
                speed_x = self.speed_projectile * math.cos(radians+0.261799)
                speed_y = self.speed_projectile * math.sin(radians+0.261799)
                projectile2 = MProjectile(self)
                projectile2.velocity_x = speed_x
                projectile2.velocity_y = speed_y
                projectile2.rect.x = self.rect.x
                projectile2.rect.y = self.rect.y
                projectile2.original_image = pygame.image.load(resource_path("assets/spider_projectile.png"))
                projectile2.image = pygame.transform.rotate(projectile2.original_image, int(angle+75))
                projectile2.size = projectile2.image.get_size()
                projectile2.image = pygame.transform.smoothscale(projectile2.image, (round(projectile2.size[0]/2), round(projectile2.size[1]/2)))
                # 3eme projectile
                speed_x = self.speed_projectile * math.cos(radians-0.261799)
                speed_y = self.speed_projectile * math.sin(radians-0.261799)
                projectile3 = MProjectile(self)
                projectile3.velocity_x = speed_x
                projectile3.velocity_y = speed_y
                projectile3.rect.x = self.rect.x
                projectile3.rect.y = self.rect.y
                projectile3.original_image = pygame.image.load(resource_path("assets/spider_projectile.png"))
                projectile3.image = pygame.transform.rotate(projectile3.original_image, int(angle+105))
                projectile3.size = projectile3.image.get_size()
                projectile3.image = pygame.transform.smoothscale(projectile3.image, (round(projectile3.size[0]/2), round(projectile3.size[1]/2)))
                self.map.game.all_projectiles_m.add(projectile2)
                self.map.game.all_projectiles_m.add(projectile3)
            elif self.name == "red_slime":
                projectile.image = pygame.transform.smoothscale(pygame.image.load(resource_path("assets/red_projectilem.png")), (40, 40))
                speed_x = randint(8,11) * math.cos(radians + ((randint(1,174533*30)-174533)/10000000))
                speed_y = randint(8,11) * math.sin(radians + ((randint(1,174533*30)-174533)/10000000))
                projectile2 = MProjectile(self)
                projectile2.velocity_x = speed_x
                projectile2.velocity_y = speed_y
                projectile2.rect.x = self.rect.x
                projectile2.rect.y = self.rect.y
                projectile2.image = pygame.transform.smoothscale(pygame.image.load(resource_path("assets/red_projectilem.png")), (40, 40))
                self.map.game.all_projectiles_m.add(projectile2)

            elif self.name == "tesseract":
                image = pygame.image.load(resource_path("assets/ice_projectile.png"))
                type_attack = randint(0,4)
                if type_attack <= 2:
                    for i in range(0,14):
                        projectile = MProjectile(self)
                        projectile.original_image = image
                        projectile.image = pygame.transform.smoothscale(projectile.original_image,(50, 39))
                        projectile.image = pygame.transform.rotate(projectile.image, int(angle + 25 * i))
                        speed_x = self.speed_projectile * math.cos(radians - 0.436332 * i)
                        speed_y = self.speed_projectile * math.sin(radians - 0.436332 * i)
                        projectile.velocity_x = speed_x
                        projectile.velocity_y = speed_y
                        projectile.rect.x = self.rect.x + 30
                        projectile.rect.y = self.rect.y + 30

                        projectile.bullet_lifetime = 3000

                        self.map.game.all_projectiles_m.add(projectile)
                else:
                    for i in range(0,randint(7,12)):
                        angle = (180 / math.pi) * -radians
                        rng = round(randint(0,30+i*5) - 15+(i/2*5))
                        projectile = MProjectile(self)
                        projectile.original_image = image
                        projectile.image = pygame.transform.smoothscale(projectile.original_image,(50, 39))
                        projectile.image = pygame.transform.rotate(projectile.image, int(angle + rng))
                        speed_x = self.speed_projectile*2 * math.cos(radians - 0.0174533*rng)
                        speed_y = self.speed_projectile*2 * math.sin(radians - 0.0174533*rng)

                        projectile.rect.x = self.rect.x + 30
                        projectile.rect.y = self.rect.y + 30

                        projectile.velocity_x = speed_x
                        projectile.velocity_y = speed_y

                        projectile.bullet_lifetime = 1000

                        self.map.game.all_projectiles_m.add(projectile)

            elif self.name == "nuzlock":
                type_attack = randint(0,4)
                if type_attack <= 2:
                    image = pygame.image.load(resource_path("assets/thunder_ball.png"))
                    projectile = MProjectile(self)
                    projectile.original_image = image
                    projectile.image = pygame.transform.smoothscale(projectile.original_image,(100, 100))
                    projectile.original_image = projectile.image
                    speed_x = self.speed_projectile * math.cos(radians)
                    speed_y = self.speed_projectile * math.sin(radians)
                    projectile.velocity_x = speed_x
                    projectile.velocity_y = speed_y
                    projectile.velocity = self.speed_projectile
                    projectile.rect.x = self.rect.x + 30
                    projectile.rect.y = self.rect.y + 30

                    projectile.bullet_lifetime = 2000
                else:
                    for i in range(0, 3):
                        image = pygame.image.load(resource_path("assets/thunder_ball.png"))
                        projectile = MProjectile(self)
                        projectile.name = "little_thunder_ball"
                        projectile.original_image = image
                        projectile.image = pygame.transform.smoothscale(projectile.original_image,(30, 30))
                        projectile.original_image = projectile.image
                        projectile.velocity = self.speed_projectile * 2
                        speed_x = self.speed_projectile * math.cos(radians)
                        speed_y = self.speed_projectile * math.sin(radians)
                        projectile.velocity_x = speed_x
                        projectile.velocity_y = speed_y
                        projectile.rect.x = self.rect.x + 30 + randint(0,200)-100
                        projectile.rect.y = self.rect.y + 30 + randint(0,200)-100

                        projectile.bullet_lifetime = 1200

                        self.map.game.all_projectiles_m.add(projectile)


            self.map.game.all_projectiles_m.add(projectile)
            self.countdown = self.projectile_cooldown
            pygame.mixer.Channel(6).play(pygame.mixer.Sound(resource_path(r'assets\Sound\slime_growl.wav')))
        else:
            self.countdown -= 1

    def remove(self):
        self.game.map.all_monsters.remove(self)

    def damage(self, amount):
        if not self.aggro:
            self.hard_aggro = True
        self.health -= amount
        if self.health <= 0:
            pygame.mixer.Channel(5).play(pygame.mixer.Sound(resource_path(r'assets\Sound\enemy_death.wav')))
            for i in range(20):
                self.map.game.particules.append([[self.rect.x+randint(0,60), self.rect.y+randint(0,60)]
                                                       , [randint(0, 20) / 10 - 1, -2], randint(10, 25),
                                                    (0+randint(0,10),0+randint(0,10),0+randint(0,10))])
            # Rand stats
            self.health = self.max_health
            self.kill()
            nbr_gems = randint(0, self.drop_of_money+1)
            if nbr_gems == 0: return
            for i in range(0, nbr_gems):
                gem = Gems(self)
                gem.rect.x = self.rect.x
                gem.rect.y = self.rect.y
            self.map.game.all_gems.add(gem)


    def set_monster(self, name):
        if name == "slime":
            monster = self
            monster.image = pygame.image.load(resource_path("assets/sprites/Ennemy/slime2.png")).convert_alpha()
            monster.name = "Slime"
            monster.max_health = 100  # Point de vie maximum du monstre
            monster.health = 100  # Point de vie actuel du monstre
            monster.velocity = 5  # Vitesse du monstre
            monster.projectile_cooldown = 75  # Temps entre 2 projectiles 60 = 1s
            monster.size_x, monster.size_y = monster.image.get_size()
            monster.image = pygame.transform.smoothscale(monster.image, (round(monster.size_x / 3), round(monster.size_y / 3)))
            monster.rect = monster.image.get_rect()
            monster.rect.x = randint(65,60*64-1)
            monster.rect.y = randint(65, 45 * 64 - 1)
        else:
            monster = self
        self.map.all_monsters.add(monster)

class Dragon(pygame.sprite.Sprite):

    def __init__(self,map):
        super().__init__()
        self.player = Player(self)

        self.name = "dragon"

        self.map = map
        self.game = self.map.game

        self.image = pygame.image.load(resource_path("assets/sprites/Ennemy/dragon1.png")).convert_alpha()
        self.size_x,self.size_y = self.image.get_size()
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.y = 0

        self.max_health = 2000  # Point de vie maximum du monstre
        self.health = 2000  # Point de vie actuel du monstre
        self.velocity = 0  # Vitesse du monstre
        self.vx = self.vy = 0  # vitesse x et y du monstre

        self.distance = 0  # distance entre le monstre et le joueur

        self.phase = 1  # Valeur initiale = 0
        self.hard_aggro = False
        self.aggro = False

        self.projectile = MProjectile(self)
        self.projectile_cooldown = 200  # Temps entre 2 projectiles 60 = 1s
        self.speed_projectile = 10  # Vitesse du projectile
        self.projectile_life = 1000
        self.countdown = 0

        self.turn = 0

        self.time = 0

    def update(self):
        if self.phase == 1:
            self.projectile_cooldown = 80  # Vitesse initiale = 80
            if self.turn <= 5:
                if self.countdown <= 0:
                    self.firethrower()
                    self.countdown = self.projectile_cooldown
                    self.turn +=1
                    if self.turn == 6:
                        self.countdown = 200
            elif self.turn > 5 and self.countdown <= 0:
                self.turn = 0
            self.countdown -= 1
            if self.health < 1000:
                self.phase =2
                self.turn = 1
        elif self.phase == 2:
            if self.turn < 150:
                self.projectile_cooldown = 15  # Vitesse initiale = 15
                if self.countdown <= 0:
                    self.rapidshot()
                    self.countdown = self.projectile_cooldown
            elif self.turn < 320:
                self.projectile_cooldown = 5  # Valeur initiale = 5
                if self.countdown <= 0:
                    self.wall_of_fire()
                    self.countdown = self.projectile_cooldown
            else:
                self.turn = 0
            self.turn += 1
            self.countdown -= 1
            if self.health <= 0:
                self.phase = 4



    def firethrower(self):
        for i in range(5,15):
            for player in self.map.game.all_players:
                radians = math.atan2(player.rect.centery - (self.rect.y + 300), player.rect.centerx - (self.rect.x + 420))
            angle = (180 / math.pi) * -radians
            rng = round(randint(0,30+i*5) - (15+(i/2*5)))

            image = pygame.image.load(resource_path("assets/boule_de_feu.png"))
            projectile = MProjectile(self)
            projectile.original_image = image
            projectile.image = pygame.transform.smoothscale(projectile.original_image, (100, 100))
            projectile.image = pygame.transform.rotate(projectile.image,(angle+90+rng))
            projectile.original_image = projectile.image
            speed_x = self.speed_projectile * math.cos(radians - 0.0174533*rng)
            speed_y = self.speed_projectile * math.sin(radians - 0.0174533*rng)
            projectile.velocity_x = speed_x
            projectile.velocity_y = speed_y
            projectile.velocity = self.speed_projectile
            projectile.rect.x = self.rect.x + 420 + randint(0,30)
            projectile.rect.y = self.rect.y + 300 + randint(0,30)

            projectile.bullet_lifetime = 2400

            self.map.game.all_projectiles_m.add(projectile)

    def rapidshot(self):
        for player in self.map.game.all_players:
            radians = math.atan2(player.rect.centery - (self.rect.y + 300), player.rect.centerx - (self.rect.x + 420))
        angle = (180 / math.pi) * -radians
        rng = round(randint(0,30)) - 15

        image = pygame.image.load(resource_path("assets/boule_de_feu.png"))
        projectile = MProjectile(self)
        projectile.original_image = image
        projectile.image = pygame.transform.smoothscale(projectile.original_image, (100, 100))
        projectile.image = pygame.transform.rotate(projectile.image, (angle+90+rng))
        projectile.original_image = projectile.image
        speed_x = self.speed_projectile * math.cos(radians - 0.0174533*rng)
        speed_y = self.speed_projectile * math.sin(radians - 0.0174533*rng)
        projectile.velocity_x = speed_x
        projectile.velocity_y = speed_y
        projectile.velocity = self.speed_projectile
        projectile.rect.x = self.rect.x + 420 + randint(0,30)
        projectile.rect.y = self.rect.y + 300 + randint(0,30)

        projectile.bullet_lifetime = 2000
        self.map.game.all_projectiles_m.add(projectile)

    def wall_of_fire(self):
        axe = choice(["x","y","-y"])
        projectile = MProjectile(self)
        image = pygame.image.load(resource_path("assets/boule_de_feu.png"))
        projectile.name = "wall_of_fire"
        projectile.original_image = image
        projectile.image = pygame.transform.smoothscale(projectile.original_image, (100, 100))
        projectile.bullet_lifetime = 10000
        vitesse = 10
        if axe == "x":
            projectile.rect.x = randint(65,3840)
            projectile.rect.y = 65
            projectile.velocity_x = 0
            projectile.velocity_y = vitesse
        elif axe == "-x":
            projectile.image = pygame.transform.rotate(projectile.image, (180))
            projectile.rect.x = randint(65,3840)
            projectile.rect.y = 1500
            projectile.velocity_x = 0
            projectile.velocity_y = -vitesse
        elif axe == "y":
            projectile.image = pygame.transform.rotate(projectile.image, (90))
            projectile.rect.y = randint(65,1764)
            projectile.rect.x = 65
            projectile.velocity_x = vitesse
            projectile.velocity_y = 0
        else:
            projectile.image = pygame.transform.rotate(projectile.image, (-90))
            projectile.rect.y = randint(65,1764)
            projectile.rect.x = 3600
            projectile.velocity_x = -vitesse
            projectile.velocity_y = 0
        self.map.game.all_projectiles_m.add(projectile)

    def damage(self, amount):
        if not self.aggro:
            self.hard_aggro = True
        self.health -= amount
        if self.health <= 0:
            pygame.mixer.Channel(5).play(pygame.mixer.Sound(resource_path(r'assets\Sound\enemy_death.wav')))
            for i in range(20):
                self.map.game.particules.append([[self.rect.x+randint(0,60), self.rect.y+randint(0,60)]
                                                       , [randint(0, 20) / 10 - 1, -2], randint(10, 25),
                                                    (0+randint(0,10),0+randint(0,10),0+randint(0,10))])
            # Rand stats
            if not self.name == "dragon":
                self.kill()
            else:
                self.game.scene.number_story = 3
                self.game.scene.fadeout(self.game.screen)
                self.game.scene.scene_manager(self.game.screen)
