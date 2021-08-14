import pygame, sys


class State:
    def __init__(self, surface):
        self.surface = surface
        self.state = []

    def update(self):
        self.state[-1].update()

    def render(self):
        self.state[-1].render(self.surface)

    def enterstate(self, state):
        self.state.append(state)

    def exitstate(self):
        self.state.pop()


class MainMenu(State):
    def __init__(self, surface):
        State(self).__init__(surface)

    def render(self):
        pass

    def update(self):
        pass


class InGame(State):
    def __init__(self, surface):
        State(self).__init__(surface)

    def render(self):
        pass

    def update(self):
        pass


class IGMenu(State):
    def __init__(self, surface):
        State(self).__init__(surface)

    def render(self):
        pass

    def update(self):
        pass