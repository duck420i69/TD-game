from GUI.Button import Button, ButtonSprites
from GUI.GUI import GUI

from Map import Map
from Control import actions_status
from State.State import State
from Tower import *
from Enemy import *

from typing import TYPE_CHECKING, Callable


if TYPE_CHECKING:
    from State.Game import Game


class InGame(State):
    def __init__(self, game: "Game", map_: Map):
        super().__init__(game)
        self.gui = GUI(game)
        # mapdata = load_map(map_)
        map_ = {
            "map": [[0 for _ in range(17)] for _ in range(15)],
            "path": [[-1, 3], [5, 3], [5, 10], [12, 10], [12, 5], [18, 5]],
            "wave data": [[("Slime", 10, 1500, 5, 1500, 0)]],
            "wave": 1,
            "money": 400,
            "live": 10
        }
        mapdata = map_
        self.money = mapdata["money"]
        self.live = mapdata["live"]
        self.current_wave = mapdata["wave"]
        self.map_ = Map(mapdata)

        self.t = 0
        self.lightning = []
        self.wave = []
        self.towers: list[Tower] = []
        self.enemies: list[Enemy] = []
        self.coin = load_image("coin.png")
        self.live_sprite = load_image("live.png")
        self.gui_sprite = load_image("ingamegui.png")
        self.frame = load_image("frame.png")
        self.element_sprite = {
            "Fire": load_image("fire_element.png"),
            "Water": load_image("water_element.png"),
            "Ice": load_image("ice_element.png"),
            "Elec": load_image("elec_element.png"),
            "Earth": [load_image("earth_element0.png"), load_image("earth_element1.png")]
        }
        self.selected = False
        self.prev_sel = False
        self.selected_tower = None
        self.gui_setup_normal()

    def gui_setup_normal(self):
        self.make_icon_button((20, 20), "Pause", self.exit_state)
        self.make_icon_button((20, 270), "Call Waves")
        self.make_icon_button((370, 80), "Fire")
        self.make_icon_button((370, 110), "Water")
        self.make_icon_button((370, 140), "Ice")
        self.make_icon_button((370, 170), "Elec")
        self.make_icon_button((370, 200), "Earth")
        self.make_icon_button((370, 230), "Wind")

    def gui_setup_tower(self):
        self.make_icon_button((20, 20), "Pause")
        self.make_icon_button((20, 270), "Call Waves")
        self.make_icon_button((370, 240), "Upgrade")
        self.make_icon_button((370, 270), "Sell")

    def render(self):
        self.game.screen.clear()
        self.map_.render(self.game.screen)
        for tower in self.towers:
            for bullet in tower.bullets:
                bullet.render(self.game.screen)
        for enemy in self.enemies:
            enemy.render(self.game.screen, self.element_sprite)
        for lightning in self.lightning:
            self.game.screen.draw_line((212, 0, 249), lightning[1], lightning[2])
        self.game.screen.rect(340, 0, 60, 300, (255, 255, 0))
        self.game.screen.blit(self.gui_sprite, 340, 0)
        self.game.screen.blit(self.frame, 342, 16)
        self.game.screen.blit(self.frame, 342, 36)
        self.gui.render(self.game.screen)
        self.game.screen.write_text(f"{self.money}", (0, 0, 0), (395, 20), 8, "topright")
        self.game.screen.write_text(f"{self.live}", (0, 0, 0), (395, 40), 8, "topright")
        self.game.screen.blit(self.coin, 345, 20)
        self.game.screen.blit(self.live_sprite, 345, 40)
        self.game.screen.render()

    def update(self, dt: float):
        ############### GAME SYSTEM ###############

        # Enemy stuff
        for enemy in self.enemies[:]:
            if enemy.delete:
                self.money += enemy.reward()
                self.enemies.remove(enemy)
                if enemy.hp > 0:
                    self.live -= enemy.life_lost
            else:
                enemy.update(dt)
                enemy.move(dt)
                for tower in self.towers:
                    if tower.is_in_range(enemy.position()):
                        tower.add_target(enemy)

        # Collision system and tower atk
        for tower in self.towers:
            tower.update(dt)
            if tower.any_target():
                target = tower.targets[tower.aim_target()]
                tower.shoot(target)
                tower.clear_target()
                if tower.effects["Elec"][0]:
                    self.lightning.append([30, target.center(), (tower.x, tower.y)])
                    next_target = None
                    prev_target = None
                    for _ in range(min(tower.effects["Elec"][2] - 1, len(self.enemies))):
                        min_ = 80
                        for enemy in self.enemies:
                            if enemy != prev_target and enemy != target:
                                distant = target.position().distance_to(enemy.position())
                                if min_ >= distant:
                                    min_ = distant
                                    next_target = enemy
                        if next_target == target:
                            next_target = None
                        if next_target is not None:
                            self.lightning.append([30, target.center(), next_target.center()])
                            tower.t = tower.t * 0.75
                            tower.shoot(next_target)
                            prev_target = target
                            target = next_target
                        else:
                            break
                    tower.t = 0
            for bullet in tower.bullets[:]:
                bullet.move(dt)
                if (not -bullet.hitbox[2] < bullet.hitbox[0] < GAMERES_WIDTH
                        or not -bullet.hitbox[3] < bullet.hitbox[1] < GAMERES_HEIGHT):
                    bullet.dead = True
                for enemy in self.enemies:
                    if enemy.hitbox[0] - bullet.hitbox[2] < bullet.hitbox[0] <= enemy.hitbox[0] + enemy.hitbox[2]:
                        if enemy.hitbox[1] - bullet.hitbox[3] < bullet.hitbox[1] <= enemy.hitbox[1] + enemy.hitbox[3]:
                            if not bullet.dead:
                                if bullet.effects["Explosion"][0]:
                                    for ene in self.enemies:
                                        distant = enemy.position().distance_to(ene.position())
                                        if distant <= bullet.effects["Explosion"][1]:
                                            ene.get_hit(bullet)
                                else:
                                    enemy.get_hit(bullet)
                                bullet.dead = True
                if bullet.dead:
                    tower.bullets.remove(bullet)

        for enemy_group in self.wave:
            # [enemy_type, lv, density, amount, selftime, timer]
            if self.t - enemy_group[5] >= 0:
                enemy_group[4] += dt
                if enemy_group[3] > 0:
                    if enemy_group[4] >= enemy_group[2]:
                        enemy_group[3] -= 1
                        enemy_group[4] = enemy_group[4] % enemy_group[2]
                        if enemy_group[0] == "Slime":
                            self.enemies.append(Slime(enemy_group[1], self.map_))
                else:
                    self.wave.remove(enemy_group)

        for lightning in self.lightning:
            if lightning[0] > 0:
                lightning[0] -= dt
            else:
                self.lightning.remove(lightning)

        if actions_status["Left Click"]["press"]:
            self.selected = False
            for tower in self.towers:
                tower.click(self.gui.mouse_pos)
                if tower.selected:
                    self.selected = True
                    self.selected_tower = tower

            if self.selected != self.prev_sel:
                if self.selected:
                    self.gui_setup_tower()
                else:
                    self.gui_setup_normal()
                self.options = self.gui.update(0)
                self.prev_sel = self.selected

        ############### GAME CONTROL ###############
        if self.options["Pause"]:
            self.exit_state()
        if self.options["Call Waves"]:
            self.t = 0
            wave = self.map_.call_wave(self.current_wave)
            print(wave)
            self.wave = [list(i) for i in wave]

        if not self.selected:
            if self.options["Fire"]:
                if actions_status["Left Click"]["press"]:
                    x = self.gui.mouse_pos[0]//self.map_.tilesize
                    y = self.gui.mouse_pos[1]//self.map_.tilesize
                    if 0 <= x <= self.map_.w and 0 <= x <= self.map_.h:
                        if self.money >= 50:
                            if self.map_.assign(11, x, y):
                                self.money -= 50
                                fire = FireTower(self.map_, x, y, 1)
                                self.towers.append(fire)
                                self.map_.place_tower(fire)
                        else:
                            print("money insufficion")
                        self.gui.buttons_dict["Fire"].press()
                        self.gui.last_act = None

            if self.options["Water"]:
                if actions_status["Left Click"]["press"]:
                    x = self.gui.mouse_pos[0]//self.map_.tilesize
                    y = self.gui.mouse_pos[1]//self.map_.tilesize
                    if 0 <= x <= self.map_.w and 0 <= x <= self.map_.h:
                        if self.money >= 50:
                            if self.map_.assign(21, x, y):
                                self.money -= 50
                                water = WaterTower(self.map_, x, y, 1)
                                self.towers.append(water)
                                self.map_.place_tower(water)
                        else:
                            print("money insufficion")
                        self.gui.buttons_dict["Water"].press()
                        self.gui.last_act = None

            if self.options["Ice"]:
                if actions_status["Left Click"]["press"]:
                    x = self.gui.mouse_pos[0]//self.map_.tilesize
                    y = self.gui.mouse_pos[1]//self.map_.tilesize
                    if 0 <= x <= self.map_.w and 0 <= x <= self.map_.h:
                        if self.money >= 50:
                            if self.map_.assign(31, x, y):
                                self.money -= 50
                                ice = IceTower(self.map_, x, y, 1)
                                self.towers.append(ice)
                                self.map_.place_tower(ice)
                        else:
                            print("money insufficion")
                        self.gui.buttons_dict["Ice"].press()
                        self.gui.last_act = None

            if self.options["Elec"]:
                if actions_status["Left Click"]["press"]:
                    x = self.gui.mouse_pos[0]//self.map_.tilesize
                    y = self.gui.mouse_pos[1]//self.map_.tilesize
                    if 0 <= x <= self.map_.w and 0 <= x <= self.map_.h:
                        if self.money >= 50:
                            if self.map_.assign(41, x, y):
                                self.money -= 50
                                elec = ElecTower(self.map_, x, y, 1)
                                self.towers.append(elec)
                                self.map_.place_tower(elec)
                        else:
                            print("money insufficion")
                        self.gui.buttons_dict["Elec"].press()
                        self.gui.last_act = None

            if self.options["Earth"]:
                if actions_status["Left Click"]["press"]:
                    x = self.gui.mouse_pos[0]//self.map_.tilesize
                    y = self.gui.mouse_pos[1]//self.map_.tilesize
                    if 0 <= x <= self.map_.w and 0 <= x <= self.map_.h:
                        if self.money >= 50:
                            if self.map_.assign(51, x, y):
                                self.money -= 50
                                earth = EarthTower(self.map_, x, y, 1)
                                self.towers.append(earth)
                                self.map_.place_tower(earth)
                        else:
                            print("money insufficion")
                        self.gui.buttons_dict["Earth"].press()
                        self.gui.last_act = None

            if self.options["Wind"]:
                if actions_status["Left Click"]["press"]:
                    x = self.gui.mouse_pos[0]//self.map_.tilesize
                    y = self.gui.mouse_pos[1]//self.map_.tilesize
                    if 0 <= x <= self.map_.w and 0 <= x <= self.map_.h:
                        if self.money >= 50:
                            if self.map_.assign(61, x, y):
                                self.money -= 50
                                wind = WindTower(self.map_, x, y, 1)
                                self.towers.append(wind)
                                self.map_.place_tower(wind)
                        else:
                            print("money insufficion")
                        self.gui.buttons_dict["Wind"].press()
                        self.gui.last_act = None

        else:
            if self.options["Upgrade"]:
                if self.selected_tower.upgrade_price is not None:
                    if self.money >= self.selected_tower.upgrade_price:
                        self.money -= self.selected_tower.upgrade_price
                        self.selected_tower.upgrade()
                    else:
                        print("insufficient money")
                else:
                    print("max lv")
            if self.options["Sell"]:
                self.money += self.selected_tower.sell()
                self.towers.remove(self.selected_tower)
                self.map_.sell_tower(self.selected_tower)
            if actions_status["Right Click"]["press"]:
                self.selected_tower.selected = False
                self.gui_setup_normal()
                self.prev_sel = True

    def make_button(self, position: tuple[int, int], name: str, on_press: Callable[[], None] = None):
        rect = pygame.Rect(0, 0, 150, 30)
        rect.center = (position[0], position[1])
        self.gui.add_button(Button(
            ButtonSprites.create_default(150, 30), 
            name, 
            rect, 
            on_press=on_press
        ))
    
    def make_icon_button(self, position: tuple[int, int], name: str, on_press: Callable[[], None] = None):
        rect = pygame.Rect(0, 0, 20, 20)
        rect.center = (position[0], position[1])
        self.gui.add_button(Button(
            ButtonSprites.create_default(20, 20), 
            name, 
            rect, 
            on_press=on_press,
            is_icon=True
        ))
