from Render import *


class Bullet:
    def __init__(self, x, y, bsize, vec2, dmg, spd):
        self.x = x
        self.y = y
        self.vec2 = vec2
        self.pos = pygame.Vector2(x, y)
        self.dmg = dmg
        self.spd = spd
        self.bsize = bsize
        self.hitbox = [x, y, bsize, bsize]

    def hitdmg(self):
        return self.dmg

    def move(self, t):
        self.pos = self.pos + self.vec2 * self.spd * t/1000
        self.hitbox = [self.pos[0], self.pos[1], self.bsize, self.bsize]

    def render(self, surface):
        surface.rect(self.pos[0], self.pos[1], self.bsize, self.bsize, (255, 255, 255))


class Tower:
    def __init__(self, map, x, y, lv):
        self.x = x * map.tilesize + map.tilesize // 2
        self.y = y * map.tilesize + map.tilesize // 2
        self.lv = lv
        self.bullets = []
        self.atk = None
        self.spd = None
        self.ran = None
        self.angle = None
        self.bsize = None
        self.t = 0

    def tower_buff(self, atk, spd):
        self.atk = self.atk * (1 + atk/100)
        self.spd = self.spd * (1 + spd/100)

    def rotate(self, x):
        pass

    def update(self, t):
        if not self.t >= 1000 / self.spd:
            self.t += t

    def inrange(self, pos):
        if self.t >= 1000 / self.spd:
            vec2 = pos - pygame.Vector2(self.x, self.y)
            if pygame.Vector2.length(vec2) <= self.ran:
                self.shoot(pos)
                self.t = self.t - 1000/self.spd

    def shoot(self, pos):
        vec2 = pos - pygame.Vector2(self.x - self.bsize/2, self.y - self.bsize/2)
        vec2 = vec2.normalize()
        self.bullets.append(Bullet(self.x - self.bsize/2, self.y - self.bsize/2, self.bsize, vec2, self.atk, 1000))


class ArrowTower(Tower):
    def __init__(self, map, x, y, lv):
        super().__init__(map, x, y, lv)
        if self.lv == 1:
            map.assign(11, x, y)
            self.type = 0
            self.atk = 1
            self.spd = 10
            self.rot = 150
            self.ran = 700
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
            self.atk = 3
            self.spd = 2
            self.rot = 150
            self.ran = 300
            self.bsize = 8
            self.spec = None
