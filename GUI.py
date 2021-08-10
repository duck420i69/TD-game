from Control import *

class GUI:
    def __init__(self):
        self.cursor = 0

    def cursor(self, controls, options):
        keycheck(controls)
        if actions["Up"]:
            self.cursor -= 1
            self.cursor = self.cursor % options
        if actions["Down"]:
            self.cursor += 1
            self.cursor = self.cursor % options
        return self.cursor

    def seleted(self):
        return True

    def button(self, x, y):
        pass