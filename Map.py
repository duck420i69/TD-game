class Tile:
    size = 100
    def __init__(self, maptype, x, y):
        pass


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


class Map(Tile):
    def __init__(self, rows, cols):
        super().__init__(maptype, x, y)
        self.defaultmap = [[0 for i in range(cols)] for j in range(rows)]
        self.map = self.defaultmap

    def assign(self, maptype, x, y):
        self.x = x
        self.y = y
        self.type0 = maptype // 10
        self.type1 = maptype % 10

        if self.type0 == 0:
            self.map[x][y] = maptype

    def remove(self, x, y):
        self.map[x][y] = self.defaultmap[x][y]

