# enemy.py
import pygame
import random
from settings import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        enemy_type = random.choice(["figures/enemy1.jpg", "figures/enemy2.jpg"])
        if "enemy1" in enemy_type:
            original_image = pygame.image.load(enemy_type)
            self.image = pygame.transform.scale(original_image, (100, 120))  # 较大的敌机
            self.score_value = 20  # 更高得分
            self.health = 3  # 需要三次击中才能摧毁
        else:
            original_image = pygame.image.load(enemy_type)
            self.image = pygame.transform.scale(original_image, (40, 50))  # 普通敌机
            self.score_value = 5  # 普通得分
            self.health = 1  # 一次击中摧毁

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed_y = random.randint(ENEMY_MIN_SPEED, ENEMY_MAX_SPEED)
        self.speed_x = random.choice([-2, -1, 1, 2])  # 左右随机移动速度
        self.is_exploding = False  # 标记敌机是否正在爆炸

    def update(self):
        if not self.is_exploding:
            self.rect.y += self.speed_y
            self.rect.x += self.speed_x

            # 碰到边界反弹
            if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
                self.speed_x *= -1

            if self.rect.top > SCREEN_HEIGHT:
                self.kill()
        else:
            self.explode_timer -= 1
            if self.explode_timer <= 0:
                self.kill()

    def hit(self):
        self.health -= 1
        if self.health <= 0:
            self.explode()

    def explode(self):
        self.is_exploding = True
        if self.rect.width == 100:
            self.image = pygame.transform.scale(pygame.image.load("figures/boom.jpg"), (100, 100))
        else:
            self.image = pygame.transform.scale(pygame.image.load("figures/boom.jpg"), (40, 40))
        self.explode_timer = 10  # 爆炸持续时间