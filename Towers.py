class Bullet:
    def __init__(self, x, y, vec2, dmg, spd):
        self.vec2 = vec2
        self.x = x
        self.y = y
        self.dmg = dmg
        self.spd = spd

    def hit(self):
        return self.dmg


class Tower:
    def __init__(self, x, y, lv):
        self.x = x
        self.y = y
        self.lv = lv
        self.bullet = []

    def rotate(self):
        pass

    def shoot(self, x, y):
        vec2 = pygame.Vector2(x - self.x, y - self.y)
        self.bullet.append(Bullet(self.x, self.y, vec2, self.atk, 200))


class Towerlv:
    pass


class ArrowTower(Tower):
    def __init__(self, x, y, lv):
        super().__init__(x, y, lv)
        if lv == 1:
            self.type = 0
            self.atk = 10
            self.spd = 1
            self.rot = 150
            self.ran = 300
            self.spec = False
        if lv == 2:
            self.atk = 10
            self.spd = 1
            self.rot = 150
            self.ran = 300
            self.spec = False
        if lv == 3:
            self.atk = 10
            self.spd = 1
            self.rot = 150
            self.ran = 300
            self.spec = False
