import pygame
import os, json

# TO DO
# pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])


actions = {
        "Quit": False,
        "Esc": False,
        "Left Click": False,
        "Right Click": False,
        "Up": False,
        "Left": False,
        "Down": False,
        "Right": False,
        "Start": False,
        "1": False,
        "2": False,
        "3": False,
        "4": False,
        "5": False,
        "6": False
    }
hold = False


def load_control():
    try:
        with open(os.path.join('assets', 'control.json'), 'r+') as file:
            control = json.load(file)
    except:
        # TO DO: Inform about control reset
        control = creat_defaultcontrol()
        save_control(control)
    return control


def save_control(data):
    with open(os.path.join(os.getcwd(), 'assets' , 'control.json'), 'w') as file:
        json.dump(data, file)


def creat_defaultcontrol():
    control = {
        "Esc": pygame.K_ESCAPE,
        "Up": pygame.K_UP,
        "Left": pygame.K_LEFT,
        "Down": pygame.K_DOWN,
        "Right": pygame.K_RIGHT,
        "Start": pygame.K_RETURN,
        "1": pygame.K_1,
        "2": pygame.K_2,
        "3": pygame.K_3,
        "4": pygame.K_4,
        "5": pygame.K_5,
        "6": pygame.K_6
    }
    return control


def control_setting():
    pass


def keycheck(control):
    global hold
    click = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            actions["Quit"] = True

        if pygame.mouse.get_pressed(3)[0] and not hold:
            click = True
            hold = True

        if not pygame.mouse.get_pressed(3)[0]:
            hold = False

        actions["Left Click"] = (click, pygame.mouse.get_pressed(3)[0])
        actions["Right Click"] = pygame.mouse.get_pressed(3)[2]

        if event.type == pygame.KEYDOWN:
            if event.key == control["Esc"]:
                actions["Esc"] = True
            if event.key == control["Up"]:
                actions["Up"] = True
            if event.key == control["Left"]:
                actions["Left"] = True
            if event.key == control["Down"]:
                actions["Down"] = True
            if event.key == control["Right"]:
                actions["Right"] = True
            if event.key == control["Start"]:
                actions["Start"] = True
            if event.key == control["1"]:
                actions["1"] = True
            if event.key == control["2"]:
                actions["2"] = True
            if event.key == control["3"]:
                actions["3"] = True
            if event.key == control["4"]:
                actions["4"] = True
            if event.key == control["5"]:
                actions["5"] = True
            if event.key == control["6"]:
                actions["6"] = True
        if event.type == pygame.KEYUP:
            if event.key == control["Esc"]:
                actions["Esc"] = False
            if event.key == control["Up"]:
                actions["Up"] = False
            if event.key == control["Left"]:
                actions["Left"] = False
            if event.key == control["Down"]:
                actions["Down"] = False
            if event.key == control["Right"]:
                actions["Right"] = False
            if event.key == control["Start"]:
                actions["Start"] = False
            if event.key == control["1"]:
                actions["1"] = False
            if event.key == control["2"]:
                actions["2"] = False
            if event.key == control["3"]:
                actions["3"] = False
            if event.key == control["4"]:
                actions["4"] = False
            if event.key == control["5"]:
                actions["5"] = False
            if event.key == control["6"]:
                actions["6"] = False


def resetkey():
    for action in actions:
        actions[action] = False


controls = load_control()
