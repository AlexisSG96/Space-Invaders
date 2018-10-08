"""
Name: Alexis Steven Garcia
Project: Space Invaders
Date: October 8, 2018
Email: AlexisSG96@csu.fullerton.edu
"""

import pygame
from pygame.sprite import Sprite


class Laser(Sprite):
    """Manages lasers fired from aliens"""
    def __init__(self, ai_settings, screen, alien):
        """Follows same logic as the bullet class"""
        super().__init__() 
        self.screen = screen 

        # Initialize laser image
        self.image = pygame.image.load('images/invader_laser.png')
        self.rect = self.image.get_rect()

        # Laser is shot from the bottom of alien
        self.rect.centerx = alien.rect.centerx 
        self.rect.top = alien.rect.bottom 

        # Y position and speed factor 
        self.y = float(self.rect.y) 
        self.speed_factor = ai_settings.laser_speed_factor

    def update(self): 
        """Move the laser down the screen""" 
        self.y += self.speed_factor 
        self.rect.y = self.y 

    def blitme(self): 
        """Draw the laser on the screen""" 
        self.screen.blit(self.image, self.rect) 
