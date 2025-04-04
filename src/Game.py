import os
import random

import pygame

from . import cfg

from .collide import collide
from .Ship import Enemy, Player

pygame.font.init()

class Game:
    # FPS of the Game
    FPS = cfg.FPS

    def __init__(self, WIN: pygame.Surface, WIDTH: int, HEIGHT: int) -> None:
        # Window
        self.WIN = WIN
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT

        # Background
        self.BG: pygame.Surface = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))
        pygame.display.set_caption("Space Invaders")

        # Game
        self.LIVES = 5
        self.LEVEL = 0
        self.ENEMIES: list[Enemy] = []
        self.WAVE_LENGTH = 5
        self.ENEMY_VEL = 1
        self.PLAYER_VEL = 5
        self.LASER_VEL = 5
        self.LOST_COUNT = 0

        self.RUN = True
        self.clock = pygame.time.Clock()
        self.PLAYER: Player = Player(300, 630)

        self.main_font: pygame.font.Font = pygame.font.SysFont("comicsans", 50)
        self.lost_font: pygame.font.Font = pygame.font.SysFont("comicsans", 60)

        self.LOST = False

    def redraw_window(self) -> None:
        self.WIN.blit(self.BG, (0,0))
        # Draw text
        level_label = self.main_font.render(f"Level: {self.LEVEL}", 1, (255,255,255))
        lives_label = self.main_font.render(f"Lives: {self.LIVES}", 1, (255,255,255))

        self.WIN.blit(lives_label, (10, 10))
        self.WIN.blit(level_label, (self.WIDTH - level_label.get_width() - 10, 10))

        for enemy in self.ENEMIES:
            enemy.draw_entity(self.WIN)

        self.PLAYER.draw_entity(self.WIN)

        pygame.display.update()

    def lost_message_render(self) -> None:
        lost_label = self.lost_font.render("You Lost!!", 1, (255,255,255))
        self.WIN.blit(lost_label, (self.WIDTH/2 - lost_label.get_width()/2, 350))
        pygame.display.update()

    def run_game(self) -> None:
        while self.RUN:
            self.clock.tick(self.FPS)
            self.redraw_window()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            if self.LIVES <= 0 or self.PLAYER.health <= 0:
                self.LOST = True
                self.LOST_COUNT += 1

            if self.LOST:
                if self.LOST_COUNT > self.FPS * 3:
                    self.RUN = False
                else:
                    self.lost_message_render()
                    continue # If LOST we don't need to do actions below

            if len(self.ENEMIES) == 0:
                self.LEVEL += 1
                self.WAVE_LENGTH += 5
                for i in range(self.WAVE_LENGTH):
                    enemy = Enemy(random.randrange(50, self.WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                    self.ENEMIES.append(enemy)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and self.PLAYER.x - self.PLAYER_VEL > 0: # left
                self.PLAYER.x -= self.PLAYER_VEL
            if keys[pygame.K_RIGHT] and self.PLAYER.x + self.PLAYER_VEL + self.PLAYER.width < self.WIDTH: # right
                self.PLAYER.x += self.PLAYER_VEL
            if keys[pygame.K_UP] and self.PLAYER.y - self.PLAYER_VEL > 0: # up
                self.PLAYER.y -= self.PLAYER_VEL
            if keys[pygame.K_DOWN] and self.PLAYER.y + self.PLAYER_VEL + self.PLAYER.height + 15 < self.HEIGHT: # down
                self.PLAYER.y += self.PLAYER_VEL
            if keys[pygame.K_SPACE]:
                self.PLAYER.shoot()

            for enemy in self.ENEMIES:
                enemy.move(self.ENEMY_VEL)
                enemy.move_lasers(self.LASER_VEL, self.PLAYER)

                if random.randrange(0, 2*60) == 1:
                    enemy.shoot()

                if collide(enemy, self.PLAYER):
                    self.PLAYER.health -= 10
                    self.ENEMIES.remove(enemy)
                elif enemy.y + enemy.height > self.HEIGHT:
                    self.LIVES -= 1
                    self.ENEMIES.remove(enemy)

            self.PLAYER.move_lasers(-self.LASER_VEL, self.ENEMIES)