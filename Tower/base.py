import pygame.sprite
from pygame import Rect, Vector2, Surface

from Enemy import Enemy
from Graphic import *


class Bullet(pygame.sprite.Sprite):
    def __init__(self, sprite: Surface, x: int, y: int, bsize: int, direction: Vector2, spd: float, effects):
        super().__init__()
        self.x = x
        self.y = y
        self.effects = effects
        self.direction = direction
        self.pos = pygame.Vector2(x, y)
        self.spd = spd
        self.bsize = bsize
        self.dead = False
        self.image = sprite
        self.rect = self.image.get_rect()
        self.hitbox = self.get_hitbox()

    def get_hitbox(self):
        hitbox = Rect(0, 0, self.bsize, self.bsize)
        hitbox.center = (self.x, self.y)
        return hitbox

    def move(self, dt: float):
        self.pos = self.pos + self.direction * self.spd * dt / 1000
        self.hitbox = self.get_hitbox()

    def render(self, surface: Surface):
        surface.blit(self.image, (self.pos[0], self.pos[1]))

    def update(self, *args, **kwargs) -> None:
        self.hitbox = self.get_hitbox()


class Tower(pygame.sprite.Sprite):
    def __init__(self, map_, x: int, y: int, lv: int):
        super().__init__()
        self.effects = {
            "Damage": 0,
            "Explosion": [False, 0],
            "Fire": [False, 0, 0],
            "Water": [False, 0],
            "Ice": [False, 0, 0],
            "Elec": [False, 0, 0],
            "Earth": [False, 0, 0],
            "Wind": [False, 0, 0]
        }
        self.map_x = x
        self.map_y = y
        self.x = x * map_.tilesize + map_.tilesize // 2
        self.y = y * map_.tilesize + map_.tilesize // 2
        self.lv = lv
        self.bullets: list[Bullet] = []
        self.targets: list[Enemy] = []
        self.atk = None
        self.spd = None
        self.ran = None
        self.rot = None
        self.angle = None
        self.bsize = None
        self.sell_price = 0
        self.upgrade_price = None
        self.t = 0
        self.bullet_image = None
        self.map = map_
        self.image = pygame.Surface((20, 20))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.selected = False
        self.get_stat()

    def click(self, pos):
        if self.rect.collidepoint(pos):
            self.selected = True
        else:
            if pos[0] < 340:
                self.selected = False

    def sell(self):
        return self.sell_price

    def upgrade(self):
        self.lv += 1
        self.get_stat()

    def get_stat(self):
        pass

    def rotate(self, x):
        pass

    def update(self, dt):
        if not self.t >= 1000 / self.spd:
            self.t += dt

    def add_target(self, enemy):
        self.targets.append(enemy)

    def clear_target(self):
        self.targets.clear()

    def any_target(self):
        return len(self.targets) > 0

    def aim_target(self):
        val = 0
        index = -1
        for i, enemy in enumerate(self.targets):
            if enemy.moveded() > val:
                val = enemy.moveded()
                index = i
        return index

    def is_in_range(self, pos):
        check = False
        if self.t >= 1000 / self.spd:
            vec2 = pos - pygame.Vector2(self.x, self.y)
            if pygame.Vector2.length(vec2) <= self.ran:
                check = True
        return check

    def shoot(self, enemy):
        distant = pygame.Vector2(self.x, self.y).distance_to(enemy.center())
        vec2 = enemy.predict_move(distant/200) - pygame.Vector2(self.x - self.bsize/2, self.y - self.bsize/2)
        vec2 = vec2.normalize()
        self.bullets.append(
            Bullet(self.bullet_image, self.x - self.bsize / 2, self.y - self.bsize / 2,
                   self.bsize, vec2, 200, self.effects))
        self.t = self.t - 1000 / self.spd

