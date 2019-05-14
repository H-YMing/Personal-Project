# _*_ coding:utf-8 _*_
import pygame
from random import randint
from pygame.locals import *
import sys
import os

WIDTH, HEIGHT = 640, 480
BACKGROUND = (255, 255, 255)
if getattr(sys, 'frozen', False):
    # 打包音频等文件时
    # CurrentPath = sys._MEIPASS
    # 不打包音频等文件时
    CurrentPath = os.getcwd()
else:
    CurrentPath = os.path.dirname(__file__)
FONTPATH = os.path.join(CurrentPath, 'simkai.ttf')
IMGPATH = os.path.join(CurrentPath, '1.png')
MUSICPATH = os.path.join(CurrentPath, '1.mp3')


# 按钮
def button(text, x, y, w, h, color, screen):
    pygame.draw.rect(screen, color, (x, y, w, h))
    font = pygame.font.Font(FONTPATH, 20)
    textRender = font.render(text, True, (0, 0, 0))
    textRect = textRender.get_rect()
    textRect.center = ((x+w/2), (y+h/2))
    screen.blit(textRender, textRect)


# 标题
def title(text, screen, scale, color=(255, 0, 0)):
    font = pygame.font.Font(FONTPATH, WIDTH//(len(text)*2))
    textRender = font.render(text, True, color)
    textRect = textRender.get_rect()
    textRect.midtop = (WIDTH/scale[0], HEIGHT/scale[1])
    screen.blit(textRender, textRect)


# 生成随机的位置坐标
def get_random_pos():
    x, y = randint(20, 540), randint(20, 430)
    return x, y


# 点击帅按钮后显示的页面
def show_shuai_interface(text, screen, color=(255, 0, 0)):
    font = pygame.font.Font(FONTPATH, WIDTH//(len(text)))
    textRender = font.render(text, True, color)
    textRect = textRender.get_rect()
    textRect.midtop = (WIDTH/2, HEIGHT/4)
    screen.blit(textRender, textRect)


# 主函数
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
    pygame.display.set_caption(u"懂得称赞是一种美德")
    clock = pygame.time.Clock()
    pygame.mixer.music.load(MUSICPATH)
    pygame.mixer.music.play(-1, 30.0)
    pygame.mixer.music.set_volume(0.25)
    bushuai_pos_x, bushuai_pos_y = 330, 250
    bushuai_width, bushuai_height = 100, 50
    bushuai_color = (0, 191, 255)
    shuai_pos_x, shuai_pos_y = 180, 250
    shuai_width, shuai_height = 100, 50
    shuai_color = (0, 191, 255)
    goback_pos_x, goback_pos_y = 50, 400
    goback_width, goback_height = 120, 50
    goback_color = (0, 191, 255)
    out_pos_x, out_pos_y = 470, 400
    out_width, out_height = 120, 50
    out_color = (0, 191, 255)
    running = True
    while True:
        if running:
            screen.fill(BACKGROUND)
            img = pygame.image.load(IMGPATH)
            imgRect = img.get_rect()
            imgRect.midtop = int(WIDTH/1.3), HEIGHT//7
            screen.blit(img, imgRect)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if mouse_pos[0] < shuai_pos_x+shuai_width+5 and mouse_pos[0] > shuai_pos_x-5 and\
                        mouse_pos[1] < shuai_pos_y+shuai_height+5 and mouse_pos[1] > shuai_pos_y-5:
                        # like_color = BACKGROUND
                        running = False
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos[0] < bushuai_pos_x+bushuai_width+5 and mouse_pos[0] > bushuai_pos_x-5 and\
                mouse_pos[1] < bushuai_pos_y+bushuai_height+5 and mouse_pos[1] > bushuai_pos_y-5:
                while True:
                    bushuai_pos_x, bushuai_pos_y = get_random_pos()
                    if mouse_pos[0] < bushuai_pos_x+bushuai_width+5 and mouse_pos[0] > bushuai_pos_x-5 and\
                        mouse_pos[1] < bushuai_pos_y+bushuai_height+5 and mouse_pos[1] > bushuai_pos_y-5:
                        continue
                    elif bushuai_pos_x < shuai_pos_x+shuai_width+5 and bushuai_pos_x > shuai_pos_x-bushuai_width-5 and\
                        bushuai_pos_y < shuai_pos_y+shuai_height+5 and bushuai_pos_y > shuai_pos_y-bushuai_height-5:
                        continue
                    break
            title(u'请客观评价编写此程序的程序员', screen, scale=[3, 8])
            button(u'帅的一匹', shuai_pos_x, shuai_pos_y, shuai_width, shuai_height, shuai_color, screen)
            button(u'真的醜', bushuai_pos_x, bushuai_pos_y, bushuai_width, bushuai_height, bushuai_color, screen)
        else:
            screen.fill(BACKGROUND)
            show_shuai_interface(u'你是一位懂得称赞的好孩子~', screen, color=(255, 0, 0))
            button(u'继续称赞', goback_pos_x, goback_pos_y, goback_width, goback_height, goback_color, screen)
            button(u'臭不要脸', out_pos_x, out_pos_y, out_width, out_height, out_color, screen)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if mouse_pos[0] < goback_pos_x+goback_width and mouse_pos[0] > goback_pos_x and\
                        mouse_pos[1] < goback_pos_y+goback_height and mouse_pos[1] > goback_pos_y:
                        running = True
                    elif mouse_pos[0] < out_pos_x+out_width and mouse_pos[0] > out_pos_x and\
                        mouse_pos[1] < out_pos_y+out_height and mouse_pos[1] > out_pos_y:
                        pygame.quit()
                        sys.exit()
        pygame.display.flip()
        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    main()
