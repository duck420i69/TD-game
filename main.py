from Towers import *
from Map import *
from Enemy import *
from Control import *
from State import *


running = True


scr = Screen(900, 600, 'fuck this shit')
map0 = Map(scr, 12, 8, 'fucku', [(0, 300), (200, 300), (200, 100), (400, 100), (400, 300), (600, 300)])
map0.render()
scr.render()
game = State(scr)

towers = []
enemies = []

clock = pygame.time.Clock()
towers.append(ArrowTower(map0, 1, 1, 1))
enemies.append(Enemy(80, 0, 0, map0))
i = 0

while running:
    t = clock.tick(60)
    keycheck(controls)

    scr.clear()
    map0.render()

    for tower in towers:
        for bullet in tower.bullets:
            for enemy in enemies:
                if enemy.hitbox[0] - bullet.hitbox[2] < bullet.hitbox[0] <= enemy.hitbox[0] + enemy.hitbox[2]:
                    if enemy.hitbox[1] - bullet.hitbox[3] < bullet.hitbox[1] <= enemy.hitbox[1] + enemy.hitbox[3]:
                        enemy.get_hit(bullet)
                        del tower.bullets[0]
            bullet.move(t)
            bullet.render(scr)

    for enemy in enemies:
        if enemy.dead(t):
            del enemy
        else:
            enemy.move(t)
            enemy.render(scr)
            for tower in towers:
                tower.inrange(enemy.position())
                tower.update(t)

    scr.render()
