import pygame
import pygame.transform

from GUI.Button import Button
from GUI.Frame import Frame
from Graphic import Screen, gameres_h, gameres_w
from Control import *


class Window:
    def __init__(self, text: str, options, width: int, height: int):
        self.window = pygame.screen((width, height))
        self.options = options
        self.opt = len(options)
        self.text = text
        self.x = width
        self.cursor = 0

    def update(self):
        if actions_status["Right"]["press"]:
            self.cursor += 1
            self.cursor = self.cursor % self.opt
        if actions_status["Left"]["press"]:
            self.cursor -= 1
            self.cursor = self.cursor % self.opt
        if actions_status["Start"]["press"]:
            self.options[self.cursor] = True

    def render(self, surface):
        surface.blit(self.window)


class GUI(Frame):
    """
    This is the most verbose shiet that i have ever written. Good luck to understand this utter fucking mess
    GUI(use_curser)
    To use this you need 'add_button' method

    use_curser: use move key to choose the option or not (default True)
    """
    def __init__(self, game, use_cursor=True):
        """
        buttons: list of button's names
        buttons_dict: link all buttons to their key (name)
        options: the output as a list of options
        opt: number of button
        last_act: name of the last button used
        selected_button: rect of the button that the mouse point at
        """
        self.game = game
        self.use_cur = use_cursor
        self.cursor = 0
        self.last_act = None
        self.opt = 0
        self.buttons_dict: dict[str, Button] = {}
        self.options = {}
        self.buttons = []
        self.sprite = pygame.sprite.Group()
        self.button_sprite = pygame.sprite.Group()
        self.selected_button = None
        self.mouse_pos = None
        self.t = 300

    def add_button(self, name, x, y, buttonsize_x, buttonsize_y, key=None, click=False, timer=0):
        image0 = pygame.Surface((buttonsize_x, buttonsize_y))
        image0.fill((255, 0, 0))
        image1 = pygame.Surface((buttonsize_x, buttonsize_y))
        image1.fill((200, 0, 0))
        button = Button((image0, image1), name, x, y, buttonsize_x, buttonsize_y, key, click, timer)
        self.buttons_dict[name] = button
        self.buttons.append(name)
        self.opt += 1
        button.add(self.button_sprite)

    def clear_button(self):
        self.buttons.clear()
        self.buttons_dict.clear()
        self.button_sprite.empty()

    def reset_button(self):
        for button in self.buttons_dict.values():
            button.reset()
        self.last_act = None

    def render(self, screen: Screen):
        self.button_sprite.draw(screen.surface)
        self.sprite.draw(screen.surface)

    def update(self, t):
        self.t += t
        self.button_sprite.update(t)
        self.selected_button = None
        mouse_pos = pygame.mouse.get_pos()
        self.mouse_pos = [(mouse_pos[0]-self.game.screen.x_offset) * gameres_w//self.game.screen.w,
                          (mouse_pos[1]-self.game.screen.y_offset) * gameres_h//self.game.screen.h]
        for button in self.buttons_dict.values():
            button.deactivate()
            if button.click:
                button.pressed = False
                button.image = button.sprites[0]
                # Key
                if button.key is not None:
                    if actions_status[button.key]["press"]:
                        button.activate()

                # Mouse
                if button.is_point(self.mouse_pos):
                    self.selected_button = button.rect
                    self.cursor = self.buttons.index(button.name)
                    if actions_status["Left Click"]["release"]:
                        button.activate()

            else:
                # Key
                if button.key is not None:
                    if actions_status[button.key]["press"]:
                        button.activate()

                # Mouse
                if button.is_point(self.mouse_pos):
                    self.selected_button = button.rect
                    self.cursor = self.buttons.index(button.name)
                    if actions_status["Left Click"]["release"]:
                        button.activate()

        if self.use_cur:
            if actions_status["Up"]["hold"] and self.t > 300:
                self.t = 0
                self.cursor -= 1
                self.cursor = self.cursor % self.opt
                print(self.buttons[self.cursor])
            elif actions_status["Down"]["hold"] and self.t > 300:
                self.t = 0
                self.cursor += 1
                self.cursor = self.cursor % self.opt
                print(self.buttons[self.cursor])
            if actions_status["Start"]["press"]:
                name = self.buttons[self.cursor]
                self.buttons_dict[name].activate()

        if actions_status["Right Click"]["press"]:
            self.reset_button()
            self.last_act = None

        not_activate = True
        for button in self.buttons_dict.values():
            if button.active:
                if not_activate:
                    if not button.hold:
                        button.press()
                        not_activate = False
                        if button.click:
                            if self.last_act is not None:
                                self.buttons_dict[self.last_act].press()
                                self.last_act = None
                        else:
                            if self.last_act is None:
                                self.last_act = button.name
                            else:
                                if self.last_act == button.name:
                                    self.last_act = None
                                else:
                                    self.buttons_dict[self.last_act].press()
                                    self.last_act = button.name
            else:
                button.release()
            self.options[button.name] = button.status()
        return self.options
