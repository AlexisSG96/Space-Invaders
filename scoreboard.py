"""
Name: Alexis Steven Garcia
Project: Space Invaders
Date: October 8, 2018
Email: AlexisSG96@csu.fullerton.edu
"""
import pygame.font
from pygame.sprite import Group
from ship import Ship


class Scoreboard:
    """Display the scoreboard."""
    def __init__(self, ai_settings, screen, stats):
        """Initialize scoreboard settings."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        # Font settings for scoring information
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 40)

        self.score_image = None
        self.score_rect = None
        self.high_score_image = None
        self.high_score_rect = None
        self.level_image = None
        self.level_rect = None
        self.ships = None
        
        # Prepare the initial score image
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ship()

    def prep_ship(self):
        """Prepare the ships in the upper left (Lives left)."""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def prep_score(self):
        """Prepare the score values."""
        # Want a rounded score for cleanness
        rounded_score = int(round(self.stats.score, -1))

        # Using the comma as a thousands separator
        score_temp = "{:,}".format(rounded_score)
        score_str = 'Score: ' + str(score_temp)
        self.score_image = self.font.render(score_str, True, self.text_color, self.ai_settings.bg_color)

        # Display the score at the top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 10

    def prep_high_score(self):
        """Prepare high score value."""
        # Same format as score
        high_score = int(round(self.stats.high_score, -1))

        high_score_str = 'High Score: ' + "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.ai_settings.bg_color)

        # Center the high score at the top of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """Prepare level image"""
        level_str = 'Level: ' + str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color, self.ai_settings.bg_color)

        # Position the level below the score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def show_score(self):
        """"Show the score, high score, level, and lives left to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)

        # Draw ships
        self.ships.draw(self.screen)
