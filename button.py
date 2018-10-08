"""
Name: Alexis Steven Garcia
Project: Space Invaders
Date: October 8, 2018
Email: AlexisSG96@csu.fullerton.edu
"""
import pygame.font
from startup import Startup


class Button:
    def __init__(self, ai_settings, screen, msg):
        """Create the play button."""
        self.startup = Startup(screen)
        self.ai_settings = ai_settings
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Set the dimensions and properties of the button
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.black = (0, 0, 0)
        self.font = pygame.font.SysFont(None, 48)

        # Build the button's rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # The button message needs to be prepped only once
        self.msg_image, self.msg_image_rect = None, None
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """Prepare the message."""
        self.msg_image = self.font.render(msg, True, self.text_color, self.black)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Draw the play button on the screen."""
        # Black screen
        self.screen.fill(self.black)
        # self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
        self.startup.draw_images()
