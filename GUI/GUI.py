import pygame

from GUI.Frame import Frame
from Control import *


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from State.Game import Game
    

class Window:
    def __init__(self, text: str, options, width: int, height: int):
        self.window = pygame.screen((width, height))
        self.options = options
        self.opt = len(options)
        self.text = text
        self.x = width
        self.cursor = 0

    def update(self):
        if actions_status["Right"]["press"]:
            self.cursor += 1
            self.cursor = self.cursor % self.opt
        if actions_status["Left"]["press"]:
            self.cursor -= 1
            self.cursor = self.cursor % self.opt
        if actions_status["Start"]["press"]:
            self.options[self.cursor] = True

    def render(self, surface):
        surface.blit(self.window)


class GUI(Frame):
    def __init__(self, game: "Game"):
        super().__init__(game.screen.screen.get_rect())
        self.game = game

    def propagate_event(self, event: pygame.event.Event) -> bool:
        if "pos" in event.dict.keys():
            event.pos = self.game.screen.to_surface_space(event.pos)
        return super().propagate_event(event)