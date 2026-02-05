import pygame
from GUI.Button import Button, ButtonSprites
from GUI.GUI import GUI
from State.InGame import InGame
from Control import actions_status
from State import State


from typing import TYPE_CHECKING, Callable
if TYPE_CHECKING:
    from State.Game import Game


class MainMenu(State.State):
    def __init__(self, game: "Game"):
        super().__init__(game)
        self.gui = GUI(game)

        self.gui.add_button(self.make_button((200, 100), "Start", 
                            lambda: self.enterstate(InGame(self.game, "fuck"))))
        self.gui.add_button(self.make_button((200, 140), "Continue"))
        self.gui.add_button(self.make_button((200, 180), "Load"))
        self.gui.add_button(self.make_button((200, 220), "Setting"))
        self.gui.add_button(self.make_button((200, 260), "Exit", self.quit_callback))

    def make_button(self, position: tuple[float], name: str, on_press: Callable[[], None] = None):
        rect = pygame.Rect(0, 0, 150, 30)
        rect.center = (position[0], position[1])
        return Button(
            ButtonSprites.create_default(150, 30), 
            name, 
            rect, 
            on_press=on_press
        )

    def render(self):
        self.game.screen.clear()
        self.gui.render(self.game.screen)
        self.game.screen.write_text("shittiest td game", (0, 0, 0), (200, 30), 20)
        self.game.screen.render()

    def quit_callback():
        actions_status["Quit"]["press"] = True