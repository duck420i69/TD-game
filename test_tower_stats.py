#!/usr/bin/env python3
"""Test script to verify tower stats loading from JSON."""

try:
    from Tower.tower_stats import load_tower_stats, get_tower_stats, get_tower_property

    print("[OK] Tower stats module imported successfully")

    # Test loading stats
    stats = load_tower_stats()
    print(f"[OK] Tower stats loaded: {len(stats)} tower types found")

    # Test getting specific tower stats
    fire_stats_lv1 = get_tower_stats("FireTower", 1)
    print(f"[OK] FireTower Level 1 stats loaded: atk={fire_stats_lv1['atk']}, spd={fire_stats_lv1['spd']}")

    # Test getting tower properties
    fire_bullet = get_tower_property("FireTower", "bullet_image")
    print(f"[OK] FireTower bullet image: {fire_bullet}")

    # Test importing tower classes
    from Tower import FireTower, WaterTower, IceTower, ElecTower, EarthTower, WindTower
    print("[OK] All tower classes imported successfully")

    print("\n[SUCCESS] All tower stats loaded from JSON successfully!")

except Exception as e:
    print(f"[ERROR] {e}")
    import traceback
    traceback.print_exc()

