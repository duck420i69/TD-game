import pygame

from GUI.Button import Button
from Control import actions_status
from Graphic import Screen


class Frame:
    def __init__(self, rect: pygame.Rect):
        self.rect = rect
        self.buttons: list[Button] = []
        self.frames: list[Frame] = []
        self.renderable = pygame.sprite.Group()

    def add_button(self, button: Button):
        self.buttons.append(button)
        self.renderable.add(button)

    def propagate_event(self) -> bool:
        for frame in self.frames:
            if frame.propagate_event():
                return True
        return self.handle_event()

    def handle_event(self) -> bool:
        has_handled = False
        if actions_status["Left Click"]["press"]:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons:
                if button.is_hover(mouse_pos):
                    button.press()
                    has_handled = True
                    break
        if actions_status["Left Click"]["release"]:
            for button in self.buttons:
                if button.is_hover(mouse_pos):
                    button.release()
                button.hold = False
        return has_handled

    def render(self, screen: Screen):
        self.renderable.draw(screen)