class Effect:
    def __init__(self, name, description, duration):
        self.name = name
        self.description = description
        self.duration = duration

    def update(self, dt):
        """Update the effect on the target each turn."""
        self.duration -= dt

    def should_remove(self):
        """Check if the effect should be removed."""
        return self.duration <= 0

# add class corresponding to each effect type, e.g. SlowEffect, StunEffect, etc. that inherit from Effect and implement the update and should_remove methods accordingly.'
class SlowEffect(Effect):
    def __init__(self, duration, slow_amount):
        super().__init__("Slow", f"Reduces speed by {slow_amount}%", duration)
        self.slow_amount = slow_amount


class StunEffect(Effect):
    def __init__(self, duration):
        super().__init__("Stun", "Prevents the target from taking any actions.", duration)


class FreezeEffect(Effect):
    def __init__(self, duration):
        super().__init__("Freeze", "Immobilizes the target and reduces its speed.", duration)


class BurnEffect(Effect):
    def __init__(self, duration, damage_per_second):
        super().__init__("Burn", f"Deals {damage_per_second} damage per second.", duration)
        self.damage_per_second = damage_per_second


# Similarly, you can create other effect classes like WaterEffect, IceEffect, ElecEffect, EarthEffect, WindEffect, etc. that inherit from Effect and implement their specific behaviors in the update and should_remove methods.
class WaterEffect(Effect):
    def __init__(self, duration):
        super().__init__("Water", "Reduces fire damage taken and increases water damage dealt.", duration)

class IceEffect(Effect):
    def __init__(self, duration):
        super().__init__("Ice", "Reduces speed and increases vulnerability to fire damage.", duration)

class ElecEffect(Effect):
    def __init__(self, duration):
        super().__init__("Electric", "Stuns the target and increases vulnerability to water damage.", duration)

class EarthEffect(Effect):
    def __init__(self, duration):
        super().__init__("Earth", "Increases defense and reduces vulnerability to wind damage.", duration)

class WindEffect(Effect):
    def __init__(self, duration):
        super().__init__("Wind", "Increases evasion and reduces vulnerability to earth damage.", duration)