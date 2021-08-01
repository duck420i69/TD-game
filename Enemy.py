class Enemy:
    def __init__(self, x, y, ms, phyres, magres):
        self.x = x
        self.y = y
        self.health = 15
        self.ms = ms
        self.phyres = phyres
        self.magres = magres
        self.path = []
        self.draw = []

    def move(self):
        pass

    def get_hit(self):
        self.health -= Bullet
        if self.health <= 0:
            return True