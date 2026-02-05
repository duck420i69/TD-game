import json
import os


from typing import TYPE_CHECKING
from State.State import State
if TYPE_CHECKING:
    from State.Game import Game


class Setting(State):
    def __init__(self, game: "Game"):
        super().__init__(game)
        self.setting = None

    def load_setting(self):
        try:
            with open(os.path.join('data', 'setting.json'), 'r+') as file:
                self.setting = json.load(file)
        except:
            # TO DO: Inform about setting reset
            self.setting = self.default_setting()
            self.save_setting()

    def default_setting(self):
        default_setting = {
            "Volume": 69,
            "Resolution": (1280, 960),
            "Fullscreen": False
        }
        return default_setting

    def save_setting(self):
        with open(os.path.join(os.getcwd(), 'data', 'setting.json'), 'w') as file:
            json.dump(self.setting, file)

    def render(self):
        pass