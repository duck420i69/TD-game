# Tower Stats System Documentation

## Overview

All tower statistics have been moved from hardcoded Python classes to a centralized JSON configuration file (`assets/tower_stats.json`). This allows for easy tweaking of game balance without modifying code.

## File Structure

```
TD-game/
├── assets/
│   └── tower_stats.json          # Central tower stats configuration
├── Tower/
│   ├── tower_stats.py            # Stats loader utility functions
│   ├── base.py                   # Base Tower and Bullet classes
│   ├── FireTower.py              # Tower subclasses
│   ├── WaterTower.py
│   ├── IceTower.py
│   ├── ElecTower.py
│   ├── EarthTower.py
│   └── WindTower.py
└── State/
    └── InGame.py                 # Uses towers (no changes needed)
```

## Tower Stats JSON Format

### Basic Structure
```json
{
  "TowerName": {
    "bullet_image": "filename.png",      // Image for projectile
    "tower_image": "filename.png",       // Image for tower
    "base_charge": 7500,                 // Optional: base charge time for ElecTower
    "base_bsize": 7,                     // Optional: base bullet size
    "levels": {
      "1": { /* level 1 stats */ },
      "2": { /* level 2 stats */ },
      "3": { /* level 3 stats */ }
    }
  }
}
```

### Level Stats Structure
```json
{
  "map_id": 11,                          // Map layer ID for placement
  "atk": 8,                              // Attack damage
  "spd": 0.8,                            // Attack speed
  "rot": 150,                            // Rotation speed
  "ran": 100,                            // Attack range
  "bsize": 8,                            // Bullet size
  "sell_price": 30,                      // Money gained from selling
  "upgrade_price": 100,                  // Cost to upgrade to next level
  "charge": 10000,                       // Optional: charge time for special towers
  "effects": {
    "Damage": 8,
    "Explosion": [true, 40],
    "Fire": [true, 6000, 10],
    "Elec": [false, 0, 0]
  }
}
```

## Tower Loader Module (`tower_stats.py`)

### Functions

#### `load_tower_stats()`
Loads the tower stats JSON file and caches it in memory.

**Returns:** `dict` - All tower configurations

**Example:**
```python
from Tower.tower_stats import load_tower_stats
stats = load_tower_stats()
```

#### `get_tower_stats(tower_name, level)`
Get complete stats for a specific tower and level.

**Parameters:**
- `tower_name` (str): Tower class name (e.g., "FireTower", "WaterTower")
- `level` (int): Tower level (1, 2, or 3)

**Returns:** `dict` - Stats dictionary for that level

**Example:**
```python
from Tower.tower_stats import get_tower_stats
fire_lvl1 = get_tower_stats("FireTower", 1)
print(fire_lvl1["atk"])  # 8
```

#### `get_tower_property(tower_name, property_name)`
Get a tower-wide property (not level-specific).

**Parameters:**
- `tower_name` (str): Tower class name
- `property_name` (str): Property name (e.g., "bullet_image", "tower_image")

**Returns:** Value of the property or None

**Example:**
```python
from Tower.tower_stats import get_tower_property
bullet_img = get_tower_property("FireTower", "bullet_image")
# Returns: "firebullet.png"
```

## Tower Classes Integration

Each tower class now uses the stats loader in its `get_stat()` method:

### Example: FireTower

```python
from .tower_stats import get_tower_stats, get_tower_property

class FireTower(Tower):
    def __init__(self, map_, x, y, lv):
        super().__init__(map_, x, y, lv)
        self.bullet_image = load_image(get_tower_property("FireTower", "bullet_image"))
        self.image = load_image(get_tower_property("FireTower", "tower_image"))

    def get_stat(self):
        stats = get_tower_stats("FireTower", self.lv)
        
        # Apply map assignment
        self.map.assign(stats["map_id"], self.map_x, self.map_y)
        
        # Load stats
        self.atk = stats["atk"]
        self.spd = stats["spd"]
        self.rot = stats["rot"]
        self.ran = stats["ran"]
        self.bsize = stats["bsize"]
        self.sell_price = stats["sell_price"]
        self.upgrade_price = stats["upgrade_price"]
        
        # Load effects
        self.effects = stats["effects"].copy()
```

## Towers Configured

All 6 tower types are fully configured in the JSON:

1. **FireTower** (Fire damage, explosion)
   - Levels: 1, 2, 3
   - Effects: Fire burn, explosion damage

2. **WaterTower** (Water damage, splash)
   - Levels: 1, 2, 3
   - Effects: Water splash, explosion damage

3. **IceTower** (Ice damage, slow)
   - Levels: 1, 2, 3
   - Effects: Ice freeze, slow effect

4. **ElecTower** (Electric damage, chain)
   - Levels: 1, 2, 3
   - Effects: Electric damage, chain to nearby enemies
   - Special: Uses charge mechanic

5. **EarthTower** (Earth damage, stun)
   - Levels: 1, 2, 3
   - Effects: Earth stun effect

6. **WindTower** (Wind damage, knockback)
   - Levels: 1, 2, 3
   - Effects: Wind knockback effect

## Game Balance Tweaking

To adjust tower balance, simply edit the `assets/tower_stats.json` file:

### Example: Increase FireTower Level 1 Damage

**Before:**
```json
"1": {
  "atk": 8,
  ...
}
```

**After:**
```json
"1": {
  "atk": 12,
  ...
}
```

Changes take effect immediately when the game reloads (stats are loaded fresh each time).

## Benefits

✓ **Easy Balance Adjustments** - Change numbers without touching code
✓ **Centralized Configuration** - All stats in one place
✓ **Version Control Friendly** - JSON diffs are clear and easy to review
✓ **Data-Driven Design** - Separate data from logic
✓ **Reduced Code Duplication** - No hardcoded stats in multiple files

## Usage in InGame State

The InGame state doesn't need any changes! Tower instantiation works exactly as before:

```python
from Tower import FireTower

# Create tower - stats are loaded automatically from JSON
fire = FireTower(self.map_, x, y, 1)
```

When `get_stat()` is called during initialization, it automatically loads from the JSON file.

## Caching

Tower stats are cached in memory after the first load for performance. The cache persists for the entire game session.

To force a reload:
```python
from Tower.tower_stats import load_tower_stats, _tower_stats_cache
import Tower.tower_stats as ts
ts._tower_stats_cache = None
fresh_stats = load_tower_stats()
```

## Error Handling

If a tower or level is not found in the JSON, the loader will print an error message and return an empty dict. This prevents crashes but logs the issue clearly.

```python
# If FireTower level 5 doesn't exist in JSON:
stats = get_tower_stats("FireTower", 5)
# Prints: Error: Level 5 not found for tower 'FireTower'
# Returns: {}
```

## Migration Notes

- All tower stats previously hardcoded in Python classes have been moved to JSON
- No functional changes to tower behavior
- All tower classes now inherit their stats from the JSON file
- InGame.py imports work exactly as before
- Backward compatible - no API changes

## Future Enhancements

Possible improvements:
- Add tower-specific mechanics to JSON (e.g., ProjectileSpeed, CritChance)
- Add tower names and descriptions
- Add localization support for tower descriptions
- Add recommended upgrade paths
- Add tower combinations/synergies

