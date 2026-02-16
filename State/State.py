from GUI.GUI import *
from Enemy import *


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Game import Game


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

    def enter_state(self, state):
        self.game.state.append(state)

    def exit_state(self):
        self.game.state.pop()


class KeyBind(State):
    def __init__(self, game):
        super().__init__(game)
