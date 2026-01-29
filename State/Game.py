from Control import keycheck, controls
from Graphic import Screen
from State import MainMenu


class Game:
    def __init__(self):
        self.w = 1000
        self.h = 750
        self.surface = Screen(self.w, self.h, "Shitiest TD game ever")
        self.state = [MainMenu(self)]
        self.mainmenu = self.state

    def gameloop(self, t):
        keycheck(controls)
        self.state[-1].update(t)
        self.state[-1].render()

    def exit(self):
        self.state = self.mainmenu