# Type map (type, subtype):
# 0 : land
# add later
# -1 : cant place
# add later
# subtype = lv
# 1 : arrow
# 2 : poison
# 3 : ice
# 4 : mage
import pygame.sprite

from Graphic import *
import os, json

pygame.init()


class Map:
    def __init__(self, mapdata):
        self.tilesize = 20
        self.path = mapdata["path"]  # path is a list of pos to move to
        for i in range(len(self.path)):
            self.path[i][0] = (self.path[i][0] + 0.1) * self.tilesize
            self.path[i][1] = (self.path[i][1] + 0.1) * self.tilesize

        self.defaultmap = mapdata["map"]
        self.map = self.defaultmap
        self.w = len(self.map)
        self.h = len(self.map[0])
        self.grass = load_image("grass.png")
        self.road = load_image("path.png")
        self.sprites = pygame.sprite.Group()
        self.tower_sprite = pygame.sprite.Group()

        for j in range(len(self.map)):
            for i in range(len(self.map[j])):
                if self.map[j][i] == 11:
                    pass
                if self.map[j][i] == 0:
                    grass = Sprite(self.grass, self.tilesize * i, self.tilesize * j)
                    grass.add(self.sprites)
                if self.map[j][i] == -10:
                    road = Sprite(self.road, self.tilesize * i, self. tilesize * j)
                    road.add(self.sprites)

        self.waves = [[("Slime", 10, 1500, 5, 1500, 0)]]

    def assign(self, maptype, x, y) -> bool:
        type_ = self.map[y][x]
        if type_ // 10 == 0:
            self.map[y][x] = maptype
            return True
        elif maptype // 10 == type_ // 10:
            return True
        else:
            return False

    def place_tower(self, tower):
        self.tower_sprite.add(tower)

    def remove(self, x, y):
        self.map[y][x] = self.defaultmap[y][x]

    def sell_tower(self, tower):
        self.remove(tower.map_x, tower.map_y)
        self.tower_sprite.remove(tower)

    def call_wave(self, wave):
        return self.waves[wave - 1]

    def render(self, surface):
        self.sprites.draw(surface.surface)
        self.tower_sprite.draw(surface.surface)


def load_map():
    try:
        with open(os.path.join('data', 'map.json'), 'r+') as file:
            themap = json.load(file)
    except pygame.error:
        raise SystemExit('Could not load map "%s" %s' % (file, pygame.get_error()))
    return themap


def save_map(data):
    with open(os.path.join(os.getcwd(), 'data', 'map.json'), 'w') as file:
        json.dump(data, file)
