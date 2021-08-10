import pygame
import os, json

actions = {
        "Esc": False,
        "Up": False,
        "Left": False,
        "Down": False,
        "Right": False,
        "Start": False,
        "1": False,
        "2": False,
        "3": False,
        "4": False,
        "5": False
    }


def load_control():
    try:
        with open(os.path.join('control.json'), 'r+') as file:
            controls = json.load(file)
    except:
        controls = creat_defaultcontrol()
        save_control(controls)
    return controls


def save_control(data):
    with open(os.path.join(os.getcwd(), 'control.json'), 'w') as file:
        json.dump(data, file)


def creat_defaultcontrol():
    controls = {
        "Esc": pygame.K_ESCAPE,
        "Up": pygame.K_UP,
        "Left": pygame.K_LEFT,
        "Down": pygame.K_DOWN,
        "Right": pygame.K_RIGHT,
        "Start": pygame.K_KP_ENTER,
        "1": pygame.K_1,
        "2": pygame.K_2,
        "3": pygame.K_3,
        "4": pygame.K_4,
        "5": pygame.K_5
    }
    return controls


def control_setting():
    pass


def keycheck(controls):
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == controls["Esc"]:
                actions["Esc"] = True
            if event.key == controls["Up"]:
                actions["Up"] = True
            if event.key == controls["Left"]:
                actions["Left"] = True
            if event.key == controls["Down"]:
                actions["Down"] = True
            if event.key == controls["Right"]:
                actions["Right"] = True
            if event.key == controls["Start"]:
                actions["Start"] = True
            if event.key == controls["1"]:
                actions["1"] = True
            if event.key == controls["2"]:
                actions["2"] = True
            if event.key == controls["3"]:
                actions["3"] = True
            if event.key == controls["4"]:
                actions["4"] = True
            if event.key == controls["5"]:
                actions["5"] = True
        if event.type == pygame.KEYUP:
            if event.key == controls["Esc"]:
                actions["Esc"] = False
            if event.key == controls["Up"]:
                actions["Up"] = False
            if event.key == controls["Left"]:
                actions["Left"] = False
            if event.key == controls["Down"]:
                actions["Down"] = False
            if event.key == controls["Right"]:
                actions["Right"] = False
            if event.key == controls["Start"]:
                actions["Start"] = False
            if event.key == controls["1"]:
                actions["1"] = False
            if event.key == controls["2"]:
                actions["2"] = False
            if event.key == controls["3"]:
                actions["3"] = False
            if event.key == controls["4"]:
                actions["4"] = False
            if event.key == controls["5"]:
                actions["5"] = False


def click():
    pos = pygame.mouse.get_pos()
    return pos
