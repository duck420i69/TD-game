from Graphic import load_image
from .base import Tower
from .tower_stats import get_tower_stats, get_tower_property


class WaterTower(Tower):
    def __init__(self, map_, x, y, lv):
        super().__init__(map_, x, y, lv)
        self.bullet_image = load_image(get_tower_property("WaterTower", "bullet_image"))
        self.image = load_image(get_tower_property("WaterTower", "tower_image"))

    def get_stat(self):
        stats = get_tower_stats("WaterTower", self.lv)

        # Apply map assignment
        self.map.assign(stats["map_id"], self.map_x, self.map_y)

        # Load stats
        self.atk = stats["atk"]
        self.spd = stats["spd"]
        self.rot = stats["rot"]
        self.ran = stats["ran"]
        self.bsize = stats["bsize"]
        self.sell_price = stats["sell_price"]
        self.upgrade_price = stats["upgrade_price"]

        # Load effects
        self.effects = stats["effects"].copy()

