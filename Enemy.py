from Graphic import *


class Enemy:
    def __init__(self, ms, phyres, magres, themap):
        super().__init__()
        self.maxhp = 300
        self.hp = self.maxhp
        self.ms = ms
        self.phyres = phyres
        self.magres = magres

        self.path = themap.path
        self.i = 1
        self.pos = pygame.Vector2(self.path[0])
        self.moved = 0

        slime0 = load_image("slime0.png")
        slime1 = load_image("slime1.png")
        self.sprite = [slime0, slime1]
        self.frame = 0
        self.t = 0
        self.animate = 2

        self.hitbox_w, self.hitbox_h = 30, 30
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
        self.t += t
        if pygame.Vector2.dot(self.vec, self.b4vec) > 0:
            self.pos = self.pos + self.mvec * self.ms * t/1000
            self.moved += self.ms * t/1000
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

    def moveded(self):
        return self.moved

    def dead(self, t):
        return self.delete

    def position(self):
        return self.feet

    def get_hit(self, bullet):
        self.hp -= bullet.hitdmg()
        if self.hp <= 0:
            self.delete = True

    def predict_pos(self, t):
        lenght = self.ms * t/1000
        vec = self.end - self.pos
        i = self.i
        pos = [0, 0]
        while lenght > 0:
            if i < len(self.path) - 1:
                move = vec.length()
                lenght -= move
                i += 1
                vec = pygame.Vector2(self.path[i]) - pygame.Vector2(self.path[i-1])
            else:
                pos = self.path[i]
        if lenght <= 0:
            lenght = abs(lenght)
            vec.scale_to_length(lenght)
            pos = pygame.Vector2(self.path[i-1]) - vec
        return pos

    def render(self, surface):
        self.t = self.t % 800
        self.frame = self.t // 400
        image = self.sprite[self.frame]
        surface.blit(image, self.pos[0], self.pos[1])
        surface.rect(self.pos[0] - 6, self.pos[1] - 11, 22, 7, (128, 128, 128))
        surface.rect(self.pos[0] - 5, self.pos[1] - 10, 20 * (self.hp/self.maxhp), 5, (255, 0, 0))
