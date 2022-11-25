import random
import time
from random import choice
import pygame  # 一般模組
from pygame.locals import *  # 要import這個才能夠下控制鍵的指令

pygame.init()
win = pygame.display.set_mode((800, 600), 0, 32)  # 視窗大小

# 可想像這是在視窗上開一個畫布
bg = pygame.Surface(win.get_size())
bg = bg.convert()
bg.fill((0, 0, 0))
pygame.display.set_caption("Bricks Breaker")
game_over = False
start_message = True
hacker_mode = False

brick_color = (20, 123, 200)
brick_color_2 = (255, 191, 0)
two_colors = [brick_color, brick_color_2]
three_colors=[brick_color, brick_color_2,(255,0,0)]
# 要設定偵數
clock = pygame.time.Clock()

# ball
stick_ball = False
ball_pos1, ball_pos2 = (350, 450)
ball_speed_x = 3
ball_speed_y = 4
ball_moving = False


# bat
bat_pos1 = 350
bat_pos2 = 500
rect_length = 100
rect_width = 20


bricks = dict()
rc = [] #random colors
for i in range(45):
    random_color = random.choice(two_colors)
    rc.append(random_color)

for i, c in zip(range(8), rc):
    for j, c2 in zip(range(5), rc):
        bricks[(i, j)] = random.choice([c, c2])


def display_bricks(bricks):
    for i, j in list(bricks):
        if (i, j) not in list(bricks):
            continue
        pygame.draw.rect(win, bricks[(i, j)], (i * 100, j * 60, 100, 60))
        pygame.draw.rect(win, (0, 0, 0), (i * 100, j * 60, 100, 60), 3)

    return bricks


def display_space():
    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 30)
    text = font.render('Press Space to Start!', 1, (255, 255, 255))
    space = win.blit(text, (win.get_width() // 2 - (text.get_width() // 2), (win.get_height() // 2 + 30)))

def display_author():
    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 30)
    text = font.render('Created by Potoro Pao', 1, (255, 255, 255))
    win.blit(text, (win.get_width()-text.get_width(),550))

def display_win():
    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    text = font.render('Congratulations!', 1, (255, 255, 255))
    win.blit(text, (win.get_width() // 2 - (text.get_width() // 2), (win.get_height() // 2 - (text.get_height() // 2))))


def display_gameover():
    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    text = font.render('Game Over', 1, (255, 255, 255))
    win.blit(text, (win.get_width() // 2 - (text.get_width() // 2), (win.get_height() // 2 - (text.get_height() // 2))))

def display_hacker_mode():
    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 30)
    text = font.render('Hacker Mode On', 1, (255, 255, 255))
    win.blit(text, (0,550))

# pygame loop
# 主遊戲程式

while not game_over:

    dt = clock.tick(50)  # 偵數50  FPS 50

    win.blit(bg, (0, 0))  # 畫布   Create a canvas like tkinter
    # or everything will look like old fashion multiwindows on windowsXP
    # when things moving
    bat = pygame.draw.rect(win, (0, 255, 0), (bat_pos1, bat_pos2, rect_length, rect_width))  # 板子
    ball = pygame.draw.circle(win, (255, 0, 0), (ball_pos1, ball_pos2), 10)  # 球

    left_bricks = display_bricks(bricks)
    if start_message:
        display_space()

    for event in pygame.event.get():  # 設定右上角的關掉
        if event.type == pygame.QUIT:
            game_over = True
    # do keyboard control
    pressed = pygame.key.get_pressed()  # control the bat

    if pressed[K_LEFT]:
        bat_pos1 -= 10
        pygame.draw.rect(win, (0, 255, 0), (bat_pos1, bat_pos2, rect_length, rect_width))
    if bat_pos1 < 0:
        bat_pos1 += 10
    if pressed[K_RIGHT]:
        bat_pos1 += 10
    if bat_pos1 + bat.width - 1 >= win.get_width():
        bat_pos1 -= 10

    # ----start ball moving
    if pressed[K_SPACE]:
        ball_moving = True
        start_message = False
    if ball_moving:
        ball_pos1 = ball_pos1 + ball_speed_x
        ball_pos2 = ball_pos2 + ball_speed_y
        if ball_pos1 >= win.get_width():
            ball_speed_x = -ball_speed_x
        if ball_pos2 >= win.get_height():
            ball_speed_y = -ball_speed_y
        if ball_pos1 <= 0:
            ball_speed_x = -ball_speed_x
        if ball_pos2 <= 0:
            ball_speed_y = -ball_speed_y

        # bounce the ball with bat
        if (bat_pos1 + bat.width + 10 >= ball_pos1 + 5 > bat_pos1 - 10) and (
                bat_pos2 + bat.height >= ball_pos2 + 5 > bat_pos2):
            ball_speed_x = ball_speed_x
            ball_speed_y = -ball_speed_y
            if pressed[K_x]:
                stick_ball = True
                if stick_ball:  # bat ability sticky bat

                    ball_pos1 = bat_pos1 + bat.width // 2
                    ball_pos2 = bat_pos2
                    ball_speed_y = 0  # once the x is pressed yspeed
                    # will change to 0
            elif not pressed[K_x]:  # so i have to set the speed back to -4
                ball_speed_y = -4

        # bounce the bricks
        if event.type == pygame.KEYDOWN:
            if hacker_mode == True and event.key == pygame.K_h:
                hacker_mode = False
            elif hacker_mode==False:
                if pressed[K_h]:
                    hacker_mode=True

        if hacker_mode:
            display_hacker_mode()
            ball=pygame.draw.circle(win, random.choice(three_colors), (ball_pos1, ball_pos2), 10)
            for (x, y) in list(left_bricks):
                if ((x * 100 + 100) > ball_pos1 >= x) and ((y * 60 + 60) > ball_pos2 > y):
                    if bricks[(x, y)] == brick_color_2:
                        ball_speed_x = ball_speed_x
                        ball_speed_y = -ball_speed_y
                        bricks[(x, y)] = brick_color
                        pygame.draw.rect(win, bricks[(x, y)], (x * 100, y * 60, 100, 60))
                        pygame.draw.rect(win, (0, 0, 0), (x * 100, y * 60, 100, 60), 3)
                    else:
                        ball_speed_x = ball_speed_x
                        ball_speed_y = -ball_speed_y
                        del bricks[(x, y)]


        elif not hacker_mode:
            for (x, y) in list(left_bricks):
                if ((x * 100 + 100) > ball_pos1 >= x * 100) and ((y * 60 + 60) > ball_pos2 > y * 60):
                    if bricks[(x, y)] == brick_color_2:
                        ball_speed_x = ball_speed_x
                        ball_speed_y = -ball_speed_y
                        bricks[(x, y)] = brick_color
                        pygame.draw.rect(win, bricks[(x, y)], (x * 100, y * 60, 100, 60))
                        pygame.draw.rect(win, (0, 0, 0), (x * 100, y * 60, 100, 60), 3)
                    else:
                        ball_speed_x = ball_speed_x
                        ball_speed_y = -ball_speed_y
                        del bricks[(x, y)]




        # win game
        if bricks == {}:
            display_win()
            display_author()
            pygame.display.update()
            time.sleep(3)
            game_over = True

        # lose game
        if ball_pos2 >= win.get_height():
            display_gameover()
            pygame.display.update()
            time.sleep(3)
            game_over = True

    pygame.display.update()
pygame.quit()
