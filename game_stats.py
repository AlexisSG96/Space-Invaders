"""
Name: Alexis Steven Garcia
Project: Space Invaders
Date: October 8, 2018
Email: AlexisSG96@csu.fullerton.edu
"""


class GameStats:
    def __init__(self, ai_settings):
        """Initialize Game Stats"""
        self.ai_settings = ai_settings
        self.ships_left = 0
        self.high_score = None
        self.score = None
        self.level = None
        self.reset_stats()
        self.get_high_score()
        # Start game in an inactive state
        self.game_active = False

    def reset_stats(self):
        """Reset Stats if needed"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1

    def get_high_score(self):
        """Open text file and get previous high score if any"""
        with open('high_score.txt', 'r') as file:
            self.high_score = int(file.readline())

    def save_high_score(self):
        """Write new high score to text file if needed"""
        with open('high_score.txt', 'w') as file:
            file.write(str(self.high_score))
