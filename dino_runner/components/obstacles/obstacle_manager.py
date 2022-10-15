import pygame
import random

from dino_runner.utils.constants import SHIELD_TYPE, SMALL_CACTUS, LARGE_CACTUS, BIRD, HAMMER_TYPE, SOUND
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.bird import Bird


class ObstacleManager:
    def __init__(self):
        self.obstacles = []

    def update(self, game):
        if len(self.obstacles) == 0:
            if random.randint(0, 2) == 0:
                self.obstacles.append(Cactus(SMALL_CACTUS, 325))

            elif random.randint(0, 2) == 1:
                self.obstacles.append(Cactus(LARGE_CACTUS, 300))

            elif random.randint(0, 2) == 2:
                self.obstacles.append(Bird(BIRD))

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.dino_rect.colliderect(obstacle.rect):
                if game.player.type != SHIELD_TYPE and game.player.type != HAMMER_TYPE:
                    game.death_count += 1
                    SOUND[1].play()
                    game.playing = False
                    break
                else:
                    self.obstacles.remove(obstacle)

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)

    def reset_obstacle(self):
        self.obstacles = []






