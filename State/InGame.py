from GUI import GUI
from Graphic import load_image
from Map import Map
from State import Game, State
from Graphic import gameres_h, gameres_w
from Control import actions_status


class InGame(State.State):
    def __init__(self, game: Game.Game, map_):
        super().__init__(game)
        self.gui = GUI.GUI(game, False)
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
        self.towers = []
        self.enemies = []
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
        self.gui.clear_button()
        self.gui.add_button("Pause", 20, 20, 20, 20, "Esc")
        self.gui.add_button("Call Waves", 20, 270, 20, 20, None, True)
        self.gui.add_button("Fire", 370, 80, 20, 20, "1")
        self.gui.add_button("Water", 370, 110, 20, 20, "2")
        self.gui.add_button("Ice", 370, 140, 20, 20, "3")
        self.gui.add_button("Elec", 370, 170, 20, 20, "4")
        self.gui.add_button("Earth", 370, 200, 20, 20, "5")
        self.gui.add_button("Wind", 370, 230, 20, 20, "6")

    def gui_setup_tower(self):
        self.gui.clear_button()
        self.gui.add_button("Pause", 20, 20, 20, 20, "Esc")
        self.gui.add_button("Call Waves", 20, 270, 20, 20, None, True)
        self.gui.add_button("Upgrade", 370, 240, 20, 20, None, True)
        self.gui.add_button("Sell", 370, 270, 20, 20, None, True)

    def render(self):
        self.game.surface.clear()
        self.map_.render(self.game.surface)
        for tower in self.towers:
            for bullet in tower.bullets:
                bullet.render(self.game.surface)
        for enemy in self.enemies:
            enemy.render(self.game.surface, self.element_sprite)
        for lightning in self.lightning:
            self.game.surface.draw_line((212, 0, 249), lightning[1], lightning[2])
        self.game.surface.rect(340, 0, 60, 300, (255, 255, 0))
        self.game.surface.blit(self.gui_sprite, 340, 0)
        self.game.surface.blit(self.frame, 342, 16)
        self.game.surface.blit(self.frame, 342, 36)
        self.gui.render(self.game.surface)
        self.game.surface.write_text(f"{self.money}", (0, 0, 0), (395, 20), 8, "topright")
        self.game.surface.write_text(f"{self.live}", (0, 0, 0), (395, 40), 8, "topright")
        self.game.surface.blit(self.coin, 345, 20)
        self.game.surface.blit(self.live_sprite, 345, 40)
        self.game.surface.render()

    def update(self, t):
        self.options = self.gui.update(t)

        ############### GAME SYSTEM ###############

        # Enemy stuff
        for enemy in self.enemies[:]:
            if enemy.delete:
                self.money += enemy.reward()
                self.enemies.remove(enemy)
                if enemy.hp > 0:
                    self.live -= enemy.life_lost
            else:
                enemy.update(t)
                enemy.move(t)
                for tower in self.towers:
                    if tower.inrange(enemy.position()):
                        tower.add_target(enemy)

        # Collision system and tower atk
        for tower in self.towers:
            tower.update(t)
            if tower.any_target():
                target = tower.target[tower.aim_target()]
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
                bullet.move(t)
                if (not -bullet.hitbox[2] < bullet.hitbox[0] < gameres_w
                        or not -bullet.hitbox[3] < bullet.hitbox[1] < gameres_h):
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
                enemy_group[4] += t
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
                lightning[0] -= t
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
            self.exitstate()
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

