# _*_ coding:utf-8 _*_
import pygame
import random
from pygame.locals import*
from sys import exit


def qq(x, y):
    while True:
        m = random.random()*680
        n = random.random()*550
        if m < (x-120) or m > (x+240) or n < (y-50) or n > (y+100):
            break
    return m, n


def main():
    x, y = qq(-240, -100)
    pygame.init()
    screen = pygame.display.set_mode((800, 600), 0, 32)
    # font = pygame.font.SysFont('arial', 16)
    font = pygame.font.Font(r'C:\Windows\Fonts\simkai.ttf', 16)
    s = u'点击'
    fw, fh = font.size(s)

    while True:
        x1, y1 = pygame.mouse.get_pos()
        if x <= x1 <= (x+120) and y <= y1 <= (y+50):
            x, y = qq(x, y)

        # pygame.display.update()
        screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
        pygame.draw.rect(screen, (255, 255, 255), (x, y, 120, 50))
        screen.blit(font.render(s, True, (255, 0, 0)), (x+(120-fw)/2, y+(50-fh)/2))
        pygame.display.update()


if __name__ == '__main__':
    main()
