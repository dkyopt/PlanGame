# player.py
import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("figures/player.png")
        self.image = pygame.transform.scale(self.image, (50, 60))  
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.power_up = False  # 是否强化
        self.hit_once = False  # 是否已经被击中一次

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += PLAYER_SPEED
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.y += PLAYER_SPEED

    def power_up_mode(self):
        self.power_up = True

    def downgrade(self):
        if self.power_up:
            self.power_up = False  # 退化到原来的火力
        elif not self.hit_once:
            self.hit_once = True  # 第一次被击中不死
        else:
            self.image = pygame.image.load("figures/cry.jpg")  # 变成哭脸
            self.image = pygame.transform.scale(self.image, (50, 60)) 
            return True  # 第二次被击中，游戏结束
        return False