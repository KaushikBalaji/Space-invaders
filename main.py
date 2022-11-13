import pygame
import random
import math
from pygame import mixer

pygame.init()
screen = pygame.display.set_mode((800, 600))

playerImg = pygame.image.load("space-invaders.png")
background = pygame.image.load("background1.jpg")
bulletImg = pygame.image.load("bullet1.png")

icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

pygame.display.set_caption("My Game")
font = pygame.font.Font('sono.ttf', 32)

bullet_state = "ready"
score = 0
score_board = 0

mixer.init()
mixer.music.load('bgm.mp3')
mixer.music.play()

def show_score(x, y):
    text = font.render("Score: " + str(score), True, "white")
    global score_board
    screen.blit(text, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def fireBullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x, y))


def enemy(img, x, y):
    screen.blit(img, (x, y))


def credits():
    msg = font.render("Game Over ..... Dieeee .... ", True, (255, 255, 255))
    msg1 = font.render("R to retry , C to close", True, (255, 255, 255))
    screen.blit(msg, (100, 300))
    screen.blit(msg1, (100, 330))
    pygame.display.update()
    while True:
        e = pygame.event.wait()
        if e.type == pygame.KEYDOWN and e.key == pygame.K_r:
            return 'r'
        elif e.type == pygame.KEYDOWN and e.key == pygame.K_c:
            return 'c'


def collison(x1, y1, x2, y2):
    dist = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    if dist <= 25:
        return True
    else:
        return False


def main():
    global score_board, bullet_state, score
    bullet_state = "ready"
    score = 0
    score_board = 0

    running = True

    # player position
    x_position = 370
    y_position = 480
    posChange = 0

    # enemy position
    enemyImg = []
    x_enemy = []
    y_enemy = []
    enemy_xchange = []
    enemy_ychange = []
    n_enemies = 5
    for i in range(n_enemies):
        enemyImg.append(pygame.image.load("pixel-alien.png"))
        x_enemy.append(random.randint(0, 735))
        y_enemy.append(random.randint(10, 40))
        enemy_xchange.append(0.3)
        enemy_ychange.append(0)

    # bullet position
    x_bullet = 374
    y_bullet = 500
    bullet_xchange = 0
    bullet_ychange = 0.2

    score_board = 0

    while running:
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    posChange = 0.3
                if event.key == pygame.K_LEFT:
                    posChange = -0.3
                if event.key == pygame.K_SPACE and bullet_state == "ready":
                    x_bullet = x_position
                    fireBullet(x_bullet, y_bullet)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    posChange = 0

        if x_position <= 0:
            x_position = 0
        if x_position >= 735:
            x_position = 735

        x_position += posChange

        for i in range(n_enemies):
            if y_enemy[i] >= 450:
                for j in range(n_enemies):
                    y_enemy[j] = 2000
                choice = credits()
                if choice == 'r':
                    main()
                else:
                    pygame.display.quit()
                    pygame.quit()
                    exit()

            x_enemy[i] += enemy_xchange[i]  # enemy moving to the boundaries
            if x_enemy[i] <= 0:
                enemy_xchange[i] = 0.3
                enemy_ychange[i] = 40
            elif x_enemy[i] >= 735:
                enemy_xchange[i] = -0.3
                enemy_ychange[i] = 40

            collided = collison(x_enemy[i], y_enemy[i], x_bullet, y_bullet)
            if collided:
                print("Bullet collision")
                y_bullet = 500
                bullet_state = "ready"
                score += 1
                score_board += 1
                print("Score: " + str(score))
                x_enemy[i] = random.randint(0, 735)
                y_enemy[i] = random.randint(10, 40)
            enemy(enemyImg[i], x_enemy[i], y_enemy[i])
            y_enemy[i] += enemy_ychange[i]  # enemy coming down
            enemy_ychange[i] = 0

        # bullet firing
        if bullet_state == "fire":
            fireBullet(x_bullet, y_bullet)
            y_bullet -= bullet_ychange
        if y_bullet <= 0:
            y_bullet = 500
            bullet_state = "ready"

        player(x_position, y_position)
        show_score(10, 10)
        pygame.display.update()


main()
