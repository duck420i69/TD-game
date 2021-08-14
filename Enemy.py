from Render import *


class Enemy:
    def __init__(self, ms, phyres, magres, themap):
        self.health = 100
        self.ms = ms
        self.phyres = phyres
        self.magres = magres

        self.path = themap.path
        self.i = 1
        self.pos = pygame.Vector2(self.path[0])

        self.sprite = []

        self.hitbox_w, self.hitbox_h = 30, 65
        self.hitbox = [self.pos[0], self.pos[1], self.hitbox_w, self.hitbox_h]
        self.feet = self.pos + pygame.Vector2(self.hitbox_w/2, self.hitbox_h)

        self.delete = False

        # Movement
        self.end = pygame.Vector2(self.path[self.i])
        self.vec = self.end - self.pos
        self.mvec = self.vec.normalize()
        self.b4vec = self.mvec

    def move(self, t):
        # Check if move to the end
        if pygame.Vector2.dot(self.vec, self.b4vec) > 0:
            self.pos = self.pos + self.mvec * self.ms * t/1000
            self.feet = self.pos + pygame.Vector2(self.hitbox_w / 2, self.hitbox_h/2)
            self.vec = self.end - self.pos
            self.hitbox = [self.pos[0], self.pos[1], self.hitbox_w, self.hitbox_h]
        # Set new end
        elif self.i < len(self.path) - 1:
            self.pos = pygame.Vector2(self.path[self.i])
            self.i += 1
            self.end = pygame.Vector2(self.path[self.i])
            self.vec = self.end - self.pos
            self.mvec = self.vec.normalize()
            self.b4vec = self.vec
        # Get to the end point
        else:
            self.delete = True

    def dead(self, t):
        return self.delete

    def position(self):
        return self.feet

    def get_hit(self, bullet):
        self.health -= bullet.hitdmg()
        if self.health <= 0:
            self.delete = True

    def render(self, surface):
        surface.rect(self.pos[0], self.pos[1], 30, 65, (255, 0, 0))
