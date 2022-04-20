# coding: utf8
import pygame  # importation des différents modules

import sys, os
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

pygame.init()  # initialiser le module pygame
from game import Game  # Importation de game.py

# définir une clock
clock = pygame.time.Clock()
FPS = 60

# définir les différentes couleurs
black_color = [0, 0, 0]

# Récupérer la taille d'écran de l'utilisateur.
base_resolution = [1920, 1080]  # Résolution de base : ca sert à rien honnêtement
display_w = pygame.display.Info().current_w  # Valeur de la largeur
display_h = pygame.display.Info().current_h  # Valeur de la hauteur
resolution = [display_w,display_h]
print(f"width = {resolution[0]}, height = {resolution[1]}")
screen = pygame.display.set_mode((resolution[0], int(resolution[1] - (75 / 1080 * resolution[1]))))  # Redimension écran

# définir arrière plan menu
bg = pygame.image.load(resource_path(r"assets\cover.png"))  # Initialisation background
bg = pygame.transform.smoothscale(bg, (display_w, display_h))  # Redimension background start_menu
bg_rect = bg.get_rect()

game = Game(resolution, screen)

# définir curseur
pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
cible_image = pygame.image.load(resource_path("cible.png"))
cible_size_x, cible_size_y = cible_image.get_size()
cible_image = pygame.transform.smoothscale(cible_image,(round(cible_size_x/8), round(cible_size_y/8)))
cible_size_x, cible_size_y = cible_image.get_size()
cible_rect = cible_image.get_rect()


def fade(screen):
    fade = pygame.Surface(resolution)
    fade.fill(black_color)
    for alpha in range(300):
        fade.set_alpha(alpha)
        screen.blit(bg,bg_rect)
        screen.blit(fade, (0, 0))
        pygame.display.flip()
        pygame.time.delay(5)

cast = 0  # Temps entre chaque sort (projectile) du joueur

game.all_players.add(game.player)
is_running = True
game.start_menu.is_start_menu = True

print(pygame.display.Info())
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])

Title_Screen_Theme = pygame.mixer.Sound(resource_path(r'assets\Sound\Title_Screen.wav'))

pygame.mixer.Channel(1).play(Title_Screen_Theme)

game.map.music_theme = pygame.mixer.Sound(resource_path(r'assets\Sound\Title_Screen.wav'))


while is_running:

    mouse_x, mouse_y = pygame.mouse.get_pos()
    cible_rect.x = mouse_x - cible_size_x / 2
    cible_rect.y = mouse_y - cible_size_y / 2


    pygame.display.set_caption(f"{clock.get_fps():.2f}")

    if game.start_menu.is_playing:  # temps de rechargement pour les projectiles du joueur
        cast += 0.1

    if game.start_menu.is_playing:  # Jeu normal
        game.update(screen)
    if game.start_menu.is_start_menu:
        screen.blit(bg, bg_rect)
        game.start_menu.start_menu(screen)
    if game.scene.is_narrating:
        game.scene.scene_manager(screen)
    if game.start_menu.is_escape_menu:  # Appose le Menu pause
        game.start_menu.escape_menu(screen)
    if game.start_menu.is_option_menu:  # Appose le Menu option
        game.start_menu.option_menu(screen, mouse_x)


    # Si on appuie sur le bouton fermer de la fenêtre, quitte le jeu.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        # Si une touche est appuyée
        elif event.type == pygame.KEYDOWN:
            game.player.pressed[event.key] = True
            if event.key == pygame.K_ESCAPE:  # Si la touche 'échap' est pressée
                # Ouvre le menu 'échap',
                if game.start_menu.is_playing:
                    game.start_menu.is_playing = False  # et met le jeu en pause.
                    game.start_menu.is_escape_menu = True
                elif game.start_menu.is_escape_menu:
                    game.start_menu.is_playing = True  # et met le jeu en pause.
                    game.start_menu.is_escape_menu = False

            if event.key == pygame.K_p:  # Si la touche I est pressée
                if game.start_menu.is_playing:
                    game.start_menu.is_playing = False
                else: game.start_menu.is_playing = True
        # Si une touche est relachée
        elif event.type == pygame.KEYUP:
            game.player.pressed[event.key] = False

        elif event.type == pygame.MOUSEBUTTONDOWN:

            # Pour lancer le jeu
            if game.start_menu.play_button_rect.collidepoint(event.pos) and not game.start_menu.is_option_menu:
                if game.start_menu.is_start_menu:
                    pygame.mixer.Channel(3).play(pygame.mixer.Sound(resource_path(r'assets\Sound\bouton_selection.mp3')))
                    game.start_menu.is_start_menu = False
                    screen.fill((black_color))
                    pygame.display.flip()
                    game.map.name = "map0"  # Valeur initiale "map0"
                    game.map.music_theme = pygame.mixer.Sound(resource_path(r'assets\Sound\1-02-Secrets-of-the-Woods.wav'))
                    build = game.map.update_map()  # Chargement de la map
                    game.scene.number_story = 0  # Valeur initiale = 0
                    # fade(screen)
                    game.start_menu.is_playing = False  # Valeur initiale = False
                    #game.scene.scene_manager(screen)
                elif game.start_menu.is_escape_menu:
                    game.start_menu.is_escape_menu = False
                    game.start_menu.is_playing = True
                    pygame.mixer.Channel(3).play(pygame.mixer.Sound(resource_path(r'assets\Sound\bouton_selection.mp3')))

                # Bouton pour aller au menu 'échap'
            elif game.escape_button_rect.collidepoint(event.pos):
                if game.start_menu.is_escape_menu:
                    pygame.mixer.Channel(3).play(pygame.mixer.Sound(resource_path(r'assets\Sound\bouton_selection.mp3')))
                    game.start_menu.is_playing = False
                    game.start_menu.is_escape_menu = True
                if not game.start_menu.is_escape_menu:
                    pygame.mixer.Channel(3).play(pygame.mixer.Sound(resource_path(r'assets\Sound\bouton_selection.mp3')))
                    game.start_menu.is_playing = True
                    game.start_menu.is_escape_menu = False

                # Bouton pour aller au menu option
            elif game.start_menu.option_button_rect.collidepoint(event.pos) and (game.start_menu.is_escape_menu or game.start_menu.is_start_menu):
                pygame.mixer.Channel(3).play(pygame.mixer.Sound(resource_path(r'assets\Sound\bouton_selection.mp3')))
                game.start_menu.is_escape_menu = False
                game.update(screen)
                game.start_menu.is_option_menu = True

                # Bouton pour quitter le jeu.
            elif game.start_menu.quit_button_rect.collidepoint(event.pos) and not game.start_menu.is_option_menu:
                if game.start_menu.is_escape_menu:
                    game.start_menu.is_escape_menu = False
                    game.start_menu.is_playing = False
                    game.start_menu.is_option_menu = False
                    game.start_menu.is_start_menu = True
                    pygame.mixer.Channel(3).play(pygame.mixer.Sound(resource_path(r'assets\Sound\goodbye_game.wav')))
                elif game.start_menu.is_start_menu:
                    pygame.mixer.Channel(3).play(pygame.mixer.Sound(resource_path(r'assets\Sound\goodbye_game.wav')))
                    is_running = False

            elif game.start_menu.is_option_menu and game.start_menu.sound_cursor_rect.collidepoint(event.pos):
                game.start_menu.sound_cursor_is_following = True

            if game.start_menu.is_playing:
                if event.button == 1:
                    if cast >= game.player.projectile.cast:
                        if len(game.player.all_projectiles) < game.player.projectile.max_projectile:
                            game.player.launch_projectile(mouse_x, mouse_y)
                            cast = 0

        elif event.type == pygame.MOUSEBUTTONUP:
            if game.start_menu.is_option_menu:
                if game.start_menu.sound_cursor_is_following:
                    game.start_menu.sound_cursor_is_following = False


    # affiche le curseur
    screen.blit(cible_image, cible_rect)

    pygame.display.flip()

    # fixer le nombre de FPS
    clock.tick(FPS)

pygame.quit()
