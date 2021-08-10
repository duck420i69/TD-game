
from Render import *


class Enemy:
    def __init__(self, screen, ms, phyres, magres, themap):
        self.health = 15
        self.ms = ms
        self.phyres = phyres
        self.magres = magres
        self.path = themap.path
        self.draw = []
        self.pos = pygame.Vector2(self.path[0])
        self.screen = screen
        self.i = 1
        self.delete = False

        # Movement
        self.end = pygame.Vector2(self.path[self.i])
        self.vec = self.end - self.pos
        self.mvec = self.vec.normalize()
        self.b4vec = self.mvec

    def move(self, t):
        if pygame.Vector2.dot(self.vec, self.b4vec) > 0:
            self.pos = self.pos + self.mvec * self.ms * t/1000
            self.vec = self.end - self.pos
        else:
            if self.i < len(self.path) - 1:
                self.pos = pygame.Vector2(self.path[self.i])
                self.i += 1
                self.end = pygame.Vector2(self.path[self.i])
                self.vec = self.end - self.pos
                self.mvec = self.vec.normalize()
                self.b4vec = self.vec
            else:
                self.delete = True

    def dead(self):
        return self.delete

    def get_hit(self, bullet):
        self.health -= bullet.hitdmg()
        if self.health <= 0:
            return True

    def render(self):
        self.screen.rect(self.pos[0], self.pos[1], 30, 65, (255, 0, 0))

