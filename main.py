import sys

import pygame

from State.Game import Game
from Control import actions_status


game = Game()
clock = pygame.time.Clock()
log_file = open("log.txt", "w")


while not actions_status["Quit"]["press"]:
    t = clock.tick(300)
    game.gameloop(t)

    # in your game loop / update()
    log_file.write(f"{actions_status["Up"]}\n")
    log_file.flush()  # make sure it's written

log_file.close()

pygame.display.quit()
pygame.quit()
sys.exit()
