import pygame


class Bullet:
    def __init__(self, x, y, vec2, dmg, spd):
        self.vec2 = vec2
        self.pos = pygame.Vector2(x, y)
        self.dmg = dmg
        self.spd = spd

    def hitdmg(self):
        return self.dmg

    def move(self, t):
        self.pos = self.pos + self.vec2 * self.spd * t/1000


class Tower:
    def __init__(self, map, x, y, lv):
        self.x = x * map.tilesize + map.tilesize // 2
        self.y = y * map.tilesize + map.tilesize // 2
        self.lv = lv
        self.angle = 0
        self.bullet = []
        self.atk = 0
        self.spd = 0
        self.ran = 0

    def range(self, x, y):
        vec = pygame.Vector2((self.x - x, self.y - y))
        self.distant = pygame.Vector2.length(vec)
        if self.distant <= self.ran:
            return True
        else:
            return False

    def tower_buff(self, atk, spd):
        self.atk = self.atk * (1 + atk/100)
        self.spd = self.spd * (1 + spd/100)

    def rotate(self, x):
        pass

    def shoot(self, x, y):
        vec2 = pygame.Vector2(x - self.x, y - self.y)
        vec2 = vec2.normalize()
        self.bullet.append(Bullet(self.x, self.y, vec2, self.atk, 200))


class ArrowTower(Tower):
    def __init__(self, map, x, y, lv):
        super().__init__(map, x, y, lv)
        if lv == 1:
            map.assign(11, x, y)
            self.type = 0
            self.atk = 10
            self.spd = 1
            self.rot = 150
            self.ran = 300
            self.spec = None
        if lv == 2:
            map.assign(12, x, y)
            self.atk = 10
            self.spd = 1
            self.rot = 150
            self.ran = 300
            self.spec = None
        if lv == 3:
            map.assign(13, x, y)
            self.atk = 10
            self.spd = 1
            self.rot = 150
            self.ran = 300
            self.spec = None
