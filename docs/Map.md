# Map module

Summary
- Provides the `Map` class which loads/render a tile map and manages tower placement and waves.
- Includes utility functions `load_map()` and `save_map()` to read/write `data/map.json`.

Tile type notes (from Map.py header)
- `0` : land
- `-1` : can't place
- `1` : arrow (tower subtype)
- `2` : poison
- `3` : ice
- `4` : mage

Module layout

Class `Map`
- __init__(mapdata)
  - `mapdata` is a dict with keys:
    - `"map"`: 2D list of integers representing tiles.
    - `"path"`: list of [x, y] grid positions for enemy pathing.
  - Internals set by init:
    - `tilesize` (20 by default)
    - `path`: coordinates converted to pixel positions: `(x+0.1)*tilesize`
    - `defaultmap` and `map`: tile layout copies
    - `w`, `h`: map dimensions (width, height)
    - loads `grass.png` and `path.png` via `load_image()`
    - `sprites` and `tower_sprite`: `pygame.sprite.Group()` instances
    - simple tile loop adds grass or road `Sprite`s for tiles code 0 and -10
    - `waves`: a placeholder waves list (`[("Slime",10,1500,5,1500,0)]`)

Methods
- `assign(maptype, x, y) -> bool`:
  - Attempts to set `self.map[y][x] = maptype` if the current tile is assignable.
  - Logic: if current tile's tens digit is `0` (i.e., `type_ // 10 == 0`) assign and return `True`.
  - If the new `maptype` shares the same tens-digit category as the existing tile, returns `True` (no change).
  - Otherwise returns `False`.
- `place_tower(tower)`:
  - Adds a tower object to `tower_sprite` group.
- `remove(x, y)`:
  - Resets `self.map[y][x]` to the original tile from `defaultmap`.
- `sell_tower(tower)`:
  - Removes the tower sprite and resets its tile via `remove(tower.map_x, tower.map_y)`.
- `call_wave(wave)`:
  - Returns the wave tuple for `wave - 1` index.
- `render(surface)`:
  - Draws `sprites` and `tower_sprite` onto `surface.surface` (expects a surface wrapper with `.surface`).

Utility functions
- `load_map()`:
  - Loads and returns the JSON object from `data/map.json`.
- `save_map(data)`:
  - Writes `data` to `data/map.json` in the current working directory.

Quick example

```py
from Map import Map, load_map

mdata = load_map()
my_map = Map(mdata)
# render in your game loop with a Surface wrapper `screen`:
# my_map.render(screen)

# place a tower (tower object must have map_x, map_y attributes when selling):
# my_map.place_tower(tower)

# assign a tile type at grid coords (x,y):
# success = my_map.assign(11, 5, 3)
```

Notes & tips
- `Map` expects `Graphic.load_image()` and a `Sprite` wrapper from `Graphic.py` to exist.
- Paths in mapdata are adjusted by `+0.1` before multiplying by `tilesize` — keep that in mind if producing path coordinates.
- The module currently treats tile code `-10` as road when creating tile sprites; adjust if your map JSON uses different codes.

File locations
- Map implementation: `Map.py`
- Generated docs: `docs/Map.md`
