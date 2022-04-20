# coding: utf8
import pygame, random
from os import path
from monster import Monster, Dragon
import sys, os
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# class pour une tile de map
class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.size_x,self.size_y = self.image.get_size()
        self.rect.x = x
        self.rect.y = y

class Map():

    def __init__(self,game):
        super(Map, self).__init__()
        self.game = game
        self.monster = Monster(self)

        self.name = "map0"  # Nom de la map
        self.update = False  # La map est elle actualisée ou non.

        self.all_monsters = pygame.sprite.Group()  # Groupe des monstres de la map
        #self.nbr_monster = 3  # Nombre de monstres à invoquer

        self.all_floor_decorations = pygame.sprite.Group()  # Groupe des décorations au niveau du sol de la map
        self.all_solid_decorations = pygame.sprite.Group()  # Groupe des décorations ayant une collision

        self.all_objects = pygame.sprite.Group()  # Groupe des structures de la map

        self.all_tiles = pygame.sprite.Group()  # Groupe des tiles de la map
        self.all_liquid_tiles = pygame.sprite.Group()

        self.music_theme = pygame.mixer.Sound(resource_path(r'assets\Sound\Title_Screen.wav'))


    # Vérification des coordonnés du joueur pour savoir si il doit changer de map
    def watching(self):
        #print(f"x: {self.game.player.rect.x}, y: {self.game.player.rect.y}")  # Coordonnées du joueur
        if self.name == "map0":
            if (self.game.player.rect.y <= 64) and (1920 > self.game.player.rect.x > 1715):
                self.music_theme = pygame.mixer.Sound(resource_path(r'assets\Sound\Deep_Forest.wav'))
                self.update = False
                self.name = "map1"
                self.update_map()
                self.game.player.rect.x = 64 * 45
                self.game.player.rect.y = 64 * 55
        if self.name == "map1":
            if (self.game.player.rect.y >= 3775) and (3008 > self.game.player.rect.x > 2808):
                self.music_theme = pygame.mixer.Sound(resource_path(r'assets\Sound\1-02-Secrets-of-the-Woods.wav'))
                self.update = False
                self.name = "map0"
                self.update_map()
                self.game.player.rect.x = 64 * 28
                self.game.player.rect.y = 64 * 4
            if (self.game.player.rect.y <= 64) and (2300 > self.game.player.rect.x > 1959):
                self.music_theme = pygame.mixer.Sound(resource_path(r'assets\Sound\Town_Theme.wav'))
                self.game.player.rect.y = 2450
                self.update = False
                self.name = "map2"
                self.update_map()
                self.game.player.rect.x = 64 * 28 + 10
                if self.game.scene.number_story == 1:
                    self.game.scene.scene_manager(self.game.screen)
        elif self.name == "map2":
            if self.game.player.rect.y >= 2550 and not self.game.scene.is_narrating:
                pygame.mixer.Channel(1).play(pygame.mixer.Sound(resource_path(r'assets\Sound\Deep_Forest.wav')))
                self.update = False
                self.name = "map1"
                self.update_map()
                self.game.player.rect.y = 210
                self.game.player.rect.x = 2000
            if self.game.player.rect.x >= 4800 and not self.game.scene.is_narrating:
                self.music_theme = pygame.mixer.Sound(resource_path(r'assets\Sound\Overworld_Theme.wav'))
                self.update = False
                self.name = "map3"
                self.update_map()
                self.game.player.rect.y = 930
                self.game.player.rect.x = 545
        elif self.name == "map3":
            if self.game.player.rect.x <= 200 and not self.game.scene.is_narrating:
                self.music_theme = pygame.mixer.Sound(resource_path(r'assets\Sound\Town_Theme.wav'))
                self.name = "map2"
                self.update = False
                self.update_map()
                self.game.player.rect.y = 100
                self.game.player.rect.x = 4600
            if self.game.player.rect.y <= 150 and not self.game.scene.is_narrating and self.name == "map3":
                self.music_theme = pygame.mixer.Sound(resource_path(r'assets\Sound\Time_Cave.wav'))
                self.update = False
                self.name = "map4"
                self.update_map()
                self.game.player.rect.y = 4672
                self.game.player.rect.x = 3456
        elif self.name == "map4":
            if self.game.player.rect.y >= 4864 and not self.game.scene.is_narrating:
                self.music_theme = pygame.mixer.Sound(resource_path(r'assets\Sound\Overworld_Theme.wav'))
                self.update = False
                self.name = "map3"
                self.update_map()
                self.game.player.rect.y = 384
                self.game.player.rect.x = 4224
            if self.game.player.rect.y < 150 and not self.game.scene.is_narrating:
                self.music_theme = pygame.mixer.Sound(resource_path(r'assets\Sound\Boss_Battle_Loop.wav'))
                self.update = False
                self.name = "map5"
                self.update_map()
                self.game.player.rect.y = 1664
                self.game.player.rect.x = 1920
                if self.game.scene.number_story == 2:
                    self.game.scene.scene_manager(self.game.screen)

    def update_map(self):
        if not self.update:

            if self.name == "map5":
                self.music_theme = pygame.mixer.Sound(resource_path("assets/Sound/Boss_Battle_Loop.wav"))

            pygame.mixer.Channel(1).play(self.music_theme, -1)

            print(self.name)

            # Réinitialisation des groupes.
            self.all_monsters.empty()
            self.game.all_tiles.empty()
            self.game.all_entity.empty()
            self.all_liquid_tiles.empty()
            self.all_floor_decorations.empty()
            self.all_solid_decorations.empty()

            # Ouverture du fichier contenant la map
            map = []
            map_folder = path.dirname(__file__)
            with open(path.join(map_folder, f'assets/Tilesets/{self.name}.txt'), "r") as data:
                for line in data:
                    map.append(line)

           # réinitialisation des coordonnées des tiles
            x = y = 0

            # Création des tiles composant la map
            for raw in map:
                x = 0
                for tile in raw:

                    # used caracters = [b i j k m r s u w x B H I J K L M R S T U W X ; .]
                    # AGDF agdf

                    # invoquer une tile de base
                    if tile == str("."):
                        img = pygame.image.load(resource_path(f"assets/Tilesets/{self.name}/plain1.jpg")).convert()
                        tile = Tile(x, y, img)
                        self.all_tiles.add(tile)
                    elif tile == "T":
                        img = pygame.image.load(resource_path(f"assets/Tilesets/{self.name}/TopRock.jpg")).convert()
                        tile = Tile(x, y, img)
                        self.game.all_entity.add(tile)
                    elif tile == "B":
                        img = pygame.image.load(resource_path(f"assets/Tilesets/{self.name}/BottomRock.jpg")).convert()
                        tile = Tile(x, y, img)
                        self.game.all_entity.add(tile)
                    elif tile == "R":
                        img = pygame.image.load(resource_path(f"assets/Tilesets/{self.name}/RightRock.jpg")).convert()
                        tile = Tile(x, y, img)
                        self.game.all_entity.add(tile)
                    elif tile == "L":
                        img = pygame.image.load(resource_path(f"assets/Tilesets/{self.name}/LeftRock.jpg")).convert()
                        tile = Tile(x, y, img)
                        self.game.all_entity.add(tile)
                    elif tile == "u":
                        img = pygame.image.load(resource_path(f"assets/Tilesets/{self.name}/TopLeftRock.jpg")).convert()
                        tile = Tile(x, y, img)
                        self.game.all_entity.add(tile)
                    elif tile == "i":
                        img = pygame.image.load(resource_path(f"assets/Tilesets/{self.name}/TopRightRock.jpg")).convert()
                        tile = Tile(x, y, img)
                        self.game.all_entity.add(tile)
                    elif tile == "j":
                        img = pygame.image.load(resource_path(f"assets/Tilesets/{self.name}/BottomLeftRock.jpg")).convert()
                        tile = Tile(x, y, img)
                        self.game.all_entity.add(tile)
                    elif tile == "k":
                        img = pygame.image.load(resource_path(f"assets/Tilesets/{self.name}/BottomRightRock.jpg")).convert()
                        tile = Tile(x, y, img)
                        self.game.all_entity.add(tile)
                    elif tile == "U":
                        img = pygame.image.load(resource_path(f"assets/Tilesets/{self.name}/ReverseTopLeftRock.jpg")).convert()
                        tile = Tile(x, y, img)
                        self.game.all_entity.add(tile)
                    elif tile == "I":
                        img = pygame.image.load(resource_path(f"assets/Tilesets/{self.name}/ReverseTopRightRock.jpg")).convert()
                        tile = Tile(x, y, img)
                        self.game.all_entity.add(tile)
                    elif tile == "J":
                        img = pygame.image.load(resource_path(f"assets/Tilesets/{self.name}/ReverseBottomRightRock.jpg")).convert()
                        tile = Tile(x, y, img)
                        self.game.all_entity.add(tile)
                    elif tile == "K":
                        img = pygame.image.load(resource_path(f"assets/Tilesets/{self.name}/ReverseBottomLeftRock.jpg")).convert()
                        tile = Tile(x, y, img)
                        self.game.all_entity.add(tile)
                    #invoquer un buisson
                    elif tile == "b":
                        img = pygame.image.load(resource_path(f"assets/Tilesets/{self.name}/plain1.jpg")).convert()
                        tile = Tile(x, y, img)
                        self.all_tiles.add(tile)
                        img = pygame.image.load(resource_path(f"assets/Tilesets/{self.name}/bush1.png"))
                        tile = Tile(x, y, img)
                        self.game.all_entity.add(tile)
                    elif tile == "S":
                        img = pygame.image.load(resource_path(f"assets/Tilesets/{self.name}/StairTop.jpg")).convert()
                        tile = Tile(x, y, img)
                        self.all_tiles.add(tile)
                    elif tile == "s":
                        img = pygame.image.load(resource_path(f"assets/Tilesets/{self.name}/sand1.jpg")).convert()
                        tile = Tile(x, y, img)
                        self.all_tiles.add(tile)
                    elif tile == "W":
                        img = pygame.image.load(resource_path(f"assets/Tilesets/{self.name}/seaTop.jpg")).convert()
                        tile = Tile(x, y, img)
                        self.all_tiles.add(tile)
                    elif tile == "w":
                        img = pygame.image.load(resource_path(f"assets/Tilesets/{self.name}/sea1.jpg")).convert()
                        tile = Tile(x, y, img)
                        self.all_liquid_tiles.add(tile)
                    elif tile == "a":
                        img = pygame.image.load(resource_path(f"assets/Tilesets/{self.name}/TopSea.jpg")).convert()
                        tile = Tile(x, y, img)
                        self.all_liquid_tiles.add(tile)
                    elif tile == "g":
                        img = pygame.image.load(resource_path(f"assets/Tilesets/{self.name}/RightSea.jpg")).convert()
                        tile = Tile(x, y, img)
                        self.all_liquid_tiles.add(tile)
                    elif tile == "d":
                        img = pygame.image.load(resource_path(f"assets/Tilesets/{self.name}/BottomSea.jpg")).convert()
                        tile = Tile(x, y, img)
                        self.all_liquid_tiles.add(tile)
                    elif tile == "f":
                        img = pygame.image.load(resource_path(f"assets/Tilesets/{self.name}/LeftSea.jpg")).convert()
                        tile = Tile(x, y, img)
                        self.all_liquid_tiles.add(tile)
                    elif tile == "A":
                        img = pygame.image.load(resource_path(f"assets/Tilesets/{self.name}/ReverseTopLeftSea.jpg")).convert()
                        tile = Tile(x, y, img)
                        self.all_liquid_tiles.add(tile)
                    elif tile == "G":
                        img = pygame.image.load(resource_path(f"assets/Tilesets/{self.name}/ReverseTopRightSea.jpg")).convert()
                        tile = Tile(x, y, img)
                        self.all_liquid_tiles.add(tile)
                    elif tile == "D":
                        img = pygame.image.load(resource_path(f"assets/Tilesets/{self.name}/ReverseBottomRightSea.jpg")).convert()
                        tile = Tile(x, y, img)
                        self.all_liquid_tiles.add(tile)
                    elif tile == "F":
                        img = pygame.image.load(resource_path(f"assets/Tilesets/{self.name}/ReverseBottomLeftSea.jpg")).convert()
                        tile = Tile(x, y, img)
                        self.all_liquid_tiles.add(tile)
                    elif tile == "c":
                        img = pygame.image.load(resource_path(f"assets/Tilesets/{self.name}/BottomRightSea.jpg")).convert()
                        tile = Tile(x, y, img)
                        self.all_liquid_tiles.add(tile)
                    elif tile == "v":
                        img = pygame.image.load(resource_path(f"assets/Tilesets/{self.name}/BottomLeftSea.jpg")).convert()
                        tile = Tile(x, y, img)
                        self.all_liquid_tiles.add(tile)

                    # invoquer un gros caillou
                    elif tile == "M":
                        img = pygame.image.load(resource_path(f"assets/Tilesets/{self.name}/plain1.jpg")).convert()
                        tile = Tile(x, y, img)
                        self.all_tiles.add(tile)
                        img = random.choice([pygame.image.load(resource_path(f"assets/Tilesets/{self.name}/rock1.png")).convert_alpha(),
                                             pygame.image.load(resource_path(f"assets/Tilesets/{self.name}/rock2.png")).convert_alpha(),
                                             pygame.image.load(resource_path(f"assets/Tilesets/{self.name}/rock3.png")).convert_alpha(),
                                             pygame.image.load(resource_path(f"assets/Tilesets/{self.name}/rock4.png")).convert_alpha()])
                        tile = Tile(x, y, img)
                        self.game.all_entity.add(tile)

                    elif tile == "m":
                        img = pygame.image.load(resource_path(f"assets/Tilesets/{self.name}/PlainTop.jpg")).convert()
                        tile = Tile(x, y, img)
                        self.game.all_entity.add(tile)

                    # invoquer une fleur
                    elif tile == ";":
                        img = pygame.image.load(resource_path(f"assets/Tilesets/{self.name}/plain1.jpg")).convert()
                        tile = Tile(x, y, img)
                        self.all_tiles.add(tile)
                        img = pygame.image.load(resource_path(f"assets/Tilesets/{self.name}/flower1.png"))
                        tile = Tile(x, y, img)
                        self.all_floor_decorations.add(tile)

                    elif tile == "*":
                        img = pygame.image.load(resource_path(f"assets/Tilesets/{self.name}/special.jpg")).convert()
                        tile = Tile(x, y, img)
                        self.all_tiles.add(tile)

                    # invoquer un petit caillou
                    elif tile == "r":
                        img = pygame.image.load(resource_path(f"assets/Tilesets/{self.name}/plain1.jpg")).convert()
                        tile = Tile(x, y, img)
                        self.all_tiles.add(tile)
                        img = pygame.image.load(resource_path(f"assets/Tilesets/{self.name}/puddle1.png"))
                        tile = Tile(x, y, img)
                        self.all_floor_decorations.add(tile)

                    #invoquer une maison
                    elif tile == "H":
                        img = pygame.image.load(resource_path(f"assets/Tilesets/{self.name}/plain1.jpg")).convert()
                        tile = Tile(x, y, img)
                        self.all_tiles.add(tile)
                        img = pygame.image.load(resource_path(f"assets/house.png")).convert_alpha()
                        hsize_x,hsize_y = img.get_size()
                        img = pygame.transform.smoothscale(img,(round(hsize_x/4),round(hsize_y/4)))
                        tile = Tile(x, y, img)
                        self.game.all_entity.add(tile)

                    # SPAWN MONSTRES
                    elif tile == "x":
                        img = pygame.image.load(resource_path(f"assets/Tilesets/{self.name}/plain1.jpg")).convert()
                        tile = Tile(x, y, img)
                        self.all_tiles.add(tile)
                        monster = Monster(self)
                        if self.name == "map0":
                            monster.name = "slime"
                            monster_image = pygame.image.load(resource_path("assets/sprites/Ennemy/slime1_3eme_version.png")).convert_alpha()
                            size_x, size_y = monster_image.get_size()
                            monster_image = pygame.transform.smoothscale(monster_image,
                                                                (round(size_x / 9), round(size_y / 9)))
                        elif self.name == "map1":
                            monster.name = "spider"
                            monster_image = pygame.image.load(resource_path("assets/sprites/Ennemy/spider2.png")).convert_alpha()
                            size_x, size_y = monster_image.get_size()
                            monster_image = pygame.transform.smoothscale(monster_image,
                                                                (round(size_x / 3), round(size_y / 3)))

                        elif self.name == "map3":
                            monster.name = "tesseract"
                            monster_image = pygame.image.load(resource_path("assets/sprites/Ennemy/spider3.png")).convert_alpha()
                            size_x, size_y = monster_image.get_size()
                            monster_image = pygame.transform.smoothscale(monster_image,
                                                                (round(size_x / 5), round(size_y / 5)))
                            monster.speed_projectile = 5
                            monster.fly_liquids = True
                        elif self.name == "map4":
                            monster.name = "nuzlock"
                            monster_image = pygame.image.load(resource_path("assets/sprites/Ennemy/Nuzlock.png")).convert_alpha()
                            size_x, size_y = monster_image.get_size()
                            monster_image = pygame.transform.smoothscale(monster_image,
                                                                (round(size_x / 6), round(size_y / 6)))
                            monster.speed_projectile = 7

                        elif self.name == "map5":
                            monster = Dragon(self)
                            monster_image = pygame.image.load(resource_path("assets/sprites/Ennemy/dragon1.png")).convert_alpha()

                        monster.image = monster_image
                        monster.rect = monster.image.get_rect()
                        monster.rect.x = x
                        monster.rect.y = y
                        self.all_monsters.add(monster)

                    elif tile == "X":
                        img = pygame.image.load(resource_path(f"assets/Tilesets/{self.name}/plain1.jpg")).convert()
                        tile = Tile(x, y, img)
                        self.all_tiles.add(tile)
                        monster = Monster(self)
                        if self.name == "map0":
                            monster.name = "red_slime"
                            monster_image = pygame.image.load(
                                resource_path("assets/sprites/Ennemy/slime2.png")).convert_alpha()
                            size_x, size_y = monster_image.get_size()
                            monster_image = pygame.transform.smoothscale(monster_image,
                                                                         (round(size_x / 3), round(size_y / 3)))

                        size_x, size_y = monster_image.get_size()
                        monster_image = pygame.transform.smoothscale(monster_image,
                                                                     (round(size_x / 3), round(size_y / 3)))

                        monster.image = monster_image
                        monster.rect = monster.image.get_rect()
                        monster.rect.x = x
                        monster.rect.y = y
                        self.all_monsters.add(monster)

                    else:pass

                    x+=64
                y+=64
                self.update = True

class Camera(object):
    def __init__(self,game, width, height):
        self.game = game
        self.camera_func = self.complex_camera
        self.state = pygame.Rect(0, 0, 1920, 1080)
        self.width = width
        self.height = height

    def apply(self, target, detail=None):
        if detail == "particule":
            if len(target) == 5:
                particule = [[target[0][0]+self.state.x, target[0][1]+self.state.y], target[1],
                             target[2],target[3],target[4]]
            else:
                particule = [[target[0][0]+self.state.x, target[0][1]+self.state.y], target[1],
                             target[2], target[3]]
            return particule
        elif detail == "hitbox":
            self.game.player.hitbox.x, self.game.player.hitbox.y = self.state.x+self.game.player.rect.x+25, self.state.y+self.game.player.rect.y+25
            return
        return target.rect.move(self.state.topleft)

    def update(self, target):
        #self.state = self.camera_func(self.state, target.rect)
        self.state = self.camera_func(self.state, target.rect)
        x = -target.rect.x + pygame.display.Info().current_w / 2
        y = -target.rect.y + pygame.display.Info().current_h / 2
        self.state = pygame.Rect(x, y, self.width, self.height)

    def complex_camera(self, camera, target_rect):
        left, top, _, _ = target_rect
        _, _, width, height = camera
        left, top, _, _ = left + width / 2, -top + height / 2, width, height

        left = min(0, left)  # stop scrolling at the left edge
        left = max(-(camera.width - 1920), left)  # stop scrolling at the right edge
        top = max(-(camera.height - 1080), top)  # stop scrolling at the bottom
        top = min(0, top)  # stop scrolling at the top
        return pygame.Rect(left, top, width, height)




