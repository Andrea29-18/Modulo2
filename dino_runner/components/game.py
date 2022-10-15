import pygame

from dino_runner.components.cloud import Cloud
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.power_ups.power_up_manager import PowerUpManager
from dino_runner.utils.constants import (BG, COLOURS, DEFAULT_TYPE, DINO_DEAD,
                                         FONT_STYLE, FPS, GAME_OVER,
                                         HAMMER_TYPE, ICON, SCREEN_HEIGHT,
                                         SCREEN_WIDTH, TITLE, RESET)


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.game_speed = 20
        self.playing = False
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.player = Dinosaur()
        self.cloud = Cloud()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()
        self.running = False
        self.score = 0
        self.death_count = 0
        self.hi_score = 0

    def update_score(self):
        self.score += 1

        if self.score % 100 == 0 and self.game_speed < 900:
            self.game_speed += 5

        if self.score > self.hi_score:
            self.hi_score = self.score

    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                if self.death_count == 0:
                    self.show_menu()
                else:
                    self.screen_death()

        pygame.display.quit()
        pygame.quit()

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
                self.running = False


    def reset_game(self):
        self.score = 0 
        self.obstacle_manager.reset_obstacle()
        self.playing = True
        self.game_speed = 20
        self.power_up_manager.reset_power_ups()

    def update(self):
        self.update_score()
        user_input = pygame.key.get_pressed()

        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.cloud.update(self.game_speed)
        self.power_up_manager.update(self)

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.player.draw(self.screen)
        self.draw_score()
        self.draw_power_up_time()
        self.obstacle_manager.draw(self.screen)
        self.cloud.draw(self.screen)
        self.power_up_manager.draw(self.screen)

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

    def gen_text(self, word:str, half_screen_width:int, half_screen_height:int, color:str, size:int):
        font = pygame.font.Font(FONT_STYLE, size)
        text = font.render(word, True, COLOURS[color])
        text_rec = text.get_rect()
        text_rec.center = (half_screen_width, half_screen_height)

        self.screen.blit(text, text_rec)

    def draw_score(self):
        if self.death_count == 0:
            self.gen_text(f'Score: {self.score}', 970, 50, 'purple', 30)
        else :
            self.gen_text(f'Hi: {self.hi_score}', 800, 50, 'purple', 30)
            self.gen_text(f'Score: {self.score}', 970, 50, 'red', 30)

    def draw_power_up_time(self):
        if self.player.has_power_up:
            time_to_show = round((self.player.power_time_up - pygame.time.get_ticks()) / 1000, 2)
            if time_to_show >= 0:
                if self.player.type == HAMMER_TYPE:
                    self.gen_text(f'{self.player.type.capitalize()} enabled for:  {time_to_show}  seconds', 500, 150, 'black', 18)
                else:
                    self.gen_text(f'{self.player.type.capitalize()} enabled for:  {time_to_show}  seconds', 500, 150, 'red', 18)
            else:
                self.has_power_up = False
                self.player.type = DEFAULT_TYPE

    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
            elif event.type == pygame.KEYDOWN:
                self.run()

    def show_menu(self):

        self.running = True

        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2
        self.screen.fill(COLOURS['black'])
        self.gen_text('Press any key to start ..', half_screen_width, half_screen_height, 'green', 50)

        pygame.display.update()
        self.handle_events_on_menu()

    def screen_death(self):
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2

        self.screen.fill(COLOURS['black'])
        self.screen.blit(GAME_OVER, (365, 100))
        self.screen.blit(DINO_DEAD, (500, 190))
        self.screen.blit(RESET, (half_screen_width -30 , half_screen_height + 220))
        self.gen_text('try again', half_screen_width - 50, half_screen_height + 180, 'white', 40)
        self.gen_text(f'Score: {self.score}', half_screen_width, half_screen_height + 70, 'green', 30)
        self.gen_text(f'Death Count: {self.death_count}', half_screen_width, half_screen_height + 130, 'purple', 30)

        pygame.display.update()
        self.handle_events_on_menu()
