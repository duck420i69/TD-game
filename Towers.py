import pygame.sprite

from Graphic import *


class Bullet(pygame.sprite.Sprite):
    def __init__(self, sprite, x, y, bsize, vec2, dmg, spd):
        super().__init__()
        self.x = x
        self.y = y
        self.vec2 = vec2
        self.pos = pygame.Vector2(x, y)
        self.dmg = dmg
        self.spd = spd
        self.bsize = bsize
        self.hitbox = [x, y, bsize, bsize]
        self.dead = False
        self.image = sprite
        self.rect = self.image.get_rect()

    def hitdmg(self):
        return self.dmg

    def move(self, t):
        self.pos = self.pos + self.vec2 * self.spd * t/1000
        self.hitbox = [self.pos[0], self.pos[1], self.bsize, self.bsize]

    def render(self, surface):
        surface.blit(self.image, self.pos[0], self.pos[1])

    def update(self, *args, **kwargs) -> None:
        self.rect.topleft = [self.x, self.y]


class Tower(pygame.sprite.Sprite):
    def __init__(self, map, x, y, lv):
        super().__init__()
        self.x = x * map.tilesize + map.tilesize // 2
        self.y = y * map.tilesize + map.tilesize // 2
        self.lv = lv
        self.bullets = []
        self.target = []
        self.atk = None
        self.spd = None
        self.ran = None
        self.angle = None
        self.bsize = None
        self.t = 0
        self.bullet_image = None

    def tower_buff(self, atk, spd):
        self.atk = self.atk * (1 + atk/100)
        self.spd = self.spd * (1 + spd/100)

    def rotate(self, x):
        pass

    def update(self, t):
        if not self.t >= 1000 / self.spd:
            self.t += t

    def add_target(self, enemy):
        self.target.append(enemy)

    def clear_target(self):
        self.target.clear()

    def any_target(self):
        if len(self.target) > 0:
            return True
        return False

    def aim_target(self):
        val = 0
        for i, enemy in enumerate(self.target):
            if enemy.moveded() > val:
                val = enemy.moveded()
                index = i
        return index

    def inrange(self, pos):
        check = False
        if self.t >= 1000 / self.spd:
            vec2 = pos - pygame.Vector2(self.x, self.y)
            if pygame.Vector2.length(vec2) <= self.ran:
                check = True
        return check

    def shoot(self, pos):
        vec2 = pos - pygame.Vector2(self.x - self.bsize/2, self.y - self.bsize/2)
        vec2 = vec2.normalize()
        self.bullets.append(Bullet(self.bullet_image, self.x - self.bsize/2, self.y - self.bsize/2, self.bsize, vec2, self.atk, 900))
        self.t = self.t - 1000 / self.spd


class ArrowTower(Tower):
    def __init__(self, map, x, y, lv):
        super().__init__(map, x, y, lv)
        self.bullet_image = load_image("mage bullet 3.png")
        if self.lv == 1:
            map.assign(11, x, y)
            self.type = 0
            self.atk = 13
            self.spd = 8
            self.rot = 150
            self.ran = 250
            self.bsize = 8
            self.spec = None
        if self.lv == 2:
            map.assign(12, x, y)
            self.atk = 2
            self.spd = 1.5
            self.rot = 150
            self.ran = 300
            self.bsize = 8
            self.spec = None
        if self.lv == 3:
            map.assign(13, x, y)
            self.atk = 30
            self.spd = 5
            self.rot = 150
            self.ran = 300
            self.bsize = 8
            self.spec = None
