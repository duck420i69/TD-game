import pygame.transform

from Control import *


class Button(pygame.sprite.Sprite):
    def __init__(self, sprites, name, x, y, buttonsize_x, buttonsize_y, key):
        super().__init__()
        self.key = key
        self.name = name
        self.sprite = sprites
        self.sizex, self.sizey = buttonsize_x, buttonsize_y
        self.x, self.y = x - buttonsize_x//2, y - buttonsize_y//2
        self.pressed = False
        self.image = self.sprite[0]
        self.image = pygame.transform.scale(self.image, (self.sizex, self.sizey))

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        font = pygame.font.Font(None, 18)
        text_surface = font.render(self.name, True, (0, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        for image in self.sprite:
            image.blit(text_surface, text_rect)

    def press(self):
        print(f"press {self.name}")
        self.pressed = not self.pressed

    def is_point(self, pos):
        if self.x <= pos[0] < self.x + self.sizex and self.y <= pos[1] < self.y + self.sizey:
            return True
        else:
            return False

    def reset(self):
        self.pressed = False

    def status(self):
        return self.pressed

    def update(self, *args, **kwargs) -> None:

        if self.pressed:
            self.image = self.sprite[1]
        else:
            self.image = self.sprite[0]


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
    def __init__(self, use_cursor=True):
        """
        buttons: list of button's names
        buttons_dict: link all buttons to their key (name)
        options: the output as a list of options
        opt: number of button
        last_act: name of the last button used
        selected_button: rect of the button that the mouse point at
        """
        self.use_cur = use_cursor
        self.cursor = 0
        self.last_act = None
        self.opt = 0
        self.buttons_dict = {}
        self.options = {}
        self.buttons = []
        self.button_sprite = pygame.sprite.Group()
        self.selected_button = None

    def add_button(self, name, x, y, buttonsize_x, buttonsize_y, key=None):
        image = pygame.Surface((buttonsize_x, buttonsize_y))
        image.fill((255, 0, 0))
        button = Button((image, image), name, x, y, buttonsize_x, buttonsize_y, key)
        self.buttons_dict[name] = button
        self.buttons.append(name)
        self.opt += 1
        button.add(self.button_sprite)

    def clear_button(self):
        self.buttons.clear()
        self.buttons_dict.clear()
        self.button_sprite.empty()

    def reset_button(self):
        for button in self.buttons:
            button.reset()

    def render(self, surface):
        self.button_sprite.update()
        self.button_sprite.draw(surface.surface)

    def update(self):
        self.selected_button = None
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons_dict.values():
            # Key
            if button.key is not None:
                if actions[button.key]:
                    if self.last_act is None:
                        self.last_act = button.name
                        button.press()
                    else:
                        if button.name == self.last_act:
                            button.press()
                            self.last_act = None
                        else:
                            self.buttons_dict[self.last_act].press()
                            button.press()
                            self.cursor = self.buttons.index(button.name)
                            self.last_act = button.name
            # Mouse
            if button.is_point(mouse_pos):
                self.selected_button = button.rect
                if actions["Left Click"][0]:
                    if self.last_act is None:
                        self.last_act = button.name
                        button.press()
                    else:
                        if button.name == self.last_act:
                            button.press()
                            self.last_act = None
                        else:
                            self.buttons_dict[self.last_act].press()
                            button.press()
                            self.cursor = self.buttons.index(button.name)
                            self.last_act = button.name

        if self.use_cur:
            if actions["Up"]:
                self.cursor -= 1
                self.cursor = self.cursor % self.opt
            if actions["Down"]:
                self.cursor += 1
                self.cursor = self.cursor % self.opt
            # Enter
            if actions["Start"]:
                name = self.buttons[self.cursor]
                if self.last_act is None:
                    self.last_act = name
                    self.buttons_dict[name].press()
                else:
                    if name == self.last_act:
                        self.buttons_dict[name].press()
                        self.last_act = None
                    else:
                        self.buttons_dict[self.last_act].press()
                        self.buttons_dict[name].press()
                        self.last_act = name

        if actions["Right Click"]:
            self.reset_button()

        for button in self.buttons_dict.values():
            self.options[button.name] = button.status()

        return self.options
