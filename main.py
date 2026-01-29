import sys
from State.State import *


game = Game()
clock = pygame.time.Clock()


while not actions_status["Quit"]:
    t = clock.tick(300)
    game.gameloop(t)

pygame.display.quit()
pygame.quit()
sys.exit()
