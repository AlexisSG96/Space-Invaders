"""
Name: Alexis Steven Garcia
Project: Space Invaders
Date: October 8, 2018
Email: AlexisSG96@csu.fullerton.edu
"""
import pygame
from pygame.sprite import Sprite
from pygame import Surface


class Bunker(Sprite):
    """Represents bunker bits and pieces that can be destroyed"""
    def __init__(self, ai_settings, screen, row, col):
        """Create the bunker piece object"""
        super().__init__()
        self.screen = screen
        self.height = ai_settings.bunker_block_size
        self.width = ai_settings.bunker_block_size
        self.color = ai_settings.bunker_color

        # Surface is used to represent any image
        self.image = Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.row = row
        self.col = col

    def update(self):
        """Draw the bits of the bunker to the screen"""
        self.screen.blit(self.image, self.rect)


def create_bunker(ai_settings, screen, position):
    """Create a bunker built from smaller pieces"""
    bunker = pygame.sprite.Group()
    for row in range(5):
        for col in range(9):
            # Don't draw full rows of blocks on last two rows, to style the bunker
            if not ((row > 3 and (1 < col < 7)) or
                    (row > 2 and (2 < col < 6)) or
                    (row == 0 and (col < 1 or col > 7))):
                block = Bunker(ai_settings=ai_settings, screen=screen, row=row, col=col)
                block.rect.x = int(ai_settings.screen_width * 0.15) + (250 * position) + (col * block.width)
                block.rect.y = int(ai_settings.screen_height * 0.8) + (row * block.height)
                bunker.add(block)
    return bunker
