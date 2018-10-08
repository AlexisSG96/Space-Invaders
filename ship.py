"""
Name: Alexis Steven Garcia
Project: Space Invaders
Date: October 8, 2018
Email: AlexisSG96@csu.fullerton.edu
"""
import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """Represents ship object."""
    def __init__(self, ai_settings, screen):
        """Create the ship."""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the ship image and get its rect
        self.ship_image = None
        self.image = None
        self.death_frames = None
        self.death_index = None
        self.last_frame = None
        self.initialize_images()
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each new ship at the bottom center of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Store a decimal value for the ship's center
        self.center = float(self.rect.centerx)

        # Movement flag
        self.moving_right = False
        self.moving_left = False

        # Status flag
        self.dead = False

        # Sound
        self.ship_death_sound = pygame.mixer.Sound('sounds/ship_death.wav')
        self.ship_death_sound.set_volume(0.5)
        self.ship_shoot = pygame.mixer.Sound('sounds/invader_shoot.wav')
        self.ship_shoot.set_volume(0.5)
        self.channel = ai_settings.ship_channel

    def initialize_images(self):
        """Initialize ship images and death animation."""
        self.ship_image = pygame.image.load('images/ship.png')
        self.image = self.ship_image
        self.death_frames = []
        self.death_frames.append(pygame.image.load('images/ship_death/ship_death_1.png'))
        self.death_frames.append(pygame.image.load('images/ship_death/ship_death_2.png'))
        self.death_frames.append(pygame.image.load('images/ship_death/ship_death_3.png'))
        self.death_frames.append(pygame.image.load('images/ship_death/ship_death_4.png'))
        self.death_frames.append(pygame.image.load('images/ship_death/ship_death_5.png'))
        self.death_frames.append(pygame.image.load('images/ship_death/ship_death_6.png'))

    def update(self):
        """Update based on whether ship is alive or has been destroyed."""
        # If not dead, move the ship
        if not self.dead:
            # Update the ship's center value, not the rect
            if self.moving_right and self.rect.right < self.screen_rect.right:
                self.center += self.ai_settings.ship_speed_factor
            if self.moving_left and self.rect.left > 0:
                self.center -= self.ai_settings.ship_speed_factor

            # Update rect object from self.center
            self.rect.centerx = self.center
        # Else is dead so start death animation
        else:
            time_test = pygame.time.get_ticks()
            if abs(time_test - self.last_frame) > 250:
                self.death_index += 1
                if self.death_index < len(self.death_frames):
                    self.image = self.death_frames[self.death_index]
                    self.last_frame = time_test
                else:
                    self.dead = False
                    self.image = self.ship_image

    def center_ship(self):
        """Center the ship to middle bottom."""
        self.center = self.screen_rect.centerx

    def ship_death(self):
        """Ship dead settings"""
        self.dead = True
        self.death_index = 0
        self.image = self.death_frames[self.death_index]
        self.last_frame = pygame.time.get_ticks()
        self.channel.play(self.ship_death_sound)

    def ship_bullet_sound(self):
        """Play ship shoot sound."""
        self.channel.play(self.ship_shoot)

    def blitme(self):
        """Draw ship to the screen."""
        self.screen.blit(self.image, self.rect)
