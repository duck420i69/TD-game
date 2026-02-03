import os
import pygame

from typing import Callable


class ButtonSprites:
    def __init__(self, default: pygame.Surface, pressed: pygame.Surface, hover: pygame.Surface):
        self.default = default
        self.pressed = pressed
        self.hover = hover

    @staticmethod
    def create_default(size_x, size_y):
        default = pygame.Surface((size_x, size_y))
        default.fill((255, 0, 0))
        pressed = pygame.Surface((size_x, size_y))
        pressed.fill((100, 0, 0))
        hover = pygame.Surface((size_x, size_y))
        hover.fill((200, 0, 0))
        return ButtonSprites(default, pressed, hover)


class Button(pygame.sprite.Sprite):
    def __init__(self, 
                 sprites: ButtonSprites, 
                 name: str, 
                 rect: pygame.Rect = None, 
                 is_icon: bool = False, 
                 on_press: Callable[[], None] = None,
                 on_release: Callable[[], None] = None):
        super().__init__()

        self.hover = False
        self.hold = False
        self.pressed = False
        self.name = name
        self.is_icon = is_icon

        self.sprites = sprites
        self.image = self.sprites.default

        self.on_press = on_press
        self.on_release = on_release
        
        if rect is None:
            self.rect = rect
        else:
            self.rect = self.image.get_rect()

        self.font = pygame.font.Font(os.path.join("assets", "PressStart2P-vaV7.ttf"), 12)
        self._render()

    def press(self):
        if not self.hold:
            self.pressed = True
            print(f"{self.name} {self.pressed}")
            self.on_press()
        self.hold = True
        self._render()

    def release(self):
        if self.hold:
            self.pressed = False
            if self.hover:
                self.on_release()
        self.hold = False

    def is_hover(self, pos: pygame.Vector2):
        self.hover = self.rect.collidepoint(pos)
        return self.hover

    def reset(self):
        self.pressed = False
        self.hold = False
        self.image = self.sprites.default

    def update(self, t=0, *args, **kwargs) -> None:
        pass

    def _render(self):
        if self.pressed:
            self.image = self.sprites.pressed
        elif self.hover:
            self.image = self.sprites.hover
        else:
            self.image = self.sprites.default
        
        if self.is_icon:
            return
        
        # Render text
        text_surf = self.font.render(self.name, False, "black")
        text_rect = text_surf.get_rect(
            center=self.image.get_rect().center
        )

        self.image.blit(text_surf, text_rect)
