import os
import pygame
from pygame.constants import FULLSCREEN, DOUBLEBUF

flags0 = FULLSCREEN | DOUBLEBUF
flags1 = DOUBLEBUF

main_dir = os.path.split(os.path.abspath(__file__))[0]

gameres_w, gameres_h = 400, 300


def load_image(name):
    file = os.path.join(main_dir, "assets", "sprites", name)
    try:
        image = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s' % (file, pygame.get_error()))
    return image.convert_alpha()


class Sprite(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def pos(self, x, y):
        self.rect.topleft = [x, y]


class Screen:
    """Handle writing, game window, final render process"""
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)

    def __init__(self, w, h, title):
        """
        w: width of the window
        h: height of the window
        title: title on the window
        """
        super().__init__()
        global gameres_w
        global gameres_h
        self.ratio = gameres_w/gameres_h
        self.w = w
        self.h = h
        self.x_offset = 0
        self.y_offset = 0
        pygame.display.set_caption(title)

        # Implement this later
        # self.screen = pygame.display.set_mode(resolution, flags, 16)
        self.screen = pygame.display.set_mode((w, h))

        self.surface = pygame.Surface((gameres_w, gameres_h))
        self.screen.fill(Screen.BLUE)
        self.sprites = pygame.sprite.Group()
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

    def add_sprite(self, sprite):
        self.sprites.add(sprite)

    def remove_sprite(self, sprite):
        self.sprites.remove(sprite)

    def draw(self, sprites):
        sprites.draw(self.surface)

    def draw_line(self, color, pos1, pos2):
        pygame.draw.line(self.surface, color, pos1, pos2, 2)

    def write_text(self, text, color, pos, size, align="center"):
        font = pygame.font.Font(os.path.join("assets", "PressStart2P-vaV7.ttf"), size)
        text_surface = font.render(text, False, color)
        text_rect = text_surface.get_rect()
        if align == "center":
            text_rect.center = pos
        elif align == "topright":
            text_rect.topright = pos
        self.surface.blit(text_surface, text_rect)

    def render(self):
        self.screen.blit(pygame.transform.scale(self.surface, (self.w, self.h)), (self.x_offset, self.y_offset))
        pygame.display.flip()
