import sys
from State import *


game = Game()
clock = pygame.time.Clock()


while not actions["Quit"]:
    t = clock.tick(300)
    game.gameloop(t)

pygame.display.quit()
pygame.quit()
sys.exit()
