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
from Render import *
pygame.init()


class Map:
    def __init__(self, surface, w_tile, h_tile, themap, path):
        self.defaultmap = [[0 for _ in range(w_tile)] for _ in range(h_tile)]  # = themap
        self.path = path  # path is a list of pos to move to
        self.w = w_tile
        self.h = h_tile
        self.tilesize = surface.getw()//w_tile
        self.surface = surface
        self.map = self.defaultmap

    def assign(self, maptype, x, y):
        if self.map[y][x] // 10 == 0:
            self.map[y][x] = maptype

    def remove(self, x, y):
        self.map[y][x] = self.defaultmap[y][x]

    def render(self):
        for j in range(self.h):
            for i in range(self.w):
                if self.map[j][i] == 11:
                    red = (255, 0, 0)
                    self.surface.rect(self.tilesize * i, self.tilesize * j, self.tilesize, self.tilesize, red)
                if self.map[j][i] == 0:
                    green = (0, 255, 0)
                    self.surface.rect(self.tilesize * i, self.tilesize * j, self.tilesize, self.tilesize, green)
                if self.map[j][i] == -10:
                    brown = (150, 84, 69)
                    self.surface.rect(self.tilesize * i, self.tilesize * j, self.tilesize, self.tilesize, brown)
