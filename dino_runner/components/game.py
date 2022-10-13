import random

import pygame

from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.utils.constants import (BG, DEFAULT_TYPE, DINO_DEAD,
                                         FONT_STYLE, FPS, GAME_OVER, ICON,
                                         SCREEN_HEIGHT, SCREEN_WIDTH, TITLE,
                                         Cloud)


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.x_pos_cloud = 0
        self.y_pos_cloud = 100
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.running = False
        self.score = 0
        self.death_count = 0
        self.menssage = ""
        self.positionX = 0
        self.positionY = 0

    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()
        pygame.display.quit()
        pygame.quit()
        

    def reset_game(self):
        self.obstacle_manager.reset_obstacles()
        self.playing = True
        self.game_speed = 20

    def run(self):
        # Game loop: events - update - draw
        self.reset_game()
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        self.update_score()
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        #self.draw_cloud()
        self.draw_score()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))

        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def draw_cloud(self):
        image_width = Cloud.get_width()
        self.screen.blit(Cloud, (self.x_pos_cloud, self.y_pos_cloud))
        self.screen.blit(Cloud, (image_width + self.x_pos_cloud, self.y_pos_cloud))

        if self.x_pos_cloud <= -image_width:
            self.screen.blit(Cloud, (image_width + self.x_pos_cloud, self.y_pos_cloud))
            self.x_pos_cloud = 0
        self.x_pos_cloud -= self.game_speed

    def generarte_menssage(self,menssage, positionX, positionY):
        font = pygame.font.Font(FONT_STYLE, 30)
        text = font.render(menssage, True, (0, 0, 0))
        text_rec = text.get_rect()
        text_rec.center = (positionX,positionY)
        self.screen.blit(text, text_rec)

    def draw_score(self):
        self.menssage = f'Score: {self.score}'
        self.positionX = 1000
        self.positionY = 50
        self.generarte_menssage(self.menssage, self.positionX,self.positionY)

    def update_score(self):
        self.score += 1

        if self.score % 100 == 0 and self.game_speed < 700:
            self.game_speed += 5 

    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
            elif event.type == pygame.KEYDOWN:
               self.score = 0
               self.run() 

    def show_menu(self):
        self.screen.fill((204, 255, 229))
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2

        if self.death_count == 0:
            self.screen.blit(ICON, (half_screen_width -20, half_screen_height -140))
            self.menssage = "Press any key to start"
            self.generarte_menssage(self.menssage, half_screen_width,half_screen_height)
        else:
            self.screen.fill((255, 102, 102))
            self.screen.blit(DINO_DEAD, (half_screen_width -20, half_screen_height -140))
            self.menssage = f'Deaths: {self.death_count}'
            self.generarte_menssage(self.menssage, half_screen_width - 460 ,half_screen_height -250)

            self.screen.blit(GAME_OVER, (half_screen_width - 180, half_screen_height - 250))

            self.menssage = f'Score: {self.score}'
            self.generarte_menssage(self.menssage, half_screen_width, half_screen_height)

            self.menssage = "Press any key to start"
            self.generarte_menssage(self.menssage, half_screen_width,half_screen_height + 250)
        pygame.display.update()
        self.handle_events_on_menu()