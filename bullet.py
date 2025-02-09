# bullet.py
import pygame
from settings import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction=0):
        super().__init__()
        self.image = pygame.image.load("figures/bullet.png")
        self.image = pygame.transform.scale(self.image, (10, 10))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.direction = direction  # 0: 直线, -1: 左偏, 1: 右偏

    def update(self):
        if self.direction == 0:
            self.rect.y -= BULLET_SPEED
        elif self.direction == -1:
            self.rect.y -= BULLET_SPEED
            self.rect.x -= 2
        elif self.direction == 1:
            self.rect.y -= BULLET_SPEED
            self.rect.x += 2
        
        if self.rect.bottom < 0:
            self.kill()