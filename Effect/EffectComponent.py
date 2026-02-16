from Effect.base import SlowEffect, StunEffect, FreezeEffect, BurnEffect, WaterEffect, IceEffect, ElecEffect, EarthEffect, WindEffect


class EffectComponent:
    def __init__(self):
        self.slow = []
        self.stun = None
        self.freeze = None

        self.fire = None
        self.water = None
        self.ice = None
        self.elec = None
        self.earth = None
        self.wind = None

    def on_start(self):
        pass

    def on_update(self, dt):
        pass

    def on_end(self):
        pass

    def add_effect(self, effect):
        # Depending on the type of effect, add it to the appropriate list or variable
        if isinstance(effect, SlowEffect):
            self.slow.append(effect)
        elif isinstance(effect, StunEffect):
            self.stun = effect
        elif isinstance(effect, FreezeEffect):
            self.freeze = effect
        elif isinstance(effect, BurnEffect):
            self.fire = effect
        elif isinstance(effect, WaterEffect):
            self.water = effect
        elif isinstance(effect, IceEffect):
            self.ice = effect
        elif isinstance(effect, ElecEffect):
            self.elec = effect
        elif isinstance(effect, EarthEffect):
            self.earth = effect
        elif isinstance(effect, WindEffect):
            self.wind = effect

    def remove_effect(self, effect):
        # Depending on the type of effect, remove it from the appropriate list or variable
        if isinstance(effect, SlowEffect):
            self.slow.remove(effect)
        elif isinstance(effect, StunEffect):
            self.stun = None
        elif isinstance(effect, FreezeEffect):
            self.freeze = None
        elif isinstance(effect, BurnEffect):
            self.fire = None
        elif isinstance(effect, WaterEffect):
            self.water = None
        elif isinstance(effect, IceEffect):
            self.ice = None
        elif isinstance(effect, ElecEffect):
            self.elec = None
        elif isinstance(effect, EarthEffect):
            self.earth = None
        elif isinstance(effect, WindEffect):
            self.wind = None
