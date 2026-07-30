import os
from typing import Union
import pygame
from pygame.constants import FULLSCREEN, DOUBLEBUF
from constants import GAMERES_WIDTH, GAMERES_HEIGHT

flags0 = FULLSCREEN | DOUBLEBUF
flags1 = DOUBLEBUF

main_dir = os.path.split(os.path.abspath(__file__))[0]


def load_image(name):
    file = os.path.join(main_dir, "assets", "sprites", name)
    try:
        image = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s' % (file, pygame.get_error()))
    return image.convert_alpha()   


class Sprite(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, x: int, y: int):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def pos(self, x, y):
        self.rect.topleft = (x, y)


class Screen:
    """Handle writing, game window, final render process"""
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)

    def __init__(self, w: int, h: int, title: str):
        """
        w: width of the window
        h: height of the window
        title: title on the window
        """
        super().__init__()
        self.ratio = GAMERES_WIDTH / GAMERES_HEIGHT
        self.w = w
        self.h = h
        self.x_offset = 0
        self.y_offset = 0
        pygame.display.set_caption(title)

        # Implement this later
        # self.screen = pygame.display.set_mode(resolution, flags, 16)
        self.screen = pygame.display.set_mode((w, h))
        self.surface = pygame.Surface((GAMERES_WIDTH, GAMERES_HEIGHT))
        self.screen.fill(Screen.BLUE)
        
        self.sprites = pygame.sprite.Group()
        self.font_cache = {}
        if self.w > self.h * self.ratio:
            self.x_offset = int(self.w - self.h * self.ratio) // 2
            self.w = int(self.h * self.ratio)
        if self.h > self.w / self.ratio:
            self.y_offset = int(self.h - self.w / self.ratio) // 2
            self.h = int(self.w / self.ratio)

    def clear(self):
        self.surface.fill(Screen.WHITE)

    def rect(self, x, y, w, h, color):
        pygame.draw.rect(self.surface, color, (x, y, w, h))

    def blit(self, image, x, y):
        self.surface.blit(image, (x, y))

    def render(self):
        self.screen.blit(pygame.transform.scale(self.surface, (self.w, self.h)), (self.x_offset, self.y_offset))
        pygame.display.flip()

    def to_surface_space(self, vec2: Union[tuple[int, int], pygame.Vector2]):
        return ((vec2[0] - self.x_offset) * GAMERES_WIDTH  // self.w,
                (vec2[1] - self.y_offset) * GAMERES_HEIGHT // self.h)

    def write_text(self, text: str, color: tuple, position: tuple, size: int, align: str = "topleft"):
        if size not in self.font_cache:
            self.font_cache[size] = pygame.font.Font(None, size)
        font = self.font_cache[size]
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        setattr(text_rect, align, position)
        self.surface.blit(text_surface, text_rect)
 