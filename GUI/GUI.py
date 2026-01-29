import pygame.transform

from Graphic import gameres_h, gameres_w
from Control import *


class Button(pygame.sprite.Sprite):
    def __init__(self, sprites, name, x, y, buttonsize_x, buttonsize_y, key, click, timer):
        super().__init__()
        self.hold = False
        self.click = click
        self.timer = timer
        self.t = 0
        self.active = False
        self.pressed = False

        self.key = key
        self.name = name

        self.sprite = sprites
        self.sizex, self.sizey = buttonsize_x, buttonsize_y
        self.x, self.y = x - buttonsize_x//2, y - buttonsize_y//2
        self.image = self.sprite[0]

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def press(self):
        if not self.hold:
            self.pressed = not self.pressed
            self.hold = True
            print(f"{self.name} {self.pressed}")
        if self.timer > 0:
            if self.t >= self.timer:
                self.hold = False
                self.t -= self.timer

        if self.pressed:
            self.image = self.sprite[1]
        else:
            self.image = self.sprite[0]

    def release(self):
        self.hold = False

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def is_point(self, pos):
        return self.rect.collidepoint(pos)

    def reset(self):
        self.pressed = False
        self.hold = False
        self.image = self.sprite[0]

    def status(self):
        return self.pressed

    def update(self, t=0, *args, **kwargs) -> None:
        if self.timer > 0:
            self.t += t


class Window:
    def __init__(self, text, options, width, height):
        self.window = pygame.Surface((width, height))
        self.options = options
        self.opt = len(options)
        self.text = text
        self.x = width
        self.cursor = 0

    def update(self):
        if actions["Right"]:
            self.cursor += 1
            self.cursor = self.cursor % self.opt
        if actions["Left"]:
            self.cursor -= 1
            self.cursor = self.cursor % self.opt
        if actions["Start"]:
            self.options[self.cursor] = True

    def render(self, surface):
        surface.blit(self.window)


class GUI:
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
        self.buttons_dict = {}
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

    def render(self, surface):
        self.button_sprite.draw(surface.surface)
        self.sprite.draw(surface.surface)

    def update(self, t):
        self.t += t
        self.button_sprite.update(t)
        self.selected_button = None
        mouse_pos = pygame.mouse.get_pos()
        self.mouse_pos = [(mouse_pos[0]-self.game.surface.x_offset) * gameres_w//self.game.surface.w,
                          (mouse_pos[1]-self.game.surface.y_offset) * gameres_h//self.game.surface.h]
        for button in self.buttons_dict.values():
            button.deactivate()
            if button.click:
                button.pressed = False
                button.image = button.sprite[0]
                # Key
                if button.key is not None:
                    if actions[button.key]:
                        button.activate()

                # Mouse
                if button.is_point(self.mouse_pos):
                    self.selected_button = button.rect
                    self.cursor = self.buttons.index(button.name)
                    if actions["Left Click"][0]:
                        button.activate()

            else:
                # Key
                if button.key is not None:
                    if actions[button.key]:
                        button.activate()

                # Mouse
                if button.is_point(self.mouse_pos):
                    self.selected_button = button.rect
                    self.cursor = self.buttons.index(button.name)
                    if actions["Left Click"][0]:
                        button.activate()

        if self.use_cur:
            if actions["Up"] and self.t > 300:
                self.t = 0
                self.cursor -= 1
                self.cursor = self.cursor % self.opt
                print(self.buttons[self.cursor])
            elif actions["Down"] and self.t > 300:
                self.t = 0
                self.cursor += 1
                self.cursor = self.cursor % self.opt
                print(self.buttons[self.cursor])
            if actions["Start"]:
                name = self.buttons[self.cursor]
                self.buttons_dict[name].activate()

        if actions["Right Click"]:
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
