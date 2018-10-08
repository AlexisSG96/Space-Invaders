"""
Name: Alexis Steven Garcia
Project: Space Invaders
Date: October 8, 2018
Email: AlexisSG96@csu.fullerton.edu
"""
import pygame
import game_functions as gf
from game_stats import GameStats 
from scoreboard import Scoreboard 
from button import Button 
from settings import Settings 
from ship import Ship
from bunker import create_bunker

  
def run_game():
    """Create the game and run it."""
    pygame.init()

    # Setup pygame, settings, display, and start button
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('Space Invaders')
    play_button = Button(ai_settings=ai_settings, screen=screen, msg='Play')
  
    # Setup game stats and scoreboard 
    stats = GameStats(ai_settings=ai_settings)
    sb = Scoreboard(ai_settings=ai_settings, screen=screen, stats=stats)

    # Setup ship, bullets, lasers, aliens, and ufo
    ship = Ship(ai_settings=ai_settings, screen=screen)
    bullets = pygame.sprite.Group() 
    lasers = pygame.sprite.Group() 
    aliens = pygame.sprite.Group()
    ufo = pygame.sprite.Group()

    # Create 4 bunkers
    bunker = pygame.sprite.Group(create_bunker(ai_settings, screen, 0),
                                 create_bunker(ai_settings, screen, 1),
                                 create_bunker(ai_settings, screen, 2),
                                 create_bunker(ai_settings, screen, 3))

    # Create a fleet of invaders
    gf.create_fleet(ai_settings=ai_settings, screen=screen, ship=ship, aliens=aliens)
   
    while True: 
        gf.check_events(ai_settings=ai_settings, screen=screen, stats=stats, sb=sb,
                        play_button=play_button, ship=ship, aliens=aliens, lasers=lasers, bullets=bullets)
        if stats.game_active: 
            ship.update() 
            gf.update_bullets(ai_settings=ai_settings, screen=screen, stats=stats, sb=sb,
                              ship=ship, aliens=aliens, lasers=lasers, bullets=bullets, ufo=ufo)
            gf.update_lasers(ai_settings=ai_settings, screen=screen, stats=stats, sb=sb,
                             ship=ship, aliens=aliens, lasers=lasers, bullets=bullets, ufo=ufo)
            gf.update_aliens(ai_settings=ai_settings, screen=screen, stats=stats, sb=sb, ship=ship,
                             aliens=aliens, lasers=lasers, bullets=bullets, ufo=ufo)
        gf.update_screen(ai_settings=ai_settings, screen=screen, stats=stats, sb=sb, ship=ship, aliens=aliens,
                         lasers=lasers, bullets=bullets, play_button=play_button, bunkers=bunker, ufo=ufo)


run_game()
