from GUI import GUI
from State.InGame import InGame
from Control import actions_status
from State.SaveLoad import SaveLoad
from State.Setting import Setting
from State.State import State


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from State.Game import Game


class IGMenu(State):
    def __init__(self, game: "Game"):
        super().__init__(game)
        self.gui.add_button("Resume", 200, 60, 100, 20)
        self.gui.add_button("Save & Load", 200, 90, 100, 20)
        self.gui.add_button("Setting", 200, 120, 100, 20)
        self.gui.add_button("Exit", 200, 150, 100, 20)

    def render(self):
        pass

    def update(self, t):
        self.options = self.gui.update(t)
        if self.options["Resume"] or actions_status["Esc"]:
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