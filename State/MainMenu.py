from GUI import GUI
from State import InGame, State
from Control import actions_status

class MainMenu(State.State):
    def __init__(self, game):
        super().__init__(game)
        self.gui = GUI.GUI(game)
        self.gui.add_button("Start", 200, 100, 150, 30)
        self.gui.add_button("Continue", 200, 140, 150, 30)
        self.gui.add_button("Load", 200, 180, 150, 30)
        self.gui.add_button("Setting", 200, 220, 150, 30)
        self.gui.add_button("Exit", 200, 260, 150, 30)

    def render(self):
        self.game.surface.clear()
        self.gui.render(self.game.surface)
        self.game.surface.write_text("shittiest td game", (0, 0, 0), (200, 30), 20)
        self.game.surface.render()

    def update(self, t):
        self.options = self.gui.update(t)
        if self.options["Start"]:
            self.enterstate(InGame(self.game, "fuck"))
        if self.options["Continue"]:
            pass
        if self.options["Load"]:
            pass
        if self.options["Setting"]:
            pass
        if self.options["Exit"]:
            actions_status["Quit"]["press"] = True
