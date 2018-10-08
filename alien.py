"""
Name: Alexis Steven Garcia
Project: Space Invaders
Date: October 8, 2018
Email: AlexisSG96@csu.fullerton.edu
"""
import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """Represents aliens in the fleet."""
    def __init__(self, ai_settings, screen, alien_type=3): 
        """Initialize alien and set starting position."""
        super().__init__() 
        self.screen = screen 
        self.ai_settings = ai_settings 
        self.alien_type = alien_type

        # Initialize invader images and set rect attribute
        self.images = None 
        self.image = None 
        self.image_index = None 
        self.death_index = None 
        self.last_frame = None 
        self.death_frames = None 
        self.rect = None 
        self.initialize_images()

        # Start new aliens at top left of the screen 
        self.rect.x = self.rect.width 
        self.rect.y = self.rect.height

        # Store alien's exact position 
        self.x = float(self.rect.x)

        # Killed flag 
        self.dead = False

        # Alien Sounds
        self.death_sound = pygame.mixer.Sound('sounds/invader_killed.wav')
        self.death_sound.set_volume(0.3)
        self.invader_shoot_sound = pygame.mixer.Sound('sounds/invader_shoot.wav')
        self.invader_shoot_sound.set_volume(0.3)

        # Choose channel to mix with background music
        self.channel = ai_settings.alien_channel

    def initialize_images(self):
        """Initialize different images for each alien (animations)."""
        if self.alien_type == 1: 
            self.images = []
            self.images.append((pygame.image.load('images/red_1.png')))
            self.images.append((pygame.image.load('images/red_2.png')))
            self.image_index = 0
            self.image = self.images[self.image_index]
            self.death_frames = []
            self.death_frames.append(pygame.image.load('images/invader_death/red_death1.png'))
            self.death_frames.append(pygame.image.load('images/invader_death/red_death2.png'))
            self.death_frames.append(pygame.image.load('images/invader_death/red_death3.png'))
            self.death_frames.append(pygame.image.load('images/invader_death/red_death4.png'))
            self.rect = self.image.get_rect() 
        elif self.alien_type == 2: 
            self.images = [] 
            self.images.append((pygame.image.load('images/blue_1.png')))
            self.images.append((pygame.image.load('images/blue_2.png')))
            self.image_index = 0 
            self.image = self.images[self.image_index] 
            self.death_frames = []
            self.death_frames.append(pygame.image.load('images/invader_death/blue_death1.png'))
            self.death_frames.append(pygame.image.load('images/invader_death/blue_death2.png'))
            self.death_frames.append(pygame.image.load('images/invader_death/blue_death3.png'))
            self.death_frames.append(pygame.image.load('images/invader_death/blue_death4.png'))
            self.rect = self.image.get_rect()
        else: 
            self.images = [] 
            self.images.append((pygame.image.load('images/green_1.png')))
            self.images.append((pygame.image.load('images/green_2.png')))
            self.image_index = 0 
            self.image = self.images[self.image_index] 
            self.death_frames = []
            self.death_frames.append(pygame.image.load('images/invader_death/green_death1.png'))
            self.death_frames.append(pygame.image.load('images/invader_death/green_death2.png'))
            self.death_frames.append(pygame.image.load('images/invader_death/green_death3.png'))
            self.death_frames.append(pygame.image.load('images/invader_death/green_death4.png'))
            self.rect = self.image.get_rect() 
        self.last_frame = pygame.time.get_ticks() 

    def invader_shoot(self):
        """Play the invader shoot sound."""
        self.channel.play(self.invader_shoot_sound)

    def check_edges(self): 
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect() 
        if self.rect.right >= screen_rect.right: 
            return True 
        elif self.rect.left <= 0: 
            return True 
        else: 
            return False 

    def begin_death(self): 
        """Set alien's death flag and begin death animation."""
        self.dead = True 
        self.death_index = 0 
        self.image = self.death_frames[self.death_index] 
        self.last_frame = pygame.time.get_ticks()
        self.channel.play(self.death_sound)

    def update(self):
        """Move alien to the right or left, play idle animations or death animations."""
        # Move to the right or left
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x
        # Get the time in milliseconds
        time_test = pygame.time.get_ticks()
        if not self.dead:
            # If invader isn't dead, make the alien seem animated
            if abs(self.last_frame - time_test) > 1000:
                self.last_frame = time_test
                self.image_index = (self.image_index + 1) % len(self.images)
                self.image = self.images[self.image_index]
        else:
            # If invader is killed, start death animation
            # Make animation quick but perceivable
            if abs(self.last_frame - time_test) > 20:
                self.last_frame = time_test
                self.death_index += 1
                if self.death_index >= len(self.death_frames):
                    # Remove from all sprite groups
                    self.kill()
                else:
                    self.image = self.death_frames[self.death_index]

    def blitme(self): 
        """Draw alien at its current location."""
        self.screen.blit(self.image, self.rect) 
