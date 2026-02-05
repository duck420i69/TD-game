import pygame

from GUI.Button import Button
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

    def clear_buttons(self):
        self.buttons.clear()
        self.renderable.clear()
        for frame in self.frames:
            frame.clear_buttons()

    def propagate_event(self, event: pygame.event.Event) -> bool:
        for frame in self.frames:
            if frame.propagate_event(event):
                return True
        for button in self.buttons:
            if button.handle_event(event):
                print(f"Button {button} handle {event}")
                return True
        return False

    def render(self, screen: Screen):
        self.renderable.draw(screen.surface)