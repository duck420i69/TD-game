import pygame


class Screen:
    white = (255, 255, 255)

    def __init__(self, w, h, title):
        self.gameres_w = 600
        self.gameres_h = 400
        self.ratio = self.gameres_w/self.gameres_h
        self.w = w
        self.h = h
        self.x_offset = 0
        self.y_offset = 0
        pygame.display.set_caption(title)
        self.scn = pygame.display.set_mode((w, h))
        self.surface = pygame.Surface((self.gameres_w, self.gameres_h))
        self.scn.fill(Screen.white)
        sprites = pygame.sprite.Group()
        if self.w > self.h * self.ratio:
            self.x_offset = int(self.w - self.h * self.ratio) // 2
            self.w = int(self.h * self.ratio)
        if self.h > self.w / self.ratio:
            self.y_offset = int(self.h - self.w / self.ratio) // 2
            self.h = int(self.w / self.ratio)

    def clear(self):
        self.surface.fill((255, 255, 255))

    def rect(self, x, y, w, h, color):
        pygame.draw.rect(self.surface, color, (x, y, w, h))

    def getw(self):
        return self.gameres_w

    def geth(self):
        return self.gameres_h

    def render(self):
        self.scn.blit(pygame.transform.scale(self.surface, (self.w, self.h)), (self.x_offset, self.y_offset))
        pygame.display.flip()
