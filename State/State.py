from GUI.GUI import *
from Control import *
from Map import *
from Towers import *
from Enemy import *


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from State.Game import Game


class State:
    def __init__(self, game: "Game"):
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


class KeyBind(State):
    def __init__(self, game):
        super().__init__(game)
