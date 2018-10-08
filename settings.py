"""
Name: Alexis Steven Garcia
Project: Space Invaders
Date: October 8, 2018
Email: AlexisSG96@csu.fullerton.edu
"""
from pygame import mixer


class Settings:
    """Settings of the game."""
    def __init__(self):
        """Initialize the game settings."""
        # Screen Settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (200, 200, 200)

        # Ship settings
        self.ship_speed_factor = None
        self.ship_limit = 3

        # Bullet Settings
        self.bullet_speed_factor = None
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Alien laser settings
        self.laser_speed_factor = None
        self.lasers_allowed = 1
        self.laser_time = 1000
        self.laser_stamp = None

        # Alien settings
        self.alien_speed_factor = None
        self.fleet_drop_speed = 10
        self.fleet_direction = None
        self.alien_points = None

        # UFO settings
        self.ufo_speed_factor = None
        self.time_from_last_ufo = None
        self.ufo_interval = 25000
        self.ufo_points = [50, 100, 150]

        # Bunker setting
        self.bunker_block_size = 12
        self.bunker_color = (0, 255, 0)

        # How quickly the game speeds up
        self.speedup_scale = 1.2
        
        # How quickly the alien point values increase
        self.score_scale = 1.5

        # Initialize a channel for each object that needs one
        self.audio_channels = 4
        self.ship_channel = mixer.Channel(0)
        self.alien_channel = mixer.Channel(1)
        self.death_channel = mixer.Channel(2)
        self.ufo_channel = mixer.Channel(3)

        self.initialize_dynamic_settings()
        self.initialize_audio_settings()

    def initialize_dynamic_settings(self):
        """Initialize dynamic settings."""
        # Speed factor for each object
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.laser_speed_factor = 1.25
        self.alien_speed_factor = 1
        self.ufo_speed_factor = self.alien_speed_factor * 2

        # Fleet direction of 1 represents right; -1 represents left
        self.fleet_direction = 1

        # Scoring
        self.alien_points = {'1': 50,
                             '2': 20,
                             '3': 40}

    def increase_speed(self):
        """Increase speed after each level."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        
    def initialize_audio_settings(self):
        """Initialize mixer settings."""
        # Allows for other sounds to be played with background music
        mixer.init()
        mixer.set_num_channels(self.audio_channels)
        mixer.music.load('sounds/background_music.wav')
        mixer.music.set_volume(0.75)
