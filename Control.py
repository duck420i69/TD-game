import pygame
import os, json

# TO DO
# pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])


actions = ["Quit", "Esc", "Left Click", "Right Click",
        "Up", "Left", "Down", "Right", "Start",
        "1", "2", "3", "4", "5", "6"]

actions_status = {k: { "press": False, "hold": False, "release": False } for k in actions}

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


def handle_key(key: str, press: bool):
    if press and not actions_status[key]["hold"]:
        actions_status[key]["press"] = True
    if not press and actions_status[key]["hold"]:
        actions_status[key]["release"] = True
    actions_status[key]["hold"] = press


def keycheck(control: dict[str, int], events: list[pygame.event.Event]):
    for action in actions:
        actions_status[action]["press"] = False
        actions_status[action]["release"] = False

    for event in events:
        if event.type == pygame.QUIT:
            actions_status["Quit"] = { "press": True, "hold": True }
       
        handle_key("Left Click", pygame.mouse.get_pressed(3)[0])
        handle_key("Right Click", pygame.mouse.get_pressed(3)[2])

        if event.type == pygame.KEYDOWN:
            for key in control.keys():
                if event.key == control[key]:
                    handle_key(key, True)
                
        if event.type == pygame.KEYUP:
            for key in control.keys():
                if event.key == control[key]:
                    handle_key(key, False)


def resetkey():
    for action in actions:
        actions_status[action] = { "press": False, "hold": False }


controls = load_control()
