import sys
from pygame.locals import *
from Towers import *
from Map import *
from Enemy import *
from Control import *
from State import *

running = True
controls = load_control()


scr = Screen(900, 600, 'fuck this shit')
map0 = Map(scr, 3, 2, 'fucku', [(0, 300), (200, 300), (200, 100), (400, 100), (400, 300), (600, 300)])
map0.assign(-10, 2, 0)
map0.render()
scr.render()
game = State(controls, scr)
print(map0.map)

tower1 = ArrowTower(map0, 1, 1, 2)
tower1.shoot(0, 0)


enemies = []

clock = pygame.time.Clock()

while game.run():
    t = clock.tick(60)
    if game.currentstate() == "menu":
        game.menu()
    if game.currentstate() == "ingame":
        game.ingame(map0, t)
    if game.currentstate() == "ingame_menu":
        game.ingame_menu()
