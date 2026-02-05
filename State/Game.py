import pygame
from Control import keycheck, controls
from Graphic import Screen
from State.MainMenu import MainMenu


class Game:
    def __init__(self):
        self.w = 1000
        self.h = 750
        self.screen = Screen(self.w, self.h, "Shitiest TD game ever")
        self.state = [MainMenu(self)]
        self.mainmenu = self.state[:]

    def gameloop(self, dt):
        events = pygame.event.get()
        keycheck(controls, events)
        self.state[-1].handle_events(events)
        self.state[-1].update(dt)
        self.state[-1].render()

    def exit(self):
        self.state = self.mainmenu