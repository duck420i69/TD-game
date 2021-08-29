import pygame.time

from Map import *
from Enemy import *
from GUI import *
from Control import *


class Game:
    def __init__(self):
        self.surface = Screen(400, 300, "Shitiest TD game ever")
        self.state = [MainMenu(self)]
        self.mainmenu = self.state

    def gameloop(self, t):
        keycheck(controls)
        self.state[-1].update(t)
        self.state[-1].render()

    def exit(self):
        self.state = self.mainmenu


class State:
    def __init__(self, game):
        self.game = game

    def update(self, t):
        pass

    def render(self):
        pass

    def enterstate(self, state):
        self.game.state.append(state)

    def exitstate(self):
        self.game.state.pop()


class MainMenu(State):
    def __init__(self, game):
        super().__init__(game)
        self.gui = GUI()
        self.options = {}
        self.gui.add_button("Start", 200, 60, 100, 20)
        self.gui.add_button("Continue", 200, 90, 100, 20)
        self.gui.add_button("Load", 200, 120, 100, 20)
        self.gui.add_button("Setting", 200, 150, 100, 20)
        self.gui.add_button("Exit", 200, 180, 100, 20)

    def render(self):
        self.game.surface.clear()
        self.gui.render(self.game.surface)
        self.game.surface.render()

    def update(self, t):
        self.options = self.gui.update()
        if self.options["Start"]:
            self.enterstate(InGame(self.game))
        if self.options["Continue"]:
            pass
        if self.options["Load"]:
            pass
        if self.options["Setting"]:
            pass
        if self.options["Exit"]:
            actions["Quit"] = True


class InGame(State):
    def __init__(self, game):
        super().__init__(game)
        self.options = {}
        self.gui = GUI()
        path = [[-1, 3], [3, 6], [7, 6], [7, 10], [3, 10], [3, 12]]
        self.map0 = Map(12, 10, 'fucku', path)
        self.towers = []
        self.enemies = []

    def render(self):
        self.game.surface.clear()
        self.map0.render(self.game.surface)
        for tower in self.towers:
            for bullet in tower.bullets:
                bullet.render(self.game.surface)
        for enemy in self.enemies:
            enemy.render(self.game.surface)
        self.gui.render(self.game.surface)
        self.game.surface.render()

    def update(self, t):
        self.options = self.gui.update()
        j = 0

        ############### GAME SYSTEM ###############

        # Enemy stuff
        for enemy in self.enemies[:]:
            if enemy.dead(t):
                self.enemies.remove(enemy)
            else:
                enemy.move(t)
                for tower in self.towers:
                    if tower.inrange(enemy.position()):
                        tower.add_target(enemy)

        # Collision system and tower atk
        for tower in self.towers:
            tower.update(t)
            if tower.any_target():
                tower.shoot(tower.target[tower.aim_target()].position())
            tower.clear_target()

            for bullet in tower.bullets[:]:
                bullet.move(t)
                if (not -bullet.hitbox[2] < bullet.hitbox[0] < gameres_w
                        or not -bullet.hitbox[3] < bullet.hitbox[1] < gameres_h):
                    bullet.dead = True
                for enemy in self.enemies:
                    if enemy.hitbox[0] - bullet.hitbox[2] < bullet.hitbox[0] <= enemy.hitbox[0] + enemy.hitbox[2]:
                        if enemy.hitbox[1] - bullet.hitbox[3] < bullet.hitbox[1] <= enemy.hitbox[1] + enemy.hitbox[3]:
                            enemy.get_hit(bullet)
                            bullet.dead = True

                if bullet.dead:
                    tower.bullets.remove(bullet)

        j += t
        if j > 1500:
            self.enemies.append(Enemy(80, 0, 0, self.map0))
            j = 0

        ############### GAME CONTROL ###############
        if actions["Esc"]:
            self.enterstate(IGMenu(self.game))
        if actions["1"]:
            self.options["Arrow"] = True
        if actions["2"]:
            self.options["Magic"] = True
        if actions["3"]:
            self.options["Bomb"] = True
        if actions["4"]:
            self.options["Poison"] = True
        if actions["5"]:
            self.options["Ice"] = True

        ############### GUI SETUP ###############


class IGMenu(State):
    def __init__(self, game):
        super().__init__(game)
        self.options = {}
        self.gui = GUI()
        self.gui.add_button("Resume", 200, 60, 100, 20)
        self.gui.add_button("Save & Load", 200, 90, 100, 20)
        self.gui.add_button("Setting", 200, 120, 100, 20)
        self.gui.add_button("Exit", 200, 150, 100, 20)

    def render(self):
        pass

    def update(self, t):
        keycheck(controls)
        self.options = self.gui.update()
        if self.options["Resume"] or actions["Esc"]:
            self.gui.reset_button()
            self.exitstate()
        if self.options["Save & Load"]:
            self.gui.reset_button()
            self.enterstate(SaveLoad(self.game))
        if self.options["Setting"]:
            self.gui.reset_button()
            self.enterstate(Setting(self.game))
        if self.options["Exit"]:
            self.gui.reset_button()
            self.game.exit()


class SaveLoad(State):
    def __init__(self, game):
        super().__init__(game)
        self.gui = GUI(4)

    def render(self):
        pass

    def update(self, t):
        pass


class Setting(State):
    def __init__(self, game):
        super().__init__(game)
        self.gui = GUI()
        self.setting = None

    def load_setting(self):
        try:
            with open(os.path.join('data', 'setting.json'), 'r+') as file:
                self.setting = json.load(file)
        except pygame.error:
            # TO DO: Inform about setting reset
            # self.setting = sumshiet
            self.save_setting()

    def save_setting(self):
        with open(os.path.join(os.getcwd(), 'data', 'setting.json'), 'w') as file:
            json.dump(self.setting, file)

    def render(self):
        pass

    def update(self, t):
        pass
