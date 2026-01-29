from State import Game, State
from GUI.GUI import *
from Control import *
from Map import *
from Towers import *
from Enemy import *


class State:
    def __init__(self, game: Game.Game):
        self.game = game
        self.gui = GUI(game)
        self.options = {}

    def update(self, t):
        pass

    def render(self):
        pass

    def enterstate(self, state):
        self.gui.reset_button()
        self.game.state.append(state)

    def exitstate(self):
        self.game.state.pop()


class IGMenu(State):
    def __init__(self, game):
        super().__init__(game)
        self.gui.add_button("Resume", 200, 60, 100, 20)
        self.gui.add_button("Save & Load", 200, 90, 100, 20)
        self.gui.add_button("Setting", 200, 120, 100, 20)
        self.gui.add_button("Exit", 200, 150, 100, 20)

    def render(self):
        pass

    def update(self, t):
        keycheck(controls)
        self.options = self.gui.update(t)
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

    def render(self):
        pass

    def update(self, t):
        pass


class Setting(State):
    def __init__(self, game):
        super().__init__(game)
        self.setting = None

    def load_setting(self):
        try:
            with open(os.path.join('data', 'setting.json'), 'r+') as file:
                self.setting = json.load(file)
        except:
            # TO DO: Inform about setting reset
            self.setting = self.default_setting()
            self.save_setting()

    def default_setting(self):
        default_setting = {
            "Volume": 69,
            "Resolution": (1280, 960),
            "Fullscreen": False
        }
        return default_setting

    def save_setting(self):
        with open(os.path.join(os.getcwd(), 'data', 'setting.json'), 'w') as file:
            json.dump(self.setting, file)

    def render(self):
        pass

    def update(self, t):
        pass


class KeyBind(State):
    def __init__(self, game):
        super().__init__(game)
