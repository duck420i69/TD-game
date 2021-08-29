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
    def __init__(self, w_tile, h_tile, themap, path):
        self.defaultmap = [[0 for _ in range(w_tile)] for _ in range(h_tile)]  # = themap
        self.w = w_tile
        self.h = h_tile
        self.tilesize = 20
        self.path = path  # path is a list of pos to move to
        for i in range(len(self.path)):
            self.path[i][0] = (self.path[i][0] + 0.1) * self.tilesize
            self.path[i][1] = (self.path[i][1] + 0.1) * self.tilesize

        self.map = self.defaultmap
        self.grass = load_image("grass.png")
        self.road = load_image("path.png")
        self.sprites = pygame.sprite.Group()

    def assign(self, maptype, x, y):
        if self.map[y][x] // 10 == 0:
            self.map[y][x] = maptype

    def remove(self, x, y):
        self.map[y][x] = self.defaultmap[y][x]

    def init_sprite(self):
        for j in range(self.h):
            for i in range(self.w):
                if self.map[j][i] == 11:
                    pass
                if self.map[j][i] == 0:
                    grass = Sprite(self.grass, self.tilesize * i, self.tilesize * j)
                    grass.add(self.sprites)
                if self.map[j][i] == -10:
                    road = Sprite(self.road, self.tilesize * i, self. tilesize * j)
                    road.add(self.sprites)

    def render(self, surface):
        surface.draw(self.sprites)


def load_map():
    try:
        with open(os.path.join('map.json'), 'r+') as file:
            themap = json.load(file)
    except pygame.error:
        raise SystemExit('Could not load map "%s" %s' % (file, pygame.get_error()))
    return themap


def save_map(data):
    with open(os.path.join(os.getcwd(), 'map.json'), 'w') as file:
        json.dump(data, file)
