import pygame, sys
from pygame.locals import *
from Towers import *
gamename = 'TD'
pygame.init()
screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption(gamename)

tower1 = ArrowTower(10, 10, 2)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
