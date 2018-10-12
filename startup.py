import pygame.font


class Startup:
    def __init__(self, screen):
        """Initialize the startup screen."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.black = (0, 0, 0)
        self.green = (0, 255, 0)
        self.white = (255, 255, 255)

        # Different sized fonts for each thing
        self.space_font = pygame.font.SysFont(None, 250)
        self.invader_font = pygame.font.SysFont(None, 150)
        self.pt_font = pygame.font.SysFont(None, 40)

        self.space_image = None
        self.space_image_word = 'SPACE'
        self.space_image_rect = None
        self.invader_image = None
        self.invader_image_word = 'INVADERS'
        self.invader_image_rect = None
        self.alien_image_1 = None
        self.alien_rect_1 = None
        self.alien_points_1 = 50
        self.alien_points_image_1 = None
        self.alien_points_rect_1 = None
        self.alien_image_2 = None
        self.alien_rect_2 = None
        self.alien_points_2 = 100
        self.alien_points_image_2 = None
        self.alien_points_rect_2 = None
        self.alien_image_3 = None
        self.alien_rect_3 = None
        self.alien_points_3 = 150
        self.alien_points_image_3 = None
        self.alien_points_rect_3 = None
        self.ufo_image = None
        self.ufo_rect = None
        self.ufo_points = '???'
        self.ufo_points_image = None
        self.ufo_points_rect = None

        self.alien_image_4 = None
        self.alien_image_5 = None
        self.alien_image_6 = None

        self.last_frame = 0
        self.next_frame = None
        self.animation = 0

        # Prepare the initial score image
        self.prep_images()
        self.position()

    def prep_images(self):
        """Prepare images."""
        self.alien_image_1 = pygame.image.load('images/blue_1.png')
        self.alien_image_2 = pygame.image.load('images/red_1.png')
        self.alien_image_3 = pygame.image.load('images/green_1.png')
        self.alien_image_4 = pygame.image.load('images/blue_2.png')
        self.alien_image_5 = pygame.image.load('images/red_2.png')
        self.alien_image_6 = pygame.image.load('images/green_2.png')
        self.ufo_image = pygame.image.load('images/ufo.png')

        self.alien_points_image_1 = self.get_score_str(self.alien_points_1)
        self.alien_points_image_2 = self.get_score_str(self.alien_points_2)
        self.alien_points_image_3 = self.get_score_str(self.alien_points_3)
        self.ufo_points_image = self.get_score_str(self.ufo_points)
        self.space_image = self.space_font.render(str(self.space_image_word), True, self.white, self.black)
        self.invader_image = self.invader_font.render(str(self.invader_image_word), True, self.green, self.black)

    def get_score_str(self, pts):
        """Used to render font for each score"""
        score_str = ' = ' + str(pts)
        return self.pt_font.render(score_str, True, self.white, self.black)

    def position(self):
        """Position the images in the startup screen correctly."""
        self.alien_points_rect_1 = self.alien_points_image_1.get_rect()
        self.alien_points_rect_1.center = self.screen_rect.center
        self.alien_points_rect_1.y += 50
        self.alien_points_rect_1.x += 15
        self.alien_rect_1 = self.alien_image_1.get_rect()
        self.alien_rect_1.y = self.alien_points_rect_1.y
        self.alien_rect_1.x = self.alien_points_rect_1.x - 50
        self.alien_points_rect_2 = self.alien_points_image_2.get_rect()
        self.alien_points_rect_2.center = self.screen_rect.center
        self.alien_points_rect_2.y += 100
        self.alien_points_rect_2.x += 25
        self.alien_rect_2 = self.alien_image_2.get_rect()
        self.alien_rect_2.y = self.alien_points_rect_2.y
        self.alien_rect_2.x = self.alien_points_rect_2.x - 50
        self.alien_points_rect_3 = self.alien_points_image_3.get_rect()
        self.alien_points_rect_3.center = self.screen_rect.center
        self.alien_points_rect_3.y += 150
        self.alien_points_rect_3.x += 25
        self.alien_rect_3 = self.alien_image_3.get_rect()
        self.alien_rect_3.y = self.alien_points_rect_3.y
        self.alien_rect_3.x = self.alien_points_rect_3.x - 50
        self.ufo_points_rect = self.ufo_points_image.get_rect()
        self.ufo_points_rect.center = self.screen_rect.center
        self.ufo_points_rect.y += 200
        self.ufo_points_rect.x += 25
        self.ufo_rect = self.ufo_image.get_rect()
        self.ufo_rect.y = self.ufo_points_rect.y
        self.ufo_rect.x = self.ufo_points_rect.x - 55
        self.space_image_rect = self.space_image.get_rect()
        self.space_image_rect.center = self.screen_rect.center
        self.space_image_rect.y -= 250
        self.invader_image_rect = self.space_image.get_rect()
        self.invader_image_rect.center = self.screen_rect.center
        self.invader_image_rect.y -= 100
        self.invader_image_rect.x += 25

    def draw_images(self):
        """Draw the images on the screen."""
        self.screen.blit(self.space_image, self.space_image_rect)
        self.screen.blit(self.invader_image, self.invader_image_rect)
        time_test = pygame.time.get_ticks()
        if self.animation == 1:
            self.screen.blit(self.alien_image_1, self.alien_rect_1)
            self.screen.blit(self.alien_image_2, self.alien_rect_2)
            self.screen.blit(self.alien_image_3, self.alien_rect_3)
            self.last_frame = pygame.time.get_ticks()
            if abs(time_test - self.next_frame) > 750:
                self.animation = 0
        else:
            self.screen.blit(self.alien_image_4, self.alien_rect_1)
            self.screen.blit(self.alien_image_5, self.alien_rect_2)
            self.screen.blit(self.alien_image_6, self.alien_rect_3)
            if abs(time_test - self.last_frame) > 500:
                self.next_frame = pygame.time.get_ticks()
                self.animation = 1
        self.screen.blit(self.alien_points_image_1, self.alien_points_rect_1)
        self.screen.blit(self.alien_points_image_2, self.alien_points_rect_2)
        self.screen.blit(self.alien_points_image_3, self.alien_points_rect_3)
        self.screen.blit(self.ufo_points_image, self.ufo_points_rect)
        self.screen.blit(self.ufo_image, self.ufo_rect)
