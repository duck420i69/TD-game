import pygame.sprite

from Enemy import Enemy
from Graphic import *


class Bullet(pygame.sprite.Sprite):
    def __init__(self, sprite, x, y, bsize, vec2, spd, effect):
        super().__init__()
        self.x = x
        self.y = y
        self.effects = effect
        self.vec2 = vec2
        self.pos = pygame.Vector2(x, y)
        self.spd = spd
        self.bsize = bsize
        self.hitbox = [x, y, bsize, bsize]
        self.dead = False
        self.image = sprite
        self.rect = self.image.get_rect()

    def move(self, t):
        self.pos = self.pos + self.vec2 * self.spd * t/1000
        self.hitbox = [self.pos[0], self.pos[1], self.bsize, self.bsize]

    def render(self, surface):
        surface.blit(self.image, self.pos[0], self.pos[1])

    def update(self, *args, **kwargs) -> None:
        self.rect.topleft = [self.x, self.y]


class Tower(pygame.sprite.Sprite):
    def __init__(self, map_, x, y, lv):
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
        self.target: list[Enemy] = []
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
        self.rect.center = [self.x, self.y]
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

    def shoot(self, enemy):
        distant = pygame.Vector2(self.x, self.y).distance_to(enemy.center())
        vec2 = enemy.predict_move(distant/200) - pygame.Vector2(self.x - self.bsize/2, self.y - self.bsize/2)
        vec2 = vec2.normalize()
        self.bullets.append(
            Bullet(self.bullet_image, self.x - self.bsize / 2, self.y - self.bsize / 2,
                   self.bsize, vec2, 200, self.effects))
        self.t = self.t - 1000 / self.spd


# self.effect = {
#    "Damage": dmg,
#    "Explosion": [Active, Range],
#    "Fire": [Active, time, DoT],
#    "Water": [Active, time],
#    "Ice": [Active, time, slow],
#    "Elec": [Active, time, chain],
#    "Earth": [Active, time, stun],
#    "Wind": [Active, time, Mutiplier]
# }


class FireTower(Tower):
    def __init__(self, map_, x, y, lv):
        super().__init__(map_, x, y, lv)
        self.bullet_image = load_image("firebullet.png")
        self.image = load_image("firetower.png")

    def get_stat(self):
        self.effects = {
            "Damage": self.atk,
            "Explosion": [True, 40],
            "Fire": [True, 6000, 10],
            "Elec": [False, 0, 0],
        }
        if self.lv == 1:
            self.map.assign(11, self.map_x, self.map_y)
            self.atk = 8
            self.spd = 0.8
            self.rot = 150
            self.ran = 100
            self.bsize = 8
            self.sell_price = 30
            self.upgrade_price = 100
            self.effects["Damage"] = self.atk
        if self.lv == 2:
            self.map.assign(12, self.map_x, self.map_y)
            self.atk = 20
            self.spd = 1
            self.rot = 120
            self.ran = 160
            self.bsize = 8
            self.sell_price = 125
            self.upgrade_price = 150
            self.effects["Damage"] = self.atk
            self.effects["Fire"] = [True, 6000, 25]
        if self.lv == 3:
            self.map.assign(13, self.map_x, self.map_y)
            self.atk = 75
            self.spd = 1.2
            self.rot = 150
            self.ran = 140
            self.bsize = 8
            self.sell_price = 200
            self.upgrade_price = None
            self.effects["Damage"] = self.atk
            self.effects["Fire"] = [True, 8000, 45]


class WaterTower(Tower):
    def __init__(self, map_, x, y, lv):
        super().__init__(map_, x, y, lv)
        self.bullet_image = load_image("waterbullet.png")
        self.image = load_image("watertower.png")

    def get_stat(self):
        if self.lv == 1:
            self.map.assign(21, self.map_x, self.map_y)
            self.atk = 10
            self.spd = 0.8
            self.rot = 150
            self.ran = 100
            self.bsize = 8
            self.sell_price = 30
            self.upgrade_price = 100
        if self.lv == 2:
            self.map.assign(22, self.map_x, self.map_y)
            self.atk = 25
            self.spd = 1
            self.rot = 120
            self.ran = 160
            self.bsize = 8
            self.sell_price = 80
            self.upgrade_price = 150
        if self.lv == 3:
            self.map.assign(23, self.map_x, self.map_y)
            self.atk = 50
            self.spd = 1.2
            self.rot = 150
            self.ran = 140
            self.bsize = 8
            self.sell_price = 120
            self.upgrade_price = None
        self.effects = {
            "Damage": self.atk,
            "Explosion": [True, 60],
            "Water": [True, 4500],
            "Elec": [False, 0, 0],
        }


class IceTower(Tower):
    def __init__(self, map_, x, y, lv):
        super().__init__(map_, x, y, lv)
        self.bullet_image = load_image("icebullet.png")
        self.image = load_image("icetower.png")
        self.bsize = 7

    def get_stat(self):
        self.effects = {
            "Damage": self.atk,
            "Explosion": [True, 25],
            "Ice": [True, 4000, 0.2],
            "Elec": [False, 0, 0],
        }
        if self.lv == 1:
            self.map.assign(31, self.map_x, self.map_y)
            self.atk = 5
            self.spd = 1
            self.rot = 150
            self.ran = 250
            self.bsize = 8
            self.sell_price = 30
            self.upgrade_price = 80
            self.effects["Damage"] = self.atk
        if self.lv == 2:
            self.map.assign(32, self.map_x, self.map_y)
            self.atk = 2
            self.spd = 1.5
            self.rot = 150
            self.ran = 300
            self.bsize = 8
            self.sell_price = 75
            self.upgrade_price = 150
            self.effects["Damage"] = self.atk
            self.effects["Ice"] = [True, 4500, 0.3]
        if self.lv == 3:
            self.map.assign(33, self.map_x, self.map_y)
            self.atk = 30
            self.spd = 5
            self.rot = 150
            self.ran = 300
            self.bsize = 8
            self.sell_price = 200
            self.upgrade_price = None
            self.effects["Damage"] = self.atk
            self.effects["Ice"] = [True, 5000, 0.4]


class ElecTower(Tower):
    def __init__(self, map_, x, y, lv):
        super().__init__(map_, x, y, lv)
        self.image = load_image("electower.png")
        self.charge = 7500

    def get_stat(self):
        if self.lv == 1:
            self.map.assign(41, self.map_x, self.map_y)
            self.atk = 15
            self.rot = 150
            self.ran = 250
            self.sell_price = 30
            self.upgrade_price = 100
        if self.lv == 2:
            self.map.assign(42, self.map_x, self.map_y)
            self.atk = 80
            self.rot = 150
            self.ran = 300
            self.sell_price = 125
            self.upgrade_price = 200
        if self.lv == 3:
            self.map.assign(43, self.map_x, self.map_y)
            self.atk = 150
            self.rot = 150
            self.ran = 300
            self.charge = 10000
            self.sell_price = 200
            self.upgrade_price = None
        self.effects = {
            "Damage": self.atk,
            "Elec": [True, 6000, 4],
        }

    def shoot(self, enemy):
        enemy.hp -= self.atk * self.t/1000 * (1 - enemy.immune["Elec"][1]) * (1 + enemy.x_dmg["Elec"][0])
        enemy.status["Elec"] = self.effects["Elec"].copy()
        if enemy.hp <= 0:
            enemy.delete = True

    def update(self, t):
        if self.t < self.charge:
            self.t += t
        else:
            self.t = self.charge

    def inrange(self, pos):
        check = False
        if self.t >= 2500:
            vec2 = pos - pygame.Vector2(self.x, self.y)
            if pygame.Vector2.length(vec2) <= self.ran:
                check = True
        return check


class EarthTower(Tower):
    def __init__(self, map_, x, y, lv):
        super().__init__(map_, x, y, lv)
        self.bullet_image = load_image("mage bullet 3.png")
        self.image = load_image("earthtower.png")
        if self.lv == 1:
            self.map.assign(51, self.map_x, self.map_y)
            self.atk = 5
            self.spd = 1
            self.rot = 150
            self.ran = 250
            self.bsize = 8
        if self.lv == 2:
            self.map.assign(52, self.map_x, self.map_y)
            self.atk = 2
            self.spd = 1.5
            self.rot = 150
            self.ran = 300
            self.bsize = 8
        if self.lv == 3:
            self.map.assign(53, self.map_x, self.map_y)
            self.atk = 30
            self.spd = 5
            self.rot = 150
            self.ran = 300
            self.bsize = 8
        self.effects = {
            "Damage": self.atk,
            "Explosion": [True, 25],
            "Earth": [True, 6000, 3],
            "Elec": [False, 0, 0],
        }


class WindTower(Tower):
    def __init__(self, map_, x, y, lv):
        super().__init__(map_, x, y, lv)
        self.bullet_image = load_image("windbullet.png")
        self.image = load_image("windtower.png")
        self.bsize = 4

    def get_stat(self):
        if self.lv == 1:
            self.map.assign(61, self.map_x, self.map_y)
            self.atk = 5
            self.spd = 1
            self.rot = 150
            self.ran = 250
            self.bsize = 8
        if self.lv == 2:
            self.map.assign(62, self.map_x, self.map_y)
            self.atk = 2
            self.spd = 1.5
            self.rot = 150
            self.ran = 300
            self.bsize = 8
        if self.lv == 3:
            self.map.assign(63, self.map_x, self.map_y)
            self.atk = 30
            self.spd = 5
            self.rot = 150
            self.ran = 300
            self.bsize = 8
        self.effects = {
            "Damage": self.atk,
            "Explosion": [False, 0],
            "Wind": [True, 500, 1.2],
            "Elec": [False, 0, 0],
        }
