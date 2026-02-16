import pygame
from GUI.Button import Button, ButtonSprites
from GUI.GUI import GUI
from State.InGame import InGame
from Control import actions_status
from State.State import State


from typing import TYPE_CHECKING, Callable
if TYPE_CHECKING:
    from State.Game import Game


def quit_callback():
    actions_status["Quit"]["press"] = True


class MainMenu(State):
    def __init__(self, game: "Game"):
        super().__init__(game)
        self.gui = GUI(game)

        self.add_button((200, 100), "Start",
                        lambda: self.enter_state(InGame(self.game, "fuck")))
        self.add_button((200, 140), "Continue")
        self.add_button((200, 180), "Load")
        self.add_button((200, 220), "Setting")
        self.add_button((200, 260), "Exit", quit_callback)

    def add_button(self, position: tuple[int, int], name: str, on_press: Callable[[], None] = None):
        rect = pygame.Rect(0, 0, 150, 30)
        rect.center = (position[0], position[1])
        self.gui.add_button(
            Button(
                ButtonSprites.create_default(150, 30),
                name,
                rect,
                on_press=on_press))

    def render(self):
        self.game.screen.clear()
        self.gui.render(self.game.screen)
        self.game.screen.write_text("shittiest td game", (0, 0, 0), (200, 30), 20)
        self.game.screen.render()

