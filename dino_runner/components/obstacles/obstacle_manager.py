from dino_runner.utils.constants import SMALL_CACTUS
from dino_runner.utils.constants import LARGE_CACTUS
from dino_runner.components.obstacles.cactusLarge import CactusLarge
from dino_runner.components.obstacles.cactus import Cactus

class ObstacleManager:
    def __init__(self):
        self.obstacles = []
        
    def update(self, game):
        if len(self.obstacles) == 0:
            cactus = Cactus(SMALL_CACTUS)
            cactusLarge = CactusLarge(LARGE_CACTUS)
            self.obstacles.append(cactus)
            self.obstacles.append(cactusLarge)

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)

            if game.player.dino_rect.colliderect(obstacle):
                print("MUERTE")
                pygame.time.delay(1000)
                game.playing = False
                break


    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)