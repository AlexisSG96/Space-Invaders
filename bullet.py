"""
Name: Alexis Steven Garcia
Project: Space Invaders
Date: October 8, 2018
Email: AlexisSG96@csu.fullerton.edu
"""
import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Manages bullets fired from a ship"""
    def __init__(self, ai_settings, screen, ship):
        """Create a bullet object at the given ship's current position."""
        super() .__init__()
        self.screen = screen

        # Create a bullet rect and set correct dimensions
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)

        # Shoots out of top of ship
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Store the bullet's position as a decimal value
        self.y = float(self.rect.y)

        # Color of ships bullet and speed
        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """Move bullet shot from ship up the screen"""
        # Update the decimal position of the bullet
        self.y -= self.speed_factor
        # Update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw bullet on the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)
