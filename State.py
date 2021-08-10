import pygame


class State:
    def __init__(self, controls, screen):
        self.controls = controls
        self.scr = screen
        self.state = ["menu"]
        self.running = True

    def run(self):
        return self.running

    def currentstate(self):
        return self.state[-1]

    def enterstate(self, state):
        self.state.append(state)

    def exitstate(self):
        self.state.pop()

    def menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def ingame(self, themap, t):
        self.map = themap


        self.map.render()

    def ingame_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

