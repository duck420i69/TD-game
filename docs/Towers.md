# Towers module

Summary
- Documents the `Tower` system: `Bullet`, base `Tower`, and concrete tower classes (`FireTower`, `WaterTower`, `IceTower`, `ElecTower`, `EarthTower`, `WindTower`).
- Describes the effects schema used by towers and bullets.

Classes

`Bullet`
- Purpose: simple projectile container used by towers.
- Attributes:
  - `image`: sprite image
  - `pos`: `pygame.Vector2` pixel position
  - `spd`: speed (pixels/sec)
  - `bsize`: bullet size (hitbox square)
  - `hitbox`: [x, y, w, h]
  - `effects`: dict of effects applied to hit enemies
  - `dead`: bool flag
- Methods:
  - `move(t)`: advance position by `vec2 * spd * t/1000` and update hitbox
  - `render(surface)`: draw bullet
  - `update(...)`: syncs `rect` for pygame

`Tower` (base)
- Purpose: base class for all towers; manages position, stats, bullets, and targeting.
- Initialization: `Tower(map_, x, y, lv)`
  - `map_`: `Map` instance used to assign tile codes and get `tilesize`
  - `(x, y)`: grid coordinates (map cells)
  - `lv`: level
- Important attributes (selected):
  - `map_x`, `map_y`: grid coords
  - `x`, `y`: pixel center coords computed from `map_.tilesize`
  - `effects`: dict describing bullet/tower effects
  - `atk`, `spd`, `ran`, `bsize`: attack, attack speed, range, bullet size
  - `bullets`: list of active `Bullet` objects
  - `target`: list of tracked `Enemy` objects
  - `t`: internal timer used for firing cadence
  - `sell_price`, `upgrade_price`
- Key methods:
  - `click(pos)`: select/deselect tower using `pygame.Rect.collidepoint`
  - `sell()`: return `sell_price`
  - `upgrade()`: increment `lv` and call `get_stat()`
  - `get_stat()`: (override) set stats per level and call `map.assign(...)` to mark tile type
  - `tower_buff(atk, spd)`: apply percent buffs to attack and speed
  - `update(dt)`: accumulate `t` toward firing threshold
  - `add_target(enemy)`, `clear_target()`, `any_target()`
  - `aim_target()`: choose target by greatest distance travelled (progress)
  - `inrange(pos)`: check if a position (pygame.Vector2) is within range and if tower ready to fire
  - `shoot(enemy)`: spawn a `Bullet` aiming at predicted enemy position (uses `enemy.predict_move`)

Tower subclasses (overview)
- `FireTower`:
  - Uses `firebullet.png` and `firetower.png` images.
  - Calls `map.assign(11/12/13, x, y)` depending on level.
  - Level examples: lv1 `atk=8, spd=0.8, ran=100`; lv3 strong DoT (`Fire` DoT increased).
  - Effects include `Damage`, `Explosion`, `Fire` DoT.

- `WaterTower`:
  - `map.assign(21/22/23, ...)`
  - Effects include `Damage`, `Explosion`, `Water` (status time), `Elec` placeholder.

- `IceTower`:
  - `map.assign(31/32/33, ...)`
  - Effects include `Damage`, `Explosion`, `Ice` (slow with time and slow factor).

- `ElecTower`:
  - Uses a channel/charge mechanic (`charge` and `t`), deals continuous/instant damage when firing.
  - `shoot` applies `Elec` status and reduces enemy hp directly using `self.atk * self.t/1000`.
  - `inrange` requires `t >= 2500` to enable firing.

- `EarthTower`:
  - `map.assign(51/52/53, ...)`
  - Effects include `Earth` status that stacks toward stun.

- `WindTower`:
  - `map.assign(61/62/63, ...)`
  - Effects include `Wind` (multiplier) and relatively fast bullets.

Effects schema
- Effects are dictionaries attached to towers/bullets and read by `Enemy.get_hit()`/`dmg_recieve()`.
- Common keys and formats (observed in code and comments):
  - `"Damage"`: numeric base damage (number)
  - `"Explosion"`: `[Active(bool), Range(int)]` — area-of-effect flag and radius
  - `"Fire"`: `[Active(bool), time(ms), DoT_amount]` — applies burning damage over time
  - `"Water"`: `[Active(bool), time(ms)]` — water status used in combos
  - `"Ice"`: `[Active(bool), time(ms), slow_fraction]` — applies slow stacks to `debuff["Slow"]`
  - `"Elec"`: `[Active(bool), time(ms), chain_count]` — electric status/chain behavior
  - `"Earth"`: `[Active(bool), time(ms), stacks_to_stun]` — stacks toward stun
  - `"Wind"`: `[Active(bool), time(ms), multiplier]` — multiplies some effect or value
- Example effects dict from tower classes is set in `get_stat()` and used to construct `Bullet` instances.

Interactions and combos (high level)
- `Enemy.get_hit()` contains many interaction rules:
  - `Fire` vs `Water`/`Ice` changes extra damage (`x_dmg`) and resets some statuses.
  - `Water` + `Earth` -> applies a `Slow` debuff.
  - `Water` + `Ice` -> can cause `Freeze` debuff (used as a combo).
  - `Earth` stacks (3 or more) trigger `Stun` debuff lasting a set time.
  - `Elec` and `Fire`/`Ice` interactions modify damage multipliers.
- Towers set `effects` and bullets pass those to `Enemy.get_hit()` on collision.

Usage examples

- Create and place a tower (assumes `map_` is a `Map` instance):

```py
from Towers import FireTower
# create a level-1 fire tower at grid cell (5,3)
ft = FireTower(map_, 5, 3, 1)
map_.place_tower(ft)
```

- Tower firing flow (game loop sketch):

```py
# each frame / tick
for tower in map_.tower_sprite:
    tower.update(dt)
    # for each enemy in enemy_list: if tower.inrange(enemy.position()): tower.add_target(enemy)
    if tower.any_target():
        target = tower.target[tower.aim_target()]
        if tower.inrange(target.center()):
            tower.shoot(target)
    # update bullets
    for b in tower.bullets:
        b.move(dt)
        b.update(dt)
        # check collision with enemies, call enemy.get_hit(bullet) on hit
```

Files
- Implementation: [Towers.py](Towers.py)
- Related enemy logic: [Enemy.py](Enemy.py)
- Generated docs: [docs/Towers.md](docs/Towers.md)

Notes & recommendations
- `Tower.get_stat()` is where per-level stats and `map.assign` calls are made — extend it to add new levels or variants.
- `Bullet.effects` should follow the schema above; `Enemy.get_hit()` implements many hard-coded interactions — update carefully.
- `ElecTower` uses a charge mechanic; its `shoot` differs and directly modifies `Enemy.hp` instead of spawning `Bullet` instances.

