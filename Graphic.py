import pygame, os
from pygame.locals import *

flags = FULLSCREEN | DOUBLEBUF

# pygame.font.Font()
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
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def pos(self, x, y):
        self.rect.topleft = [x, y]


class Screen:
    white = (255, 255, 255)

    def __init__(self, w, h, title):
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
        # screen = pygame.display.set_mode(resolution, flags, 16)
        self.scn = pygame.display.set_mode((w, h))

        self.surface = pygame.Surface((gameres_w, gameres_h))
        self.scn.fill(Screen.white)
        self.sprites = pygame.sprite.Group()
        if self.w > self.h * self.ratio:
            self.x_offset = int(self.w - self.h * self.ratio) // 2
            self.w = int(self.h * self.ratio)
        if self.h > self.w / self.ratio:
            self.y_offset = int(self.h - self.w / self.ratio) // 2
            self.h = int(self.w / self.ratio)

    def clear(self):
        self.surface.fill((0, 0, 255))

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

    def write_text(self, text, pos, size):
        font = pygame.font.Font(None, size)
        text_surface = font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.center = pos
        self.surface.blit(text_surface, text_rect)

    def render(self):
        self.scn.blit(pygame.transform.scale(self.surface, (self.w, self.h)), (self.x_offset, self.y_offset))
        pygame.display.flip()
