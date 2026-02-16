from Graphic import load_image
import pygame
from .base import Tower
from .tower_stats import get_tower_stats, get_tower_property


class ElecTower(Tower):
    def __init__(self, map_, x, y, lv):
        super().__init__(map_, x, y, lv)
        self.image = load_image(get_tower_property("ElecTower", "tower_image"))
        self.charge = get_tower_property("ElecTower", "base_charge") or 7500

    def get_stat(self):
        stats = get_tower_stats("ElecTower", self.lv)

        # Apply map assignment
        self.map.assign(stats["map_id"], self.map_x, self.map_y)

        # Load stats
        self.atk = stats["atk"]
        self.rot = stats["rot"]
        self.ran = stats["ran"]
        self.sell_price = stats["sell_price"]
        self.upgrade_price = stats["upgrade_price"]

        # Update charge if specified in this level
        if "charge" in stats:
            self.charge = stats["charge"]

        # Load effects
        self.effects = stats["effects"].copy()

    # ...existing code...
    def shoot(self, enemy):
        enemy.hp -= self.atk * self.t/1000 * (1 - enemy.immune["Elec"][1]) * (1 + enemy.x_dmg["Elec"][0])
        enemy.status["Elec"] = self.effects["Elec"].copy()
        if enemy.hp <= 0:
            enemy.delete = True

    def update(self, dt):
        if self.t < self.charge:
            self.t += dt
        else:
            self.t = self.charge

    def is_in_range(self, pos):
        check = False
        if self.t >= 2500:
            vec2 = pos - pygame.Vector2(self.x, self.y)
            if pygame.Vector2.length(vec2) <= self.ran:
                check = True
        return check

