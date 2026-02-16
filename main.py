import sys

import pygame

from State.Game import Game
from Control import actions_status

if __name__ == "__main__":
    game = Game()
    clock = pygame.time.Clock()


    while not actions_status["Quit"]["press"]:
        t = clock.tick(300)
        game.gameloop(t)


    pygame.display.quit()
    pygame.quit()
    sys.exit()
