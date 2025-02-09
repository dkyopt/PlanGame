# food.py
import pygame
import random
from settings import *

class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("figures/food.jpg")
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(0, SCREEN_HEIGHT // 2)
        self.speed_x = random.choice([-2, -1, 1, 2])  # 左右随机移动速度
        self.speed_y = random.randint(1, 3)  # 缓慢向下移动

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # 碰到边界反弹
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.speed_x *= -1

        if self.rect.top > SCREEN_HEIGHT:
            self.kill()