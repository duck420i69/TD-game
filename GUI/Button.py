import os
import pygame


class ButtonSprites:
    def __init__    


class Button(pygame.sprite.Sprite):
    def __init__(self, sprites: list[pygame.Surface], name, x, y, buttonsize_x, buttonsize_y, key, click, timer):
        super().__init__()
        self.hold = False
        self.click = click
        self.timer = timer
        self.t = 0
        self.active = False
        self.pressed = False

        self.key = key
        self.name = name

        self.sprites = sprites
        self.sizex, self.sizey = buttonsize_x, buttonsize_y
        self.x, self.y = x - buttonsize_x//2, y - buttonsize_y//2
        self.image = self.sprites[0]

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.font = pygame.font.Font(os.path.join("assets", "PressStart2P-vaV7.ttf"), 12)
        self._render()

    def press(self):
        if not self.hold:
            self.pressed = not self.pressed
            self.hold = True
            print(f"{self.name} {self.pressed}")
        if self.timer > 0:
            if self.t >= self.timer:
                self.hold = False
                self.t -= self.timer

        if self.pressed:
            self.image = self.sprites[1]
        else:
            self.image = self.sprites[0]
        self._render()

    def release(self):
        self.hold = False

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def is_point(self, pos):
        return self.rect.collidepoint(pos)

    def reset(self):
        self.pressed = False
        self.hold = False
        self.image = self.sprites[0]

    def status(self):
        return self.pressed

    def update(self, t=0, *args, **kwargs) -> None:
        if self.timer > 0:
            self.t += t

    def _render(self):
        # Render text
        text_surf = self.font.render(self.name, True, "black")
        text_rect = text_surf.get_rect(
            center=self.image.get_rect().center
        )

        # Blit text on top
        self.image.blit(text_surf, text_rect)
