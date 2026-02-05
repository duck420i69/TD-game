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

    def update(self, dt):
        pass

    def render(self):
        pass

    def handle_events(self, events: list[pygame.event.Event]):
        for event in events:
            self.gui.propagate_event(event)

    def enterstate(self, state):
        self.game.state.append(state)

    def exitstate(self):
        self.game.state.pop()


class KeyBind(State):
    def __init__(self, game):
        super().__init__(game)
