import sys
from Towers import *
from State import *


running = True

window_width, window_height = 800, 600
scr = Screen(window_width, window_height, 'fuck this shit')
map0 = Map(20, 15, 'fucku', [[-1, 3], [3, 3], [3, 8], [8, 8], [8, 3], [12, 3]])
game = Game()

towers = []
enemies = []

clock = pygame.time.Clock()


while not actions["Quit"]:
    t = clock.tick(100)
    game.gameloop(t)

pygame.display.quit()
pygame.quit()
sys.exit()
