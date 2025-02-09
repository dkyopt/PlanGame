# main.py
import pygame
import sys
from player import Player
from enemy import Enemy
from bullet import Bullet
from food import Food
from settings import *
import random

# 初始化pygame
pygame.init()

# 设置屏幕
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("飞机大战")

# 加载并缩放背景图片，填充整个屏幕
background = pygame.image.load("figures/background.png")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# 创建玩家
player = Player()

# 创建精灵组
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
foods = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# 初始化得分
score = 0
font = pygame.font.SysFont(None, 36)

# 定时生成敌机和食物
ENEMY_EVENT = pygame.USEREVENT
FOOD_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(ENEMY_EVENT, ENEMY_SPAWN_TIME)
pygame.time.set_timer(FOOD_EVENT, 10000)  # 每10秒生成一次食物

# 游戏主循环
clock = pygame.time.Clock()
running = True
game_over = False

while running:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if not game_over:
            if event.type == ENEMY_EVENT:
                enemy = Enemy()
                enemies.add(enemy)
                all_sprites.add(enemy)
            elif event.type == FOOD_EVENT:
                if random.random() < 0.3:  # 30%概率生成食物
                    food = Food()
                    foods.add(food)
                    all_sprites.add(food)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if player.power_up:
                        # 三向发射
                        for direction in [-1, 0, 1]:
                            bullet = Bullet(player.rect.centerx, player.rect.top, direction)
                            bullets.add(bullet)
                            all_sprites.add(bullet)
                    else:
                        bullet = Bullet(player.rect.centerx, player.rect.top)
                        bullets.add(bullet)
                        all_sprites.add(bullet)

    if not game_over:
        # 获取按键
        keys = pygame.key.get_pressed()
        player.update(keys)

        # 更新子弹、敌机和食物
        bullets.update()
        enemies.update()
        foods.update()

        # 检测子弹和敌机碰撞
        hits = pygame.sprite.groupcollide(bullets, enemies, True, False)
        for hit in hits:
            for enemy in hits[hit]:
                enemy.hit()  # 调用hit方法减少血量
                if enemy.is_exploding:
                    score += enemy.score_value  # 根据敌机类型增加得分
                    print(f"敌机被击中! 当前得分: {score}")

        # 检测玩家和敌机碰撞
        if pygame.sprite.spritecollide(player, enemies, False):
            if player.downgrade():  # 判断是否需要游戏结束
                print("游戏结束! 按ESC退出")
                game_over = True

        # 检测玩家和食物碰撞
        if pygame.sprite.spritecollide(player, foods, True):
            player.power_up_mode()  # 玩家获得三向射击能力
            print("获得强化! 三向射击开启!")

    # 绘制背景，清除重影
    screen.blit(background, (0, 0))

    # 绘制所有精灵
    all_sprites.draw(screen)

    # 显示得分
    score_surface = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_surface, (10, 10))

    if game_over:
        game_over_surface = font.render('游戏结束! 按ESC退出', True, (255, 0, 0))
        game_over_rect = game_over_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(game_over_surface, game_over_rect)

    # 更新显示
    pygame.display.flip()

    # 处理游戏结束后的退出
    if game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False

pygame.quit()
