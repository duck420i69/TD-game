"""Tower stats loader - handles reading and managing tower statistics from JSON."""

import json
import os

_tower_stats_cache = None


def load_tower_stats():
    """Load tower statistics from the JSON file."""
    global _tower_stats_cache

    if _tower_stats_cache is not None:
        return _tower_stats_cache

    try:
        stats_path = os.path.join('assets', 'tower_stats.json')
        with open(stats_path, 'r') as f:
            _tower_stats_cache = json.load(f)
        return _tower_stats_cache
    except FileNotFoundError:
        print(f"Error: Could not find tower_stats.json at {stats_path}")
        return {}


def get_tower_stats(tower_name, level):
    """
    Get stats for a specific tower and level.

    Args:
        tower_name (str): Name of the tower (e.g., 'FireTower')
        level (int): Tower level (1, 2, or 3)

    Returns:
        dict: Tower stats for the given level
    """
    stats = load_tower_stats()
    level_str = str(level)

    if tower_name not in stats:
        print(f"Error: Tower '{tower_name}' not found in stats")
        return {}

    if level_str not in stats[tower_name].get('levels', {}):
        print(f"Error: Level {level} not found for tower '{tower_name}'")
        return {}

    return stats[tower_name]['levels'][level_str]


def get_tower_property(tower_name, property_name):
    """
    Get a tower-wide property (e.g., bullet_image, tower_image).

    Args:
        tower_name (str): Name of the tower
        property_name (str): Property name (e.g., 'bullet_image', 'tower_image')

    Returns:
        Value of the property or None if not found
    """
    stats = load_tower_stats()

    if tower_name not in stats:
        return None

    return stats[tower_name].get(property_name)

