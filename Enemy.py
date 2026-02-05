from Graphic import *


class Enemy:
    """
    Lot, lot of code with weird engineering
    Handling all the effect and movement of enemy
    """
    def __init__(self, lv, themap):
        super().__init__()
        self.shadow = load_image("shadow.png")
        self.shadow.set_alpha(40)
        self.money = 5
        self.maxhp = 100
        self.lv = lv
        self.maxhp = self.maxhp * (1.05 ** self.lv)
        self.hp = self.maxhp
        self.life_lost = 1
        self.nor_ms = 30
        self.ms = self.nor_ms

        self.x_dmg = {
            "Fire": [0, 0],
            "Water": [0, 0],
            "Ice": [0, 0],
            "Elec": [0, 0],
            "Earth": [0, 0],
            "Wind": [0, 0],
        }
        self.debuff = {
            "Stun": [False, False, 0 , 0],
            "Freeze": [False, False, 0, 0],
            "Slow": []
        }

        self.immune = {
            "Fire": [False, 0],
            "Water": [False, 0],
            "Ice": [False, 0],
            "Elec": [False, 0],
            "Earth": [False, 0],
            "Wind": [False, 0],
            "Slow": [False, 0],
            "Stun": [False, 0],
            "Freeze": [False, 0]
        }

        self.normal_status = {
            "Fire": [False, 0, 0],
            "Water": [False, 0],
            "Ice": [False, 0, 0],
            "Elec": [False, 0, 0],
            "Earth": [False, 0, 0],
            "Wind": [False, 0, 0],
        }
        self.status = self.normal_status.copy()

        self.path = themap.path
        self.i = 1
        self.pos = pygame.Vector2(self.path[0])
        self.moved = 0

        slime0 = load_image("slime0.png")
        slime1 = load_image("slime1.png")
        self.sprite = [slime0, slime1]
        self.frame = 0
        self.t = 0
        self.animate = 2
        self.between_time = 300

        self.hitbox_w, self.hitbox_h = 16, 16
        self.hitbox = [self.pos[0], self.pos[1], self.hitbox_w, self.hitbox_h]
        self.feet = self.pos + pygame.Vector2(self.hitbox_w/2, self.hitbox_h)

        self.delete = False

        # Movement
        self.end = pygame.Vector2(self.path[self.i])
        self.vec = self.end - self.pos
        self.mvec = self.vec.normalize()
        self.b4vec = self.mvec

    def move(self, t):
        if not self.debuff["Freeze"][0] and not self.debuff["Stun"][0]:
            # Check if move to the end
            if pygame.Vector2.dot(self.vec, self.b4vec) > 0:
                self.pos = self.pos + self.mvec * self.ms * t/1000
                self.moved += self.ms * t/1000
                self.feet = self.pos + pygame.Vector2(self.hitbox_w / 2, self.hitbox_h)
                self.vec = self.end - self.pos
                self.hitbox = [self.pos[0], self.pos[1], self.hitbox_w, self.hitbox_h]
            # Set new end
            elif self.i < len(self.path) - 1:
                self.pos = pygame.Vector2(self.path[self.i])
                self.i += 1
                self.end = pygame.Vector2(self.path[self.i])
                self.vec = self.end - self.pos
                self.mvec = self.vec.normalize()
                self.b4vec = self.vec
            # Get to the end point
            else:
                self.delete = True

    def moveded(self):
        return self.moved

    def reward(self):
        return self.money

    def position(self):
        return self.feet

    def center(self):
        return self.pos + pygame.Vector2(self.hitbox_w/2, self.hitbox_h/2)

    def dmg_recieve(self, bullet, type):
        self.hp -= bullet.effects["Damage"] * (1 - self.immune[type][1]) * (1 + self.x_dmg[type][0])

    def get_hit(self, bullet):
        for key in bullet.effects.keys():
            # Effect that happen right away when bullet hit
            if key == "Earth":
                if bullet.effects[key][0]:
                    if not self.debuff["Stun"][1]:
                        stack = self.status[key][2]
                        self.status[key] = bullet.effects[key].copy()
                        self.status[key][2] = stack + 1
                    if self.debuff["Freeze"][0]:
                        self.debuff["Freeze"] = [False, True, 0, 2000]
                        self.x_dmg[key] = [1.5, 0]
                    self.dmg_recieve(bullet, key)

            elif key == "Fire":
                if bullet.effects[key][0]:
                    if self.status["Water"][0]:
                        self.x_dmg["Fire"] = [-0.25, 0]
                        self.status["Water"] = self.normal_status["Water"].copy()
                    elif self.status["Ice"][0]:
                        self.x_dmg["Fire"] = [0.75, 0]
                        self.status["Ice"] = self.normal_status["Ice"].copy()
                    elif self.debuff["Freeze"][0]:
                        self.debuff["Freeze"] = [False, False, 0, 0]
                    else:
                        if self.status[key][2] < bullet.effects[key][2]:
                            self.status[key] = bullet.effects[key].copy()
                        else:
                            dot = self.status[key][2]
                            self.status[key] = bullet.effects[key].copy()
                            self.status[key][2] = dot
                    self.dmg_recieve(bullet, key)

            elif key == "Water":
                if bullet.effects[key][0]:
                    if not self.debuff["Freeze"][1]:
                        self.status[key] = bullet.effects[key].copy()
                    elif self.status["Fire"][0]:
                        self.status["Fire"] = self.normal_status["Fire"].copy()
                        self.x_dmg[key] = [0.25, 0]
                    elif self.status["Elec"][0]:
                        self.hp -= bullet.effects["Damage"] * (1 - self.immune["Elec"][1]) * (1 + self.x_dmg["Elec"][0])
                        self.status[key] = bullet.effects[key].copy()
                    else:
                        self.status[key] = bullet.effects[key].copy()
                    self.dmg_recieve(bullet, key)

            elif key == "Elec":
                if bullet.effects[key][0]:
                    self.status[key] = bullet.effects[key].copy()
                    self.dmg_recieve(bullet, key)

            elif key == "Wind":
                if bullet.effects[key][0]:
                    self.status[key] = bullet.effects[key].copy()
                    self.dmg_recieve(bullet, key)

            elif key == "Ice":
                if bullet.effects[key][0]:
                    self.debuff["Slow"].append(bullet.effects["Ice"].copy())
                    if self.status["Fire"][0]:
                        self.x_dmg["Ice"] = [0.75, 0]
                    if not self.debuff["Freeze"][1]:
                        self.status[key] = bullet.effects[key].copy()
                    self.dmg_recieve(bullet, key)

        if self.hp <= 0:
            self.delete = True

    def predict_move(self, t):
        if self.debuff["Freeze"][0] or self.debuff["Stun"][0]:
            pos = self.pos
        else:
            lenght = t * self.ms
            i = self.i
            pos = self.pos
            vec = self.end - self.pos
            vec_lenght = vec.length()
            prev_lenght = lenght
            lenght -= vec_lenght
            while lenght > 0:
                if i < len(self.path) - 1:
                    pos = pygame.Vector2(self.path[i])
                    i += 1
                    end = pygame.Vector2(self.path[i])
                    vec = end - pos
                    vec_lenght = vec.length()
                    prev_lenght = lenght
                    lenght -= vec_lenght
                else:
                    lenght = 0
            if lenght == 0:
                pos = self.path[i]
            else:
                vec.scale_to_length(prev_lenght)
                pos = pos + vec
            pos = pos + pygame.Vector2(self.hitbox_w/2, self.hitbox_h/2)
        return pos

    def render(self, surface, element_sprite):
        self.t = self.t % (self.between_time * self.animate)
        self.frame = self.t // self.between_time
        image = self.sprite[self.frame]
        surface.blit(self.shadow, self.pos[0] + 1, self.feet[1] - 7)
        surface.blit(image, self.pos[0], self.pos[1])
        x = self.pos[0] - 6
        for element, status in self.status.items():
            if status[0]:
                if element == "Earth":
                    if status[2] == 1:
                        surface.blit(element_sprite["Earth"][0], x, self.pos[1] - 14)
                        x += 3
                    elif status[2] == 2:
                        surface.blit(element_sprite["Earth"][1], x, self.pos[1] - 14)
                        x += 3
                else:
                    if element != "Wind":
                        surface.blit(element_sprite[element], x, self.pos[1] - 14)
                        x += 3
        surface.rect(self.pos[0] - 6, self.pos[1] - 11, 22, 5, (128, 128, 128))
        surface.rect(self.pos[0] - 5, self.pos[1] - 10, 20 * (self.hp/self.maxhp), 3, (255, 0, 0))

    # noinspection PyUnresolvedReferences
    def update(self, dt):
        # bottom
        for key in self.status.keys():
            if self.status[key][0]:
                self.status[key][1] -= dt
            if self.status[key][1] < 0:
                self.status[key] = self.normal_status[key].copy()
        for key in self.x_dmg.keys():
            if self.x_dmg[key][1] > 0:
                self.x_dmg[key][1] -= dt
            else:
                self.x_dmg[key] = [0, 0]

        slow_debuff = 0
        for key in self.debuff.keys():
            if key == "Slow":
                for slow in self.debuff["Slow"]:
                    if slow[0]:
                        if slow[1] > 0:
                            slow[1] -= dt
                            if slow[2] > slow_debuff:
                                slow_debuff = slow[2]
                        else:
                            slow[0] = False
                    else:
                        self.debuff["Slow"].remove(slow)
            else:
                if self.debuff[key][0]:
                    self.debuff[key][2] -= dt
                    if self.debuff[key][2] < 0:
                        self.debuff[key][0] = False
                        self.debuff[key][2] = 0
                if self.debuff[key][1]:
                    self.debuff[key][3] -= dt
                    if self.debuff[key][3] < 0:
                        self.debuff[key] = [False, False, 0, 0]

        if self.status["Earth"][2] >= 3:
            self.debuff["Stun"] = [True, True, 3000, 5000]
            self.status["Earth"][2] = 0

        if self.status["Fire"][0]:
            self.hp -= self.status["Fire"][2] * dt/1000
            if self.hp <= 0:
                self.delete = True

        if self.status["Water"][0] and self.status["Earth"][0]:
            # noinspection PyTypeChecker
            self.debuff["Slow"].append([True, 4000, 0.6])
            self.status["Water"] = self.normal_status["Water"].copy()
            self.status["Earth"] = self.normal_status["Earth"].copy()

        if self.status["Water"][0] and self.status["Ice"][0]:
            if not self.debuff["Freeze"][1]:
                self.debuff["Freeze"] = [True, True, 4000, 6000]
                self.status["Water"] = self.normal_status["Water"].copy()
                self.status["Ice"] = self.normal_status["Ice"].copy()

        if not self.immune["Slow"][0]:
            slow_amount = (1 - slow_debuff * (1 - self.immune["Slow"][1]))
            self.ms = self.nor_ms * slow_amount
        else:
            slow_amount = 0

        if not self.debuff["Freeze"][0] and not self.debuff["Stun"][0]:
            self.t += int(dt * (slow_amount/2))


class Slime(Enemy):
    def __init__(self, lv, themap):
        super().__init__(lv, themap)

        self.between_time = 100
        self.sprite = [load_image("slime0.png"), load_image("slime1.png"), load_image("slime2.png"),
                       load_image("slime3.png"), load_image("slime4.png"), load_image("slime5.png")]
        self.animate = 6
