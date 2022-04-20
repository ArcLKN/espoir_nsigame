import pygame
from Caracters.Smile import Smile
from Caracters.Dragon import Dragon
import sys, os
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

black_color = [0,0,0]


class Cutscenes():

    def __init__(self,game):
        self.is_narrating = False
        self.game = game
        self.player = self.game.player
        self.menu = self.game.start_menu
        self.number_story = int()

        self.i = 0
        self.y = 0
        self.state = 0

        self.text = str()
        self.textl2 = ""
        self.actual_texte = str()
        self.actual_textel2 = str()
        self.font = pygame.font.SysFont('Comic Sans MS', 48)
        self.textsurface = self.font.render(self.actual_texte, True, (255,255,255))
        self.textsurfacel2 = self.font.render(self.actual_texte, True, (255, 255, 255))
        self.num_texte = 1
        self.max_texte = int()
        self.list_text = []
        self.state_caracter = []

        self.cat = Smile()
        self.dragon = Dragon()

        self.banner = pygame.image.load(resource_path(r"assets\sprites\Talk_Icon\banner.png"))
        self.banner_rect = self.banner.get_rect()
        self.banner_rect.y = 500

        self.number_image = 1

        self.text_y = -1000


    def redraw(self,screen):
        screen.fill(black_color)

        for e in self.game.map.all_tiles:
            if (self.player.rect.x + 64 * 13 > e.rect.x > self.player.rect.x - 64 * 14) and (
                    self.player.rect.y + 64 * 7 > e.rect.y > self.player.rect.y - 64 * 8):
                screen.blit(e.image, self.game.camera.apply(e))
        for e in self.game.map.all_liquid_tiles:
            if (self.player.rect.x + e.size_x * 13 > e.rect.x > self.player.rect.x - e.size_x * 14) and (self.player.rect.y + e.size_y * 7 > e.rect.y > self.player.rect.y - e.size_y * 8):
                screen.blit(e.image, self.game.camera.apply(e))
        for e in self.game.map.all_solid_decorations:
            if (self.player.rect.x + 64 * 13 > e.rect.x > self.player.rect.x - 64 * 14) and (
                    self.player.rect.y + 64 * 7 > e.rect.y > self.player.rect.y - 64 * 8):
                screen.blit(e.image, self.game.camera.apply(e))
        for e in self.game.map.all_floor_decorations:
            if (self.player.rect.x + 64 * 13 > e.rect.x > self.player.rect.x - 64 * 14) and (
                    self.player.rect.y + 64 * 7 > e.rect.y > self.player.rect.y - 64 * 8):
                screen.blit(e.image, self.game.camera.apply(e))
        for e in self.game.all_entity:
            if (self.player.rect.x + 64 * 13 > e.rect.x > self.player.rect.x - 64 * 14) and (
                    self.player.rect.y + 64 * 7 > e.rect.y > self.player.rect.y - 64 * 8):
                screen.blit(e.image, self.game.camera.apply(e))
        for e in self.game.all_players:
            screen.blit(e.image, self.game.camera.apply(e))
            self.game.camera.update(e)

    def fadein(self, screen):
        fade = pygame.Surface(self.game.resolution)
        fade.fill(black_color)
        fade.set_alpha(300)
        for alpha in range(300):
            fade.set_alpha(300-alpha)
            self.redraw(screen)
            screen.blit(fade,(0,0))
            pygame.display.flip()
            pygame.time.delay(5)

    def fadeout(self, screen):
        fade = pygame.Surface(self.game.resolution)
        fade.fill(black_color)
        fade.set_alpha(0)
        for alpha in range(300):
            fade.set_alpha(alpha)
            self.redraw(screen)
            screen.blit(fade,(0,0))
            pygame.display.flip()
            pygame.time.delay(5)


    def scene_0(self,screen):

        self.redraw(screen)  # redessine l'écran

        if self.state == 0:
            self.player.image = pygame.image.load(resource_path("assets/sprites/Player/cartoonWOAback.png"))
            size_x, size_y = self.player.image.get_size()
            self.player.image = pygame.transform.smoothscale(self.player.image,(int(size_x/1920*1536/2.5),int(size_x/1920*1536/2.5)))
            self.game.player.rect.y = 3900  # Valeur initiale = 3700
            self.game.player.rect.x = 1400  # Valeur initiale = 1400
            self.state = 1  # Passage à la scène suivante
            #self.fadeout(screen)

        if self.state == 1:
            if self.game.player.rect.y > 3500:
                self.game.player.rect.y -= 1  # Valeur initiale = 1
            else:
                for i in range(10):
                    self.game.player.rect.y -= 2
                self.state = 2  # Passage à la scène suivante, valeur initiale = 2
        elif self.state == 2:
            if self.i < 320:  # Valeur initiale = 320
                if self.y < 80:
                    self.game.player.rect.y += 1
                    self.y += 1
                elif self.y < 160:
                    self.game.player.rect.y -= 1
                    self.y += 1
                else:self.y = 0
                self.i += 1
            else:
                self.state = 3  # Passe à la scène suivante. Valeur initiale = 3
        elif self.state == 3:
            self.cat.downanimate()
            if self.cat.rect.y < 300:
                self.cat.rect.y += 4
            if self.cat.rect.x < 650:
                self.cat.rect.x += 4
            else:
                self.state = 4  # Passe à la scène suivante. Valeur initiale = 4
                self.i = 0
                self.y = 0
                self.max_texte = 16  # Nombre maximum de texte
        elif self.state == 4:
            screen.blit(self.game.player.image, self.game.player.rect)
            if self.num_texte == 1:
                self.text = 'Hm...'
            elif self.num_texte == 2:
                self.text = 'Étrange coincidence...'
            elif self.num_texte == 3:
                self.text = "Il a l'air bien mal en point en tout cas."
            elif self.num_texte == 4:
                self.text = "Que devrais-je faire..."
            elif self.num_texte == 5:  # Joueur arrive
                self.text = "...!"
                self.state_caracter = ['off','on']
            elif self.num_texte == 6:
                self.text = "Ah! Tiens il se réveille!"
                self.state_caracter = ['on','off']
            elif self.num_texte == 7:
                self.text = "Hey! Ca va ?"
                self.state_caracter = ['on','off']
            elif self.num_texte == 8:
                self.text = "Hm... j'ai vraiment mal à la tête... mais attend..."
                self.state_caracter = ['off','on']
            elif self.num_texte == 9:
                self.text = "COMMENT CA SE FAIT QUE TU PUISSES PARLER !!??"
                self.state_caracter = ['off','on']
            elif self.num_texte == 10:
                self.text = "Hmm... oui, j'imagine que cela doit paraître incroyable pour toi."
                self.textl2 = "Mais je t'en prie... calme toi."
                self.state_caracter = ['on','off']
            elif self.num_texte == 11:
                self.text = "Dis-toi juste que le dieu Camion-kun t'a envoyé dans ce monde..."
                self.textl2 = "Au bon moment d'ailleurs figure toi!"
                self.state_caracter = ['on','off']
            elif self.num_texte == 12:
                self.text = "Hm...d'accord."
                self.state_caracter = ['off', 'on']
            elif self.num_texte == 13:
                self.text = "Abrégeons. Nous n'avons pas de temps pour flemmarder."
                self.state_caracter = ['on','off']
            elif self.num_texte == 14:
                self.text = "Retrouve moi au village. Il se trouve au Nord de ces plaines."
                self.state_caracter = ['on','off']
            elif self.num_texte == 15:
                self.text = "Ah et oui... Tu devrais porter quelque chose..."
                self.textl2 = "Prend cette armure... c'est tout ce que j'ai."
                self.state_caracter = ['on','off']
                self.player.image = pygame.image.load("assets/sprites/Player/cartoonback1.png")
                size_x, size_y = self.player.image.get_size()
                self.player.image = pygame.transform.smoothscale(self.player.image, (
                int(size_x / 1920 * 1536 / 2.5), int(size_x / 1920 * 1536 / 2.5)))
            elif self.num_texte == 16:
                self.text = "Prend aussi ce grimoire,"
                self.textl2 = "il ne faudrait pas qu'il t'arrive un accident malencontreux."
                self.state_caracter = ['on','off']

            if len(self.text) + len(self.textl2) == self.i:  # Vérifie que c'est le dernier caractère
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:  # Attend une touche pour passer au txt suivant
                        if not self.num_texte == self.max_texte:  # Vérifie que ce n'est pas le dernier texte
                            self.num_texte += 1
                            self.actual_texte = str()
                            self.actual_textel2 = str()
                            self.text = str()
                            self.textl2 = ""
                            self.i = 0
                        else:
                            self.text = str()
                            self.list_text = []
                            self.textl2 = str()
                            self.actual_texte = str()
                            self.actual_textel2 = ()
                            self.state = 5
            else:
                if self.i < len(self.text):
                    self.textsurfacel2 = self.font.render("", True, (255, 255, 255))
                    self.actual_texte += self.text[self.i]
                    self.textsurface = self.font.render(self.actual_texte, True, (255, 255, 255))
                    self.i += 1
                elif not self.textl2 == "":
                    self.actual_textel2 += self.textl2[self.i-len(self.text)]
                    self.textsurfacel2 = self.font.render(self.actual_textel2, True, (255, 255, 255))
                    self.i += 1
                else:
                    self.textsurfacel2 = self.font.render("", True, (255, 255, 255))

        elif self.state == 5:
            if self.cat.rect.y > -100:
                self.cat.rect.y -= 4
            else:
                self.state = 0
                self.game.start_menu.is_playing = True
                self.is_narrating = False
                self.number_story = 1
                self.player.rect.width = 64
                self.player.rect.height = 125

        screen.blit(self.game.player.image, self.game.player.rect)
        if self.state in [3,5]:
            screen.blit(self.cat.image, self.cat.rect)
        if self.state in [4]:
            screen.blit(self.cat.image, self.cat.rect)
            screen.blit(self.banner,self.banner_rect)
            if self.state_caracter == ['on','off']:
                self.cat.avataranimate()
                screen.blit(self.player.avatar_off,self.player.avatar_rect)
                screen.blit(self.cat.avatar,self.cat.avatar_rect)
                screen.blit(self.cat.title, self.cat.title_rect)
            elif self.state_caracter == ['off','on']:
                screen.blit(self.player.avatar,self.player.avatar_rect)
                screen.blit(self.player.title, self.player.title_rect)
                screen.blit(self.cat.avatar_off,self.cat.avatar_rect)
            else:
                self.cat.avataranimate()
                screen.blit(self.cat.avatar,self.cat.avatar_rect)
                screen.blit(self.cat.title, self.cat.title_rect)
            screen.blit(self.textsurface,(30,560))
            screen.blit(self.textsurfacel2, (30, 630))


    def scene_1(self,screen):
        self.redraw(screen)
        if self.state == 0:
            self.game.player.image = pygame.transform.smoothscale(pygame.image.load(resource_path("assets\sprites\Player\cartoonback1.png")),
                                                                  (int(self.game.player.size_x / 3.2), int(self.game.player.size_x / 3.2)))
            self.game.player.rect.x = 1810
            self.game.player.rect.y = 2550
            self.state = 1  # Passe à la scène suivante. Valeur initiale = 1
        elif self.state == 1:
            if self.game.player.rect.y > 2000:
                self.game.player.rect.y -= 10
            else:
                self.cat.rect.x = -100
                self.cat.rect.y = -100
                self.state = 2  # Passe à la scène suivante. Valeur initiale = 2
                self.number_image = 1
                self.game.player.avatar = pygame.image.load(resource_path(r"assets\sprites\Talk_Icon\Player\1-1.png"))
                self.game.player.avatar_off = pygame.image.load(resource_path(r"assets\sprites\Talk_Icon\Player\1-0.png"))
                self.game.player.avatar_rect.y = -20  # -20
                self.game.player.avatar_rect.x = 900  # 900
        elif self.state == 2:
            if self.cat.rect.y < 350:
                self.cat.rect.y += 4
                if self.number_image == 1:self.number_image = 2
                else:self.number_image = 1
                self.cat.image = pygame.image.load(resource_path(f"assets\sprites\Lame\Front{self.number_image}.png"))
                self.cat.rect.x += 6
            else:
                self.cat.image = pygame.image.load(resource_path(f"assets\sprites\Lame\Front1.png"))
                self.state = 3
                self.i = 0
                self.num_texte = 0  # numéro du premier texte. Valeur initiale = 0
                self.list_text = [
                    ["Ah te voilà enfin.",[True,False]],
                    ["Tu en as mit du temps.", [True, False]],
                    ["M'enfin passons. Nous n'avons pas le temps.", [True, False]],
                    ["Si tu es arrivé ici c'est que tu as bien quelques tripes j'imagine.", [True, False]],
                    ["Te voici dans le village de Seulvillage !", [True, False]],
                    ["Si tu as besoins de quoique ce soit pendant ton aventure.", [True, False], "Tu peux l'acheter ici."],
                    ["Au Nord du village tu vas trouver ce pour quoi tu es ici.", [True, False]],
                    ["Mais fais attention si tu y vas, c'est la que commence", [True, False], "les vrai dangers."],
                    ["Mais ducoup je suis ici pour quoi..?", [False, True]],
                    ["Tu poses trop de question.", [True, False]],
                    ["Dis toi juste que le mal opprime de faibles créatures", [True, False], "telles que nous."],
                    ["Mais c'est pas gentil d'être méchant !", [False, True]],
                    ["Oui. Et c'est pas méchant d'être gentil.", [True, False]],
                    ["*choqué de la brutalité des propos*", [False, True]],
                    ["Seul toi peut y remédier.", [True, False]],
                    ["Je compte sur toi Héro !", [True, False]],
                    ["Non..!", [True, False]],
                    ["Le monde compte sur toi ! *petite larme*", [True, False]],
                    ["Je vois..! Alors vous pouvez compter sur moi !", [False, True]],
                    ["Merci Héro, le monde s'en souviendra.", [True, False]],
                    ["Bonne chance.", [True, False]]
                ]
                self.max_texte = len(self.list_text)-1

        elif self.state == 3:

            self.text = self.list_text[self.num_texte][0]
            self.state_caracter = self.list_text[self.num_texte][1]
            if len(self.list_text[self.num_texte]) >= 3:
                print(self.list_text[self.num_texte][2])
                self.textl2 = self.list_text[self.num_texte][2]

            if len(self.text) + len(self.textl2) == self.i:  # Vérifie que c'est le dernier caractère
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:  # Attend une touche pour passer au txt suivant
                        if not self.num_texte == self.max_texte:  # Vérifie que ce n'est pas le dernier texte
                            self.num_texte += 1
                            self.actual_texte = str()
                            self.actual_textel2 = str()
                            self.text = str()
                            self.textl2 = ""
                            self.i = 0
                        else:
                            self.text = str()
                            self.list_text = []
                            self.textl2 = str()
                            self.actual_texte = str()
                            self.actual_textel2 = ()
                            self.state = 4


            elif self.i < len(self.text):
                self.textsurfacel2 = self.font.render("", True, (255, 255, 255))
                self.actual_texte += self.text[self.i]
                self.textsurface = self.font.render(self.actual_texte, True, (255, 255, 255))
                self.i += 1
            elif not self.textl2 == "" and (len(self.text) + len(self.textl2) > self.i):
                self.actual_textel2 += self.textl2[self.i - len(self.text)]
                self.textsurfacel2 = self.font.render(self.actual_textel2, True, (255, 255, 255))
                self.i += 1
            else:
                self.textsurfacel2 = self.font.render("", True, (255, 255, 255))

        elif self.state == 4:
            if self.cat.rect.y > - 100:
                self.cat.rect.y -= 4
            else:
                self.state = 0
                self.game.start_menu.is_playing = True
                self.is_narrating = False
                self.number_story = 2

        if self.state in [2]:
            screen.blit(self.cat.image, self.cat.rect)
        if self.state in [3]:
            screen.blit(self.cat.image, self.cat.rect)
            if self.state_caracter == [True,False]:
                self.cat.avataranimate()
                screen.blit(self.player.avatar_off,self.player.avatar_rect)
                screen.blit(self.cat.avatar,self.cat.avatar_rect)
                screen.blit(self.banner, self.banner_rect)
                screen.blit(self.cat.title, self.cat.title_rect)
            elif self.state_caracter == [False,True]:
                screen.blit(self.player.avatar,self.player.avatar_rect)
                screen.blit(self.cat.avatar_off,self.cat.avatar_rect)
                screen.blit(self.banner, self.banner_rect)
                screen.blit(self.player.title, self.player.title_rect)
            else:
                self.cat.avataranimate()
                screen.blit(self.cat.avatar,self.cat.avatar_rect)
                screen.blit(self.banner, self.banner_rect)
            screen.blit(self.textsurface,(30,560))
            screen.blit(self.textsurfacel2, (30, 630))

    def scene_2(self, screen):
        self.redraw(screen)
        for e in self.game.all_monsters:  # importer les images des monstres
            screen.blit(e.image, self.game.camera.apply(e))
        if self.state == 0:
            self.game.player.avatar = pygame.image.load(resource_path(r"assets\sprites\Talk_Icon\Player\1-1.png"))
            self.game.player.avatar_off = pygame.image.load(resource_path(r"assets\sprites\Talk_Icon\Player\1-0.png"))
            self.game.player.avatar_rect.x = 900  # 900
            self.player.avatar_rect.y -= 110
            self.game.player.image = pygame.transform.smoothscale(
                pygame.image.load(resource_path("assets\sprites\Player\cartoonback1.png")),
                (int(self.game.player.size_x / self.player.player_global_size),
                 int(self.game.player.size_x / self.player.player_global_size)))
            self.player.rect.x += 600
            self.banner = pygame.image.load(resource_path(r"assets\sprites\Talk_Icon\red_banner.png"))
            self.state = 1  # Passe à la scène suivante. Valeur initiale = 1
        elif self.state == 1:
            if self.game.player.rect.y > 1000:
                self.game.player.rect.y -= 6  # Valeur initiale = 4
            else:
                self.i = 0
                self.num_texte = 0  # numéro du premier texte. Valeur initiale = 0
                self.list_text = [
                    ["Qui ose venir s'infiltrer dans mon domaine !!!", [True, False]],
                    ["Je suis venu arrêter vos méfaits !!", [False, True]],
                    ["Je suis un méchant vraiment très très méchant.", [True, False]],
                    ["Comment comptes tu m'arrêter petit homme !?", [True, False]],
                    ["Le pouvoir de l'amitié n'a aucune limite !!", [False, True]],
                    ["Tu es un weeb ! Tu n'as aucun ami !", [True, False], "Mouahahahahahaahaha ψ(._. )>"],
                    ["*URGH* *comment peut-il être aussi puissant.*", [False, True]],
                    ["Hmpf ! Venant de la part d'un dragonnet qui a peur de sortir de", [False, True], "sa grotte ca ne me fait ni chaud ni froid."],
                    ["C'... c'est même pas vrai d'abord ! C'est juste que...", [True, False], "il fait pas très beau dehors..."],
                    ["Pff ton excuse est ridicule !", [False, True], "En garde malotru, tu ne me laisses pas le choix !!"],
                    ["GRRRRROOOOOUUUUUUAAA !!!!!!", [True, False]],
                ]
                self.max_texte = len(self.list_text) - 1
                self.state = 2  # Passage à la scène suivante, valeur initiale = 2
        elif self.state == 2:
            self.text = self.list_text[self.num_texte][0]
            self.state_caracter = self.list_text[self.num_texte][1]
            if len(self.list_text[self.num_texte]) >= 3:
                self.textl2 = self.list_text[self.num_texte][2]

            if len(self.text) + len(self.textl2) == self.i:  # Vérifie que c'est le dernier caractère
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:  # Attend une touche pour passer au txt suivant
                        if not self.num_texte == self.max_texte:  # Vérifie que ce n'est pas le dernier texte
                            self.num_texte += 1
                            self.actual_texte = str()
                            self.actual_textel2 = str()
                            self.text = str()
                            self.textl2 = ""
                            self.i = 0
                        else:
                            self.text = str()
                            self.list_text = []
                            self.textl2 = str()
                            self.actual_texte = str()
                            self.actual_textel2 = ()
                            self.state = 3

            elif self.i < len(self.text):
                self.textsurfacel2 = self.font.render("", True, (255, 255, 255))
                self.actual_texte += self.text[self.i]
                self.textsurface = self.font.render(self.actual_texte, True, (255, 255, 255))
                self.i += 1
            elif not self.textl2 == "" and (len(self.text) + len(self.textl2) > self.i):
                self.actual_textel2 += self.textl2[self.i - len(self.text)]
                self.textsurfacel2 = self.font.render(self.actual_textel2, True, (255, 255, 255))
                self.i += 1
            else:
                self.textsurfacel2 = self.font.render("", True, (255, 255, 255))

        elif self.state == 3:
            for e in self.game.all_monsters:
                e.state = 1
            self.state = 0
            self.game.start_menu.is_playing = True
            self.is_narrating = False
            self.number_story = 3

        if self.state in [2]:
            if self.state_caracter == [True, False]:
                screen.blit(self.player.avatar_off, self.player.avatar_rect)
                screen.blit(self.dragon.avatar, self.dragon.avatar_rect)
                screen.blit(self.banner, self.banner_rect)
                screen.blit(self.dragon.title, self.dragon.title_rect)
            elif self.state_caracter == [False, True]:
                screen.blit(self.player.avatar, self.player.avatar_rect)
                screen.blit(self.dragon.avatar_off, self.dragon.avatar_rect)
                screen.blit(pygame.image.load(resource_path("assets/sprites/Talk_Icon/banner.png")), self.banner_rect)
                screen.blit(self.player.title, self.player.title_rect)
            screen.blit(self.textsurface,(30,560))
            screen.blit(self.textsurfacel2, (30, 630))


    def scene_3(self, screen):
        self.redraw(screen)
        for e in self.game.all_monsters:  # importer les images des monstres
            screen.blit(e.image, self.game.camera.apply(e))
        if self.state == 0:
            self.game.player.avatar = pygame.image.load(resource_path(r"assets\sprites\Talk_Icon\Player\1-1.png"))
            self.game.player.avatar_off = pygame.image.load(resource_path(r"assets\sprites\Talk_Icon\Player\1-0.png"))
            self.game.player.avatar_rect.x = 900  # 900
            self.player.avatar_rect.y -= 110
            self.game.player.image = pygame.transform.smoothscale(
                pygame.image.load(resource_path("assets\sprites\Player\cartoonback1.png")),
                (int(self.game.player.size_x / self.player.player_global_size),
                 int(self.game.player.size_x / self.player.player_global_size)))
            self.player.rect.x = 2300
            self.player.rect.y = 1000
            self.banner = pygame.image.load(resource_path(r"assets\sprites\Talk_Icon\red_banner.png"))
            self.i = 0
            self.num_texte = 0  # numéro du premier texte. Valeur initiale = 0
            self.list_text = [
                ["URGH !!", [True, False]],
                ["Tu es puissant petit homme.", [True, False],"C'était un beau combat."],
                ["J'imagine que je n'ai pas le choix.", [True, False], "De toutes facons mes vacances sont bientôt terminées."],
                ["On se reverra mais pour l'instant je m'en vais.", [True, False]],
                ["À bientôt.", [True, False]],
            ]
            self.max_texte = len(self.list_text) - 1
            self.state = 1  # Passage à la scène suivante, valeur initiale = 1
            self.fadein(screen)

        elif self.state in [1,4]:
            self.text = self.list_text[self.num_texte][0]
            self.state_caracter = self.list_text[self.num_texte][1]
            if len(self.list_text[self.num_texte]) >= 3:
                self.textl2 = self.list_text[self.num_texte][2]

            if len(self.text) + len(self.textl2) == self.i:  # Vérifie que c'est le dernier caractère
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:  # Attend une touche pour passer au txt suivant
                        if not self.num_texte == self.max_texte:  # Vérifie que ce n'est pas le dernier texte
                            self.num_texte += 1
                            self.actual_texte = str()
                            self.actual_textel2 = str()
                            self.text = str()
                            self.textl2 = ""
                            self.i = 0
                        else:
                            self.text = str()
                            self.list_text = []
                            self.textl2 = str()
                            self.actual_texte = str()
                            self.actual_textel2 = ()
                            if self.state == 1:
                                self.state = 2
                                self.fadeout(screen)
                            elif self.state == 4:
                                self.state = 5


            elif self.i < len(self.text):
                self.textsurfacel2 = self.font.render("", True, (255, 255, 255))
                self.actual_texte += self.text[self.i]
                self.textsurface = self.font.render(self.actual_texte, True, (255, 255, 255))
                self.i += 1
            elif not self.textl2 == "" and (len(self.text) + len(self.textl2) > self.i):
                self.actual_textel2 += self.textl2[self.i - len(self.text)]
                self.textsurfacel2 = self.font.render(self.actual_textel2, True, (255, 255, 255))
                self.i += 1
            else:
                self.textsurfacel2 = self.font.render("", True, (255, 255, 255))

        elif self.state == 2:
            self.player.rect.x = 1800
            self.player.rect.y = 2200
            self.banner = pygame.image.load(resource_path(r"assets\sprites\Talk_Icon\banner.png"))
            self.game.map.name = "map2"
            self.game.map.music_theme = pygame.mixer.Sound(resource_path(r'assets\Sound\Town_Theme.wav'))
            self.game.map.update = False
            self.game.map.update_map()
            self.fadein(screen)
            self.state = 3
        elif self.state == 3:
            self.i = 0
            self.num_texte = 0  # numéro du premier texte. Valeur initiale = 0
            self.list_text = [
                ["Héro ! Te voilà de retour !", [True, False]],
                ["Je savais que nous pouvions compter sur toi !!", [True, False]],
                ["Nous te sommes infiniment reconnaisant. Et nous sommes désolé", [True, False], "de t'avoir lancé sur cette aventure sans trop ton consentement."],
                ["Je pense que maintenant tu peux rentrer chez toi,", [True, False],"nous t'avons préparer un moyen de rentrer."],
            ]
            self.max_texte = len(self.list_text) - 1
            self.state = 4

        elif self.state == 5:
            self.list_text = [
                "Thank you a lot to have played my game.",
                "I'm a beginner developper",
                "and i did pratically everything on my own.",
                "I hope you enjoyed ! :D",
                "",
                "Credits",
                "",
                "Tilesets :",
                "Lime Zu -> @lime_px",
                "",
                "Music :",
                "A guy I don't remember the name but thx",
                "",
                "Menu illustration :",
                "Yoshiro -> insta: yoshiro.hideyoshi",
                "",
                "Programmation :",
                "Me -> Kalido#9499",
                "",
                "Sprites :",
                "Me -> Kalido#9499",
                "",
                "Other things :",
                "Me -> Kalido#9499",
                "",
                "THE END"
            ]
            self.max_texte = len(self.list_text) - 1
            self.textsurface = self.font.render(self.list_text[self.num_texte], True,
                                                (255, 255, 255))
            self.num_texte = 0
            self.fadeout(screen)
            self.state = 6

        elif self.state == 6:
            screen.fill(black_color)
            if self.num_texte < self.max_texte:
                self.text_y += 5
                if self.text_y > 800:
                    self.num_texte+=1
                    self.textsurface = self.font.render(self.list_text[self.num_texte], True, (255,255,255))
                    self.text_y = -50
            else:
                self.text_y = -50
                self.state = 7
                pygame.font.SysFont('Comic Sans MS', 150)
                self.textsurface = self.font.render("THE END", True, (255, 255, 255))
                pygame.mixer.Channel(1).play(pygame.mixer.Sound(resource_path(r'assets\Sound\_Senbon_Zakura_-Piano_ballade_ver-.mp3')))
            screen.blit(self.textsurface, (400-len(self.list_text[self.num_texte])/2, self.text_y))

        elif self.state == 7:
            screen.fill(black_color)
            if self.text_y < 400:
                self.text_y += 1
                screen.blit(self.textsurface, (680, self.text_y))
            else:
                screen.blit(self.textsurface, (680, 400))
                pygame.time.wait(10000)
                self.game.start_menu.is_playing = False
                self.is_narrating = False
                self.game.start_menu.is_start_menu = True

        if self.state == 1:
            if self.state_caracter == [True, False]:
                screen.blit(self.player.avatar_off, self.player.avatar_rect)
                screen.blit(self.dragon.avatar, self.dragon.avatar_rect)
                screen.blit(self.banner, self.banner_rect)
                screen.blit(self.dragon.title, self.dragon.title_rect)
            elif self.state_caracter == [False, True]:
                screen.blit(self.player.avatar, self.player.avatar_rect)
                screen.blit(self.dragon.avatar_off, self.dragon.avatar_rect)
                screen.blit(pygame.image.load(resource_path("assets/sprites/Talk_Icon/banner.png")), self.banner_rect)
                screen.blit(self.player.title, self.player.title_rect)
            screen.blit(self.textsurface, (30, 560))
            screen.blit(self.textsurfacel2, (30, 630))
        elif self.state == 4:
            if self.state_caracter == [True, False]:
                screen.blit(self.player.avatar_off, self.player.avatar_rect)
                screen.blit(self.cat.avatar, self.cat.avatar_rect)
                screen.blit(self.banner, self.banner_rect)
                screen.blit(self.cat.title, self.cat.title_rect)
            elif self.state_caracter == [False, True]:
                screen.blit(self.player.avatar, self.player.avatar_rect)
                screen.blit(self.cat.avatar_off, self.cat.avatar_rect)
                screen.blit(pygame.image.load(resource_path("assets/sprites/Talk_Icon/banner.png")), self.banner_rect)
                screen.blit(self.player.title, self.player.title_rect)
            screen.blit(self.textsurface, (30, 560))
            screen.blit(self.textsurfacel2, (30, 630))


    # savoir quelle scène doit être jouée
    def scene_manager(self,screen):
        self.is_narrating = True
        self.menu.is_playing = False
        if self.number_story == 0:
            self.scene_0(screen)
        elif self.number_story == 1:
            self.scene_1(screen)
        elif self.number_story == 2:
            self.scene_2(screen)
        elif self.number_story == 3:
            self.scene_3(screen)