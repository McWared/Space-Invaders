import os
from typing import Literal

import pygame

from .Laser import Laser

WIDTH, HEIGHT = 750, 750

# Load images
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))

# Player's ship
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

# Lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

class Ship:
    COOLDOWN = 30

    def __init__(self, x: int, y: int, health = 100) -> None:
        self.x = x
        self.y = y
        self.health = health
        self.ship_img: pygame.Surface = None
        self.laser_img: pygame.Surface = None
        self.lasers: list[Laser] = []
        self.cool_down_counter = 0

    def draw_entity(self, window: pygame.Surface) -> None:
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    # Abstract method
    def move_lasers(self, vel: int, objs) -> None:
        raise NotImplementedError("Please Implement this method")
    
    # Abstract method
    def draw_healthbar(self, window: pygame.Surface) -> None:
        raise NotImplementedError("Please Implement this method")

    def cooldown(self) -> None:
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self) -> None:
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    @property
    def width(self) -> None:
        return self.ship_img.get_width()

    @property
    def height(self) -> None:
        return self.ship_img.get_height()
    

class Player(Ship):
    def __init__(self, x: int, y: int, health = 100, damage = 50) -> None:
        Ship.__init__(self, x, y)
        self.max_health = health
        self.damage = damage
        self.ship_img: pygame.Surface = YELLOW_SPACE_SHIP
        self.laser_img: pygame.Surface = YELLOW_LASER
        self.mask: pygame.Mask = pygame.mask.from_surface(self.ship_img)


    def move_lasers(self, vel: int, objs: list[Ship]) -> None: # TODO: move class Enemy(Ship) to another file -> able to write list[Enemy]
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        obj.health -= self.damage
                        if obj.health == 0:
                            objs.remove(obj)
                        if laser in self.lasers: # Anti-bug IF
                            self.lasers.remove(laser)

    def draw_entity(self, window) -> None:
        Ship.draw_entity(self, window)
        self.draw_healthbar(window)

    def draw_healthbar(self, window) -> None:
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10)) # red part
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10)) # green part

class Enemy(Ship):
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LASER),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER)
    }
    HEALTH_MAP = {
        "red": 100,
        "green": 100,
        "blue": 50 
    }
    DAMAGE_MAP = {
        "red": 20,
        "green": 20,
        "blue": 10
    }

    def __init__(self, x, y, color: Literal['red', 'green', 'blue']) -> None:
        Ship.__init__(self, x, y)
        self.color = color
        self.health = Enemy.HEALTH_MAP[color]
        self.max_health = Enemy.HEALTH_MAP[color]
        self.damage = Enemy.DAMAGE_MAP[color]
        self.ship_img, self.laser_img = Enemy.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def draw_entity(self, window) -> None:
        Ship.draw_entity(self, window)
        self.draw_healthbar(window)

    def draw_healthbar(self, window) -> None:
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10)) # red part
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10)) # green part
        if self.max_health == 100:
            pygame.draw.rect(window, (0,0,0), (self.x + self.ship_img.get_width() / 2, self.y + self.ship_img.get_height() + 10, 1, 10)) # black half-divisor

    def move(self, vel) -> None:
        self.y += vel

    def shoot(self) -> None:
        if self.cool_down_counter == 0:
            laser = Laser(self.x-20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def move_lasers(self, vel: int, player: Player) -> None:
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(player):
                player.health -= self.damage
                self.lasers.remove(laser)