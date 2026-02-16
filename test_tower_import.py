#!/usr/bin/env python3
"""Test script to verify the Tower package refactoring."""

try:
    from Tower import Tower, Bullet, FireTower, WaterTower, IceTower, ElecTower, EarthTower, WindTower
    print("[OK] All classes imported successfully from Tower package")
    print(f"[OK] Tower base class: {Tower.__name__}")
    print(f"[OK] Bullet class: {Bullet.__name__}")
    print(f"[OK] FireTower class: {FireTower.__name__}")
    print(f"[OK] WaterTower class: {WaterTower.__name__}")
    print(f"[OK] IceTower class: {IceTower.__name__}")
    print(f"[OK] ElecTower class: {ElecTower.__name__}")
    print(f"[OK] EarthTower class: {EarthTower.__name__}")
    print(f"[OK] WindTower class: {WindTower.__name__}")
    print("\n[SUCCESS] Refactoring complete! All tower classes are properly organized in the Tower package.")
except Exception as e:
    print(f"[ERROR] {e}")
    import traceback
    traceback.print_exc()


